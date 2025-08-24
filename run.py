from core.system import cardinal

if __name__ == '__main__':
    cardinal.run()
#endif










# import os
# import importlib
# from flask import Flask

# app = Flask(__name__)

# def addBlueprint(bp, prefix):
#     print("addBlueprint called")
#     app.register_blueprint(bp, url_prefix=prefix)
# #enddef

# @app.route('/')
# def hello():
#     return 'Hello, World!'
# #enddef

# # Dynamically import all route files in the 'routes' directory
# app_dir = 'app'
# for folder in os.listdir(app_dir):
#     folder_path = os.path.join(app_dir, folder)
#     if os.path.isdir(folder_path):
#         routes_file = os.path.join(folder_path, 'routes.py')
#         if os.path.isfile(routes_file):
#             module_name = os.path.splitext(os.path.basename(routes_file))[0]
#             module = importlib.import_module(f'{app_dir}.{folder}.{module_name}')
#             bp = getattr(module, module_name)
#             addBlueprint(bp, f'/{folder}')
#         #endif
#     #endif
# #endfor

# if __name__ == '__main__':
#     app.run()
# #endif

