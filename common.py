import os
import folder_paths

module_root_directory_training = os.path.dirname(os.path.realpath(__file__))
module_js_directory_training = os.path.join(module_root_directory_training, "js")

application_root_directory = os.path.dirname(folder_paths.__file__)
application_web_extensions_directory = os.path.join(application_root_directory, "web", "extensions", "cg-nodes", "training")
    
class TrainingBase:
    def __init__(self):
        pass
    FUNCTION = "func"
    CATEGORY = "utilities/training"
    REQUIRED = {}
    OPTIONAL = None
    HIDDEN = None
    @classmethod    
    def INPUT_TYPES(s):
        types = {"required": s.REQUIRED}
        if s.OPTIONAL:
            types["optional"] = s.OPTIONAL
        if s.HIDDEN:
            types["hidden"] = s.HIDDEN
        return types
    RETURN_TYPES = ()
    RETURN_NAMES = ()

def modify_returns(returns, ui_key):
    if not isinstance(returns,dict):
        returns = { "result": returns }
    returns['ui'] = returns.get('ui',{})
    returns['ui'][ui_key] = returns['result'][-1]
    returns['result'] = returns['result'][:-1]
    return returns

def textdisplay(clazz):
    clazz.DESCRIPTION = "displays_text," + (clazz.DESCRIPTION if hasattr(clazz,'DESCRIPTION') else "")
    clazz.OUTPUT_NODE = True
    _FUNCTION = getattr(clazz,'FUNCTION')
    def _func_textdisplay(self, **kwargs):
        return modify_returns(getattr(self, _FUNCTION)(**kwargs), 'text_displayed')

    clazz.FUNCTION = '_func_textdisplay'
    clazz._func_textdisplay = _func_textdisplay
    return clazz

def terminator(clazz):
    clazz.DESCRIPTION = "terminator," + (clazz.DESCRIPTION if hasattr(clazz,'DESCRIPTION') else "")
    _FUNCTION = getattr(clazz,'FUNCTION')
    def _func_terminator(self, **kwargs):
        return modify_returns(getattr(self, _FUNCTION)(**kwargs), 'terminate')
    clazz.FUNCTION = '_func_terminator'
    clazz._func_terminator = _func_terminator
    return clazz    

def selfmodify(clazz):
    clazz.DESCRIPTION = "self_modify," + (clazz.DESCRIPTION if hasattr(clazz,'DESCRIPTION') else "")
    _FUNCTION = getattr(clazz,'FUNCTION')
    def _func_self_modify(self, **kwargs):
        return modify_returns(getattr(self, _FUNCTION)(**kwargs), 'self_modify')
    clazz.FUNCTION = '_func_self_modify'
    clazz._func_self_modify = _func_self_modify
    return clazz   