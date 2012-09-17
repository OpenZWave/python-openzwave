diff --git a/debian/patches/setup.py b/debian/patches/setup.py
--- a/debian/patches/setup.py
+++ b/debian/patches/setup.py
@@ -1,17 +0,0 @@
-diff --git a/setup.py b/setup.py
---- a/setup.py
-+++ b/setup.py
-@@ -87,10 +87,10 @@
-     )]
- else:
-     ext_modules += [Extension("libopenzwave", ["lib/libopenzwave.pyx"],
--                             libraries=['udev', 'stdc++'],
-+                             libraries=['udev', 'stdc++', 'openzwave'],
-                              language="c++",
--                             extra_objects=['openzwave/cpp/lib/linux/libopenzwave.a'],
--                             include_dirs=['openzwave/cpp/src', 'openzwave/cpp/src/value_classes', 'openzwave/cpp/src/platform']
-+                             extra_objects=['/usr/lib/libopenzwave.a'],
-+                             include_dirs=['/usr/include/openzwave', '/usr/include/openzwave/value_classes', '/usr/include/openzwave/platform']
-     )]
-
- setup(
diff --git a/setup.py b/setup.py
--- a/setup.py
+++ b/setup.py
@@ -77,10 +77,10 @@
     )]
 else:
     ext_modules = [Extension("libopenzwave", ["lib/libopenzwave.pyx"],
-                             libraries=['udev', 'stdc++'],
+                             libraries=['udev', 'stdc++', 'openzwave'],
                              language="c++",
-                             extra_objects=['openzwave/cpp/lib/linux/libopenzwave.a'],
-                             include_dirs=['openzwave/cpp/src', 'openzwave/cpp/src/value_classes', 'openzwave/cpp/src/platform']
+                             extra_objects=['/usr/lib/libopenzwave.a'],
+                             include_dirs=['/usr/include/openzwave', '/usr/include/openzwave/value_classes', '/usr/include/openzwave/platform']
     )]
 
 setup(
