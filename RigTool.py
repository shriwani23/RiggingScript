import maya.cmds as mc

"""
locator creation method
name: createSL
parameters: name, loc
    string name: name of locator
    vector loc: vector containing x,y,z val of locator
returns: locator
"""
def createSL(name,loc):
    myLoc=mc.spaceLocator(n=name)
    mc.setAttr(myLoc[0]+'.tx',loc[0])
    mc.setAttr(myLoc[0]+'.ty',loc[1])
    mc.setAttr(myLoc[0]+'.tz',loc[2])
    return(myLoc[0])  

"""
alignment tool: aligns two objects
name: alignTool
parameters: a, b
    a: object1
    b: object to assign object 1's loc
no return    
"""
def alignTool(a,b):
    mc.setAttr(b+'.tx',mc.getAttr(a+'.tx'))
    mc.setAttr(b+'.ty',mc.getAttr(a+'.ty'))
    mc.setAttr(b+'.tz',mc.getAttr(a+'.tz'))
    mc.setAttr(b+'.rx',mc.getAttr(a+'.rx'))
    mc.setAttr(b+'.ry',mc.getAttr(a+'.ry'))
    mc.setAttr(b+'.rz',mc.getAttr(a+'.rz'))

"""
lock translation method: locks all translations of given object
name: lockTranslation
    parameters: obj
    object obj: designated object to lock translations for
no return
"""    
def lockTranslation(obj):
    mc.setAttr(obj+'.tx',lock=True)
    mc.setAttr(obj+'.ty',lock=True)
    mc.setAttr(obj+'.tz',lock=True)

"""
connection creation method: connects specificed locators
name: createConnection
parameters: locOne, locTwo
    locator locOne: locator 1
    locator locTwo: locator 2
return: curve connection between locators
"""
def createConnection(locOne,locTwo):
    myCurve=mc.curve(d=1,p=[(0,0,0),(0,0,0)])
    mc.select(myCurve+'.cv[0]')
    clusterOne=mc.cluster(name=locOne+'_Cluster')
    alignTool(locOne,clusterOne[1])
    mc.parent(clusterOne[1],locOne)
    mc.select(myCurve+'.cv[1]')
    clusterTwo=mc.cluster(name=locTwo+'_Cluster')
    alignTool(locTwo,clusterTwo[1])
    mc.parent(clusterTwo[1],locTwo)
    mc.setAttr(myCurve+'.template',1)
    mc.setAttr(clusterOne[1]+'.visibility',0)
    mc.setAttr(clusterTwo[1]+'.visibility',0)
    lockTranslation(clusterOne[1])
    lockTranslation(clusterTwo[1])
    lockTranslation(myCurve)
    
    return myCurve

"""
proxy skeleton generator: creates proxy skeleton with initial joint positions
name: proxySkeleton
no arguments
no return
"""
def proxySkeleton():
    
    mc.select(all=True)
    mc.delete()

    # JOINTS
    C_Pelvis=createSL('C_PelvisLoc',(0,14,0))
    C_Waist=createSL('C_WaistLoc',(0,15,0))
    C_LowerChest=createSL('C_LowerChestLoc',(0,18,0))
    C_Sternum=createSL('C_SternumLoc',(0,22,0))
    C_UpperChest=createSL('C_UpperChestLoc',(0,24,0))
    C_LowerNeck=createSL('C_LowerNeckLoc',(0,24.5,0))
    C_MidNeck=createSL('C_MidNeckLoc',(0,25,0))
    C_HeadBase=createSL('C_HeadBaseLoc',(0,26,0))
    C_HeadTop=createSL('C_HeadTopLoc',(0,28.5,0))
    
    #left hand
    L_Clavical=createSL('L_ClavicleLoc',(-1,24,0))
    L_Shoulder=createSL('L_ShoulderLoc',(-3,24,0))
    L_Elbow=createSL('L_ElbowLoc',(-3.5,19,-1))
    L_Wrist=createSL('L_WristLoc',(-3.5,15,0))
    L_FingerBase=createSL('L_FingerBaseLoc',(-3.5,14,-0.2))
    L_FingerTip=createSL('L_FingerTipLoc',(-3.5,12,0))
    #right hand
    R_Clavical=createSL('R_ClavicleLoc',(1,24,0))
    R_Shoulder=createSL('R_ShoulderLoc',(3,24,0))
    R_Elbow=createSL('R_ElbowLoc',(3.5,19,-1))
    R_Wrist=createSL('R_WristLoc',(3.5,15,0))
    R_FingerBase=createSL('R_FingerBaseLoc',(3.5,14,-.2))
    R_FingerTip=createSL('R_FingerTipLoc',(3.5,12,0))
    
    #left leg
    L_Hip=createSL('L_HipLoc',(-2,12,0))
    L_Knee=createSL('L_KneeLoc',(-2,7,.5))
    L_Ankle=createSL('L_AnkleLoc',(-2,1.5,0))
    L_BallOfFoot=createSL('L_BallOfFootLoc',(-2,0,1))
    L_ToeTip=createSL('L_ToeTipLoc',(-2,0,3))
    #right leg
    R_Hip=createSL('R_HipLoc',(2,12,0))
    R_Knee=createSL('R_KneeLoc',(2,7,.5))
    R_Ankle=createSL('R_AnkleLoc',(2,1.5,0))
    R_BallOfFoot=createSL('R_BallOfFootLoc',(2,0,1))
    R_ToeTip=createSL('R_ToeTipLoc',(2,0,3))
    
    
    # CONNECTIONS
    
    createConnection(C_Pelvis,C_Waist)
    createConnection(C_Waist,C_LowerChest)
    createConnection(C_LowerChest,C_Sternum)
    createConnection(C_Sternum,C_UpperChest)
    createConnection(C_UpperChest,C_LowerNeck)
    createConnection(C_LowerNeck,C_MidNeck)
    createConnection(C_MidNeck,C_HeadBase)
    createConnection(C_HeadBase,C_HeadTop)
    
    #left arm  
    createConnection(C_UpperChest,L_Clavical)
    createConnection(L_Clavical,L_Shoulder)
    createConnection(L_Shoulder,L_Elbow)
    createConnection(L_Elbow,L_Wrist)
    createConnection(L_Wrist,L_FingerBase)
    createConnection(L_FingerBase,L_FingerTip)
    #right arm
    createConnection(C_UpperChest,R_Clavical)
    createConnection(R_Clavical,R_Shoulder)
    createConnection(R_Shoulder,R_Elbow)
    createConnection(R_Elbow,R_Wrist)
    createConnection(R_Wrist,R_FingerBase)
    createConnection(R_FingerBase,R_FingerTip)
    
    #left leg
    createConnection(C_Pelvis,L_Hip)
    createConnection(L_Hip,L_Knee)
    createConnection(L_Knee,L_Ankle)
    createConnection(L_Ankle,L_BallOfFoot)
    createConnection(L_BallOfFoot,L_ToeTip)
    #right leg
    createConnection(C_Pelvis,R_Hip)
    createConnection(R_Hip,R_Knee)
    createConnection(R_Knee,R_Ankle)
    createConnection(R_Ankle,R_BallOfFoot)
    createConnection(R_BallOfFoot,R_ToeTip)
    
    
    mc.select('*Loc')
    mc.group(n='Locators')
    mc.select(cl=True)
    mc.select('curve*')
    mc.group(n='Curves')
    mc.select(cl=True)
    
    
"""
mirror objects function: mirrors objects to selected side
name: mirrorObjects
parameters: sel
    string sel: left or right
no return
"""
def mirrorObjects(sel):
    if sel=='selection':
        mySel=mc.ls(sl=True)
        #Mirror Selection
        for item in mySel:
            xVal=mc.getAttr(item+'.tx')
            yVal=mc.getAttr(item+'.ty')
            zVal=mc.getAttr(item+'.tz')
            if(item[0]=='C'):
                print('unmirrorable object selected')
            else:
                if(item[0]=='L'):
                    chosen='L_'
                    opposite='R_'
                elif(item[0]=='R'):
                    chosen='R_'
                    opposite='L_'
                    
                mirroredObject=item.replace(chosen,opposite)
                mc.setAttr(mirroredObject+'.tx', -1*(xVal))
                mc.setAttr(mirroredObject+'.ty', yVal)
                mc.setAttr(mirroredObject+'.tz', zVal)   

    elif sel=='L' or sel=='R':
        if(sel=='L'):
            chosen='L_'
            opposite='R_'
        elif(sel=='R'):
            chosen='R_'
            opposite='L_'
            
        first=mc.select(chosen+'*Loc')
        mc.select('*_ClusterHandle',d=True)
        mc.select('*_Cluster1Handle',d=True)     
        mySel=mc.ls(sl=True,tr=True)
        for item in mySel:
            xVal=mc.getAttr(item+'.tx')
            yVal=mc.getAttr(item+'.ty')
            zVal=mc.getAttr(item+'.tz')
            mirroredObject=item.replace(chosen,opposite)
            mc.setAttr(mirroredObject+'.tx', -1*(xVal))
            mc.setAttr(mirroredObject+'.ty', yVal)
            mc.setAttr(mirroredObject+'.tz', zVal)

"""
joint creator function: creates all joints, creates joint heirarchy
name: createJoints
no args
no returns
"""
def createJoints():
    mc.select('*Loc')
    sel=mc.ls(sl=True)
    mc.select(cl=True)

    for obj in sel:
        xVal=mc.getAttr(obj+'.tx')
        yVal=mc.getAttr(obj+'.ty')
        zVal=mc.getAttr(obj+'.tz')
        jointName=obj.replace('Loc','_JNT')
        myJoint=mc.joint(n=jointName,p=(xVal,yVal,zVal))
        mc.select(cl=True)
    mc.delete('Locators','Curves')
    
    mc.parent('C_HeadTop_JNT','C_HeadBase_JNT')  
    mc.parent('C_HeadBase_JNT','C_MidNeck_JNT')  
    mc.parent('C_MidNeck_JNT','C_LowerNeck_JNT') 
    mc.parent('C_LowerNeck_JNT','C_UpperChest_JNT')  
    mc.parent('C_UpperChest_JNT','C_Sternum_JNT')
    mc.parent('C_Sternum_JNT','C_LowerChest_JNT')
    mc.parent('C_LowerChest_JNT','C_Waist_JNT')
    mc.parent('C_Waist_JNT','C_Pelvis_JNT')
    
    #arms
    mc.parent('L_Clavicle_JNT','R_Clavicle_JNT','C_UpperChest_JNT')
    #left
    mc.parent('L_Shoulder_JNT','L_Clavicle_JNT')
    mc.parent('L_Elbow_JNT','L_Shoulder_JNT')
    mc.parent('L_Wrist_JNT','L_Elbow_JNT')
    mc.parent('L_FingerBase_JNT','L_Wrist_JNT')
    mc.parent('L_FingerTip_JNT','L_FingerBase_JNT')
    #right
    mc.parent('R_Shoulder_JNT','R_Clavicle_JNT')
    mc.parent('R_Elbow_JNT','R_Shoulder_JNT')
    mc.parent('R_Wrist_JNT','R_Elbow_JNT')
    mc.parent('R_FingerBase_JNT','R_Wrist_JNT')
    mc.parent('R_FingerTip_JNT','R_FingerBase_JNT')
    
    #legs
    mc.parent('L_Hip_JNT','R_Hip_JNT','C_Pelvis_JNT')
    #left
    mc.parent('L_Knee_JNT','L_Hip_JNT')
    mc.parent('L_Ankle_JNT','L_Knee_JNT')
    mc.parent('L_BallOfFoot_JNT','L_Ankle_JNT')
    mc.parent('L_ToeTip_JNT','L_BallOfFoot_JNT')
    #right
    mc.parent('R_Knee_JNT','R_Hip_JNT')
    mc.parent('R_Ankle_JNT','R_Knee_JNT')
    mc.parent('R_BallOfFoot_JNT','R_Ankle_JNT')
    mc.parent('R_ToeTip_JNT','R_BallOfFoot_JNT')
    
    makeIKs()
    makeReverseFoot()

"""
parent control function: creates two differnt types of controls, parents joints to controls
name: parentCTRL
parameters: ctrl, obj, type
    circle ctrl: designated control
    object obj: joint 
    string type: orient control or parent control
no return 
"""
def parentCTRL(ctrl,obj,type):
    offset=mc.group(ctrl,n=ctrl[0]+'_OFFSET_GRP')
    zero=mc.group(offset,n=ctrl[0]+'_ZERO_GRP')
    mc.parent(zero,obj)
    mc.setAttr(zero+'.tx',0)
    mc.setAttr(zero+'.ty',0)
    mc.setAttr(zero+'.tz',0)
    mc.setAttr(zero+'.rx',0)
    mc.setAttr(zero+'.ry',0)
    mc.setAttr(zero+'.rz',0)
    mc.parent(zero,w=True)
    #alignCtrl=mc.parentConstraint(obj,zero)
    #mc.delete(alignCtrl)
    if type=='parent':
        mc.parentConstraint(ctrl,obj)
    elif type=='orient':
        mc.orientConstraint(ctrl,obj)
        mc.setAttr(ctrl[0]+'.tx',lock=True)
        mc.setAttr(ctrl[0]+'.ty',lock=True)
        mc.setAttr(ctrl[0]+'.tz',lock=True)
        
       
"""
creates pole vectors to control direction of joint
name: createPoleVector
parameters: locName, jnt1, jnt2, jnt3, ik
    string locName: string to name new locator
    string jnt1: top joint
    string jnt2: middle joint
    string jnt3: bottom joint
    string ik: name of ik that controls the three joints
"""        
def createPoleVector(locName,jnt1,jnt2,jnt3,ik):
    pv=mc.spaceLocator(n=locName)
    pc=mc.pointConstraint(jnt1,jnt2,jnt3,locName,mo=False)
    mc.delete(pc)
    aim=mc.aimConstraint(jnt2,locName,aim=(1,0,0))
    mc.delete(aim)
    mc.move(3,r=True,wd=True,os=True,x=True)
    mc.poleVectorConstraint(locName,ik)

"""
ik maker function: creates inverse kinematic connections for arms and legs
name: makeIKs
no args
no returns
"""   
def makeIKs():
    L_LegIK= mc.ikHandle(sj='L_Hip_JNT',ee='L_Ankle_JNT',n='L_LegIK')
    R_LegIK= mc.ikHandle(sj='R_Hip_JNT',ee='R_Ankle_JNT',n='R_LegIK')
    L_ArmIK=mc.ikHandle(sj='L_Shoulder_JNT',ee='L_Wrist_JNT',n='L_ArmIK')
    R_ArmIK=mc.ikHandle(sj='R_Shoulder_JNT',ee='R_Wrist_JNT',n='R_ArmIK')
    
    #L_AnkleIK= mc.ikHandle(sj='L_Ankle_JNT',ee='L_Ankle_JNT')
    #R_AnkleIK= mc.ikHandle(sj='R_Ankle_JNT',ee='R_Ankle_JNT')
    L_BallIK= mc.ikHandle(sj='L_Ankle_JNT',ee='L_BallOfFoot_JNT',n="L_BallIK")
    R_BallIK= mc.ikHandle(sj='R_Ankle_JNT',ee='R_BallOfFoot_JNT',n="R_BallIK")
    L_ToeTipIK= mc.ikHandle(sj='L_BallOfFoot_JNT',ee='L_ToeTip_JNT',n="L_ToesIK")
    R_ToeTipIK= mc.ikHandle(sj='R_BallOfFoot_JNT',ee='R_ToeTip_JNT',n="R_ToesIK")
    
    mc.select("*IK")
    mc.group(n="IKs")

"""
reverse foot functions: makes a reverse foot
name: makeReverseFoot
no args
no returns
"""
def makeReverseFoot():
    L_revAnkle=mc.duplicate('L_Ankle_JNT',rc=True)
    R_revAnkle=mc.duplicate('R_Ankle_JNT',rc=True)
    
    mc.parent(L_revAnkle,w=True)
    mc.parent(R_revAnkle,w=True)
    for item in L_revAnkle:
        newName=item.replace('L','L_Rev')
        newName=newName.replace('JNT1','JNT')
        mc.rename(item,newName)
    for item in R_revAnkle:
        newName=item.replace('R','R_Rev')
        newName=newName.replace('JNT1','JNT')
        mc.rename(item,newName)
        
    mc.delete('effector10','effector9','effector11','effector12')
    mc.select(cl=True)
    mc.joint(n='L_Rev_Heel_JNT',p=(-2,0,-.5))
    mc.select(cl=True)
    mc.joint(n='R_Rev_Heel_JNT',p=(2,0,-.5))
    mc.select(cl=True)
   
    mc.parent('L_Rev_Ankle_JNT','L_Rev_BallOfFoot_JNT')
    mc.parent('L_Rev_BallOfFoot_JNT','L_Rev_ToeTip_JNT')
    mc.parent('L_Rev_ToeTip_JNT','L_Rev_Heel_JNT')  
    mc.parent('R_Rev_Ankle_JNT','R_Rev_BallOfFoot_JNT')
    mc.parent('R_Rev_BallOfFoot_JNT','R_Rev_ToeTip_JNT')
    mc.parent('R_Rev_ToeTip_JNT','R_Rev_Heel_JNT')
    
    mc.parent('L_LegIK','L_Rev_Ankle_JNT')
    mc.parent('L_BallIK','L_Rev_BallOfFoot_JNT')
    mc.parent('L_ToesIK','L_Rev_ToeTip_JNT')
    
    mc.parent('R_LegIK','R_Rev_Ankle_JNT')
    mc.parent('R_BallIK','R_Rev_BallOfFoot_JNT')
    mc.parent('R_ToesIK','R_Rev_ToeTip_JNT')
    
    
"""
rig maker functions: creates controls, parents joints to controls
name: makeRig
no args
no returns
"""
def makeRig():
    
    
    masterCTRL=mc.circle(n='C_CharacterMaster_CTRL',r=5,nr=(0,1,0))
    masterCTRL=masterCTRL[0]
    
    pelvisCTRL=mc.circle(n='C_Pelvis_CTRL',r=2.5,nr=(0,1,0))
    parentCTRL(pelvisCTRL,'C_Pelvis_JNT','parent')
    
    
    L_LegCTRL=mc.circle(n='L_Leg_CTRL',r=1,nr=(0,1,0))
    parentCTRL(L_LegCTRL,'L_Rev_Heel_JNT','parent')
    R_LegCTRL=mc.circle(n='R_Leg_CTRL',r=1,nr=(0,1,0))
    parentCTRL(R_LegCTRL,'R_Rev_Heel_JNT','parent')
    
    L_ToeCTRL=mc.circle(n='L_Toe_CTRL',r=.75,nr=(0,0,1))
    parentCTRL(L_ToeCTRL,'L_Rev_ToeTip_JNT','parent')
    R_ToeCTRL=mc.circle(n='R_Toe_CTRL',r=.75,nr=(0,0,1))
    parentCTRL(R_ToeCTRL,'R_Rev_ToeTip_JNT','parent')
    
    L_BallCTRL=mc.circle(n='L_Ball_CTRL',r=.75,nr=(0,0,1))
    parentCTRL(L_BallCTRL,'L_Rev_BallOfFoot_JNT','parent')
    R_BallCTRL=mc.circle(n='R_Ball_CTRL',r=.75,nr=(0,0,1))
    parentCTRL(R_BallCTRL,'R_Rev_BallOfFoot_JNT','parent')
    
    L_ArmCTRL=mc.circle(n='L_Arm_CTRL',r=1,nr=(0,1,0))
    parentCTRL(L_ArmCTRL,'L_ArmIK','parent')
    R_ArmCTRL=mc.circle(n='R_Arm_CTRL',r=1,nr=(0,1,0))
    parentCTRL(R_ArmCTRL,'R_ArmIK','parent')
    
    waistCTRL=mc.circle(n='C_Waist_CTRL',r=2,nr=(0,1,0))
    parentCTRL(waistCTRL,'C_Waist_JNT','orient')
    
    lowerChestCTRL=mc.circle(n='C_LowerChest_CTRL',r=2,nr=(0,1,0))
    parentCTRL(lowerChestCTRL,'C_LowerChest_JNT','orient')
    sternumCTRL=mc.circle(n='C_Sternum_CTRL',r=1.5,nr=(0,1,0))
    parentCTRL(sternumCTRL,'C_Sternum_JNT','orient')
    upperChestCTRL=mc.circle(n='C_UpperChest_CTRL',r=1.5,nr=(0,1,0))
    parentCTRL(upperChestCTRL,'C_UpperChest_JNT','orient')
    
    lowerNeckCTRL=mc.circle(n='C_LowerNeck_CTRL',r=1,nr=(0,1,0))
    parentCTRL(lowerNeckCTRL,'C_LowerNeck_JNT','orient')
    midNeckCTRL=mc.circle(n='C_MidNeck_CTRL',r=1,nr=(0,1,0))
    parentCTRL(midNeckCTRL,'C_MidNeck_JNT','orient')
    
    headBaseCTRL=mc.circle(n='C_HeadBase_CTRL',r=1,nr=(0,1,0))
    parentCTRL(headBaseCTRL,'C_HeadBase_JNT','orient')
    
    mc.orientConstraint(pelvisCTRL,waistCTRL)
    mc.orientConstraint(waistCTRL,lowerChestCTRL)
    mc.orientConstraint(lowerChestCTRL,sternumCTRL)
    mc.orientConstraint(sternumCTRL,upperChestCTRL)
    mc.orientConstraint(upperChestCTRL,lowerNeckCTRL)
    mc.orientConstraint(lowerNeckCTRL,midNeckCTRL)
    mc.orientConstraint(midNeckCTRL,headBaseCTRL)
    
    createPoleVector("L_ArmPV_CTRL","L_Shoulder_JNT","L_Elbow_JNT","L_Wrist_JNT","L_ArmIK")
    createPoleVector("R_ArmPV_CTRL","R_Shoulder_JNT","R_Elbow_JNT","R_Wrist_JNT","R_ArmIK")
    createPoleVector("L_LegPV_CTRL","L_Hip_JNT","L_Knee_JNT","L_Ankle_JNT","L_LegIK")
    createPoleVector("R_LegPV_CTRL","R_Hip_JNT","R_Knee_JNT","R_Ankle_JNT","R_LegIK")
    mc.select("*PV_CTRL")
    mc.group(n="PV_CTRL_GRP",w=True)
    
    mc.select("*GRP")
    mc.group(n="CTRLs",w=True)
    mc.parent("CTRLs",masterCTRL)
    
    customControls()

"""
custom control function: creates driven keyframes for specific actions
name: customControls
no args
no returns
"""
def customControls():
    # left pivToeUP
    mc.addAttr('L_Toe_CTRL',shortName='pivToeUP',longName='PivotToeUP',defaultValue=0.0,minValue=0.0,maxValue=10.0)
    mc.setAttr('L_Toe_CTRL.pivToeUP',e=True,keyable=True)
    mc.select('L_Rev_ToeTip_JNT')
    mc.setDrivenKeyframe(at='rx',cd='L_Toe_CTRL.pivToeUP')
    mc.setAttr('L_Toe_CTRL.pivToeUP',10)
    mc.setAttr('L_Rev_ToeTip_JNT.rx',90)
    mc.select('L_Rev_ToeTip_JNT')
    mc.setDrivenKeyframe(at='rx',cd='L_Toe_CTRL.pivToeUP')
    mc.setAttr('L_Toe_CTRL.pivToeUP',0)
    
    # right pivToeUP
    mc.addAttr('R_Toe_CTRL',shortName='pivToeUP',longName='PivotToeUP',defaultValue=0.0,minValue=0.0,maxValue=10.0)
    mc.setAttr('R_Toe_CTRL.pivToeUP',e=True,keyable=True)
    mc.select('R_Rev_ToeTip_JNT')
    mc.setDrivenKeyframe(at='rx',cd='R_Toe_CTRL.pivToeUP')
    mc.setAttr('R_Toe_CTRL.pivToeUP',10)
    mc.setAttr('R_Rev_ToeTip_JNT.rx',90)
    mc.select('R_Rev_ToeTip_JNT')
    mc.setDrivenKeyframe(at='rx',cd='R_Toe_CTRL.pivToeUP')
    mc.setAttr('R_Toe_CTRL.pivToeUP',0)
    
    # left pivToeSide
    mc.addAttr('L_Toe_CTRL',shortName='pivToeSIDE',longName='PivotToeSIDE',defaultValue=0.0,minValue=-10.0,maxValue=10.0)
    mc.setAttr('L_Toe_CTRL.pivToeSIDE',e=True,keyable=True)
    mc.select('L_Rev_ToeTip_JNT')
    mc.setDrivenKeyframe(at='ry',cd='L_Toe_CTRL.pivToeSIDE')
    mc.setAttr('L_Toe_CTRL.pivToeSIDE',10)
    mc.setAttr('L_Rev_ToeTip_JNT.ry',90)
    mc.select('L_Rev_ToeTip_JNT')
    mc.setDrivenKeyframe(at='ry',cd='L_Toe_CTRL.pivToeSIDE')
    mc.setAttr('L_Toe_CTRL.pivToeSIDE',-10)
    mc.setAttr('L_Rev_ToeTip_JNT.ry',-90)
    mc.select('L_Rev_ToeTip_JNT')
    mc.setDrivenKeyframe(at='ry',cd='L_Toe_CTRL.pivToeSIDE')
    mc.setAttr('L_Toe_CTRL.pivToeSIDE',0)
    
    # right pivToeSide
    mc.addAttr('R_Toe_CTRL',shortName='pivToeSIDE',longName='PivotToeSIDE',defaultValue=0.0,minValue=-10.0,maxValue=10.0)
    mc.setAttr('R_Toe_CTRL.pivToeSIDE',e=True,keyable=True)
    mc.select('R_Rev_ToeTip_JNT')
    mc.setDrivenKeyframe(at='ry',cd='R_Toe_CTRL.pivToeSIDE')
    mc.setAttr('R_Toe_CTRL.pivToeSIDE',10)
    mc.setAttr('R_Rev_ToeTip_JNT.ry',90)
    mc.select('R_Rev_ToeTip_JNT')
    mc.setDrivenKeyframe(at='ry',cd='R_Toe_CTRL.pivToeSIDE')
    mc.setAttr('R_Toe_CTRL.pivToeSIDE',-10)
    mc.setAttr('R_Rev_ToeTip_JNT.ry',-90)
    mc.select('R_Rev_ToeTip_JNT')
    mc.setDrivenKeyframe(at='ry',cd='R_Toe_CTRL.pivToeSIDE')
    mc.setAttr('R_Toe_CTRL.pivToeSIDE',0)
    
    # left ballRoll
    mc.addAttr('L_Ball_CTRL',shortName='ballRoll',longName='BallRoll',defaultValue=0.0,minValue=0.0,maxValue=10.0)
    mc.setAttr('L_Ball_CTRL.ballRoll',e=True,keyable=True)
    mc.select('L_Rev_BallOfFoot_JNT')
    mc.setDrivenKeyframe(at='ty',cd='L_Ball_CTRL.ballRoll')
    mc.setAttr('L_Ball_CTRL.ballRoll',10)
    mc.setAttr('L_Rev_BallOfFoot_JNT.ty',1)
    mc.select('L_Rev_BallOfFoot_JNT')
    mc.setDrivenKeyframe(at='ty',cd='L_Ball_CTRL.ballRoll')
    mc.setAttr('L_Ball_CTRL.ballRoll',0)
    
    # right ballRoll
    mc.addAttr('R_Ball_CTRL',shortName='ballRoll',longName='BallRoll',defaultValue=0.0,minValue=0.0,maxValue=10.0)
    mc.setAttr('R_Ball_CTRL.ballRoll',e=True,keyable=True)
    mc.select('R_Rev_BallOfFoot_JNT')
    mc.setDrivenKeyframe(at='ty',cd='R_Ball_CTRL.ballRoll')
    mc.setAttr('R_Ball_CTRL.ballRoll',10)
    mc.setAttr('R_Rev_BallOfFoot_JNT.ty',1)
    mc.select('R_Rev_BallOfFoot_JNT')
    mc.setDrivenKeyframe(at='ty',cd='R_Ball_CTRL.ballRoll')
    mc.setAttr('R_Ball_CTRL.ballRoll',0)
    

"""
tool creator functions: creates window featuring buttons for all features
name: createWindow
no args
no returns
"""    
def createWindow():
    if(mc.window('RigMaker',exists=True)):
        mc.deleteUI('RigMaker')
    mc.window('RigMaker')
    mc.columnLayout()
    mc.button('Create Proxy Rig', c='proxySkeleton()')
    mc.button('Mirror Selection',c="mirrorObjects('selection')")
    mc.button('Mirror Left to Right',c="mirrorObjects('L')")
    mc.button('Mirror Right to Left',c="mirrorObjects('R')")
    mc.button('Create Skeleton', c='createJoints()')
    mc.button('Make Rig',c='makeRig()')
    mc.showWindow('RigMaker')
    
createWindow()
    
