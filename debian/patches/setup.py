diff --git a/setup.py b/setup.py
--- a/setup.py
+++ b/setup.py
@@ -81,10 +81,10 @@
     )]
 else:
     ext_modules = [extension.Extension("libopenzwave", ["lib/libopenzwave.pyx"],
-                             libraries=['udev', 'stdc++'],
+                             libraries=['udev', 'stdc++', 'openzwave'],
                              language="c++",
-                             extra_objects=['openzwave/cpp/lib/linux/libopenzwave.a'],
-                             include_dirs=['openzwave/cpp/src', 'openzwave/cpp/src/value_classes', 'openzwave/cpp/src/platform']
+                             extra_objects=['/usr/lib/libopenzwave.a'],
+                             include_dirs=['/usr/include/openzwave', '/usr/include/openzwave/value_classes', '/usr/include/openzwave/platform']
     )]

 setup(
