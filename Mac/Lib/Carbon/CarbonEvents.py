# Generated from 'CarbonEvents.h'

def FOUR_CHAR_CODE(x): return x
def FOUR_CHAR_CODE(x): return x
false = 0
true = 1
keyAEEventClass = FOUR_CHAR_CODE('evcl')
keyAEEventID = FOUR_CHAR_CODE('evti')
eventAlreadyPostedErr = -9860
eventClassInvalidErr = -9862
eventClassIncorrectErr = -9864
eventHandlerAlreadyInstalledErr = -9866
eventInternalErr = -9868
eventKindIncorrectErr = -9869
eventParameterNotFoundErr = -9870
eventNotHandledErr = -9874
eventLoopTimedOutErr = -9875
eventLoopQuitErr = -9876
eventNotInQueueErr = -9877
eventHotKeyExistsErr = -9878
eventHotKeyInvalidErr = -9879
kEventPriorityLow = 0
kEventPriorityStandard = 1
kEventPriorityHigh = 2
kEventLeaveInQueue = false
kEventRemoveFromQueue = true
kTrackMouseLocationOptionDontConsumeMouseUp = (1 << 0)
kMouseTrackingMousePressed = 1
kMouseTrackingMouseReleased = 2
kMouseTrackingMouseExited = 3
kMouseTrackingMouseEntered = 4
kMouseTrackingMouseMoved = 5
kMouseTrackingKeyModifiersChanged = 6
kMouseTrackingUserCancelled = 7
kMouseTrackingTimedOut = 8
kEventAttributeNone = 0
kEventAttributeUserEvent = (1 << 0)
kEventClassMouse = FOUR_CHAR_CODE('mous')
kEventClassKeyboard = FOUR_CHAR_CODE('keyb')
kEventClassTextInput = FOUR_CHAR_CODE('text')
kEventClassApplication = FOUR_CHAR_CODE('appl')
kEventClassAppleEvent = FOUR_CHAR_CODE('eppc')
kEventClassMenu = FOUR_CHAR_CODE('menu')
kEventClassWindow = FOUR_CHAR_CODE('wind')
kEventClassControl = FOUR_CHAR_CODE('cntl')
kEventClassCommand = FOUR_CHAR_CODE('cmds')
kEventClassTablet = FOUR_CHAR_CODE('tblt')
kEventClassVolume = FOUR_CHAR_CODE('vol ')
kEventMouseDown = 1
kEventMouseUp = 2
kEventMouseMoved = 5
kEventMouseDragged = 6
kEventMouseWheelMoved = 10
kEventMouseButtonPrimary = 1
kEventMouseButtonSecondary = 2
kEventMouseButtonTertiary = 3
kEventMouseWheelAxisX = 0
kEventMouseWheelAxisY = 1
kEventTextInputUpdateActiveInputArea = 1
kEventTextInputUnicodeForKeyEvent = 2
kEventTextInputOffsetToPos = 3
kEventTextInputPosToOffset = 4
kEventTextInputShowHideBottomWindow = 5
kEventTextInputGetSelectedText = 6
kEventRawKeyDown = 1
kEventRawKeyRepeat = 2
kEventRawKeyUp = 3
kEventRawKeyModifiersChanged = 4
kEventHotKeyPressed = 5
kEventHotKeyReleased = 6     
kEventKeyModifierNumLockBit = 16
kEventKeyModifierFnBit = 17    
kEventKeyModifierNumLockMask = 1L << kEventKeyModifierNumLockBit
kEventKeyModifierFnMask = 1L << kEventKeyModifierFnBit
kEventAppActivated = 1
kEventAppDeactivated = 2
kEventAppQuit = 3
kEventAppLaunchNotification = 4
kEventAppLaunched = 5
kEventAppTerminated = 6
kEventAppFrontSwitched = 7     
kEventAppleEvent = 1
kEventWindowUpdate = 1
kEventWindowDrawContent = 2
kEventWindowActivated = 5
kEventWindowDeactivated = 6
kEventWindowGetClickActivation = 7
kEventWindowShowing = 22
kEventWindowHiding = 23
kEventWindowShown = 24
kEventWindowHidden = 25
kEventWindowBoundsChanging = 26
kEventWindowBoundsChanged = 27
kEventWindowResizeStarted = 28
kEventWindowResizeCompleted = 29
kEventWindowDragStarted = 30
kEventWindowDragCompleted = 31
kWindowBoundsChangeUserDrag = (1 << 0)
kWindowBoundsChangeUserResize = (1 << 1)
kWindowBoundsChangeSizeChanged = (1 << 2)
kWindowBoundsChangeOriginChanged = (1 << 3)
kEventWindowClickDragRgn = 32
kEventWindowClickResizeRgn = 33
kEventWindowClickCollapseRgn = 34
kEventWindowClickCloseRgn = 35
kEventWindowClickZoomRgn = 36
kEventWindowClickContentRgn = 37
kEventWindowClickProxyIconRgn = 38
kEventWindowCursorChange = 40
kEventWindowCollapse = 66
kEventWindowCollapsed = 67
kEventWindowCollapseAll = 68
kEventWindowExpand = 69
kEventWindowExpanded = 70
kEventWindowExpandAll = 71
kEventWindowClose = 72
kEventWindowClosed = 73
kEventWindowCloseAll = 74
kEventWindowZoom = 75
kEventWindowZoomed = 76
kEventWindowZoomAll = 77
kEventWindowContextualMenuSelect = 78
kEventWindowPathSelect = 79
kEventWindowGetIdealSize = 80
kEventWindowGetMinimumSize = 81
kEventWindowGetMaximumSize = 82
kEventWindowConstrain = 83
kEventWindowHandleContentClick = 85
kEventWindowProxyBeginDrag = 128
kEventWindowProxyEndDrag = 129
kEventWindowFocusAcquired = 200
kEventWindowFocusRelinquish = 201
kEventWindowDrawFrame = 1000
kEventWindowDrawPart = 1001
kEventWindowGetRegion = 1002
kEventWindowHitTest = 1003
kEventWindowInit = 1004
kEventWindowDispose = 1005
kEventWindowDragHilite = 1006
kEventWindowModified = 1007
kEventWindowSetupProxyDragImage = 1008
kEventWindowStateChanged = 1009
kEventWindowMeasureTitle = 1010
kEventWindowDrawGrowBox = 1011
kEventWindowGetGrowImageRegion = 1012
kEventWindowPaint = 1013
kEventMenuBeginTracking = 1
kEventMenuEndTracking = 2
kEventMenuChangeTrackingMode = 3
kEventMenuOpening = 4
kEventMenuClosed = 5
kEventMenuTargetItem = 6
kEventMenuMatchKey = 7
kEventMenuEnableItems = 8
kEventMenuDispose = 1001
kEventProcessCommand = 1
kEventCommandProcess = 1
kEventCommandUpdateStatus = 2
kHICommandOK = FOUR_CHAR_CODE('ok  ')
kHICommandCancel = FOUR_CHAR_CODE('not!')
kHICommandQuit = FOUR_CHAR_CODE('quit')
kHICommandUndo = FOUR_CHAR_CODE('undo')
kHICommandRedo = FOUR_CHAR_CODE('redo')
kHICommandCut = FOUR_CHAR_CODE('cut ')
kHICommandCopy = FOUR_CHAR_CODE('copy')
kHICommandPaste = FOUR_CHAR_CODE('past')
kHICommandClear = FOUR_CHAR_CODE('clea')
kHICommandSelectAll = FOUR_CHAR_CODE('sall')
kHICommandHide = FOUR_CHAR_CODE('hide')
kHICommandPreferences = FOUR_CHAR_CODE('pref')
kHICommandZoomWindow = FOUR_CHAR_CODE('zoom')
kHICommandMinimizeWindow = FOUR_CHAR_CODE('mini')
kHICommandArrangeInFront = FOUR_CHAR_CODE('frnt')
kHICommandAbout = FOUR_CHAR_CODE('abou')
kHICommandFromMenu = (1L << 0)
kEventControlInitialize = 1000
kEventControlDispose = 1001
kEventControlGetOptimalBounds = 1003
kEventControlDefInitialize = kEventControlInitialize
kEventControlDefDispose = kEventControlDispose
kEventControlHit = 1
kEventControlSimulateHit = 2
kEventControlHitTest = 3
kEventControlDraw = 4
kEventControlApplyBackground = 5
kEventControlApplyTextColor = 6
kEventControlSetFocusPart = 7
kEventControlGetFocusPart = 8
kEventControlActivate = 9
kEventControlDeactivate = 10
kEventControlSetCursor = 11
kEventControlContextualMenuClick = 12
kEventControlClick = 13
kEventControlTrack = 51
kEventControlGetScrollToHereStartPoint = 52
kEventControlGetIndicatorDragConstraint = 53
kEventControlIndicatorMoved = 54
kEventControlGhostingFinished = 55
kEventControlGetActionProcPart = 56
kEventControlGetPartRegion = 101
kEventControlGetPartBounds = 102
kEventControlSetData = 103
kEventControlGetData = 104
kEventControlValueFieldChanged = 151
kEventControlAddedSubControl = 152
kEventControlRemovingSubControl = 153
kEventControlBoundsChanged = 154
kEventControlOwningWindowChanged = 159
kEventControlArbitraryMessage = 201
kControlBoundsChangeSizeChanged = (1 << 2)
kControlBoundsChangePositionChanged = (1 << 3)
kEventTabletPointer = 1
kEventTabletProximity = 2
kEventVolumeMounted = 1
kEventVolumeUnmounted = 2     
typeFSVolumeRefNum = FOUR_CHAR_CODE('voln') 
kEventParamDirectObject = FOUR_CHAR_CODE('----') 
kEventParamWindowRef = FOUR_CHAR_CODE('wind')
kEventParamGrafPort = FOUR_CHAR_CODE('graf')
kEventParamDragRef = FOUR_CHAR_CODE('drag')
kEventParamMenuRef = FOUR_CHAR_CODE('menu')
kEventParamEventRef = FOUR_CHAR_CODE('evnt')
kEventParamControlRef = FOUR_CHAR_CODE('ctrl')
kEventParamRgnHandle = FOUR_CHAR_CODE('rgnh')
kEventParamEnabled = FOUR_CHAR_CODE('enab')
kEventParamDimensions = FOUR_CHAR_CODE('dims')
kEventParamAvailableBounds = FOUR_CHAR_CODE('avlb')
kEventParamAEEventID = keyAEEventID
kEventParamAEEventClass = keyAEEventClass
kEventParamCGContextRef = FOUR_CHAR_CODE('cntx')
typeWindowRef = FOUR_CHAR_CODE('wind')
typeGrafPtr = FOUR_CHAR_CODE('graf')
typeGWorldPtr = FOUR_CHAR_CODE('gwld')
typeDragRef = FOUR_CHAR_CODE('drag')
typeMenuRef = FOUR_CHAR_CODE('menu')
typeControlRef = FOUR_CHAR_CODE('ctrl')
typeCollection = FOUR_CHAR_CODE('cltn')
typeQDRgnHandle = FOUR_CHAR_CODE('rgnh')
typeOSStatus = FOUR_CHAR_CODE('osst')
typeCGContextRef = FOUR_CHAR_CODE('cntx') 
kEventParamMouseLocation = FOUR_CHAR_CODE('mloc')
kEventParamMouseButton = FOUR_CHAR_CODE('mbtn')
kEventParamClickCount = FOUR_CHAR_CODE('ccnt')
kEventParamMouseWheelAxis = FOUR_CHAR_CODE('mwax')
kEventParamMouseWheelDelta = FOUR_CHAR_CODE('mwdl')
kEventParamMouseDelta = FOUR_CHAR_CODE('mdta')
kEventParamMouseChord = FOUR_CHAR_CODE('chor')
typeMouseButton = FOUR_CHAR_CODE('mbtn')
typeMouseWheelAxis = FOUR_CHAR_CODE('mwax') 
kEventParamKeyCode = FOUR_CHAR_CODE('kcod')
kEventParamKeyMacCharCodes = FOUR_CHAR_CODE('kchr')
kEventParamKeyModifiers = FOUR_CHAR_CODE('kmod')
kEventParamKeyUnicodes = FOUR_CHAR_CODE('kuni')
typeEventHotKeyID = FOUR_CHAR_CODE('hkid') 
kEventParamTextInputSendRefCon = FOUR_CHAR_CODE('tsrc')
kEventParamTextInputSendComponentInstance = FOUR_CHAR_CODE('tsci')
kEventParamTextInputSendSLRec = FOUR_CHAR_CODE('tssl')
kEventParamTextInputReplySLRec = FOUR_CHAR_CODE('trsl')
kEventParamTextInputSendText = FOUR_CHAR_CODE('tstx')
kEventParamTextInputReplyText = FOUR_CHAR_CODE('trtx')
kEventParamTextInputSendUpdateRng = FOUR_CHAR_CODE('tsup')
kEventParamTextInputSendHiliteRng = FOUR_CHAR_CODE('tshi')
kEventParamTextInputSendClauseRng = FOUR_CHAR_CODE('tscl')
kEventParamTextInputSendPinRng = FOUR_CHAR_CODE('tspn')
kEventParamTextInputSendFixLen = FOUR_CHAR_CODE('tsfx')
kEventParamTextInputSendLeadingEdge = FOUR_CHAR_CODE('tsle')
kEventParamTextInputReplyLeadingEdge = FOUR_CHAR_CODE('trle')
kEventParamTextInputSendTextOffset = FOUR_CHAR_CODE('tsto')
kEventParamTextInputReplyTextOffset = FOUR_CHAR_CODE('trto')
kEventParamTextInputReplyRegionClass = FOUR_CHAR_CODE('trrg')
kEventParamTextInputSendCurrentPoint = FOUR_CHAR_CODE('tscp')
kEventParamTextInputSendDraggingMode = FOUR_CHAR_CODE('tsdm')
kEventParamTextInputReplyPoint = FOUR_CHAR_CODE('trpt')
kEventParamTextInputReplyFont = FOUR_CHAR_CODE('trft')
kEventParamTextInputReplyPointSize = FOUR_CHAR_CODE('trpz')
kEventParamTextInputReplyLineHeight = FOUR_CHAR_CODE('trlh')
kEventParamTextInputReplyLineAscent = FOUR_CHAR_CODE('trla')
kEventParamTextInputReplyTextAngle = FOUR_CHAR_CODE('trta')
kEventParamTextInputSendShowHide = FOUR_CHAR_CODE('tssh')
kEventParamTextInputReplyShowHide = FOUR_CHAR_CODE('trsh')
kEventParamTextInputSendKeyboardEvent = FOUR_CHAR_CODE('tske')
kEventParamTextInputSendTextServiceEncoding = FOUR_CHAR_CODE('tsse')
kEventParamTextInputSendTextServiceMacEncoding = FOUR_CHAR_CODE('tssm') 
kEventParamHICommand = FOUR_CHAR_CODE('hcmd')
typeHICommand = FOUR_CHAR_CODE('hcmd') 
kEventParamWindowFeatures = FOUR_CHAR_CODE('wftr')
kEventParamWindowDefPart = FOUR_CHAR_CODE('wdpc')
kEventParamCurrentBounds = FOUR_CHAR_CODE('crct')
kEventParamOriginalBounds = FOUR_CHAR_CODE('orct')
kEventParamPreviousBounds = FOUR_CHAR_CODE('prct')
kEventParamClickActivation = FOUR_CHAR_CODE('clac')
kEventParamWindowRegionCode = FOUR_CHAR_CODE('wshp')
kEventParamWindowDragHiliteFlag = FOUR_CHAR_CODE('wdhf')
kEventParamWindowModifiedFlag = FOUR_CHAR_CODE('wmff')
kEventParamWindowProxyGWorldPtr = FOUR_CHAR_CODE('wpgw')
kEventParamWindowProxyImageRgn = FOUR_CHAR_CODE('wpir')
kEventParamWindowProxyOutlineRgn = FOUR_CHAR_CODE('wpor')
kEventParamWindowStateChangedFlags = FOUR_CHAR_CODE('wscf')
kEventParamWindowTitleFullWidth = FOUR_CHAR_CODE('wtfw')
kEventParamWindowTitleTextWidth = FOUR_CHAR_CODE('wttw')
kEventParamWindowGrowRect = FOUR_CHAR_CODE('grct')
kEventParamAttributes = FOUR_CHAR_CODE('attr')
typeWindowRegionCode = FOUR_CHAR_CODE('wshp')
typeWindowDefPartCode = FOUR_CHAR_CODE('wdpt')
typeClickActivationResult = FOUR_CHAR_CODE('clac') 
kEventParamControlPart = FOUR_CHAR_CODE('cprt')
kEventParamInitCollection = FOUR_CHAR_CODE('icol')
kEventParamControlMessage = FOUR_CHAR_CODE('cmsg')
kEventParamControlParam = FOUR_CHAR_CODE('cprm')
kEventParamControlResult = FOUR_CHAR_CODE('crsl')
kEventParamControlRegion = FOUR_CHAR_CODE('crgn')
kEventParamControlAction = FOUR_CHAR_CODE('caup')
kEventParamControlIndicatorDragConstraint = FOUR_CHAR_CODE('cidc')
kEventParamControlIndicatorRegion = FOUR_CHAR_CODE('cirn')
kEventParamControlIsGhosting = FOUR_CHAR_CODE('cgst')
kEventParamControlIndicatorOffset = FOUR_CHAR_CODE('ciof')
kEventParamControlClickActivationResult = FOUR_CHAR_CODE('ccar')
kEventParamControlSubControl = FOUR_CHAR_CODE('csub')
kEventParamControlOptimalBounds = FOUR_CHAR_CODE('cobn')
kEventParamControlOptimalBaselineOffset = FOUR_CHAR_CODE('cobo')
kEventParamControlDataTag = FOUR_CHAR_CODE('cdtg')
kEventParamControlDataBuffer = FOUR_CHAR_CODE('cdbf')
kEventParamControlDataBufferSize = FOUR_CHAR_CODE('cdbs')
kEventParamControlDrawDepth = FOUR_CHAR_CODE('cddp')
kEventParamControlDrawInColor = FOUR_CHAR_CODE('cdic')
kEventParamControlFeatures = FOUR_CHAR_CODE('cftr')
kEventParamControlPartBounds = FOUR_CHAR_CODE('cpbd')
kEventParamControlOriginalOwningWindow = FOUR_CHAR_CODE('coow')
kEventParamControlCurrentOwningWindow = FOUR_CHAR_CODE('ccow')
typeControlActionUPP = FOUR_CHAR_CODE('caup')
typeIndicatorDragConstraint = FOUR_CHAR_CODE('cidc')
typeControlPartCode = FOUR_CHAR_CODE('cprt') 
kEventParamCurrentMenuTrackingMode = FOUR_CHAR_CODE('cmtm')
kEventParamNewMenuTrackingMode = FOUR_CHAR_CODE('nmtm')
kEventParamMenuFirstOpen = FOUR_CHAR_CODE('1sto')
kEventParamMenuItemIndex = FOUR_CHAR_CODE('item')
kEventParamMenuCommand = FOUR_CHAR_CODE('mcmd')
kEventParamEnableMenuForKeyEvent = FOUR_CHAR_CODE('fork')
kEventParamMenuEventOptions = FOUR_CHAR_CODE('meop')
typeMenuItemIndex = FOUR_CHAR_CODE('midx')
typeMenuCommand = FOUR_CHAR_CODE('mcmd')
typeMenuTrackingMode = FOUR_CHAR_CODE('mtmd')
typeMenuEventOptions = FOUR_CHAR_CODE('meop') 
kEventParamProcessID = FOUR_CHAR_CODE('psn ')
kEventParamLaunchRefCon = FOUR_CHAR_CODE('lref')
kEventParamLaunchErr = FOUR_CHAR_CODE('err ') 
kEventParamTabletPointerRec = FOUR_CHAR_CODE('tbrc')
kEventParamTabletProximityRec = FOUR_CHAR_CODE('tbpx')
typeTabletPointerRec = FOUR_CHAR_CODE('tbrc')
typeTabletProximityRec = FOUR_CHAR_CODE('tbpx') 
# sHandler = NewEventHandlerUPP( x )
kUserFocusAuto = -1
