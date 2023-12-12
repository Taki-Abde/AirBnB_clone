#!/usr/bin/python3
"""Defines the entry point of the command interpreter."""
import cmd
import re
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage
from shlex import split


class HBNBCommand(cmd.Cmd):
    """ Command interpreter class."""

    prompt = "(hbnb) "
    cls = {"BaseModel", "User", "Place", "City", "Amenity", "Review", "State"}

    def do_quit(self, arg):
        """Command quit to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF to exit the program."""
        print()
        return True

    def emptyline(self):
        """ Empty line and do nothing."""
        pass

    def do_create(self, arg):
        """ Creates a new instance of BaseModel."""
        if not arg:
            print("** class name missing **")
        else:
            try:
                new_inst = eval(arg)()
                new_inst.save()
                print(new_inst.id)
            except NameError:
                print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of an instance."""
        ar = arg.split()
        if not ar:
            print("** class name missing **")
        else:
            c_name = ar[0]
            if len(ar) == 0:
                print("** class name missing **")
            elif c_name not in HBNBCommand.cls:
                print("** class doesn't exist **")
            elif len(ar) < 2:
                print("** instance id missing **")
            else:
                obj_key = "{}.{}".format(c_name, ar[1])
                all_objs = storage.all()
                if obj_key in all_objs:
                    print(all_objs[obj_key])
                else:
                    print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance and save the change into thr JSON file."""
        ar = arg.split()
        if not ar:
            print("** class name missing **")
        else:
            try:
                c_name = ar[0]
                if c_name not in HBNBCommand.cls:
                    print("** class doesn't exist **")
                elif len(ar) < 2:
                    print("** instance id missing **")
                else:
                    obj_key = "{}.{}".format(c_name, ar[1])
                    all_objs = storage.all()
                    if obj_key in all_objs:
                        del all_objs[obj_key]
                        storage.save()
                    else:
                        print("** no instance found **")
            except IndexError:
                print("** instance id missing **")

    def do_all(self, arg):
        """Prints all string representation of all instances."""
        ar = arg.split()
        all_objs = storage.all()
        if not ar:
            print([str(obj) for obj in all_objs.values()])
        else:
            try:
                c_name = ar[0]
                if c_name not in HBNBCommand.cls:
                    print("** class doesn't exist **")
                else:
                    if hasattr(eval(c_name), "all"):
                        objs_cls = [str(obj) for obj in eval(c_name).all()]
                        print(objs_cls)
                    else:
                        objs_cls = [
                            str(obj)
                            for key, obj in all_objs.items()
                            if key.startswith(c_name + ".")
                        ]
                        print(objs_cls)
            except IndexError:
                print("** class name missing **")

    def do_update(self, arg):
        """Updates an instance based on the class name and id."""
        args = arg.split()
        if len(args) >= 4:
            key = "{}.{}".format(args[0], args[1])
            if key in storage.all():
                obj = storage.all()[key]
                setattr(obj, args[2], args[3])
                obj.save()
            else:
                print("** no instance found **")
        elif len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.cls:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif ("{}.{}".format(args[0], args[1])) not in storage.all():
            print("** no instance found **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")

    def do_count(self, arg):
        """Counts the number of instances of a class."""
        ar = arg.split()
        if not ar:
            print("** class name missing **")
        else:
            c_name = ar[0]
            if c_name not in HBNBCommand.cls:
                print("** class doesn't exist **")
            else:
                count = 0
                for obj in storage.all().values():
                    if c_name == obj.__class__.__name__:
                        count += 1
                print(count)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
