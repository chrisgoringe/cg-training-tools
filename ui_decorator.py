from collections.abc import Iterable

def recursive_add(signals:list, args):
    for arg in args:
        if isinstance(arg, str):
            signals.append(arg)
        elif isinstance(arg, Iterable):
            signals = recursive_add(signals, arg)
        else:
            raise Exception("ui_decorator takes str or iter(str)")
    return signals

def ui_signal(*args):
    """
    Return a decorator for Node classes.
    @param one or more strings or list of strings

    The decorator performs the following:
    The class has OUTPUT_NODE set to True.
    The class UI_OUTPUT is appended (or created) with a comma separated list of these signals
    The class FUNCTION is wrapped such that the last len(signals) are removed, and added to the
    ui dictionary using signals as keys.

    So ui_signals(["first","second"]) will wrap a function returning (something, somethingelse, first_signal, second_signal)
    and will return { "ui": {"first":first_signal, "second":second_signal}, "result":(something, somethingelse) }
    (except that `None` will be silently dropped)
    """
    signals = recursive_add([], args)

    def decorator(clazz):
        internal_function_name = getattr(clazz,'FUNCTION')
        if internal_function_name=='_ui_signal_decorated_function':
            raise Exception("Can't nest ui_signal decorators")
        def _ui_signal_decorated_function(self, **kwargs):
            returns = getattr(self,internal_function_name)(**kwargs)
            returns_tuple = returns['result']    if isinstance(returns,dict) else returns
            returns_ui    = returns.get('ui',{}) if isinstance(returns,dict) else {}

            popped_returns = returns_tuple[-len(signals):]
            returns_tuple  = returns_tuple[:-len(signals)]

            for i,key in enumerate(signals):
                if popped_returns[i] is not None:
                    returns_ui[key] = popped_returns[i]
                    if isinstance(returns_ui[key], str):
                        returns_ui[key] = (returns_ui[key],)

            return { "ui":returns_ui, "result": returns_tuple }
        clazz._ui_signal_decorated_function = _ui_signal_decorated_function
        clazz.FUNCTION = '_ui_signal_decorated_function'
        clazz.OUTPUT_NODE = True
        clazz.UI_OUTPUT = clazz.UI_OUTPUT+"," if hasattr(clazz, 'UI_OUTPUT') else ""
        clazz.UI_OUTPUT += ",".join(signals)
        clazz.DESCRIPTION = clazz.UI_OUTPUT+"," if hasattr(clazz, 'UI_OUTPUT') else ""
        clazz.DESCRIPTION += ",".join(signals)
        return clazz

    return decorator
        
            
