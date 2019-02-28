from onvif import ONVIFCamera
from time import sleep


class Camera:
    def __init__(self, ip, port, login, password, debug=False):
        # Connecting to the camera
        self.my_cam = ONVIFCamera(
            ip,
            port,
            login,
            password
        )

        # Getting device information
        if debug:
            print('Device information: ' + str(self.my_cam.devicemgmt.GetDeviceInformation()))
        if debug:
            print('--------------------------------------------------------------------------------')

        # Getting hostname
        if debug:
            print('Device hostname: ' + str(self.my_cam.devicemgmt.GetHostname().Name))
        if debug:
            print('--------------------------------------------------------------------------------')

        # Getting system date and time
        dt = self.my_cam.devicemgmt.GetSystemDateAndTime()
        tz = dt.TimeZone
        year = dt.UTCDateTime.Date.Year
        hour = dt.UTCDateTime.Time.Hour

        if debug:
            print('Timezone: ' + str(tz))
        if debug:
            print('Year: ' + str(year))
        if debug:
            print('Hour: ' + str(hour))
        if debug:
            print('--------------------------------------------------------------------------------')

        # Creating media service
        self.media_service = self.my_cam.create_media_service()

        # Edited "site-packages/zeep/xsd/types/simple.py"
        #     def pythonvalue(self, xmlvalue):
        #         return xmlvalue

        # Getting profiles
        self.profiles = self.media_service.GetProfiles()
        self.media_profile = self.profiles[0]

        if debug:
            print("Profiles: " + str(self.profiles))
        if debug:
            print('--------------------------------------------------------------------------------')

        # Getting token
        token = self.media_profile.token

        if debug:
            print("Token: " + str(token))
        if debug:
            print('--------------------------------------------------------------------------------')

        # Creating PTZ service
        self.ptz = self.my_cam.create_ptz_service()

        # Getting available PTZ services
        request = self.ptz.create_type('GetServiceCapabilities')
        service_capabilities = self.ptz.GetServiceCapabilities(request)

        if debug:
            print("Service capabilities: " + str(service_capabilities))
        if debug:
            print('--------------------------------------------------------------------------------')

        # Getting PTZ status
        status = self.ptz.GetStatus({'ProfileToken': token})

        if debug:
            print("PTZ status: " + str(status))
        if debug:
            print('--------------------------------------------------------------------------------')
        if debug:
            print('Pan position:' + str(status.Position.PanTilt.x))
        if debug:
            print('Tilt position:' + str(status.Position.PanTilt.y))
        if debug:
            print('Zoom position:' + str(status.Position.Zoom.x))
        if debug:
            try:
                print('Pan/Tilt Moving?:' + str(status.MoveStatus.PanTilt))
            except:
                pass
        if debug:
            print('--------------------------------------------------------------------------------')

        # Getting PTZ configuration options for getting option ranges
        request = self.ptz.create_type('GetConfigurationOptions')
        request.ConfigurationToken = self.media_profile.PTZConfiguration.token
        ptz_configuration_options = self.ptz.GetConfigurationOptions(request)

        if debug:
            print('PTZ configuration options: ' + str(ptz_configuration_options))
        if debug:
            print('--------------------------------------------------------------------------------')

        # Getting move options
        self.request_continuous_move = self.ptz.create_type('ContinuousMove')
        self.request_continuous_move.ProfileToken = self.media_profile.token

        if debug:
            print('Continuous move options: ' + str(self.request_continuous_move))
        if debug:
            print('--------------------------------------------------------------------------------')

        self.request_absolute_move = self.ptz.create_type('AbsoluteMove')
        self.request_absolute_move.ProfileToken = self.media_profile.token

        if debug:
            print('Absolute move options: ' + str(self.request_absolute_move))
        if debug:
            print('--------------------------------------------------------------------------------')

        self.request_relative_move = self.ptz.create_type('RelativeMove')
        self.request_relative_move.ProfileToken = self.media_profile.token

        if debug:
            print('Relative move options: ' + str(self.request_relative_move))
        if debug:
            print('--------------------------------------------------------------------------------')

        self.request_stop = self.ptz.create_type('Stop')
        self.request_stop.ProfileToken = self.media_profile.token

        if debug:
            print('Stop options: ' + str(self.request_stop))
        if debug:
            print('--------------------------------------------------------------------------------')

        # Creating imaging service
        self.imaging = self.my_cam.create_imaging_service()

        # Getting available imaging services
        request = self.imaging.create_type('GetServiceCapabilities')
        service_capabilities = self.ptz.GetServiceCapabilities(request)

        if debug:
            print("Service capabilities: " + str(service_capabilities))
        if debug:
            print('--------------------------------------------------------------------------------')

        # Getting imaging status
        status = self.imaging.GetStatus({'VideoSourceToken': self.profiles[0].VideoSourceConfiguration.SourceToken})

        if debug:
            print("Imaging status: " + str(status))
        if debug:
            print('--------------------------------------------------------------------------------')

        self.request_absolute_focus = self.imaging.create_type('Move')
        self.request_absolute_focus.VideoSourceToken = self.profiles[0].VideoSourceConfiguration.SourceToken

        if debug:
            print('Focus move options: ' + str(self.request_absolute_focus))
        if debug:
            print('--------------------------------------------------------------------------------')

        self.stop()

    def get_position(self):
        # Getting PTZ status
        status = self.ptz.GetStatus({'ProfileToken': self.media_profile.token})

        print("PTZ position: " + str(status.Position))
        print('--------------------------------------------------------------------------------')

    # Stop any movement
    def stop(self):
        self.request_stop.PanTilt = True
        self.request_stop.Zoom = True

        self.ptz.Stop(self.request_stop)

        # print('Stopping camera')

    # Continuous move functions
    def perform_continuous_move(self, timeout):
        # Start continuous move
        self.ptz.ContinuousMove(self.request_continuous_move)

        # Wait a certain time
        sleep(timeout)

        # Stop continuous move
        self.stop()

        # print('Continuous move completed')
        sleep(2)

    def move_tilt(self, velocity, timeout):
        print('Tilting with velocity: \'' + str(velocity) + '\' and timeout: \'' + str(timeout) + '\'')

        status = self.ptz.GetStatus({'ProfileToken': self.media_profile.token})
        status.Position.PanTilt.x = 0.0
        status.Position.PanTilt.y = velocity

        self.request_continuous_move.Velocity = status.Position

        self.perform_continuous_move(timeout)

    def move_pan(self, velocity, timeout):
        print('Panning with velocity: \'' + str(velocity) + '\' and timeout: \'' + str(timeout) + '\'')

        status = self.ptz.GetStatus({'ProfileToken': self.media_profile.token})
        status.Position.PanTilt.x = velocity
        status.Position.PanTilt.y = 0.0

        self.request_continuous_move.Velocity = status.Position

        self.perform_continuous_move(timeout)

    def move_diagonal(self, velocity_one, velocity_two, timeout):
        print('Moving diagonally with velocity: \'' + str(velocity_one) + ':' + str(velocity_two) +
              '\' and timeout: \'' + str(timeout) + '\'')

        status = self.ptz.GetStatus({'ProfileToken': self.media_profile.token})
        status.Position.PanTilt.x = velocity_one
        status.Position.PanTilt.y = velocity_two

        self.request_continuous_move.Velocity = status.Position

        self.perform_continuous_move(timeout)

    def move_zoom(self, velocity, timeout):
        print('Zooming with velocity: \'' + str(velocity) + '\' and timeout: \'' + str(timeout) + '\'')

        status = self.ptz.GetStatus({'ProfileToken': self.media_profile.token})
        status.Position.Zoom.x = velocity

        self.request_continuous_move.Velocity = status.Position

        self.perform_continuous_move(timeout)

    def move_custom(self, velocity_one, velocity_two, velocity_three, timeout_one, timeout_two, timeout_three):
        self.move_tilt(velocity_one, timeout_one)
        self.move_pan(velocity_two, timeout_two)
        self.move_zoom(velocity_three, timeout_three)

    # Absolute move functions
    def perform_absolute_move(self):
        # Start absolute move
        self.ptz.AbsoluteMove(self.request_absolute_move)

        # print('Absolute move completed')
        sleep(4)

    def move_absolute(self, x, y, z):
        print('Moving to: \'' + str(x) + ':' + str(y) + ':' + str(z))

        status = self.ptz.GetStatus({'ProfileToken': self.media_profile.token})
        status.Position.PanTilt.x = x
        status.Position.PanTilt.y = y
        status.Position.Zoom.x = z

        self.request_absolute_move.Position = status.Position

        self.perform_absolute_move()

    def change_focus(self, x):
        print('Changing focus: ' + str(x))

        # status = self.imaging.GetStatus({'VideoSourceToken': self.profiles[0].VideoSourceConfiguration.SourceToken})
        # status.FocusStatus20.Position = x

        self.request_absolute_focus.Focus = x
        self.imaging.Move(self.request_absolute_focus)