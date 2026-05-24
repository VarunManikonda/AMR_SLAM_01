# ===== SETUP (one time) =====
mkdir -p ~/claude_ws/src
cd ~/claude_ws/src
git clone https://github.com/VarunManikonda/AMR_SLAM_01.git my_amr
mkdir -p ~/claude_ws/src/my_amr/rviz
cd ~/claude_ws
colcon build --symlink-install
source install/setup.bash
ros2 pkg list | grep my_amr

# ===== SLAM MAPPING (4 terminals) =====

# Terminal 1 - robot
source ~/claude_ws/install/setup.bash
ros2 launch my_amr robot.launch.py

# Terminal 2 - SLAM Toolbox
source ~/claude_ws/install/setup.bash
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true slam_params_file:=$HOME/claude_ws/src/my_amr/config/slam_params.yaml

# Terminal 3 - RViz (Fixed Frame = map; add Map, LaserScan, RobotModel, TF)
source ~/claude_ws/install/setup.bash
ros2 run rviz2 rviz2

# Terminal 4 - teleop (drive with i j k l , slowly around the room)
source ~/claude_ws/install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard

# ===== SAVE THE MAP (new terminal, once map looks complete) =====
source ~/claude_ws/install/setup.bash
ros2 run nav2_map_server map_saver_cli -f $HOME/claude_ws/src/my_amr/maps/my_map

# ===== AUTONOMOUS NAVIGATION WITH NAV2 (2 terminals) =====

# Terminal 1 - robot
source ~/claude_ws/install/setup.bash
ros2 launch my_amr robot.launch.py

# Terminal 2 - Nav2 + RViz (wait ~5s after Terminal 1)
source ~/claude_ws/install/setup.bash
ros2 launch my_amr nav2.launch.py