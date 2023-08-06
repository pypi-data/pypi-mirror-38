from __future__ import print_function

from kabaret import flow


class NoDialogAction(flow.Action):

    def needs_dialog(self):
        return False

    def run(self, button):
        print('Well done Jolly Jumper !')

class SimpleDialogAction(flow.Action):

    def needs_dialog(self):
        return True

    def get_buttons(self):
        self.message.set('This is the action message: <3')
        return ['Ok', 'Maybe', 'Nope']

    def run(self, button):
        print('You chose {}'.format(button))

class DialogParamsAction(flow.Action):

    cut_down_trees = flow.BoolParam(True)
    skip_and_jump = flow.BoolParam(True)
    press_wild_flowers = flow.BoolParam(True)

    def needs_dialog(self):
        return True

    def get_buttons(self):
        self.message.set('Do you:')
        return ['Ok']

    def run(self, button):
        all_true = (
            self.cut_down_trees.get()
            and self.skip_and_jump.get()
            and self.press_wild_flowers.get()
        )
        if (
            self.cut_down_trees.get()
            and self.skip_and_jump.get()
            and self.press_wild_flowers.get()
        ):
            print('You hang around in bars')
        else:
            print('Do you ever party ?')

class DispatchParams(flow.Object):

    pool = flow.Param('Farm')
    priority = flow.Param(50)

    def get_flags(self):
        return [
            '-P', str(self.pool.get()),
            '-p', str(self.priority.get()),
        ]


class SequenceParam(flow.Object):

    first_frame = flow.Param(1)
    last_frame = flow.Param(100)

    def get_flags(self):
        return [
            '--first', str(self.first_frame.get()),
            '--last', str(self.last_frame.get()),
        ]

class ComplexDialogAction(flow.Action):

    dispatch = flow.Child(DispatchParams)
    sequence = flow.Child(SequenceParam)

    def needs_dialog(self):
        return True

    def get_buttons(self):
        self.message.set('Configure and Submit your job')
        return ['Submit']

    def run(self, button):
        cmd = ['spam_it']+self.dispatch.get_flags()+self.sequence.get_flags()
        print('#---> Cmd:', ' '.join(cmd))

class EditMyValueAction(flow.Action):

    _value = flow.Parent()

    def needs_dialog(self):
        return True

    def get_buttons(self):
        self.message.set('Pick a color:')
        return ['Red', 'Pink', 'Blue', 'Violet']

    def run(self, button):
        self._value.set(button)

class MyValue(flow.values.Value):

    edit = flow.Child(EditMyValueAction)

class SubDialogAction(flow.Action):

    quote = flow.Param('', MyValue)

    def needs_dialog(self):
        return True


    def run(self, button):
        print('You selected: "{}"'.format(self.quote.get()))

class ActionsGroup(flow.Object):

    no_dialog_action = flow.Child(NoDialogAction)
    simple_dialog_action = flow.Child(SimpleDialogAction)
    dialog_params_action = flow.Child(DialogParamsAction)
    complex_dialog_action = flow.Child(ComplexDialogAction)

    sub_dialog_action = flow.Child(SubDialogAction)