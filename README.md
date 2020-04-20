# PC_GUI

## Rules
   
   - Each widget has a branch - stick to it.
   - Each file type has its own folder - don't make a mess.
   - Every widget should be QWidget. 
   - If you want to use QtDesigner, don't change the generated file.
   - File generated from 'widgetname'.ui should be named 'widgetname'_ui.py 
   - Widget should be controlled via class named 'widgetname' located in 'widgetname'.py. This class should have a method called update and send. 
   - If it's possible try to keep your widget easily resizable. Add minimum and maximum size.
   - Qt is based on signals/interrupts. Heavy tasks should be handled by QThreads otherwise application will freeze. 

## Hints
Get familiar with 'connectionBar.py' - this is what your widget should look like. Each QWidget can act like an standalone application. You can run it by... take a look at connectionBar.py.

Use style sheets to create nice labels, buttons etc. Some terrible examples are included in connectionBar.py... 


Good PyQt tutorial: [LearnpyQt](https://www.learnpyqt.com/ "LearnpyQt") 