:orphan:

=======================
Notification's diagrams
=======================

Full startup process
====================

.. blockdiag::
    :width: 600

    blockdiag StartupProcess {
      orientation = portrait;

      AddOtherNode [color = silver];
      AddSleepingNode [color = silver];

      DriverReady -> AddControllerNode -> AddOtherNode;
      AddOtherNode -> AddOtherNode [style = dashed];
      AddOtherNode -> ControllerEssentialNodeQueriesComplete -> ValueChanged;
      ValueChanged -> ValueChanged [style = dashed];
      ValueChanged -> EssentialNodeQueriesComplete;
      EssentialNodeQueriesComplete -> EssentialNodeQueriesComplete [style = dashed];

      EssentialNodeQueriesComplete -> AwakeNodesQueried -> AddSleepingNode;
      AddSleepingNode -> AddSleepingNode [style = dashed];
      AddSleepingNode -> SleepingValueChanged;
      SleepingValueChanged -> SleepingValueChanged [style = dashed];
      SleepingValueChanged -> EssentialSleepingNodeQueriesComplete;
      EssentialSleepingNodeQueriesComplete -> EssentialSleepingNodeQueriesComplete [style = dashed];
      EssentialSleepingNodeQueriesComplete -> AllNodesQueriedSomeDead;

      AddNodeProcess [color = silver];
      AddNodeProcess -> NodeAdded [style = none, color = none];
      NodeAdded -> NodeProtocolInfo -> EssentialNodeQueriesComplete -> ValueAdded_Basic;
      ValueAdded_Basic -> ValueAdded_Basic [style = dashed];
      ValueAdded_Basic -> NodeNaming -> Group;
      Group -> Group [style = dashed];
      Group -> Version;
    }
