from fractions import Fraction

def get_settings(camera):
    """Returns a dictionary of settings of the camera
    Input:
        camera: PiCamera camera object
    Output:
        settings: Dictionary, the settings of the camera
    """
    settings = {}
    settings['iso'] = camera.iso
    settings['shutter_speed'] = camera.shutter_speed
    settings['exposure_speed'] = camera.exposure_speed
    settings['awb'] = camera.awb_gains

    return settings

def set_settings(camera, settings):
    """Updates the camera settings based on the settings dictionary
       Only updates existing settings
    Inputs:
        camera: PiCamera camera object
        settings: Dictionary, the settings of the camera
    Output:
        camera: PiCamera camera object with updated settings
    """
    if type(settings) is not dict:
        print('Setting imporperly formatted')
        return camera
    
    for key in settings:
        if key == 'iso':
            camera.iso = int(settings[key])
        elif key == 'shutter_speed':
            camera.shutter_speed = int(settings[key])
        elif key == 'awb':
            camera.awb_mode = 'off'
            camera.awb_gains = awb_gain_parser(settings[key])

def print_something():
    print('something')

def awb_gain_parser(awb_settings):
    """ Returns tuple of awb fractions
    Input:
        awb_settings: string, in format (Fraction(513, 256), Fraction(187, 128))
    Output:
        awb_settings: tuple of fractions, the awb setting
    """
    split_string = awb_settings.split(', ')
    print(split_string)

    first_num = int(split_string[0].split('(')[2])
    first_den = int(split_string[1][:-1])

    second_num = int(split_string[2].split('(')[1])
    second_den = int(split_string[3][:-2])

    awb_settings = (Fraction(first_num, first_den), Fraction(second_num, second_den))

    return awb_settings
