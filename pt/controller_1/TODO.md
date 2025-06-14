
# Pending Tasks

1. Bring out all the scheduling of water pumps into config
1. Test the code.
1. Create PT DevOps using these steps
   1. Create "install", "start", "update" and "stop" scripts for
      plant controller.
      Make the scripts use pm2 npm package
   1. Write manager python script that receives three STOMP messages:
      one per each script and execute them.
   1. Let `.gitlab-ci.yaml` have a release stage that checks for
      commit on "release:latest" branch and sends one of
      the STOMP message
1. Improve the controller to support W3C Thing abstraction so that
   integration with third-party IoT systems is smooth.
1. Release [greenhouse DT](https://github.com/sievericcardo/greenhouse-dt-api)
   with the next release of the plant controller
1. There are three builds of the controller which would enable
   fleet abstraction. The effort in this direction is to identify and
   construct lightweight fleet DT for these three controllers.
1. Better integration with the semantic DT technologies being developed
   in Einar's group.
