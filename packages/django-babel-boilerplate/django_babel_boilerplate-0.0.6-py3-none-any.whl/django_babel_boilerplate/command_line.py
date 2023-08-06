import sys, os
from django.core.management import utils

__version__ = "0.0.6"

project_name = sys.argv[1]

def main():
    if '-' in project_name:
        print( "ERROR: Choose different name without using hyphen '-'")
        print("FAILED to create a new project.")
    else:
        ROOT_FOLDER = os.mkdir(str(project_name))

        ROOT_PATH = os.path.join(os.path.abspath(ROOT_FOLDER), project_name)
        MAIN_APP_NAME = os.mkdir(os.path.join(ROOT_PATH, project_name))
        STATIC_FOLDER = os.mkdir(os.path.join(ROOT_PATH, 'static'))
        TEMPLATES = os.mkdir(os.path.join(ROOT_PATH, 'templates'))

        SVG_FOLDER = os.mkdir(os.path.join(ROOT_PATH, 'svg'))

        SVG_PATH = os.path.join(os.path.abspath(ROOT_FOLDER), project_name + '\\svg')
        STATIC_PATH = os.path.join(os.path.abspath(ROOT_FOLDER), project_name + '\\static')
        MAIN_APP_PATH = os.path.join(os.path.abspath(ROOT_FOLDER), project_name + '\\' + project_name)
        TEMPLATES_PATH = os.path.join(os.path.abspath(ROOT_FOLDER), project_name + '\\templates')
        SETTINGS_FOLDER = os.mkdir(os.path.join(MAIN_APP_PATH, 'settings'))
        MAIN_APP_SETTINGS_PATH = os.path.join(os.path.abspath(ROOT_FOLDER), project_name + '\\' + project_name + '\\settings')

        STATIC_COMMON_FILES = os.mkdir(os.path.join(STATIC_PATH, 'common'))
        STATIC_HOME_FILES = os.mkdir(os.path.join(STATIC_PATH, 'home'))
        STATIC_DIST_FILES = os.mkdir(os.path.join(STATIC_PATH, 'dist'))

        STATIC_COMMON_PATH = os.path.join(os.path.abspath(ROOT_FOLDER), project_name + '\\static\\common')
        STATIC_DIST_PATH = os.path.join(os.path.abspath(ROOT_FOLDER), project_name + '\\static\\dist')
        STATIC_HOME_PATH = os.path.join(os.path.abspath(ROOT_FOLDER), project_name + '\\static\\home')

        secret_key = utils.get_random_secret_key()

        svg= open(os.path.join(SVG_PATH, 'creator.svg'), "w+")
        svg.write("""
<?xml version="1.0" encoding="utf-8"?>
<!-- Generator: Adobe Illustrator 16.0.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 width="339.538px" height="414.592px" viewBox="0 0 339.538 414.592" enable-background="new 0 0 339.538 414.592"
	 xml:space="preserve">
<g>
	<g>
		<g id="face">
			<polygon fill="#F8DBB2" points="105.317,111.174 105.317,115.294 104.909,118.591 104.909,123.741 104.909,130.54 
				104.909,134.042 105.114,137.749 105.317,143.312 105.52,150.935 106.336,155.466 106.54,159.587 106.54,163.089 106.874,167.06 
				107.305,171.009 107.848,174.079 108.391,177.589 108.934,180.552 109.911,183.622 110.887,187.241 112.622,190.86 
				114.249,193.935 116.311,197.774 118.479,200.624 119.999,203.696 122.709,207.646 125.204,211.483 127.266,213.788 
				129.11,216.53 131.497,219.161 133.991,222.999 136.161,225.962 138.438,228.925 140.715,232.214 142.452,234.956 
				144.731,239.452 146.575,241.978 149.069,244.826 151.672,246.691 155.145,248.776 158.397,249.655 162.954,250.751 
				165.883,250.751 172.389,250.751 178.899,250.093 183.997,249.216 187.36,248.558 190.504,247.788 193.436,246.58 
				195.278,244.609 198.534,240.989 201.028,238.028 203.631,234.847 206.342,231.667 208.405,228.925 210.899,225.634 
				213.176,221.903 216.649,217.737 220.227,213.458 223.157,210.495 226.084,206.878 228.473,203.366 230.858,199.747 
				233.139,196.124 234.764,192.286 236.067,188.667 237.694,184.827 238.344,181.208 239.43,175.835 240.19,172.435 
				240.514,169.474 241.057,165.853 241.708,162.999 242.467,158.394 243.227,154.665 243.661,150.604 244.204,145.231 
				244.637,141.501 245.286,136.565 246.481,128.228 246.481,125.813 246.481,123.073 246.481,119.013 246.698,114.405 
				246.372,110.018 246.047,106.069 245.073,102.011 244.204,99.048 242.141,94.332 239.971,91.041 237.153,86.106 234.655,83.473 
				230.319,79.634 226.196,77.221 220.446,75.357 214.915,73.821 205.37,72.066 200.706,71.956 193.112,71.627 185.084,70.969 
				178.25,70.969 169.247,70.969 162.305,70.969 155.145,70.969 149.071,71.299 138.333,71.627 133.561,72.834 127.266,74.918 
				122.061,77.221 118.7,80.183 115.77,82.595 113.167,87.093 110.239,92.248 108.719,95.758 107.526,99.488 106.44,102.779 
				105.463,106.727 			"/>
			<g>
				<polygon stroke="#000000" stroke-miterlimit="10" points="94.503,112.618 94.594,114.365 94.685,116.204 94.685,117.398 
					95.231,119.33 95.867,121.718 96.322,123.097 97.412,124.476 98.594,125.763 99.231,127.326 99.776,128.337 100.412,130.083 
					100.958,131.646 101.322,133.484 102.141,135.232 102.958,137.347 103.414,138.816 104.321,140.472 105.049,142.402 
					105.777,143.503 106.321,144.792 107.23,146.08 108.14,147.367 109.14,148.193 110.049,148.929 110.777,149.849 
					112.231,150.767 113.323,151.318 114.595,152.054 115.958,152.605 117.323,153.158 118.686,153.708 120.231,154.078 
					122.05,154.169 124.141,154.445 125.868,154.812 127.414,154.904 129.141,155.087 131.232,155.087 132.869,155.271 
					134.778,155.546 136.778,155.546 139.232,155.64 141.687,155.363 143.961,155.179 145.871,154.998 147.324,154.628 
					149.233,153.894 150.871,153.25 152.597,152.699 154.415,151.134 156.505,149.574 157.778,148.101 159.323,145.988 
					159.959,144.425 161.323,142.035 162.504,140.011 163.415,137.529 164.233,135.416 165.051,133.578 165.415,132.382 
					166.143,130.636 167.233,130.083 168.506,129.441 169.961,128.98 171.506,128.796 172.415,128.796 174.415,129.164 
					175.688,129.533 177.143,130.636 177.87,131.646 178.325,132.841 178.959,134.589 179.506,137.07 180.143,139.093 
					180.598,141.298 181.233,143.044 181.778,144.792 182.778,146.814 183.78,149.113 184.961,150.492 186.325,152.054 
					187.78,153.525 189.235,154.812 191.506,156.007 193.688,157.019 196.143,157.937 198.325,158.214 200.235,158.396 
					202.415,158.582 204.508,158.673 206.506,158.582 208.051,158.582 210.327,158.673 212.143,158.582 213.69,158.582 
					216.145,158.582 218.508,158.582 219.69,158.306 222.143,158.123 224.508,157.937 226.143,157.386 228.417,156.375 
					230.237,155.64 232.145,154.353 233.874,152.882 235.692,150.859 236.872,149.113 238.237,147 239.145,145.253 240.417,142.677 
					241.327,140.748 242.235,138.724 243.327,136.244 244.418,133.667 246.053,131.646 248.053,129.9 249.418,127.326 
					249.958,125.212 250.413,123.466 250.866,120.523 251.047,119.052 250.686,118.226 248.684,117.398 246.774,117.123 
					244.411,116.57 241.866,116.204 239.958,116.111 237.592,115.743 235.321,115.743 232.594,115.743 230.321,115.651 
					227.592,115.467 225.321,115.376 223.592,115.283 220.139,114.916 218.229,114.64 215.864,114.64 213.229,114.732 
					210.229,114.548 207.047,114.732 203.59,115.1 201.047,115.283 198.319,115.651 195.411,115.928 192.864,116.662 
					190.411,117.398 186.956,118.132 184.137,119.052 180.864,119.511 176.772,120.339 172.682,120.523 169.499,120.248 
					166.135,119.605 164.135,119.052 163.045,118.41 160.872,117.398 157.51,116.387 155.054,115.651 151.692,114.824 
					148.055,113.629 146.054,113.077 143.145,112.709 140.053,112.342 137.236,111.974 134.691,111.699 131.873,111.238 
					128.6,111.146 126.417,110.963 123.242,110.687 120.06,110.687 117.879,110.687 114.515,110.687 112.06,110.687 
					109.606,110.687 106.333,110.872 104.333,111.146 101.696,111.515 98.97,111.974 96.514,112.342 94.878,112.525 				"/>
				<polyline fill="#F8DBB2" stroke="#000000" stroke-miterlimit="10" points="104.909,118.077 106,116.79 106.818,116.237 
					108.546,115.778 110.728,115.41 111.818,115.41 114.091,115.41 116.546,115.41 118.365,115.41 121.456,115.41 124.637,115.502 
					127.274,115.502 129.911,115.778 132.729,115.87 135.457,116.146 138.638,116.513 142.002,117.065 145.001,117.524 
					147.547,118.26 150.184,119.087 152.729,120.006 155.002,121.202 156.73,122.581 158.184,124.051 158.821,125.614 
					159.549,127.454 159.911,129.383 160.274,131.221 160.09,132.969 159.911,135.268 159.366,136.92 158.731,138.852 158,140.782 
					157.002,142.622 155.457,145.379 153.184,147.676 150.639,149.792 147.729,151.262 144.002,151.999 141.274,152.458 
					137.546,152.549 134.275,152.366 130.637,152.088 127.001,151.815 123.273,151.17 119.819,150.528 115.364,149.147 
					113.274,147.77 111.456,146.575 109.909,144.918 109.09,143.631 108.274,141.424 107.637,139.772 106.818,137.475 
					106.273,135.727 105.818,134.715 105.182,132.969 104.909,131.407 104.636,129.844 104.363,128.004 104.182,126.35 
					104.182,125.063 104.182,123.5 104.272,121.752 104.455,119.916 104.728,118.444 				"/>
				<polygon fill="#F8DBB2" stroke="#000000" stroke-miterlimit="10" points="184.87,126.511 186.143,125.039 187.415,123.57 
					189.143,122.19 191.325,121.178 193.506,120.167 196.688,119.524 199.598,118.972 202.235,118.879 204.961,118.42 
					207.233,118.329 209.69,118.053 212.235,118.053 214.417,118.053 217.235,118.053 220.78,118.053 224.053,118.42 
					226.963,118.696 229.78,118.879 232.053,119.155 235.598,120.074 238.145,120.902 239.327,122.19 240.053,123.751 
					240.327,125.408 240.237,126.787 239.963,129.267 239.78,131.476 239.053,133.587 238.418,135.886 237.69,137.541 
					237.235,139.839 236.325,141.771 235.327,143.792 234.235,145.539 233.327,147.47 232.325,149.216 231.143,150.503 
					229.417,151.791 228.143,152.802 225.78,153.72 223.053,154.548 219.508,155.101 217.325,155.375 214.506,155.466 
					211.598,155.466 208.053,155.466 204.417,155.191 201.506,154.732 199.325,154.548 197.504,153.998 195.959,153.445 
					193.961,152.435 192.233,151.791 191.596,151.421 190.688,150.687 189.688,149.767 189.143,149.033 187.959,147.376 
					186.961,145.722 186.415,144.896 185.506,142.599 184.778,141.126 183.959,138.919 183.504,137.267 183.325,135.703 
					183.233,133.404 183.233,131.841 183.504,130.187 184.053,128.808 				"/>
			</g>
		</g>
		<path fill="#F8DBB2" d="M108.047,233.828"/>
	</g>
	<polygon fill="#4F5B66" points="6.468,167.095 15.091,166.49 27.487,166.49 38.029,166.245 51.739,166.49 63.057,166.49 
		72.758,166.49 82.998,166.49 94.855,166.49 107.251,166.49 123.958,167.095 137.432,167.095 153.6,167.095 168.69,165.885 
		187.014,165.885 202.645,166.49 217.735,166.49 237.676,167.095 250.075,167.095 266.782,167.095 285.104,167.095 308.278,166.49 
		329.836,165.885 336.842,171.936 338.999,178.593 339.538,193.115 338.459,206.429 337.381,221.557 336.303,235.475 
		335.227,249.999 333.61,262.103 332.532,272.39 331.993,279.649 330.915,289.333 329.836,305.671 328.758,323.825 327.141,342.583 
		324.985,359.528 323.37,374.655 322.292,389.784 320.674,403.097 316.901,407.937 312.59,412.778 308.278,413.989 301.811,414.593 
		285.643,413.989 270.014,414.593 252.766,413.989 223.125,413.989 184.858,413.989 30.181,413.989 23.714,409.751 20.481,406.122 
		19.942,399.466 18.863,390.388 16.708,376.47 15.63,360.132 14.013,343.188 12.935,322.614 10.779,305.671 8.623,288.122 
		7.546,263.917 5.39,243.341 3.773,227.004 1.617,209.454 0,196.141 0,181.013 2.696,168.911 	"/>
	<g>
		<path fill="#FFFFFF" d="M151.088,258.994c-0.959-1.44-2.666-1.637-3.816-0.435l-16.265,17.005
			c-0.615,0.647-0.974,1.604-0.974,2.614s0.357,1.965,0.974,2.613l16.265,17.004c0.506,0.528,1.121,0.787,1.732,0.787
			c0.777,0,1.549-0.415,2.084-1.223c0.959-1.442,0.805-3.592-0.346-4.793l-13.764-14.391l13.764-14.394
			C151.891,262.585,152.047,260.439,151.088,258.994z"/>
		<path fill="#FFFFFF" d="M182.458,260.078c-1.152-1.203-2.855-1.006-3.816,0.436c-0.959,1.443-0.805,3.589,0.348,4.792
			l13.764,14.391l-13.764,14.393c-1.15,1.202-1.307,3.348-0.348,4.793c0.535,0.806,1.307,1.222,2.084,1.222
			c0.611,0,1.227-0.259,1.732-0.788l16.264-17.004c0.617-0.646,0.975-1.604,0.975-2.613c0-1.009-0.355-1.967-0.975-2.612
			L182.458,260.078z"/>
		<path fill="#FFFFFF" d="M173.073,251.246c-1.369-0.743-2.967,0.054-3.557,1.787l-16.262,47.613
			c-0.592,1.726,0.051,3.725,1.426,4.464c0.346,0.189,0.709,0.275,1.064,0.275c1.051,0,2.051-0.771,2.49-2.063l16.262-47.611
			C175.086,253.986,174.45,251.986,173.073,251.246z"/>
	</g>
	<polygon id="hair" points="96.425,121 95.758,117.333 95.227,112.518 93.021,106.032 90.758,102 90.758,91.333 90.425,84.667 89.712,76.676 
		91.424,72.34 92.091,68.673 92.092,65 90.425,65.333 92.092,59.667 93.387,57.561 89.712,55.171 84.936,53.464 88.425,47.333 
		90.758,44.667 91.918,41.518 90.758,37 95.96,35.032 104.413,32.301 105.148,29.229 99.266,24.451 101.092,20.667 105.515,18.307 
		111.092,17.667 113.232,15.233 116.425,14.333 118.092,11 123.758,11 129.425,10.333 136.092,8.667 144.092,9 151.758,9 
		157.698,8.066 160.639,8.066 157.424,3.667 155.86,0.898 165.047,0.898 175.092,0 183.758,0 194.424,0 205.836,1.238 
		209.092,2.667 215.024,3.287 213.092,7 220.424,4.667 218.698,8.408 224.577,8.749 228.622,12.162 235.233,16.259 237.758,22.667 
		241.092,30.333 241.092,36.333 241.483,42.542 246.26,43.908 249.758,45.667 253.092,55 254.092,61 254.092,76.333 254.092,87.667 
		251.774,94.426 252.092,102.667 250.424,114 249.2,127.195 245.09,130.007 243.321,129.244 242.959,124.482 241.114,125.83 
		240.379,117.296 238.176,118.32 238.092,110.667 236.092,109 235.969,103.301 234.135,104.666 232.424,92 230.092,83.667 
		229.723,79.748 222.424,85 212.424,94.667 204.424,98.667 195.424,104 184.092,107 186.758,96 175.424,97.333 168.092,102.667 
		158.424,105.667 153.653,108.763 155.092,102 148.141,102.96 142.758,104 135.758,106.333 130.136,109.446 132.424,102.667 
		135.092,97 138.219,89.989 139.424,86.667 128.664,89.989 119.425,94 112.425,99 109.758,104.667 106.779,110.772 104.313,118.705 
		104.779,125.489 103.424,131.673 98.623,122.116 	"/>
</g>
</svg>
        """)
        svg.close()

        # TEMPLATE FILE
        html= open(os.path.join(TEMPLATES_PATH, 'index.html'), "w+")
        html.write(
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Django Babel Boilerplate</title>
    {% load staticfiles %}
    {% load svg %}
</head>
<body>
  <style>
        body {
            height: 100vh;
        }

        section {
            width: 30%;
            margin: 0 auto;
            display: flex;
            align-items: center;
            height: calc(100% - 95px);
            justify-content: center;
        }

        @media screen and (max-width: 1023px) {

            section {
                width: 100%;
            }
        }

        h1 {
            text-align: center;
            padding: 30px 0;
            font-family: sans-serif;
            color: #333;
            font-size: 30px;
        }

        .logo {
            width: 150px;
            margin: 0 auto;
        }

        svg {
            width: 100%;
            height: 100%;
        }

        a {
            display: block;
            text-align: right;
            margin: 30px 0;
            font-size: 20px;
            color: #333;
            align-self: flex-end;
        }

        #hair,
        #face {
            transform: translateY(0);
            animation: 5s slide infinite ease;
            animation-delay: 5s;
        }

        @keyframes slide {

            0% {
                transform: translateY(0);
            }

            50% {
                transform: translateY(20px);
            }

            100% {
                transform: translateY(0px);
            }
        }

    </style>

    <h1>Django Babel Boilerplate</h1>
    <section>
        <div class="wrapper">
            <div class="logo">
                {% svg 'creator' %}
            </div>
            <a href="https://www.navaneethnagesh.com" target="_blank">- Navaneeth Nagesh</a>
        </div>
    </section>
</body>
</html>
""")
        html.close()

        # MAIN_APP_FILES
        wsgi= open(os.path.join(MAIN_APP_PATH, 'wsgi.py'), "w+")
        wsgi.write(
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", """ '"' + project_name + """.settings.local")

application = get_wsgi_application()
""")
        wsgi.close()

        views= open(os.path.join(MAIN_APP_PATH, 'views.py'), "w+")
        views.write(
"""
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
""")

        urls= open(os.path.join(MAIN_APP_PATH, 'urls.py'), "w+")
        urls.write(
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
]
""")
        urls.close()

        init_file= open(os.path.join(MAIN_APP_PATH, '__init__.py'), "w+")
        init_file.close()

        
        # SETTINGS BASE FILES

        staging= open(os.path.join(MAIN_APP_SETTINGS_PATH, 'staging.py'), "w+")
        staging.write(
"""
import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['']

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static-v1.0.0/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = '' + STATIC_URL
""")
        staging.close()

        production= open(os.path.join(MAIN_APP_SETTINGS_PATH, 'production.py'), "w+")
        production.write(
"""
import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['']


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

STATIC_URL = '/static-v1.0.0/'
STATIC_ROOT = '' + STATIC_URL

MEDIA_URL = '/'
MEDIA_ROOT = '/'
""")
        production.close()

        local= open(os.path.join(MAIN_APP_SETTINGS_PATH, 'local.py'), "w+")
        local.write(
"""
import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
""")
        local.close()

        base= open(os.path.join(MAIN_APP_SETTINGS_PATH, 'base.py'), "w+")
        base.write(
"""
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = """ "'" + secret_key + "'" """

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'svg'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = """ "'" + project_name + """.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = '""" + project_name + """.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SVG_DIRS=[
    os.path.join(BASE_DIR, 'svg')
]
""")
        base.close()

        

        os.mkdir(os.path.join(STATIC_COMMON_PATH, 'js'))
        os.mkdir(os.path.join(STATIC_COMMON_PATH, 'scss'))
    
        os.mkdir(os.path.join(STATIC_DIST_PATH, 'js'))
        os.mkdir(os.path.join(STATIC_DIST_PATH, 'css'))
        os.mkdir(os.path.join(STATIC_DIST_PATH, 'images'))

        os.mkdir(os.path.join(STATIC_HOME_PATH, 'js'))
        os.mkdir(os.path.join(STATIC_HOME_PATH, 'scss'))



        # ROOT FILES CREATION

        babelrc= open(os.path.join(ROOT_PATH, '.babelrc'),"w+")
        babelrc.write(
"""
{
    "presets": [
        "es2015"
    ]
}
""")
        babelrc.close() 
        
        requirements= open(os.path.join(ROOT_PATH, 'requirements.txt'), "w+")
        requirements.write(
"""
Django==2.1.1
django-inline-svg==0.1.1
pytz==2018.5
""")

        requirements_server= open(os.path.join(ROOT_PATH, 'requirements-server.txt'), "w+")
        requirements_server.write(
"""
Django==2.1.1
gunicorn==19.9.0
mysqlclient==1.3.13
pkg-resources==0.0.0
pytz==2018.5
""")
        requirements_server.close()

        package= open(os.path.join(ROOT_PATH, 'package.json'), "w+")
        package.write(
"""
{
  "name": """ '"'+ project_name +'"' """,
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "babel": "babel --watch --presets es2015 static/home/js static/common/js -d static/dist/js",
    "scss": "cd static && sass --watch common/scss:dist/css home/scss:dist/css",
    "server": "python manage.py runserver 0.0.0.0:8000",
    "start": "concurrently \\"npm run scss\\" \\"npm run babel\\" \\"npm run server\\""
  },
  "repository": {
    "type": "git",
    "url": ""
  },
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "babel-cli": "^6.26.0",
    "babel-preset-es2015": "^6.24.1",
    "concurrently": "^4.0.1",
    "sass": "^1.14.1"
  }
}
""")
        package.close()
        
        manage= open(os.path.join(ROOT_PATH, 'manage.py'), "w+")
        manage.write(
"""
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__": 
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", """ '"' + project_name + """.settings.local")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

""")
        manage.close()

        gitignore= open(os.path.join(ROOT_PATH, '.gitignore'), "w+")
        gitignore.write(
"""
*.sqlite3
*.pyc
**/migrations/
**/.sass-cache/
*.map
.idea/
.vscode/
information/
all_staticfiles/
*.zip
node_modules/
static/uploaded/
virtualenv/
""")
        gitignore.close() 
    
        print("Executing django-babel version %s." % __version__)
        print("Creating a project: %s" % project_name)
        print("HAPPY CODING. :) ")

