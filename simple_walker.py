import mujoco
import mujoco_viewer
import numpy as np

model = mujoco.MjModel.from_xml_path('walky_guy.xml')
data = mujoco.MjData(model)

# create the viewer object
viewer = mujoco_viewer.MujocoViewer(model, data)

# Apply torque to the motors
num_actuators = model.nu
torque = np.array([1.0, -1.0, -1.0])
data.ctrl[:num_actuators] = torque

switched = False
# simulate and render
for i in range(10000):
    if viewer.is_alive:
        if i%20 == 0:
            if switched:
                torque = np.array([-0.2, 0.2, 0.4])
                switched = False
            else:
                torque = np.array([0.6, -0.6, -0.6])
                switched = True
        data.ctrl[:num_actuators] = torque
        mujoco.mj_step(model, data)
        viewer.render()
    else:
        break

# close
viewer.close()