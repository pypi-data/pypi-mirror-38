"""moudule pygamer for games







    class Player
                gtm()
                    make the player folow the mouse
                    arguments: None
                    Example:
                            >>> test = pygamer.Player()
                            >>> test.gtm()
                startdraw()
                    make the player draw.
                    arguments: None
                enddraw()
                    stop the player from drawing
    
    
    
    
    class Classes
                isuse()
                    returns isuses in a class
                    Exaple:
                            >>> import pygamer
                            >>> test = pygamer.Classes()
                            >>> test.isuse()
                            None
                issafe()
                    returns if player can draw or not
                    Exaple:
                            >>> import pygamer
                            >>> test = pygamer.Classes()
                            >>> test.idsafe()
                            True
                            >>>




"""
try:

    from turtle import *

    class IsuseError:
        def __int__(self, execushen, message):
            self.execushen = execushen
            self.message = message

    class Player(Turtle):
        def __int__(self, shape = 'circle', gender = 'Male'):
            self.shape = shape
            self.gender = gender
            self.pen = 'up'
        def gtm(self, time):
            def wasd(x, y):
                self.setpos(x, y)
            onclick(wasd)
            listen()
            mainloop()
        def startdraw(self, classes):
            m = classes()
            if m.idsafe():
                self.pendown()
            else:
                print(classes + ' Is Not Safe')
                raise NameError
        def enddraw(s):
            s.penup()
    class Classes:
        def __int__(s):
            pass
        def idsafe(self):
            '''returns if player can draw or not
    Exaple:
            >>> import pygamer
            >>> test = pygamer.Classes()
            >>> test.idsafe()
            True
            >>>'''
            if self.type() == "class":
                return True
            else:
                raise IDERError
        def isuse(sa):
            """returns isuses in a class
    Exaple:
            >>> import pygamer
            >>> test = pygamer.Classes()
            >>> test.isuse()
            None
            >>>"""
            if self == self: return None
            else: raise IsuseError('ralan', self.id + '.type() != \'class\'')
    a = Classes()
    a.type = str
    a.idsafe()
except:
    print('install python from https://python.org/')