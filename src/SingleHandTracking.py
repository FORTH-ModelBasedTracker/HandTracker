"""
FORTH Model based hand tracker.
Single Hand tracking pipeline using FORTH libraries.

"""
import PyMBVCore as Core
import PyMBVAcquisition as Acquisition
import PyMBVRendering as Rendering
import PyMBVDecoding as dec
import PyHandTracker as HT

import cv2 as cv
from time import clock

import time

if __name__ == '__main__':
    print "Creating Renderer..."
    renderer = Rendering.RendererOGLCudaExposed.get()
    renderer.culling = Rendering.RendererOGLBase.Culling.CullFront
    
    erenderer = Rendering.ExposedRenderer(renderer, renderer)
    ht = HT.HandTrackerLib(2048, 2048, 64, 64)#, erenderer)
    handDec = dec.GenericDecoder()
    handDec.loadFromFile("media/hand_right_low_RH.xml")
    ht.decoder = handDec

    posvar = [10, 10, 10]
    rotvar = [0.1, 0.1, 0.1, 0.1]
    fingervar = [ 0.1, 0.1, 0.1, 0.1]

    ht.variances = Core.DoubleVector( posvar + rotvar + 5 * fingervar)
    
    print "Variances: ",list(ht.variances)
    print "Low Bounds: ",list(ht.lowBounds)
    print "High Bounds: ",list(ht.highBounds)
    print "Randomization Indices: ",list(ht.randomizationIndices)
                 
    ht.particles = 32
    ht.generations = 32
    print "Starting Grabber..."
    acq = Acquisition.OpenNIGrabber(True, True, 'media/openni.xml')
    acq.initialize()
    defaultInitPos = Core.ParamVector([ 0, 0, 900, 0, 0, 1, 0, 1.20946707135219810e-001, 1.57187812868051640e+000, 9.58033504364020840e-003, -1.78593063562731860e-001, 7.89636216585289100e-002, 2.67967456875403400e+000, 1.88385552327860720e-001, 2.20049375319072360e-002, -4.09740579183203310e-002, 1.52145111735213370e+000, 1.48366400350912500e-001, 2.85607073734409630e-002, -4.53781680931323280e-003, 1.52743247624671910e+000, 1.01751907812505270e-001, 1.08706683246161150e-001, 8.10845240231484330e-003, 1.49009228214971090e+000, 4.64716068193632560e-002, -1.44370358851376110e-001])
    
    initPos = defaultInitPos
    
    paused = False
    delay = {True:0,False:1}
    frame = 0
    count=0
    tracking = False
        
    actualFPS = 0.0
    print "Entering main Loop."
    while True:
        loopStart = time.time()*1000;
        try:
            imgs, clbs = acq.grab()
        except:
            break
        
        c = clbs[0]
        width,height = int(c.width),int(c.height)
        
        
        rndViewMat,rndProjMat = ht.step1_setupVirtualCamera(c)
        bb = ht.step2_computeBoundingBox(initPos, width, height, 0.1)

        ht.step3_zoomVirtualCamera(rndProjMat, bb,width,height)
        labels, depths = ht.step4_preprocessInput(imgs[1], imgs[0], bb)
 
        ht.step5_setObservations(labels, depths)

        fps = 0
        if tracking:
            t = clock()
            score, initPos = ht.step6_track(initPos)
            t = clock() - t
            fps = 1.0 / t
            

        viz = ht.step7_visualize(imgs[1], rndViewMat,rndProjMat, initPos)
        cv.putText(viz, 'UI FPS = %f, Track FPS = %f' % (actualFPS , fps), (20, 20), 0, 0.5, (0, 0, 255))
        
        cv.imshow("Hand Tracker",viz)

        key = cv.waitKey(delay[paused])
        if key & 255 == ord('s'):
            tracking = not tracking
            initPos = defaultInitPos
            
        if key & 255 == ord('q'):
            break
                
        if key &255 == ord('p'):
            paused = not paused
            
        frame += 1
        loopEnd = time.time()*1000;
        actualFPS = (1000.0/(loopEnd-loopStart))

        
