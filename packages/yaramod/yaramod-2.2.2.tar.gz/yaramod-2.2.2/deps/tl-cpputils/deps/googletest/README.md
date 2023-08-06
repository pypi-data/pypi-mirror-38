## Google Test

Google Test meta repository that allows easy usage of [googletest](https://github.com/google/googletest) across several interlinked projects.

## Overview

The repository contains a single `CMakeLists.txt` file which gets Google Test as an external project and exposes its targets.

## Use

Four targets are exposed: `gtest`, `gtest_main`, `gmock`, `gmock_main`. They can be used as follows:
```cmake
target_link_libraries(project-that-needs-gmock gmock_main)
```

## Requirements

* A compiler supporting C++14
  * On Windows, only Microsoft Visual C++ is supported (version >= Visual Studio 2015).
* CMake (version >= 3.6)

## License

Copyright (c) 2017 Avast Software, licensed under the MIT license. See the `LICENSE` file for more details.

See the `LICENSE-THIRD-PARTY` file for the Google Test project license.
