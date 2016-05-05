"""
FORTH Model based hand tracker.
Single Hand tracking pipeline using FORTH libraries.

"""

# Core stuff, like containers.
import PyMBVCore as Core
# Image acquisition.
import PyMBVAcquisition as Acquisition
# 3D Multi-hypothesis rendering.
import PyMBVRendering as Rendering
# Conversion of hypotheses to 3D renderables.
import PyMBVDecoding as dec
# A library which puts together the aforementioned
# and some extras to make up 3D hand tracking.
import PyHandTracker as HT

# OpenCV.
import cv2 as cv
# Timing.
from time import clock

import time

if __name__ == '__main__':
    print "Creating Renderer..."
    
    # Turn off logging
    Core.InitLog(['handTracker', 'log.severity', 'error'])
    
    # The 3D renderer is a singleton. The single instance is accessed.
    renderer = Rendering.RendererOGLCudaExposed.get()
    # OpenCV coordinate system is right handed but the renderer's
    # coordinate system is left handed. Conversion is handled, but
    # in the process front facing triangles become back facing triangles.
    # Thus, we inverse the culling order.
    # Try to set it to CullBack or CullNone to see the differences.
    renderer.culling = Rendering.RendererOGLBase.Culling.CullFront
    
    # An exposed renderer is one whose data are exposed through
    # some API. The hand tracker lib requires such a renderer.
    erenderer = Rendering.ExposedRenderer(renderer, renderer)
    
    # Create the hand tracker lib
    # params:
    #   - width (2048): max width preallocated for rendering
    #   - height (2048): max height preallocated for rendering
    #   - tileWidth (64): width of hypothesis rendering tile
    #   - tileHeight (64): height of hypothesis rendering tile
    # With the given parameter the handtracker lib will be able to
    # render at most (2048/64)x(2048x64)=1024 hypotheses in parallel.
    # The greatest this number the more the hypothesis evaluation
    # throughput. Default optimization only requires to render 64
    # hypotheses at a time.
    ht = HT.HandTrackerLib(2048, 2048, 128, 128, erenderer)
    
    # Create a decoder, i.e. an object which can transform
    # 27-D parameter vectors to 3D renderable hands.
    handDec = dec.GenericDecoder()
    # A description for a hand can be found at a file.
    handDec.loadFromFile("media/hand_right_low_RH.xml")


    # Create a 6D rigid object decoder
    objectDec = dec.SingleRigidDecoder()
    objectDec.meshFilename = "media/cube.obj"
    objectDec.scale = Core.Vector3(120.0/2.0,60.0/2.0,50.0/2.0)

    # Create slice decoders for each decoder.
    # A slice decoder splits the param vector to the proper
    # points for each decoder
    handDecSlice = dec.SlicedDecoder(handDec)
    handDecSlice.slice = Core.UIntVector(range(0,27))

    objectDecSlice = dec.SlicedDecoder(objectDec)
    objectDecSlice.slice = Core.UIntVector(range(27,34))

    # Create a combination decoder for hand and object
    combDec = dec.DecoderCombination(handDecSlice, objectDecSlice)

    # Set the combination decoder to the hand tracker lib.
    ht.decoder = combDec

    # Setup randomization variances to use during heuristic search.
    posvar = [10, 10, 10]               # 3D global translation variance
    rotvar = [0.1, 0.1, 0.1, 0.1]       # Quaternion global rotation variance
    fingervar = [ 0.1, 0.1, 0.1, 0.1]   # Per finger relative angles variance

    objectPosVar = [10, 10, 10]         # 3D translation variance for the rigid object
    objectRotVar = [0.1, 0.1, 0.1, 0.1] # Quaternion for the rigid object rotation

    # 27-D + 6-D = 3D position + 4D rotation + 5 x 4D per finger angles + 3D object pos + 4D object rotation.
    ht.variances = Core.DoubleVector( posvar + rotvar + 5 * fingervar + objectPosVar + objectRotVar)

    # update the bounds for the hand-object combination
    objectLowBounds = [-2000.0, -2000.0, -2000.0, -1.0, -1.0, -1.0, -1.0]
    objectHighBounds = [2000.0, 2000.0, 2000.0, 1.0, 1.0, 1.0, 1.0]

    ht.lowBounds = Core.DoubleVector(list(ht.lowBounds) + objectLowBounds)
    ht.highBounds = Core.DoubleVector(list(ht.highBounds) + objectHighBounds)

    print "Variances: ",list(ht.variances)
    print "Low Bounds: ",list(ht.lowBounds)
    print "High Bounds: ",list(ht.highBounds)
    print "Randomization Indices: ",list(ht.randomizationIndices)
                 
    # Set the PSO budget, i.e. particles and generations.
    ht.particles = 42
    ht.generations = 42
    
    print "Starting Grabber..."
    
    # Initialize RGBD acquisition. We will be acquiring images
    # from a saved sequence, in oni format.
    
    # User should define a path to a saved sequence in oni format.
    # Set path to empty string to perform live capture from an existing sensor.
    oniPath = 'hand-object.oni'
    acq = Acquisition.OpenNIGrabber(True, True, 'media/openni.xml', oniPath, True)
    acq.initialize()
    
    # Initialization for the hand pose of the first frame is specified.
    # If track is lost, resetting will revert track to this pose.
    defaultInitPos = Core.ParamVector([ 0, 80, 900, 0, 0, 1, 0, 1.20946707135219810e-001, 1.57187812868051640e+000, 9.58033504364020840e-003, -1.78593063562731860e-001, 7.89636216585289100e-002, 2.67967456875403400e+000, 1.88385552327860720e-001, 2.20049375319072360e-002, -4.09740579183203310e-002, 1.52145111735213370e+000, 1.48366400350912500e-001, 2.85607073734409630e-002, -4.53781680931323280e-003, 1.52743247624671910e+000, 1.01751907812505270e-001, 1.08706683246161150e-001, 8.10845240231484330e-003, 1.49009228214971090e+000, 4.64716068193632560e-002, -1.44370358851376110e-001,

                                      -50, 250, 800, -1, 0, 0, 1] # update the object initial position accordingly.
                                      )
    
    # The 3D hand pose, as is tracked in the tracking loop.
    currentHandPose = defaultInitPos
    
    # State.
    paused = False
    delay = {True:0,False:1}
    frame = 0
    count=0
    tracking = len(oniPath) > 0
    actualFPS = 0.0
    
    print "Entering main Loop."
    while True:
        loopStart = time.time()*1000;
        try:
            # Acquire images and image calibrations and break if unsuccessful.
            # imgs is a list of numpy.andrray and clbs a list of Core.CameraMeta.
            # The two lists are of equal size and elements correspond to one another.
            # In OpenNIGrabber, the first image is the depth and the second is the RGB.
            # In the media/openni.xml file it is specified that the depth will be aligned
            # to the RGB image and that mirroring will be off. The resolution is VGA.
            # It is not obligatory to use the OpenNIGrabber. As long as you can somehow provide
            # aligned depth and RGB images and corresponding Core.CameraMeta, you can use 3D
            # hand tracking.
            imgs, clbs = acq.grab()
        except:
            break
        
        # Get the depth calibration to extract some basic info.
        c = clbs[0]
        width,height = int(c.width),int(c.height)
        
        # Step 1: configure 3D rendering to match depth calibration.
        # step1_setupVirtualCamera returns a view matrix and a projection matrix (graphics).
        viewMatrix, projectionMatrix = ht.step1_setupVirtualCamera(c)
        
        # Step 2: compute the bounding box of the previously tracked hand pose.
        # For the sake of efficiency, search is performed in the vicinity of
        # the previous hand tracking solution. Rendering will be constrained
        # in the bounding box (plus some padding) of the previous tracking solution,
        # in image space.
        # The user might chose to bypass this call and compute a bounding box differently,
        # so as to incorporate other information as well.
        bb = ht.step2_computeBoundingBox(currentHandPose, width, height, 0.1)

        # Step 3: Zoom rendering to given bounding box.
        # The renderer is configures so as to map its projection space
        # to the given bounding box, i.e. zoom in.
        ht.step3_zoomVirtualCamera(projectionMatrix, bb,width,height)
        
        # Step 4: Preprocess input.
        # RGBD frames are processed to as to isolate the hand.
        # This is usually done through skin color detection in the RGB frame.
        # The user might chose to bypass this call and do foreground detection
        # in some other way. What is required is a labels image which is non-zero
        # for foreground and a depth image which contains depth values in mm.
        labels, depths = ht.step4_preprocessInput(imgs[1], imgs[0], bb)
 
        # Step5: Upload observations for GPU evaluation.
        # Hypothesis testing is performed on the GPU. Therefore, observations
        # are also uploaded to the GPU.
        ht.step5_setObservations(labels, depths)

        fps = 0
        if tracking:
            t = clock()
            # Step 6: Track.
            # Tracking is initialized with the solution for the previous frame
            # and computes the solution for the current frame. The user might
            # chose to initialize tracking from a pose other than the solution
            # from the previous frame. This solution needs to be 27-D for 3D
            # hand tracking with the specified decoder.
            score, currentHandPose = ht.step6_track(currentHandPose)
            t = clock() - t
            fps = 1.0 / t
            

        # Step 7 : Visualize.
        # This call superimposes a hand tracking solution on a RGB image
        viz = ht.step7_visualize(imgs[1], viewMatrix,projectionMatrix, currentHandPose)
        cv.putText(viz, 'UI FPS = %f, Track FPS = %f' % (actualFPS , fps), (20, 20), 0, 0.5, (0, 0, 255))
        
        cv.imshow("Hand Tracker",viz)

        key = cv.waitKey(delay[paused])
        
        # Press 's' to start/stop tracking.
        if key & 255 == ord('s'):
            tracking = not tracking
            currentHandPose = defaultInitPos
            
        # Press 'q' to quit.
        if key & 255 == ord('q'):
            break
                
        # Press 'p' to pause.
        if key &255 == ord('p'):
            paused = not paused
            
        frame += 1
        loopEnd = time.time()*1000;
        actualFPS = (1000.0/(loopEnd-loopStart))

        
