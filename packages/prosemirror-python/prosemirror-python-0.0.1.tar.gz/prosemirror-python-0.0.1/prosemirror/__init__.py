__all__ = ['__init__']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers([u'dist_2$1', u'dist', u'dist_5$1', u'dist_6$1', u'dist_8$1', u'dist_1$1', u'OrderedMap', u'dist_9$1', u'transform_doc', u'orderedmap', u'dist_10', u'dist_14', u'dist_15', u'dist_11$1', u'dist_7$1', u'dist_10$1', u'dist_18', u'dist$1', u'dist_9', u'dist_8', u'dist_4$1', u'dist_3', u'dist_2', u'dist_1', u'dist_7', u'dist_6', u'dist_5', u'dist_4', u'dist_13', u'dist_12', u'dist_11', u'dist_3$1', u'dist_17', u'dist_16', u'createCommonjsModule', u'unwrapExports', u'create_doc', u'dist_19', u'dist_13$1', u'dist_12$1'])
@Js
def PyJsHoisted_OrderedMap_(content, this, arguments, var=var):
    var = Scope({u'content':content, u'this':this, u'arguments':arguments}, var)
    var.registers([u'content'])
    var.get(u"this").put(u'content', var.get(u'content'))
PyJsHoisted_OrderedMap_.func_name = u'OrderedMap'
var.put(u'OrderedMap', PyJsHoisted_OrderedMap_)
@Js
def PyJsHoisted_createCommonjsModule_(fn, module, this, arguments, var=var):
    var = Scope({u'this':this, u'module':module, u'fn':fn, u'arguments':arguments}, var)
    var.registers([u'module', u'fn'])
    PyJs_Object_2_ = Js({})
    PyJs_Object_1_ = Js({u'exports':PyJs_Object_2_})
    return PyJsComma(PyJsComma(var.put(u'module', PyJs_Object_1_),var.get(u'fn')(var.get(u'module'), var.get(u'module').get(u'exports'))),var.get(u'module').get(u'exports'))
PyJsHoisted_createCommonjsModule_.func_name = u'createCommonjsModule'
var.put(u'createCommonjsModule', PyJsHoisted_createCommonjsModule_)
@Js
def PyJsHoisted_unwrapExports_(x, this, arguments, var=var):
    var = Scope({u'this':this, u'x':x, u'arguments':arguments}, var)
    var.registers([u'x'])
    return (var.get(u'x').get(u'default') if ((var.get(u'x') and var.get(u'x').get(u'__esModule')) and var.get(u'Object').get(u'prototype').get(u'hasOwnProperty').callprop(u'call', var.get(u'x'), Js(u'default'))) else var.get(u'x'))
PyJsHoisted_unwrapExports_.func_name = u'unwrapExports'
var.put(u'unwrapExports', PyJsHoisted_unwrapExports_)
Js(u'use strict')
PyJs_Object_0_ = Js({u'value':Js(True)})
var.get(u'Object').callprop(u'defineProperty', var.get(u'exports'), Js(u'__esModule'), PyJs_Object_0_)
pass
pass
pass
@Js
def PyJs_anonymous_4_(key, this, arguments, var=var):
    var = Scope({u'this':this, u'arguments':arguments, u'key':key}, var)
    var.registers([u'i', u'key'])
    #for JS loop
    var.put(u'i', Js(0.0))
    while (var.get(u'i')<var.get(u"this").get(u'content').get(u'length')):
        try:
            if PyJsStrictEq(var.get(u"this").get(u'content').get(var.get(u'i')),var.get(u'key')):
                return var.get(u'i')
        finally:
                var.put(u'i', Js(2.0), u'+')
    return (-Js(1.0))
PyJs_anonymous_4_._set_name(u'anonymous')
@Js
def PyJs_anonymous_5_(key, this, arguments, var=var):
    var = Scope({u'this':this, u'arguments':arguments, u'key':key}, var)
    var.registers([u'found', u'key'])
    var.put(u'found', var.get(u"this").callprop(u'find', var.get(u'key')))
    return (var.get(u'undefined') if (var.get(u'found')==(-Js(1.0))) else var.get(u"this").get(u'content').get((var.get(u'found')+Js(1.0))))
PyJs_anonymous_5_._set_name(u'anonymous')
@Js
def PyJs_anonymous_6_(key, value, newKey, this, arguments, var=var):
    var = Scope({u'this':this, u'newKey':newKey, u'value':value, u'key':key, u'arguments':arguments}, var)
    var.registers([u'newKey', u'self', u'value', u'content', u'key', u'found'])
    var.put(u'self', (var.get(u"this").callprop(u'remove', var.get(u'newKey')) if (var.get(u'newKey') and (var.get(u'newKey')!=var.get(u'key'))) else var.get(u"this")))
    var.put(u'found', var.get(u'self').callprop(u'find', var.get(u'key')))
    var.put(u'content', var.get(u'self').get(u'content').callprop(u'slice'))
    if (var.get(u'found')==(-Js(1.0))):
        var.get(u'content').callprop(u'push', (var.get(u'newKey') or var.get(u'key')), var.get(u'value'))
    else:
        var.get(u'content').put((var.get(u'found')+Js(1.0)), var.get(u'value'))
        if var.get(u'newKey'):
            var.get(u'content').put(var.get(u'found'), var.get(u'newKey'))
    return var.get(u'OrderedMap').create(var.get(u'content'))
PyJs_anonymous_6_._set_name(u'anonymous')
@Js
def PyJs_anonymous_7_(key, this, arguments, var=var):
    var = Scope({u'this':this, u'arguments':arguments, u'key':key}, var)
    var.registers([u'content', u'found', u'key'])
    var.put(u'found', var.get(u"this").callprop(u'find', var.get(u'key')))
    if (var.get(u'found')==(-Js(1.0))):
        return var.get(u"this")
    var.put(u'content', var.get(u"this").get(u'content').callprop(u'slice'))
    var.get(u'content').callprop(u'splice', var.get(u'found'), Js(2.0))
    return var.get(u'OrderedMap').create(var.get(u'content'))
PyJs_anonymous_7_._set_name(u'anonymous')
@Js
def PyJs_anonymous_8_(key, value, this, arguments, var=var):
    var = Scope({u'this':this, u'value':value, u'key':key, u'arguments':arguments}, var)
    var.registers([u'value', u'key'])
    return var.get(u'OrderedMap').create(Js([var.get(u'key'), var.get(u'value')]).callprop(u'concat', var.get(u"this").callprop(u'remove', var.get(u'key')).get(u'content')))
PyJs_anonymous_8_._set_name(u'anonymous')
@Js
def PyJs_anonymous_9_(key, value, this, arguments, var=var):
    var = Scope({u'this':this, u'value':value, u'key':key, u'arguments':arguments}, var)
    var.registers([u'content', u'value', u'key'])
    var.put(u'content', var.get(u"this").callprop(u'remove', var.get(u'key')).get(u'content').callprop(u'slice'))
    var.get(u'content').callprop(u'push', var.get(u'key'), var.get(u'value'))
    return var.get(u'OrderedMap').create(var.get(u'content'))
PyJs_anonymous_9_._set_name(u'anonymous')
@Js
def PyJs_anonymous_10_(place, key, value, this, arguments, var=var):
    var = Scope({u'this':this, u'place':place, u'value':value, u'key':key, u'arguments':arguments}, var)
    var.registers([u'value', u'content', u'without', u'place', u'key', u'found'])
    var.put(u'without', var.get(u"this").callprop(u'remove', var.get(u'key')))
    var.put(u'content', var.get(u'without').get(u'content').callprop(u'slice'))
    var.put(u'found', var.get(u'without').callprop(u'find', var.get(u'place')))
    var.get(u'content').callprop(u'splice', (var.get(u'content').get(u'length') if (var.get(u'found')==(-Js(1.0))) else var.get(u'found')), Js(0.0), var.get(u'key'), var.get(u'value'))
    return var.get(u'OrderedMap').create(var.get(u'content'))
PyJs_anonymous_10_._set_name(u'anonymous')
@Js
def PyJs_anonymous_11_(f, this, arguments, var=var):
    var = Scope({u'this':this, u'arguments':arguments, u'f':f}, var)
    var.registers([u'i', u'f'])
    #for JS loop
    var.put(u'i', Js(0.0))
    while (var.get(u'i')<var.get(u"this").get(u'content').get(u'length')):
        try:
            var.get(u'f')(var.get(u"this").get(u'content').get(var.get(u'i')), var.get(u"this").get(u'content').get((var.get(u'i')+Js(1.0))))
        finally:
                var.put(u'i', Js(2.0), u'+')
PyJs_anonymous_11_._set_name(u'anonymous')
@Js
def PyJs_anonymous_12_(map, this, arguments, var=var):
    var = Scope({u'this':this, u'map':map, u'arguments':arguments}, var)
    var.registers([u'map'])
    var.put(u'map', var.get(u'OrderedMap').callprop(u'from', var.get(u'map')))
    if var.get(u'map').get(u'size').neg():
        return var.get(u"this")
    return var.get(u'OrderedMap').create(var.get(u'map').get(u'content').callprop(u'concat', var.get(u"this").callprop(u'subtract', var.get(u'map')).get(u'content')))
PyJs_anonymous_12_._set_name(u'anonymous')
@Js
def PyJs_anonymous_13_(map, this, arguments, var=var):
    var = Scope({u'this':this, u'map':map, u'arguments':arguments}, var)
    var.registers([u'map'])
    var.put(u'map', var.get(u'OrderedMap').callprop(u'from', var.get(u'map')))
    if var.get(u'map').get(u'size').neg():
        return var.get(u"this")
    return var.get(u'OrderedMap').create(var.get(u"this").callprop(u'subtract', var.get(u'map')).get(u'content').callprop(u'concat', var.get(u'map').get(u'content')))
PyJs_anonymous_13_._set_name(u'anonymous')
@Js
def PyJs_anonymous_14_(map, this, arguments, var=var):
    var = Scope({u'this':this, u'map':map, u'arguments':arguments}, var)
    var.registers([u'i', u'map', u'result'])
    var.put(u'result', var.get(u"this"))
    var.put(u'map', var.get(u'OrderedMap').callprop(u'from', var.get(u'map')))
    #for JS loop
    var.put(u'i', Js(0.0))
    while (var.get(u'i')<var.get(u'map').get(u'content').get(u'length')):
        try:
            var.put(u'result', var.get(u'result').callprop(u'remove', var.get(u'map').get(u'content').get(var.get(u'i'))))
        finally:
                var.put(u'i', Js(2.0), u'+')
    return var.get(u'result')
PyJs_anonymous_14_._set_name(u'anonymous')
PyJs_Object_3_ = Js({u'constructor':var.get(u'OrderedMap'),u'find':PyJs_anonymous_4_,u'get':PyJs_anonymous_5_,u'update':PyJs_anonymous_6_,u'remove':PyJs_anonymous_7_,u'addToStart':PyJs_anonymous_8_,u'addToEnd':PyJs_anonymous_9_,u'addBefore':PyJs_anonymous_10_,u'forEach':PyJs_anonymous_11_,u'prepend':PyJs_anonymous_12_,u'append':PyJs_anonymous_13_,u'subtract':PyJs_anonymous_14_})
@Js
def PyJs_anonymous_15_(this, arguments, var=var):
    var = Scope({u'this':this, u'arguments':arguments}, var)
    var.registers([])
    return (var.get(u"this").get(u'content').get(u'length')>>Js(1.0))
PyJs_anonymous_15_._set_name(u'anonymous')
PyJs_Object_3_.define_own_property(u'size', {"get":PyJs_anonymous_15_, "configurable":True, "enumerable":True})
var.get(u'OrderedMap').put(u'prototype', PyJs_Object_3_)
@Js
def PyJs_anonymous_16_(value, this, arguments, var=var):
    var = Scope({u'this':this, u'arguments':arguments, u'value':value}, var)
    var.registers([u'content', u'value', u'prop'])
    if var.get(u'value').instanceof(var.get(u'OrderedMap')):
        return var.get(u'value')
    var.put(u'content', Js([]))
    if var.get(u'value'):
        for PyJsTemp in var.get(u'value'):
            var.put(u'prop', PyJsTemp)
            var.get(u'content').callprop(u'push', var.get(u'prop'), var.get(u'value').get(var.get(u'prop')))
    return var.get(u'OrderedMap').create(var.get(u'content'))
PyJs_anonymous_16_._set_name(u'anonymous')
var.get(u'OrderedMap').put(u'from', PyJs_anonymous_16_)
var.put(u'orderedmap', var.get(u'OrderedMap'))
@Js
def PyJs_anonymous_17_(module, exports, this, arguments, var=var):
    var = Scope({u'this':this, u'exports':exports, u'arguments':arguments, u'module':module}, var)
    var.registers([u'compareDeep', u'joinable', u'Slice', u'OPT_PRESERVE_WS', u'normalizeList', u'resolveName', u'copy', u'insertInto', u'OPT_OPEN_LEFT', u'NodeContext', u'module', u'replace', u'DOMParser', u'gatherToDOM', u'checkForDeadEnds', u'emptyAttrs', u'parseStyles', u'close', u'OrderedMap', u'ContentMatch', u'defaultAttrs', u'Node', u'NodeRange', u'prototypeAccessors$1$2', u'parseExprRange', u'Fragment', u'resolveCacheSize', u'replaceTwoWay', u'wsOptionsFor', u'ignoreTags', u'findDiffEnd', u'parseExprSeq', u'nullFrom', u'Schema', u'TokenStream', u'_interopDefault', u'initAttrs', u'parseExpr', u'parseExprAtom', u'resolveCachePos', u'TextNode', u'addNode', u'wrapMarks', u'matches', u'MarkType', u'replaceThreeWay', u'addRange', u'checkJoin', u'listTags', u'removeRange', u'OPT_PRESERVE_WS_FULL', u'gatherMarks', u'computeAttrs', u'prototypeAccessors$1$1', u'prototypeAccessors$1$3', u'Mark', u'parseNum', u'blockTags', u'ParseContext', u'NodeType', u'replaceOuter', u'nfa', u'retIndex', u'prototypeAccessors$6', u'dfa', u'prototypeAccessors$4', u'prototypeAccessors$5', u'prototypeAccessors$2', u'prototypeAccessors$3', u'prototypeAccessors$1', u'findDiffStart', u'doc', u'DOMSerializer', u'resolveCache', u'ReplaceError', u'Attribute', u'prepareSliceForReplace', u'found', u'parseExprSubscript', u'prototypeAccessors', u'ResolvedPos', u'exports', u'cmp'])
    @Js
    def PyJsHoisted_compareDeep_(a, b, this, arguments, var=var):
        var = Scope({u'a':a, u'this':this, u'b':b, u'arguments':arguments}, var)
        var.registers([u'a', u'b', u'i', u'p$1', u'p', u'array'])
        if PyJsStrictEq(var.get(u'a'),var.get(u'b')):
            return Js(True)
        if ((var.get(u'a') and (var.get(u'a',throw=False).typeof()==Js(u'object'))).neg() or (var.get(u'b') and (var.get(u'b',throw=False).typeof()==Js(u'object'))).neg()):
            return Js(False)
        var.put(u'array', var.get(u'Array').callprop(u'isArray', var.get(u'a')))
        if (var.get(u'Array').callprop(u'isArray', var.get(u'b'))!=var.get(u'array')):
            return Js(False)
        if var.get(u'array'):
            if (var.get(u'a').get(u'length')!=var.get(u'b').get(u'length')):
                return Js(False)
            #for JS loop
            var.put(u'i', Js(0.0))
            while (var.get(u'i')<var.get(u'a').get(u'length')):
                try:
                    if var.get(u'compareDeep')(var.get(u'a').get(var.get(u'i')), var.get(u'b').get(var.get(u'i'))).neg():
                        return Js(False)
                finally:
                        (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        else:
            for PyJsTemp in var.get(u'a'):
                var.put(u'p', PyJsTemp)
                if (var.get(u'b').contains(var.get(u'p')).neg() or var.get(u'compareDeep')(var.get(u'a').get(var.get(u'p')), var.get(u'b').get(var.get(u'p'))).neg()):
                    return Js(False)
            for PyJsTemp in var.get(u'b'):
                var.put(u'p$1', PyJsTemp)
                if var.get(u'a').contains(var.get(u'p$1')).neg():
                    return Js(False)
        return Js(True)
    PyJsHoisted_compareDeep_.func_name = u'compareDeep'
    var.put(u'compareDeep', PyJsHoisted_compareDeep_)
    @Js
    def PyJsHoisted_joinable_(PyJsArg_246265666f7265_, PyJsArg_246166746572_, depth, this, arguments, var=var):
        var = Scope({u'this':this, u'$before':PyJsArg_246265666f7265_, u'$after':PyJsArg_246166746572_, u'depth':depth, u'arguments':arguments}, var)
        var.registers([u'node', u'$before', u'$after', u'depth'])
        var.put(u'node', var.get(u'$before').callprop(u'node', var.get(u'depth')))
        var.get(u'checkJoin')(var.get(u'node'), var.get(u'$after').callprop(u'node', var.get(u'depth')))
        return var.get(u'node')
    PyJsHoisted_joinable_.func_name = u'joinable'
    var.put(u'joinable', PyJsHoisted_joinable_)
    @Js
    def PyJsHoisted_resolveName_(stream, name, this, arguments, var=var):
        var = Scope({u'this':this, u'name':name, u'stream':stream, u'arguments':arguments}, var)
        var.registers([u'name', u'stream', u'typeName', u'type$1', u'result', u'type', u'types'])
        var.put(u'types', var.get(u'stream').get(u'nodeTypes'))
        var.put(u'type', var.get(u'types').get(var.get(u'name')))
        if var.get(u'type'):
            return Js([var.get(u'type')])
        var.put(u'result', Js([]))
        for PyJsTemp in var.get(u'types'):
            var.put(u'typeName', PyJsTemp)
            var.put(u'type$1', var.get(u'types').get(var.get(u'typeName')))
            if (var.get(u'type$1').get(u'groups').callprop(u'indexOf', var.get(u'name'))>(-Js(1.0))):
                var.get(u'result').callprop(u'push', var.get(u'type$1'))
        if (var.get(u'result').get(u'length')==Js(0.0)):
            var.get(u'stream').callprop(u'err', ((Js(u"No node type or group '")+var.get(u'name'))+Js(u"' found")))
        return var.get(u'result')
    PyJsHoisted_resolveName_.func_name = u'resolveName'
    var.put(u'resolveName', PyJsHoisted_resolveName_)
    @Js
    def PyJsHoisted_insertInto_(content, dist, insert, parent, this, arguments, var=var):
        var = Scope({u'content':content, u'insert':insert, u'dist':dist, u'arguments':arguments, u'parent':parent, u'this':this}, var)
        var.registers([u'index', u'dist', u'parent', u'insert', u'offset', u'content', u'inner', u'child', u'ref'])
        var.put(u'ref', var.get(u'content').callprop(u'findIndex', var.get(u'dist')))
        var.put(u'index', var.get(u'ref').get(u'index'))
        var.put(u'offset', var.get(u'ref').get(u'offset'))
        var.put(u'child', var.get(u'content').callprop(u'maybeChild', var.get(u'index')))
        if ((var.get(u'offset')==var.get(u'dist')) or var.get(u'child').get(u'isText')):
            if (var.get(u'parent') and var.get(u'parent').callprop(u'canReplace', var.get(u'index'), var.get(u'index'), var.get(u'insert')).neg()):
                return var.get(u"null")
            return var.get(u'content').callprop(u'cut', Js(0.0), var.get(u'dist')).callprop(u'append', var.get(u'insert')).callprop(u'append', var.get(u'content').callprop(u'cut', var.get(u'dist')))
        var.put(u'inner', var.get(u'insertInto')(var.get(u'child').get(u'content'), ((var.get(u'dist')-var.get(u'offset'))-Js(1.0)), var.get(u'insert')))
        return (var.get(u'inner') and var.get(u'content').callprop(u'replaceChild', var.get(u'index'), var.get(u'child').callprop(u'copy', var.get(u'inner'))))
    PyJsHoisted_insertInto_.func_name = u'insertInto'
    var.put(u'insertInto', PyJsHoisted_insertInto_)
    @Js
    def PyJsHoisted_replace_(PyJsArg_2466726f6d_, PyJsArg_24746f_, slice, this, arguments, var=var):
        var = Scope({u'this':this, u'$from':PyJsArg_2466726f6d_, u'slice':slice, u'$to':PyJsArg_24746f_, u'arguments':arguments}, var)
        var.registers([u'$from', u'slice', u'$to'])
        if (var.get(u'slice').get(u'openStart')>var.get(u'$from').get(u'depth')):
            PyJsTempException = JsToPyException(var.get(u'ReplaceError').create(Js(u'Inserted content deeper than insertion position')))
            raise PyJsTempException
        if ((var.get(u'$from').get(u'depth')-var.get(u'slice').get(u'openStart'))!=(var.get(u'$to').get(u'depth')-var.get(u'slice').get(u'openEnd'))):
            PyJsTempException = JsToPyException(var.get(u'ReplaceError').create(Js(u'Inconsistent open depths')))
            raise PyJsTempException
        return var.get(u'replaceOuter')(var.get(u'$from'), var.get(u'$to'), var.get(u'slice'), Js(0.0))
    PyJsHoisted_replace_.func_name = u'replace'
    var.put(u'replace', PyJsHoisted_replace_)
    @Js
    def PyJsHoisted_gatherToDOM_(obj, this, arguments, var=var):
        var = Scope({u'this':this, u'obj':obj, u'arguments':arguments}, var)
        var.registers([u'toDOM', u'obj', u'result', u'name'])
        PyJs_Object_354_ = Js({})
        var.put(u'result', PyJs_Object_354_)
        for PyJsTemp in var.get(u'obj'):
            var.put(u'name', PyJsTemp)
            var.put(u'toDOM', var.get(u'obj').get(var.get(u'name')).get(u'spec').get(u'toDOM'))
            if var.get(u'toDOM'):
                var.get(u'result').put(var.get(u'name'), var.get(u'toDOM'))
        return var.get(u'result')
    PyJsHoisted_gatherToDOM_.func_name = u'gatherToDOM'
    var.put(u'gatherToDOM', PyJsHoisted_gatherToDOM_)
    @Js
    def PyJsHoisted_checkForDeadEnds_(match, stream, this, arguments, var=var):
        var = Scope({u'this':this, u'stream':stream, u'match':match, u'arguments':arguments}, var)
        var.registers([u'node', u'j', u'stream', u'i', u'work', u'dead', u'next', u'state', u'nodes', u'match'])
        #for JS loop
        var.put(u'i', Js(0.0))
        var.put(u'work', Js([var.get(u'match')]))
        while (var.get(u'i')<var.get(u'work').get(u'length')):
            try:
                var.put(u'state', var.get(u'work').get(var.get(u'i')))
                var.put(u'dead', var.get(u'state').get(u'validEnd').neg())
                var.put(u'nodes', Js([]))
                #for JS loop
                var.put(u'j', Js(0.0))
                while (var.get(u'j')<var.get(u'state').get(u'next').get(u'length')):
                    try:
                        var.put(u'node', var.get(u'state').get(u'next').get(var.get(u'j')))
                        var.put(u'next', var.get(u'state').get(u'next').get((var.get(u'j')+Js(1.0))))
                        var.get(u'nodes').callprop(u'push', var.get(u'node').get(u'name'))
                        if (var.get(u'dead') and (var.get(u'node').get(u'isText') or var.get(u'node').callprop(u'hasRequiredAttrs')).neg()):
                            var.put(u'dead', Js(False))
                        if (var.get(u'work').callprop(u'indexOf', var.get(u'next'))==(-Js(1.0))):
                            var.get(u'work').callprop(u'push', var.get(u'next'))
                    finally:
                            var.put(u'j', Js(2.0), u'+')
                if var.get(u'dead'):
                    var.get(u'stream').callprop(u'err', ((Js(u'Only non-generatable nodes (')+var.get(u'nodes').callprop(u'join', Js(u', ')))+Js(u') in a required position')))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
    PyJsHoisted_checkForDeadEnds_.func_name = u'checkForDeadEnds'
    var.put(u'checkForDeadEnds', PyJsHoisted_checkForDeadEnds_)
    @Js
    def PyJsHoisted_wrapMarks_(marks, str, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'str':str, u'marks':marks}, var)
        var.registers([u'i', u'str', u'marks'])
        #for JS loop
        var.put(u'i', (var.get(u'marks').get(u'length')-Js(1.0)))
        while (var.get(u'i')>=Js(0.0)):
            try:
                var.put(u'str', (((var.get(u'marks').get(var.get(u'i')).get(u'type').get(u'name')+Js(u'('))+var.get(u'str'))+Js(u')')))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())-Js(1))+Js(1))
        return var.get(u'str')
    PyJsHoisted_wrapMarks_.func_name = u'wrapMarks'
    var.put(u'wrapMarks', PyJsHoisted_wrapMarks_)
    @Js
    def PyJsHoisted_parseStyles_(style, this, arguments, var=var):
        var = Scope({u'this':this, u'style':style, u'arguments':arguments}, var)
        var.registers([u're', u'style', u'm', u'result'])
        var.put(u're', JsRegExp(u'/\\s*([\\w-]+)\\s*:\\s*([^;]+)/g'))
        var.put(u'result', Js([]))
        while var.put(u'm', var.get(u're').callprop(u'exec', var.get(u'style'))):
            var.get(u'result').callprop(u'push', var.get(u'm').get(u'1'), var.get(u'm').get(u'2').callprop(u'trim'))
        return var.get(u'result')
    PyJsHoisted_parseStyles_.func_name = u'parseStyles'
    var.put(u'parseStyles', PyJsHoisted_parseStyles_)
    @Js
    def PyJsHoisted_close_(node, content, this, arguments, var=var):
        var = Scope({u'node':node, u'content':content, u'this':this, u'arguments':arguments}, var)
        var.registers([u'node', u'content'])
        if var.get(u'node').get(u'type').callprop(u'validContent', var.get(u'content')).neg():
            PyJsTempException = JsToPyException(var.get(u'ReplaceError').create((Js(u'Invalid content for node ')+var.get(u'node').get(u'type').get(u'name'))))
            raise PyJsTempException
        return var.get(u'node').callprop(u'copy', var.get(u'content'))
    PyJsHoisted_close_.func_name = u'close'
    var.put(u'close', PyJsHoisted_close_)
    @Js
    def PyJsHoisted_parseExprRange_(stream, expr, this, arguments, var=var):
        var = Scope({u'this':this, u'expr':expr, u'arguments':arguments, u'stream':stream}, var)
        var.registers([u'max', u'expr', u'stream', u'min'])
        var.put(u'min', var.get(u'parseNum')(var.get(u'stream')))
        var.put(u'max', var.get(u'min'))
        if var.get(u'stream').callprop(u'eat', Js(u',')):
            if (var.get(u'stream').get(u'next')!=Js(u'}')):
                var.put(u'max', var.get(u'parseNum')(var.get(u'stream')))
            else:
                var.put(u'max', (-Js(1.0)))
        if var.get(u'stream').callprop(u'eat', Js(u'}')).neg():
            var.get(u'stream').callprop(u'err', Js(u'Unclosed braced range'))
        PyJs_Object_230_ = Js({u'type':Js(u'range'),u'min':var.get(u'min'),u'max':var.get(u'max'),u'expr':var.get(u'expr')})
        return PyJs_Object_230_
    PyJsHoisted_parseExprRange_.func_name = u'parseExprRange'
    var.put(u'parseExprRange', PyJsHoisted_parseExprRange_)
    @Js
    def PyJsHoisted_parseExpr_(stream, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'stream':stream}, var)
        var.registers([u'exprs', u'stream'])
        var.put(u'exprs', Js([]))
        while 1:
            var.get(u'exprs').callprop(u'push', var.get(u'parseExprSeq')(var.get(u'stream')))
            if not var.get(u'stream').callprop(u'eat', Js(u'|')):
                break
        PyJs_Object_225_ = Js({u'type':Js(u'choice'),u'exprs':var.get(u'exprs')})
        return (var.get(u'exprs').get(u'0') if (var.get(u'exprs').get(u'length')==Js(1.0)) else PyJs_Object_225_)
    PyJsHoisted_parseExpr_.func_name = u'parseExpr'
    var.put(u'parseExpr', PyJsHoisted_parseExpr_)
    @Js
    def PyJsHoisted_replaceTwoWay_(PyJsArg_2466726f6d_, PyJsArg_24746f_, depth, this, arguments, var=var):
        var = Scope({u'this':this, u'$from':PyJsArg_2466726f6d_, u'depth':depth, u'$to':PyJsArg_24746f_, u'arguments':arguments}, var)
        var.registers([u'content', u'$from', u'depth', u'type', u'$to'])
        var.put(u'content', Js([]))
        var.get(u'addRange')(var.get(u"null"), var.get(u'$from'), var.get(u'depth'), var.get(u'content'))
        if (var.get(u'$from').get(u'depth')>var.get(u'depth')):
            var.put(u'type', var.get(u'joinable')(var.get(u'$from'), var.get(u'$to'), (var.get(u'depth')+Js(1.0))))
            var.get(u'addNode')(var.get(u'close')(var.get(u'type'), var.get(u'replaceTwoWay')(var.get(u'$from'), var.get(u'$to'), (var.get(u'depth')+Js(1.0)))), var.get(u'content'))
        var.get(u'addRange')(var.get(u'$to'), var.get(u"null"), var.get(u'depth'), var.get(u'content'))
        return var.get(u'Fragment').create(var.get(u'content'))
    PyJsHoisted_replaceTwoWay_.func_name = u'replaceTwoWay'
    var.put(u'replaceTwoWay', PyJsHoisted_replaceTwoWay_)
    @Js
    def PyJsHoisted_findDiffEnd_(a, b, posA, posB, this, arguments, var=var):
        var = Scope({u'a':a, u'b':b, u'arguments':arguments, u'this':this, u'posB':posB, u'posA':posA}, var)
        var.registers([u'a', u'b', u'posB', u'same', u'posA', u'minSize', u'childA', u'childB', u'inner', u'iA', u'iB', u'size'])
        #for JS loop
        var.put(u'iA', var.get(u'a').get(u'childCount'))
        var.put(u'iB', var.get(u'b').get(u'childCount'))
        while 1:
            if ((var.get(u'iA')==Js(0.0)) or (var.get(u'iB')==Js(0.0))):
                PyJs_Object_19_ = Js({u'a':var.get(u'posA'),u'b':var.get(u'posB')})
                return (var.get(u"null") if (var.get(u'iA')==var.get(u'iB')) else PyJs_Object_19_)
            var.put(u'childA', var.get(u'a').callprop(u'child', var.put(u'iA',Js(var.get(u'iA').to_number())-Js(1))))
            var.put(u'childB', var.get(u'b').callprop(u'child', var.put(u'iB',Js(var.get(u'iB').to_number())-Js(1))))
            var.put(u'size', var.get(u'childA').get(u'nodeSize'))
            if (var.get(u'childA')==var.get(u'childB')):
                var.put(u'posA', var.get(u'size'), u'-')
                var.put(u'posB', var.get(u'size'), u'-')
                continue
            if var.get(u'childA').callprop(u'sameMarkup', var.get(u'childB')).neg():
                PyJs_Object_20_ = Js({u'a':var.get(u'posA'),u'b':var.get(u'posB')})
                return PyJs_Object_20_
            if (var.get(u'childA').get(u'isText') and (var.get(u'childA').get(u'text')!=var.get(u'childB').get(u'text'))):
                var.put(u'same', Js(0.0))
                var.put(u'minSize', var.get(u'Math').callprop(u'min', var.get(u'childA').get(u'text').get(u'length'), var.get(u'childB').get(u'text').get(u'length')))
                while ((var.get(u'same')<var.get(u'minSize')) and (var.get(u'childA').get(u'text').get(((var.get(u'childA').get(u'text').get(u'length')-var.get(u'same'))-Js(1.0)))==var.get(u'childB').get(u'text').get(((var.get(u'childB').get(u'text').get(u'length')-var.get(u'same'))-Js(1.0))))):
                    (var.put(u'same',Js(var.get(u'same').to_number())+Js(1))-Js(1))
                    (var.put(u'posA',Js(var.get(u'posA').to_number())-Js(1))+Js(1))
                    (var.put(u'posB',Js(var.get(u'posB').to_number())-Js(1))+Js(1))
                PyJs_Object_21_ = Js({u'a':var.get(u'posA'),u'b':var.get(u'posB')})
                return PyJs_Object_21_
            if (var.get(u'childA').get(u'content').get(u'size') or var.get(u'childB').get(u'content').get(u'size')):
                var.put(u'inner', var.get(u'findDiffEnd')(var.get(u'childA').get(u'content'), var.get(u'childB').get(u'content'), (var.get(u'posA')-Js(1.0)), (var.get(u'posB')-Js(1.0))))
                if var.get(u'inner'):
                    return var.get(u'inner')
            var.put(u'posA', var.get(u'size'), u'-')
            var.put(u'posB', var.get(u'size'), u'-')
        
    PyJsHoisted_findDiffEnd_.func_name = u'findDiffEnd'
    var.put(u'findDiffEnd', PyJsHoisted_findDiffEnd_)
    @Js
    def PyJsHoisted_parseExprSeq_(stream, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'stream':stream}, var)
        var.registers([u'exprs', u'stream'])
        var.put(u'exprs', Js([]))
        while 1:
            var.get(u'exprs').callprop(u'push', var.get(u'parseExprSubscript')(var.get(u'stream')))
            if not ((var.get(u'stream').get(u'next') and (var.get(u'stream').get(u'next')!=Js(u')'))) and (var.get(u'stream').get(u'next')!=Js(u'|'))):
                break
        PyJs_Object_226_ = Js({u'type':Js(u'seq'),u'exprs':var.get(u'exprs')})
        return (var.get(u'exprs').get(u'0') if (var.get(u'exprs').get(u'length')==Js(1.0)) else PyJs_Object_226_)
    PyJsHoisted_parseExprSeq_.func_name = u'parseExprSeq'
    var.put(u'parseExprSeq', PyJsHoisted_parseExprSeq_)
    @Js
    def PyJsHoisted_nullFrom_(nfa, node, this, arguments, var=var):
        var = Scope({u'node':node, u'this':this, u'arguments':arguments, u'nfa':nfa}, var)
        var.registers([u'node', u'result', u'nfa', u'scan'])
        @Js
        def PyJsHoisted_scan_(node, this, arguments, var=var):
            var = Scope({u'node':node, u'this':this, u'arguments':arguments}, var)
            var.registers([u'node', u'term', u'i', u'to', u'edges', u'ref'])
            var.put(u'edges', var.get(u'nfa').get(var.get(u'node')))
            if ((var.get(u'edges').get(u'length')==Js(1.0)) and var.get(u'edges').get(u'0').get(u'term').neg()):
                return var.get(u'scan')(var.get(u'edges').get(u'0').get(u'to'))
            var.get(u'result').callprop(u'push', var.get(u'node'))
            #for JS loop
            var.put(u'i', Js(0.0))
            while (var.get(u'i')<var.get(u'edges').get(u'length')):
                try:
                    var.put(u'ref', var.get(u'edges').get(var.get(u'i')))
                    var.put(u'term', var.get(u'ref').get(u'term'))
                    var.put(u'to', var.get(u'ref').get(u'to'))
                    if (var.get(u'term').neg() and (var.get(u'result').callprop(u'indexOf', var.get(u'to'))==(-Js(1.0)))):
                        var.get(u'scan')(var.get(u'to'))
                finally:
                        (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        PyJsHoisted_scan_.func_name = u'scan'
        var.put(u'scan', PyJsHoisted_scan_)
        var.put(u'result', Js([]))
        var.get(u'scan')(var.get(u'node'))
        return var.get(u'result').callprop(u'sort', var.get(u'cmp'))
        pass
    PyJsHoisted_nullFrom_.func_name = u'nullFrom'
    var.put(u'nullFrom', PyJsHoisted_nullFrom_)
    @Js
    def PyJsHoisted_dfa_(nfa, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'nfa':nfa}, var)
        var.registers([u'labeled', u'explore', u'nfa'])
        @Js
        def PyJsHoisted_explore_(states, this, arguments, var=var):
            var = Scope({u'states':states, u'this':this, u'arguments':arguments}, var)
            var.registers([u'i', u'states', u'state', u'states$1', u'out'])
            var.put(u'out', Js([]))
            @Js
            def PyJs_anonymous_237_(node, this, arguments, var=var):
                var = Scope({u'node':node, u'this':this, u'arguments':arguments}, var)
                var.registers([u'node'])
                @Js
                def PyJs_anonymous_238_(ref, this, arguments, var=var):
                    var = Scope({u'this':this, u'ref':ref, u'arguments':arguments}, var)
                    var.registers([u'known', u'to', u'term', u'set', u'ref'])
                    var.put(u'term', var.get(u'ref').get(u'term'))
                    var.put(u'to', var.get(u'ref').get(u'to'))
                    if var.get(u'term').neg():
                        return var.get('undefined')
                    var.put(u'known', var.get(u'out').callprop(u'indexOf', var.get(u'term')))
                    var.put(u'set', ((var.get(u'known')>(-Js(1.0))) and var.get(u'out').get((var.get(u'known')+Js(1.0)))))
                    @Js
                    def PyJs_anonymous_239_(node, this, arguments, var=var):
                        var = Scope({u'node':node, u'this':this, u'arguments':arguments}, var)
                        var.registers([u'node'])
                        if var.get(u'set').neg():
                            var.get(u'out').callprop(u'push', var.get(u'term'), var.put(u'set', Js([])))
                        if (var.get(u'set').callprop(u'indexOf', var.get(u'node'))==(-Js(1.0))):
                            var.get(u'set').callprop(u'push', var.get(u'node'))
                    PyJs_anonymous_239_._set_name(u'anonymous')
                    var.get(u'nullFrom')(var.get(u'nfa'), var.get(u'to')).callprop(u'forEach', PyJs_anonymous_239_)
                PyJs_anonymous_238_._set_name(u'anonymous')
                var.get(u'nfa').get(var.get(u'node')).callprop(u'forEach', PyJs_anonymous_238_)
            PyJs_anonymous_237_._set_name(u'anonymous')
            var.get(u'states').callprop(u'forEach', PyJs_anonymous_237_)
            var.put(u'state', var.get(u'labeled').put(var.get(u'states').callprop(u'join', Js(u',')), var.get(u'ContentMatch').create((var.get(u'states').callprop(u'indexOf', (var.get(u'nfa').get(u'length')-Js(1.0)))>(-Js(1.0))))))
            #for JS loop
            var.put(u'i', Js(0.0))
            while (var.get(u'i')<var.get(u'out').get(u'length')):
                try:
                    var.put(u'states$1', var.get(u'out').get((var.get(u'i')+Js(1.0))).callprop(u'sort', var.get(u'cmp')))
                    var.get(u'state').get(u'next').callprop(u'push', var.get(u'out').get(var.get(u'i')), (var.get(u'labeled').get(var.get(u'states$1').callprop(u'join', Js(u','))) or var.get(u'explore')(var.get(u'states$1'))))
                finally:
                        var.put(u'i', Js(2.0), u'+')
            return var.get(u'state')
        PyJsHoisted_explore_.func_name = u'explore'
        var.put(u'explore', PyJsHoisted_explore_)
        var.put(u'labeled', var.get(u'Object').callprop(u'create', var.get(u"null")))
        return var.get(u'explore')(var.get(u'nullFrom')(var.get(u'nfa'), Js(0.0)))
        pass
    PyJsHoisted_dfa_.func_name = u'dfa'
    var.put(u'dfa', PyJsHoisted_dfa_)
    @Js
    def PyJsHoisted__interopDefault_(ex, this, arguments, var=var):
        var = Scope({u'this':this, u'ex':ex, u'arguments':arguments}, var)
        var.registers([u'ex'])
        return (var.get(u'ex').get(u'default') if ((var.get(u'ex') and PyJsStrictEq(var.get(u'ex',throw=False).typeof(),Js(u'object'))) and var.get(u'ex').contains(Js(u'default'))) else var.get(u'ex'))
    PyJsHoisted__interopDefault_.func_name = u'_interopDefault'
    var.put(u'_interopDefault', PyJsHoisted__interopDefault_)
    @Js
    def PyJsHoisted_parseExprAtom_(stream, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'stream':stream}, var)
        var.registers([u'expr', u'stream', u'exprs'])
        if var.get(u'stream').callprop(u'eat', Js(u'(')):
            var.put(u'expr', var.get(u'parseExpr')(var.get(u'stream')))
            if var.get(u'stream').callprop(u'eat', Js(u')')).neg():
                var.get(u'stream').callprop(u'err', Js(u'Missing closing paren'))
            return var.get(u'expr')
        else:
            if JsRegExp(u'/\\W/').callprop(u'test', var.get(u'stream').get(u'next')).neg():
                @Js
                def PyJs_anonymous_231_(type, this, arguments, var=var):
                    var = Scope({u'this':this, u'type':type, u'arguments':arguments}, var)
                    var.registers([u'type'])
                    if (var.get(u'stream').get(u'inline')==var.get(u"null")):
                        var.get(u'stream').put(u'inline', var.get(u'type').get(u'isInline'))
                    else:
                        if (var.get(u'stream').get(u'inline')!=var.get(u'type').get(u'isInline')):
                            var.get(u'stream').callprop(u'err', Js(u'Mixing inline and block content'))
                    PyJs_Object_232_ = Js({u'type':Js(u'name'),u'value':var.get(u'type')})
                    return PyJs_Object_232_
                PyJs_anonymous_231_._set_name(u'anonymous')
                var.put(u'exprs', var.get(u'resolveName')(var.get(u'stream'), var.get(u'stream').get(u'next')).callprop(u'map', PyJs_anonymous_231_))
                (var.get(u'stream').put(u'pos',Js(var.get(u'stream').get(u'pos').to_number())+Js(1))-Js(1))
                PyJs_Object_233_ = Js({u'type':Js(u'choice'),u'exprs':var.get(u'exprs')})
                return (var.get(u'exprs').get(u'0') if (var.get(u'exprs').get(u'length')==Js(1.0)) else PyJs_Object_233_)
            else:
                var.get(u'stream').callprop(u'err', ((Js(u"Unexpected token '")+var.get(u'stream').get(u'next'))+Js(u"'")))
    PyJsHoisted_parseExprAtom_.func_name = u'parseExprAtom'
    var.put(u'parseExprAtom', PyJsHoisted_parseExprAtom_)
    @Js
    def PyJsHoisted_defaultAttrs_(attrs, this, arguments, var=var):
        var = Scope({u'this':this, u'attrs':attrs, u'arguments':arguments}, var)
        var.registers([u'attrName', u'attr', u'defaults', u'attrs'])
        var.put(u'defaults', var.get(u'Object').callprop(u'create', var.get(u"null")))
        for PyJsTemp in var.get(u'attrs'):
            var.put(u'attrName', PyJsTemp)
            var.put(u'attr', var.get(u'attrs').get(var.get(u'attrName')))
            if var.get(u'attr').get(u'hasDefault').neg():
                return var.get(u"null")
            var.get(u'defaults').put(var.get(u'attrName'), var.get(u'attr').get(u'default'))
        return var.get(u'defaults')
    PyJsHoisted_defaultAttrs_.func_name = u'defaultAttrs'
    var.put(u'defaultAttrs', PyJsHoisted_defaultAttrs_)
    @Js
    def PyJsHoisted_addNode_(child, target, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'target':target, u'child':child}, var)
        var.registers([u'last', u'target', u'child'])
        var.put(u'last', (var.get(u'target').get(u'length')-Js(1.0)))
        if (((var.get(u'last')>=Js(0.0)) and var.get(u'child').get(u'isText')) and var.get(u'child').callprop(u'sameMarkup', var.get(u'target').get(var.get(u'last')))):
            var.get(u'target').put(var.get(u'last'), var.get(u'child').callprop(u'withText', (var.get(u'target').get(var.get(u'last')).get(u'text')+var.get(u'child').get(u'text'))))
        else:
            var.get(u'target').callprop(u'push', var.get(u'child'))
    PyJsHoisted_addNode_.func_name = u'addNode'
    var.put(u'addNode', PyJsHoisted_addNode_)
    @Js
    def PyJsHoisted_matches_(dom, selector, this, arguments, var=var):
        var = Scope({u'this':this, u'selector':selector, u'arguments':arguments, u'dom':dom}, var)
        var.registers([u'selector', u'dom'])
        return (((var.get(u'dom').get(u'matches') or var.get(u'dom').get(u'msMatchesSelector')) or var.get(u'dom').get(u'webkitMatchesSelector')) or var.get(u'dom').get(u'mozMatchesSelector')).callprop(u'call', var.get(u'dom'), var.get(u'selector'))
    PyJsHoisted_matches_.func_name = u'matches'
    var.put(u'matches', PyJsHoisted_matches_)
    @Js
    def PyJsHoisted_replaceThreeWay_(PyJsArg_2466726f6d_, PyJsArg_247374617274_, PyJsArg_24656e64_, PyJsArg_24746f_, depth, this, arguments, var=var):
        var = Scope({u'depth':depth, u'$to':PyJsArg_24746f_, u'arguments':arguments, u'$start':PyJsArg_247374617274_, u'this':this, u'$from':PyJsArg_2466726f6d_, u'$end':PyJsArg_24656e64_}, var)
        var.registers([u'$to', u'$start', u'$from', u'content', u'depth', u'openStart', u'openEnd', u'$end'])
        var.put(u'openStart', ((var.get(u'$from').get(u'depth')>var.get(u'depth')) and var.get(u'joinable')(var.get(u'$from'), var.get(u'$start'), (var.get(u'depth')+Js(1.0)))))
        var.put(u'openEnd', ((var.get(u'$to').get(u'depth')>var.get(u'depth')) and var.get(u'joinable')(var.get(u'$end'), var.get(u'$to'), (var.get(u'depth')+Js(1.0)))))
        var.put(u'content', Js([]))
        var.get(u'addRange')(var.get(u"null"), var.get(u'$from'), var.get(u'depth'), var.get(u'content'))
        if ((var.get(u'openStart') and var.get(u'openEnd')) and (var.get(u'$start').callprop(u'index', var.get(u'depth'))==var.get(u'$end').callprop(u'index', var.get(u'depth')))):
            var.get(u'checkJoin')(var.get(u'openStart'), var.get(u'openEnd'))
            var.get(u'addNode')(var.get(u'close')(var.get(u'openStart'), var.get(u'replaceThreeWay')(var.get(u'$from'), var.get(u'$start'), var.get(u'$end'), var.get(u'$to'), (var.get(u'depth')+Js(1.0)))), var.get(u'content'))
        else:
            if var.get(u'openStart'):
                var.get(u'addNode')(var.get(u'close')(var.get(u'openStart'), var.get(u'replaceTwoWay')(var.get(u'$from'), var.get(u'$start'), (var.get(u'depth')+Js(1.0)))), var.get(u'content'))
            var.get(u'addRange')(var.get(u'$start'), var.get(u'$end'), var.get(u'depth'), var.get(u'content'))
            if var.get(u'openEnd'):
                var.get(u'addNode')(var.get(u'close')(var.get(u'openEnd'), var.get(u'replaceTwoWay')(var.get(u'$end'), var.get(u'$to'), (var.get(u'depth')+Js(1.0)))), var.get(u'content'))
        var.get(u'addRange')(var.get(u'$to'), var.get(u"null"), var.get(u'depth'), var.get(u'content'))
        return var.get(u'Fragment').create(var.get(u'content'))
    PyJsHoisted_replaceThreeWay_.func_name = u'replaceThreeWay'
    var.put(u'replaceThreeWay', PyJsHoisted_replaceThreeWay_)
    @Js
    def PyJsHoisted_addRange_(PyJsArg_247374617274_, PyJsArg_24656e64_, depth, target, this, arguments, var=var):
        var = Scope({u'depth':depth, u'target':target, u'$start':PyJsArg_247374617274_, u'this':this, u'arguments':arguments, u'$end':PyJsArg_24656e64_}, var)
        var.registers([u'node', u'endIndex', u'target', u'$start', u'i', u'depth', u'startIndex', u'$end'])
        var.put(u'node', (var.get(u'$end') or var.get(u'$start')).callprop(u'node', var.get(u'depth')))
        var.put(u'startIndex', Js(0.0))
        var.put(u'endIndex', (var.get(u'$end').callprop(u'index', var.get(u'depth')) if var.get(u'$end') else var.get(u'node').get(u'childCount')))
        if var.get(u'$start'):
            var.put(u'startIndex', var.get(u'$start').callprop(u'index', var.get(u'depth')))
            if (var.get(u'$start').get(u'depth')>var.get(u'depth')):
                (var.put(u'startIndex',Js(var.get(u'startIndex').to_number())+Js(1))-Js(1))
            else:
                if var.get(u'$start').get(u'textOffset'):
                    var.get(u'addNode')(var.get(u'$start').get(u'nodeAfter'), var.get(u'target'))
                    (var.put(u'startIndex',Js(var.get(u'startIndex').to_number())+Js(1))-Js(1))
        #for JS loop
        var.put(u'i', var.get(u'startIndex'))
        while (var.get(u'i')<var.get(u'endIndex')):
            try:
                var.get(u'addNode')(var.get(u'node').callprop(u'child', var.get(u'i')), var.get(u'target'))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        if ((var.get(u'$end') and (var.get(u'$end').get(u'depth')==var.get(u'depth'))) and var.get(u'$end').get(u'textOffset')):
            var.get(u'addNode')(var.get(u'$end').get(u'nodeBefore'), var.get(u'target'))
    PyJsHoisted_addRange_.func_name = u'addRange'
    var.put(u'addRange', PyJsHoisted_addRange_)
    @Js
    def PyJsHoisted_checkJoin_(main, sub, this, arguments, var=var):
        var = Scope({u'this':this, u'main':main, u'sub':sub, u'arguments':arguments}, var)
        var.registers([u'main', u'sub'])
        if var.get(u'sub').get(u'type').callprop(u'compatibleContent', var.get(u'main').get(u'type')).neg():
            PyJsTempException = JsToPyException(var.get(u'ReplaceError').create((((Js(u'Cannot join ')+var.get(u'sub').get(u'type').get(u'name'))+Js(u' onto '))+var.get(u'main').get(u'type').get(u'name'))))
            raise PyJsTempException
    PyJsHoisted_checkJoin_.func_name = u'checkJoin'
    var.put(u'checkJoin', PyJsHoisted_checkJoin_)
    @Js
    def PyJsHoisted_removeRange_(content, PyJsArg_66726f6d_, to, this, arguments, var=var):
        var = Scope({u'content':content, u'to':to, u'this':this, u'from':PyJsArg_66726f6d_, u'arguments':arguments}, var)
        var.registers([u'indexTo', u'index', u'from', u'offset', u'content', u'to', u'offsetTo', u'child', u'ref', u'ref$1'])
        var.put(u'ref', var.get(u'content').callprop(u'findIndex', var.get(u'from')))
        var.put(u'index', var.get(u'ref').get(u'index'))
        var.put(u'offset', var.get(u'ref').get(u'offset'))
        var.put(u'child', var.get(u'content').callprop(u'maybeChild', var.get(u'index')))
        var.put(u'ref$1', var.get(u'content').callprop(u'findIndex', var.get(u'to')))
        var.put(u'indexTo', var.get(u'ref$1').get(u'index'))
        var.put(u'offsetTo', var.get(u'ref$1').get(u'offset'))
        if ((var.get(u'offset')==var.get(u'from')) or var.get(u'child').get(u'isText')):
            if ((var.get(u'offsetTo')!=var.get(u'to')) and var.get(u'content').callprop(u'child', var.get(u'indexTo')).get(u'isText').neg()):
                PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'Removing non-flat range')))
                raise PyJsTempException
            return var.get(u'content').callprop(u'cut', Js(0.0), var.get(u'from')).callprop(u'append', var.get(u'content').callprop(u'cut', var.get(u'to')))
        if (var.get(u'index')!=var.get(u'indexTo')):
            PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'Removing non-flat range')))
            raise PyJsTempException
        return var.get(u'content').callprop(u'replaceChild', var.get(u'index'), var.get(u'child').callprop(u'copy', var.get(u'removeRange')(var.get(u'child').get(u'content'), ((var.get(u'from')-var.get(u'offset'))-Js(1.0)), ((var.get(u'to')-var.get(u'offset'))-Js(1.0)))))
    PyJsHoisted_removeRange_.func_name = u'removeRange'
    var.put(u'removeRange', PyJsHoisted_removeRange_)
    @Js
    def PyJsHoisted_copy_(obj, this, arguments, var=var):
        var = Scope({u'this':this, u'obj':obj, u'arguments':arguments}, var)
        var.registers([u'copy', u'obj', u'prop'])
        PyJs_Object_332_ = Js({})
        var.put(u'copy', PyJs_Object_332_)
        for PyJsTemp in var.get(u'obj'):
            var.put(u'prop', PyJsTemp)
            var.get(u'copy').put(var.get(u'prop'), var.get(u'obj').get(var.get(u'prop')))
        return var.get(u'copy')
    PyJsHoisted_copy_.func_name = u'copy'
    var.put(u'copy', PyJsHoisted_copy_)
    @Js
    def PyJsHoisted_parseNum_(stream, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'stream':stream}, var)
        var.registers([u'result', u'stream'])
        if JsRegExp(u'/\\D/').callprop(u'test', var.get(u'stream').get(u'next')):
            var.get(u'stream').callprop(u'err', ((Js(u"Expected number, got '")+var.get(u'stream').get(u'next'))+Js(u"'")))
        var.put(u'result', var.get(u'Number')(var.get(u'stream').get(u'next')))
        (var.get(u'stream').put(u'pos',Js(var.get(u'stream').get(u'pos').to_number())+Js(1))-Js(1))
        return var.get(u'result')
    PyJsHoisted_parseNum_.func_name = u'parseNum'
    var.put(u'parseNum', PyJsHoisted_parseNum_)
    @Js
    def PyJsHoisted_wsOptionsFor_(preserveWhitespace, this, arguments, var=var):
        var = Scope({u'this':this, u'preserveWhitespace':preserveWhitespace, u'arguments':arguments}, var)
        var.registers([u'preserveWhitespace'])
        return ((var.get(u'OPT_PRESERVE_WS') if var.get(u'preserveWhitespace') else Js(0.0))|(var.get(u'OPT_PRESERVE_WS_FULL') if PyJsStrictEq(var.get(u'preserveWhitespace'),Js(u'full')) else Js(0.0)))
    PyJsHoisted_wsOptionsFor_.func_name = u'wsOptionsFor'
    var.put(u'wsOptionsFor', PyJsHoisted_wsOptionsFor_)
    @Js
    def PyJsHoisted_replaceOuter_(PyJsArg_2466726f6d_, PyJsArg_24746f_, slice, depth, this, arguments, var=var):
        var = Scope({u'depth':depth, u'slice':slice, u'$to':PyJsArg_24746f_, u'arguments':arguments, u'this':this, u'$from':PyJsArg_2466726f6d_}, var)
        var.registers([u'node', u'index', u'slice', u'end', u'parent', u'$from', u'content', u'start', u'depth', u'inner', u'$to', u'ref'])
        var.put(u'index', var.get(u'$from').callprop(u'index', var.get(u'depth')))
        var.put(u'node', var.get(u'$from').callprop(u'node', var.get(u'depth')))
        if ((var.get(u'index')==var.get(u'$to').callprop(u'index', var.get(u'depth'))) and (var.get(u'depth')<(var.get(u'$from').get(u'depth')-var.get(u'slice').get(u'openStart')))):
            var.put(u'inner', var.get(u'replaceOuter')(var.get(u'$from'), var.get(u'$to'), var.get(u'slice'), (var.get(u'depth')+Js(1.0))))
            return var.get(u'node').callprop(u'copy', var.get(u'node').get(u'content').callprop(u'replaceChild', var.get(u'index'), var.get(u'inner')))
        else:
            if var.get(u'slice').get(u'content').get(u'size').neg():
                return var.get(u'close')(var.get(u'node'), var.get(u'replaceTwoWay')(var.get(u'$from'), var.get(u'$to'), var.get(u'depth')))
            else:
                if (((var.get(u'slice').get(u'openStart').neg() and var.get(u'slice').get(u'openEnd').neg()) and (var.get(u'$from').get(u'depth')==var.get(u'depth'))) and (var.get(u'$to').get(u'depth')==var.get(u'depth'))):
                    var.put(u'parent', var.get(u'$from').get(u'parent'))
                    var.put(u'content', var.get(u'parent').get(u'content'))
                    return var.get(u'close')(var.get(u'parent'), var.get(u'content').callprop(u'cut', Js(0.0), var.get(u'$from').get(u'parentOffset')).callprop(u'append', var.get(u'slice').get(u'content')).callprop(u'append', var.get(u'content').callprop(u'cut', var.get(u'$to').get(u'parentOffset'))))
                else:
                    var.put(u'ref', var.get(u'prepareSliceForReplace')(var.get(u'slice'), var.get(u'$from')))
                    var.put(u'start', var.get(u'ref').get(u'start'))
                    var.put(u'end', var.get(u'ref').get(u'end'))
                    return var.get(u'close')(var.get(u'node'), var.get(u'replaceThreeWay')(var.get(u'$from'), var.get(u'start'), var.get(u'end'), var.get(u'$to'), var.get(u'depth')))
    PyJsHoisted_replaceOuter_.func_name = u'replaceOuter'
    var.put(u'replaceOuter', PyJsHoisted_replaceOuter_)
    @Js
    def PyJsHoisted_nfa_(expr, this, arguments, var=var):
        var = Scope({u'this':this, u'expr':expr, u'arguments':arguments}, var)
        var.registers([u'node', u'nfa', u'expr', u'compile', u'edge', u'connect'])
        @Js
        def PyJsHoisted_node_(this, arguments, var=var):
            var = Scope({u'this':this, u'arguments':arguments}, var)
            var.registers([])
            return (var.get(u'nfa').callprop(u'push', Js([]))-Js(1.0))
        PyJsHoisted_node_.func_name = u'node'
        var.put(u'node', PyJsHoisted_node_)
        @Js
        def PyJsHoisted_compile_(expr, PyJsArg_66726f6d_, this, arguments, var=var):
            var = Scope({u'this':this, u'expr':expr, u'from':PyJsArg_66726f6d_, u'arguments':arguments}, var)
            var.registers([u'next$2', u'from', u'cur', u'i', u'loop$1', u'i$2', u'i$1', u'expr', u'next$1', u'next', u'loop'])
            if (var.get(u'expr').get(u'type')==Js(u'choice')):
                @Js
                def PyJs_anonymous_236_(out, expr, this, arguments, var=var):
                    var = Scope({u'this':this, u'expr':expr, u'arguments':arguments, u'out':out}, var)
                    var.registers([u'expr', u'out'])
                    return var.get(u'out').callprop(u'concat', var.get(u'compile')(var.get(u'expr'), var.get(u'from')))
                PyJs_anonymous_236_._set_name(u'anonymous')
                return var.get(u'expr').get(u'exprs').callprop(u'reduce', PyJs_anonymous_236_, Js([]))
            else:
                if (var.get(u'expr').get(u'type')==Js(u'seq')):
                    #for JS loop
                    var.put(u'i', Js(0.0))
                    while 1:
                        try:
                            var.put(u'next', var.get(u'compile')(var.get(u'expr').get(u'exprs').get(var.get(u'i')), var.get(u'from')))
                            if (var.get(u'i')==(var.get(u'expr').get(u'exprs').get(u'length')-Js(1.0))):
                                return var.get(u'next')
                            var.get(u'connect')(var.get(u'next'), var.put(u'from', var.get(u'node')()))
                        finally:
                                (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
                else:
                    if (var.get(u'expr').get(u'type')==Js(u'star')):
                        var.put(u'loop', var.get(u'node')())
                        var.get(u'edge')(var.get(u'from'), var.get(u'loop'))
                        var.get(u'connect')(var.get(u'compile')(var.get(u'expr').get(u'expr'), var.get(u'loop')), var.get(u'loop'))
                        return Js([var.get(u'edge')(var.get(u'loop'))])
                    else:
                        if (var.get(u'expr').get(u'type')==Js(u'plus')):
                            var.put(u'loop$1', var.get(u'node')())
                            var.get(u'connect')(var.get(u'compile')(var.get(u'expr').get(u'expr'), var.get(u'from')), var.get(u'loop$1'))
                            var.get(u'connect')(var.get(u'compile')(var.get(u'expr').get(u'expr'), var.get(u'loop$1')), var.get(u'loop$1'))
                            return Js([var.get(u'edge')(var.get(u'loop$1'))])
                        else:
                            if (var.get(u'expr').get(u'type')==Js(u'opt')):
                                return Js([var.get(u'edge')(var.get(u'from'))]).callprop(u'concat', var.get(u'compile')(var.get(u'expr').get(u'expr'), var.get(u'from')))
                            else:
                                if (var.get(u'expr').get(u'type')==Js(u'range')):
                                    var.put(u'cur', var.get(u'from'))
                                    #for JS loop
                                    var.put(u'i$1', Js(0.0))
                                    while (var.get(u'i$1')<var.get(u'expr').get(u'min')):
                                        try:
                                            var.put(u'next$1', var.get(u'node')())
                                            var.get(u'connect')(var.get(u'compile')(var.get(u'expr').get(u'expr'), var.get(u'cur')), var.get(u'next$1'))
                                            var.put(u'cur', var.get(u'next$1'))
                                        finally:
                                                (var.put(u'i$1',Js(var.get(u'i$1').to_number())+Js(1))-Js(1))
                                    if (var.get(u'expr').get(u'max')==(-Js(1.0))):
                                        var.get(u'connect')(var.get(u'compile')(var.get(u'expr').get(u'expr'), var.get(u'cur')), var.get(u'cur'))
                                    else:
                                        #for JS loop
                                        var.put(u'i$2', var.get(u'expr').get(u'min'))
                                        while (var.get(u'i$2')<var.get(u'expr').get(u'max')):
                                            try:
                                                var.put(u'next$2', var.get(u'node')())
                                                var.get(u'edge')(var.get(u'cur'), var.get(u'next$2'))
                                                var.get(u'connect')(var.get(u'compile')(var.get(u'expr').get(u'expr'), var.get(u'cur')), var.get(u'next$2'))
                                                var.put(u'cur', var.get(u'next$2'))
                                            finally:
                                                    (var.put(u'i$2',Js(var.get(u'i$2').to_number())+Js(1))-Js(1))
                                    return Js([var.get(u'edge')(var.get(u'cur'))])
                                else:
                                    if (var.get(u'expr').get(u'type')==Js(u'name')):
                                        return Js([var.get(u'edge')(var.get(u'from'), var.get(u"null"), var.get(u'expr').get(u'value'))])
        PyJsHoisted_compile_.func_name = u'compile'
        var.put(u'compile', PyJsHoisted_compile_)
        @Js
        def PyJsHoisted_edge_(PyJsArg_66726f6d_, to, term, this, arguments, var=var):
            var = Scope({u'this':this, u'to':to, u'term':term, u'from':PyJsArg_66726f6d_, u'arguments':arguments}, var)
            var.registers([u'to', u'term', u'edge', u'from'])
            PyJs_Object_234_ = Js({u'term':var.get(u'term'),u'to':var.get(u'to')})
            var.put(u'edge', PyJs_Object_234_)
            var.get(u'nfa').get(var.get(u'from')).callprop(u'push', var.get(u'edge'))
            return var.get(u'edge')
        PyJsHoisted_edge_.func_name = u'edge'
        var.put(u'edge', PyJsHoisted_edge_)
        @Js
        def PyJsHoisted_connect_(edges, to, this, arguments, var=var):
            var = Scope({u'this':this, u'to':to, u'edges':edges, u'arguments':arguments}, var)
            var.registers([u'to', u'edges'])
            @Js
            def PyJs_anonymous_235_(edge, this, arguments, var=var):
                var = Scope({u'this':this, u'edge':edge, u'arguments':arguments}, var)
                var.registers([u'edge'])
                return var.get(u'edge').put(u'to', var.get(u'to'))
            PyJs_anonymous_235_._set_name(u'anonymous')
            var.get(u'edges').callprop(u'forEach', PyJs_anonymous_235_)
        PyJsHoisted_connect_.func_name = u'connect'
        var.put(u'connect', PyJsHoisted_connect_)
        var.put(u'nfa', Js([Js([])]))
        var.get(u'connect')(var.get(u'compile')(var.get(u'expr'), Js(0.0)), var.get(u'node')())
        return var.get(u'nfa')
        pass
        pass
        pass
        pass
    PyJsHoisted_nfa_.func_name = u'nfa'
    var.put(u'nfa', PyJsHoisted_nfa_)
    @Js
    def PyJsHoisted_retIndex_(index, offset, this, arguments, var=var):
        var = Scope({u'this':this, u'index':index, u'arguments':arguments, u'offset':offset}, var)
        var.registers([u'index', u'offset'])
        var.get(u'found').put(u'index', var.get(u'index'))
        var.get(u'found').put(u'offset', var.get(u'offset'))
        return var.get(u'found')
    PyJsHoisted_retIndex_.func_name = u'retIndex'
    var.put(u'retIndex', PyJsHoisted_retIndex_)
    @Js
    def PyJsHoisted_doc_(options, this, arguments, var=var):
        var = Scope({u'this':this, u'options':options, u'arguments':arguments}, var)
        var.registers([u'options'])
        return (var.get(u'options').get(u'document') or var.get(u'window').get(u'document'))
    PyJsHoisted_doc_.func_name = u'doc'
    var.put(u'doc', PyJsHoisted_doc_)
    @Js
    def PyJsHoisted_gatherMarks_(schema, marks, this, arguments, var=var):
        var = Scope({u'this':this, u'marks':marks, u'arguments':arguments, u'schema':schema}, var)
        var.registers([u'ok', u'name', u'i', u'prop', u'marks', u'mark$1', u'found', u'mark', u'schema'])
        var.put(u'found', Js([]))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u'marks').get(u'length')):
            try:
                var.put(u'name', var.get(u'marks').get(var.get(u'i')))
                var.put(u'mark', var.get(u'schema').get(u'marks').get(var.get(u'name')))
                var.put(u'ok', var.get(u'mark'))
                if var.get(u'mark'):
                    var.get(u'found').callprop(u'push', var.get(u'mark'))
                else:
                    for PyJsTemp in var.get(u'schema').get(u'marks'):
                        var.put(u'prop', PyJsTemp)
                        var.put(u'mark$1', var.get(u'schema').get(u'marks').get(var.get(u'prop')))
                        if ((var.get(u'name')==Js(u'_')) or (var.get(u'mark$1').get(u'spec').get(u'group') and (var.get(u'mark$1').get(u'spec').get(u'group').callprop(u'split', Js(u' ')).callprop(u'indexOf', var.get(u'name'))>(-Js(1.0))))):
                            var.get(u'found').callprop(u'push', var.put(u'ok', var.get(u'mark$1')))
                if var.get(u'ok').neg():
                    PyJsTempException = JsToPyException(var.get(u'SyntaxError').create(((Js(u"Unknown mark type: '")+var.get(u'marks').get(var.get(u'i')))+Js(u"'"))))
                    raise PyJsTempException
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return var.get(u'found')
    PyJsHoisted_gatherMarks_.func_name = u'gatherMarks'
    var.put(u'gatherMarks', PyJsHoisted_gatherMarks_)
    @Js
    def PyJsHoisted_initAttrs_(attrs, this, arguments, var=var):
        var = Scope({u'this':this, u'attrs':attrs, u'arguments':arguments}, var)
        var.registers([u'attrs', u'result', u'name'])
        var.put(u'result', var.get(u'Object').callprop(u'create', var.get(u"null")))
        if var.get(u'attrs'):
            for PyJsTemp in var.get(u'attrs'):
                var.put(u'name', PyJsTemp)
                var.get(u'result').put(var.get(u'name'), var.get(u'Attribute').create(var.get(u'attrs').get(var.get(u'name'))))
        return var.get(u'result')
    PyJsHoisted_initAttrs_.func_name = u'initAttrs'
    var.put(u'initAttrs', PyJsHoisted_initAttrs_)
    @Js
    def PyJsHoisted_parseExprSubscript_(stream, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'stream':stream}, var)
        var.registers([u'expr', u'stream'])
        var.put(u'expr', var.get(u'parseExprAtom')(var.get(u'stream')))
        #for JS loop
        
        while 1:
            if var.get(u'stream').callprop(u'eat', Js(u'+')):
                PyJs_Object_227_ = Js({u'type':Js(u'plus'),u'expr':var.get(u'expr')})
                var.put(u'expr', PyJs_Object_227_)
            else:
                if var.get(u'stream').callprop(u'eat', Js(u'*')):
                    PyJs_Object_228_ = Js({u'type':Js(u'star'),u'expr':var.get(u'expr')})
                    var.put(u'expr', PyJs_Object_228_)
                else:
                    if var.get(u'stream').callprop(u'eat', Js(u'?')):
                        PyJs_Object_229_ = Js({u'type':Js(u'opt'),u'expr':var.get(u'expr')})
                        var.put(u'expr', PyJs_Object_229_)
                    else:
                        if var.get(u'stream').callprop(u'eat', Js(u'{')):
                            var.put(u'expr', var.get(u'parseExprRange')(var.get(u'stream'), var.get(u'expr')))
                        else:
                            break
        
        return var.get(u'expr')
    PyJsHoisted_parseExprSubscript_.func_name = u'parseExprSubscript'
    var.put(u'parseExprSubscript', PyJsHoisted_parseExprSubscript_)
    @Js
    def PyJsHoisted_findDiffStart_(a, b, pos, this, arguments, var=var):
        var = Scope({u'a':a, u'this':this, u'b':b, u'pos':pos, u'arguments':arguments}, var)
        var.registers([u'a', u'b', u'i', u'j', u'pos', u'childA', u'childB', u'inner'])
        #for JS loop
        var.put(u'i', Js(0.0))
        while 1:
            try:
                if ((var.get(u'i')==var.get(u'a').get(u'childCount')) or (var.get(u'i')==var.get(u'b').get(u'childCount'))):
                    return (var.get(u"null") if (var.get(u'a').get(u'childCount')==var.get(u'b').get(u'childCount')) else var.get(u'pos'))
                var.put(u'childA', var.get(u'a').callprop(u'child', var.get(u'i')))
                var.put(u'childB', var.get(u'b').callprop(u'child', var.get(u'i')))
                if (var.get(u'childA')==var.get(u'childB')):
                    var.put(u'pos', var.get(u'childA').get(u'nodeSize'), u'+')
                    continue
                if var.get(u'childA').callprop(u'sameMarkup', var.get(u'childB')).neg():
                    return var.get(u'pos')
                if (var.get(u'childA').get(u'isText') and (var.get(u'childA').get(u'text')!=var.get(u'childB').get(u'text'))):
                    #for JS loop
                    var.put(u'j', Js(0.0))
                    while (var.get(u'childA').get(u'text').get(var.get(u'j'))==var.get(u'childB').get(u'text').get(var.get(u'j'))):
                        try:
                            (var.put(u'pos',Js(var.get(u'pos').to_number())+Js(1))-Js(1))
                        finally:
                                (var.put(u'j',Js(var.get(u'j').to_number())+Js(1))-Js(1))
                    return var.get(u'pos')
                if (var.get(u'childA').get(u'content').get(u'size') or var.get(u'childB').get(u'content').get(u'size')):
                    var.put(u'inner', var.get(u'findDiffStart')(var.get(u'childA').get(u'content'), var.get(u'childB').get(u'content'), (var.get(u'pos')+Js(1.0))))
                    if (var.get(u'inner')!=var.get(u"null")):
                        return var.get(u'inner')
                var.put(u'pos', var.get(u'childA').get(u'nodeSize'), u'+')
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
    PyJsHoisted_findDiffStart_.func_name = u'findDiffStart'
    var.put(u'findDiffStart', PyJsHoisted_findDiffStart_)
    @Js
    def PyJsHoisted_ReplaceError_(message, this, arguments, var=var):
        var = Scope({u'this':this, u'message':message, u'arguments':arguments}, var)
        var.registers([u'message', u'err'])
        var.put(u'err', var.get(u'Error').callprop(u'call', var.get(u"this"), var.get(u'message')))
        var.get(u'err').put(u'__proto__', var.get(u'ReplaceError').get(u'prototype'))
        return var.get(u'err')
    PyJsHoisted_ReplaceError_.func_name = u'ReplaceError'
    var.put(u'ReplaceError', PyJsHoisted_ReplaceError_)
    @Js
    def PyJsHoisted_prepareSliceForReplace_(slice, PyJsArg_24616c6f6e67_, this, arguments, var=var):
        var = Scope({u'this':this, u'slice':slice, u'$along':PyJsArg_24616c6f6e67_, u'arguments':arguments}, var)
        var.registers([u'node', u'slice', u'parent', u'extra', u'i', u'$along'])
        var.put(u'extra', (var.get(u'$along').get(u'depth')-var.get(u'slice').get(u'openStart')))
        var.put(u'parent', var.get(u'$along').callprop(u'node', var.get(u'extra')))
        var.put(u'node', var.get(u'parent').callprop(u'copy', var.get(u'slice').get(u'content')))
        #for JS loop
        var.put(u'i', (var.get(u'extra')-Js(1.0)))
        while (var.get(u'i')>=Js(0.0)):
            try:
                var.put(u'node', var.get(u'$along').callprop(u'node', var.get(u'i')).callprop(u'copy', var.get(u'Fragment').callprop(u'from', var.get(u'node'))))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())-Js(1))+Js(1))
        PyJs_Object_78_ = Js({u'start':var.get(u'node').callprop(u'resolveNoCache', (var.get(u'slice').get(u'openStart')+var.get(u'extra'))),u'end':var.get(u'node').callprop(u'resolveNoCache', ((var.get(u'node').get(u'content').get(u'size')-var.get(u'slice').get(u'openEnd'))-var.get(u'extra')))})
        return PyJs_Object_78_
    PyJsHoisted_prepareSliceForReplace_.func_name = u'prepareSliceForReplace'
    var.put(u'prepareSliceForReplace', PyJsHoisted_prepareSliceForReplace_)
    @Js
    def PyJsHoisted_computeAttrs_(attrs, value, this, arguments, var=var):
        var = Scope({u'this':this, u'attrs':attrs, u'value':value, u'arguments':arguments}, var)
        var.registers([u'given', u'attr', u'value', u'name', u'attrs', u'built'])
        var.put(u'built', var.get(u'Object').callprop(u'create', var.get(u"null")))
        for PyJsTemp in var.get(u'attrs'):
            var.put(u'name', PyJsTemp)
            var.put(u'given', (var.get(u'value') and var.get(u'value').get(var.get(u'name'))))
            if PyJsStrictEq(var.get(u'given'),var.get(u'undefined')):
                var.put(u'attr', var.get(u'attrs').get(var.get(u'name')))
                if var.get(u'attr').get(u'hasDefault'):
                    var.put(u'given', var.get(u'attr').get(u'default'))
                else:
                    PyJsTempException = JsToPyException(var.get(u'RangeError').create((Js(u'No value supplied for attribute ')+var.get(u'name'))))
                    raise PyJsTempException
            var.get(u'built').put(var.get(u'name'), var.get(u'given'))
        return var.get(u'built')
    PyJsHoisted_computeAttrs_.func_name = u'computeAttrs'
    var.put(u'computeAttrs', PyJsHoisted_computeAttrs_)
    @Js
    def PyJsHoisted_normalizeList_(dom, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'dom':dom}, var)
        var.registers([u'prevItem', u'dom', u'name', u'child'])
        #for JS loop
        var.put(u'child', var.get(u'dom').get(u'firstChild'))
        var.put(u'prevItem', var.get(u"null"))
        while var.get(u'child'):
            try:
                var.put(u'name', (var.get(u'child').get(u'nodeName').callprop(u'toLowerCase') if (var.get(u'child').get(u'nodeType')==Js(1.0)) else var.get(u"null")))
                if ((var.get(u'name') and var.get(u'listTags').callprop(u'hasOwnProperty', var.get(u'name'))) and var.get(u'prevItem')):
                    var.get(u'prevItem').callprop(u'appendChild', var.get(u'child'))
                    var.put(u'child', var.get(u'prevItem'))
                else:
                    if (var.get(u'name')==Js(u'li')):
                        var.put(u'prevItem', var.get(u'child'))
                    else:
                        if var.get(u'name'):
                            var.put(u'prevItem', var.get(u"null"))
            finally:
                    var.put(u'child', var.get(u'child').get(u'nextSibling'))
    PyJsHoisted_normalizeList_.func_name = u'normalizeList'
    var.put(u'normalizeList', PyJsHoisted_normalizeList_)
    @Js
    def PyJsHoisted_cmp_(a, b, this, arguments, var=var):
        var = Scope({u'a':a, u'this':this, u'b':b, u'arguments':arguments}, var)
        var.registers([u'a', u'b'])
        return (var.get(u'a')-var.get(u'b'))
    PyJsHoisted_cmp_.func_name = u'cmp'
    var.put(u'cmp', PyJsHoisted_cmp_)
    PyJs_Object_18_ = Js({u'value':Js(True)})
    var.get(u'Object').callprop(u'defineProperty', var.get(u'exports'), Js(u'__esModule'), PyJs_Object_18_)
    pass
    var.put(u'OrderedMap', var.get(u'_interopDefault')(var.get(u'orderedmap')))
    pass
    pass
    @Js
    def PyJs_Fragment_22_(content, size, this, arguments, var=var):
        var = Scope({u'content':content, u'this':this, u'Fragment':PyJs_Fragment_22_, u'arguments':arguments, u'size':size}, var)
        var.registers([u'i', u'content', u'size', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        var.get(u"this").put(u'content', var.get(u'content'))
        var.get(u"this").put(u'size', (var.get(u'size') or Js(0.0)))
        if (var.get(u'size')==var.get(u"null")):
            #for JS loop
            var.put(u'i', Js(0.0))
            while (var.get(u'i')<var.get(u'content').get(u'length')):
                try:
                    var.get(u'this$1').put(u'size', var.get(u'content').get(var.get(u'i')).get(u'nodeSize'), u'+')
                finally:
                        (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
    PyJs_Fragment_22_._set_name(u'Fragment')
    var.put(u'Fragment', PyJs_Fragment_22_)
    PyJs_Object_24_ = Js({})
    PyJs_Object_25_ = Js({})
    PyJs_Object_26_ = Js({})
    PyJs_Object_23_ = Js({u'firstChild':PyJs_Object_24_,u'lastChild':PyJs_Object_25_,u'childCount':PyJs_Object_26_})
    var.put(u'prototypeAccessors$1', PyJs_Object_23_)
    @Js
    def PyJs_nodesBetween_27_(PyJsArg_66726f6d_, to, f, nodeStart, parent, this, arguments, var=var):
        var = Scope({u'to':to, u'from':PyJsArg_66726f6d_, u'arguments':arguments, u'parent':parent, u'f':f, u'this':this, u'nodeStart':nodeStart, u'nodesBetween':PyJs_nodesBetween_27_}, var)
        var.registers([u'f', u'end', u'parent', u'to', u'i', u'nodeStart', u'this$1', u'pos', u'start', u'child', u'from'])
        var.put(u'this$1', var.get(u"this"))
        if PyJsStrictEq(var.get(u'nodeStart'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'nodeStart', Js(0.0))
        #for JS loop
        var.put(u'i', Js(0.0))
        var.put(u'pos', Js(0.0))
        while (var.get(u'pos')<var.get(u'to')):
            try:
                var.put(u'child', var.get(u'this$1').get(u'content').get(var.get(u'i')))
                var.put(u'end', (var.get(u'pos')+var.get(u'child').get(u'nodeSize')))
                if (((var.get(u'end')>var.get(u'from')) and PyJsStrictNeq(var.get(u'f')(var.get(u'child'), (var.get(u'nodeStart')+var.get(u'pos')), var.get(u'parent'), var.get(u'i')),Js(False))) and var.get(u'child').get(u'content').get(u'size')):
                    var.put(u'start', (var.get(u'pos')+Js(1.0)))
                    var.get(u'child').callprop(u'nodesBetween', var.get(u'Math').callprop(u'max', Js(0.0), (var.get(u'from')-var.get(u'start'))), var.get(u'Math').callprop(u'min', var.get(u'child').get(u'content').get(u'size'), (var.get(u'to')-var.get(u'start'))), var.get(u'f'), (var.get(u'nodeStart')+var.get(u'start')))
                var.put(u'pos', var.get(u'end'))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
    PyJs_nodesBetween_27_._set_name(u'nodesBetween')
    var.get(u'Fragment').get(u'prototype').put(u'nodesBetween', PyJs_nodesBetween_27_)
    @Js
    def PyJs_descendants_28_(f, this, arguments, var=var):
        var = Scope({u'this':this, u'descendants':PyJs_descendants_28_, u'arguments':arguments, u'f':f}, var)
        var.registers([u'f'])
        var.get(u"this").callprop(u'nodesBetween', Js(0.0), var.get(u"this").get(u'size'), var.get(u'f'))
    PyJs_descendants_28_._set_name(u'descendants')
    var.get(u'Fragment').get(u'prototype').put(u'descendants', PyJs_descendants_28_)
    @Js
    def PyJs_textBetween_29_(PyJsArg_66726f6d_, to, blockSeparator, leafText, this, arguments, var=var):
        var = Scope({u'to':to, u'from':PyJsArg_66726f6d_, u'leafText':leafText, u'blockSeparator':blockSeparator, u'this':this, u'textBetween':PyJs_textBetween_29_, u'arguments':arguments}, var)
        var.registers([u'separated', u'from', u'leafText', u'blockSeparator', u'text', u'to'])
        var.put(u'text', Js(u''))
        var.put(u'separated', Js(True))
        @Js
        def PyJs_anonymous_30_(node, pos, this, arguments, var=var):
            var = Scope({u'node':node, u'this':this, u'pos':pos, u'arguments':arguments}, var)
            var.registers([u'node', u'pos'])
            if var.get(u'node').get(u'isText'):
                var.put(u'text', var.get(u'node').get(u'text').callprop(u'slice', (var.get(u'Math').callprop(u'max', var.get(u'from'), var.get(u'pos'))-var.get(u'pos')), (var.get(u'to')-var.get(u'pos'))), u'+')
                var.put(u'separated', var.get(u'blockSeparator').neg())
            else:
                if (var.get(u'node').get(u'isLeaf') and var.get(u'leafText')):
                    var.put(u'text', var.get(u'leafText'), u'+')
                    var.put(u'separated', var.get(u'blockSeparator').neg())
                else:
                    if (var.get(u'separated').neg() and var.get(u'node').get(u'isBlock')):
                        var.put(u'text', var.get(u'blockSeparator'), u'+')
                        var.put(u'separated', Js(True))
        PyJs_anonymous_30_._set_name(u'anonymous')
        var.get(u"this").callprop(u'nodesBetween', var.get(u'from'), var.get(u'to'), PyJs_anonymous_30_, Js(0.0))
        return var.get(u'text')
    PyJs_textBetween_29_._set_name(u'textBetween')
    var.get(u'Fragment').get(u'prototype').put(u'textBetween', PyJs_textBetween_29_)
    @Js
    def PyJs_append_31_(other, this, arguments, var=var):
        var = Scope({u'this':this, u'other':other, u'arguments':arguments, u'append':PyJs_append_31_}, var)
        var.registers([u'content', u'i', u'other', u'last', u'first'])
        if var.get(u'other').get(u'size').neg():
            return var.get(u"this")
        if var.get(u"this").get(u'size').neg():
            return var.get(u'other')
        var.put(u'last', var.get(u"this").get(u'lastChild'))
        var.put(u'first', var.get(u'other').get(u'firstChild'))
        var.put(u'content', var.get(u"this").get(u'content').callprop(u'slice'))
        var.put(u'i', Js(0.0))
        if (var.get(u'last').get(u'isText') and var.get(u'last').callprop(u'sameMarkup', var.get(u'first'))):
            var.get(u'content').put((var.get(u'content').get(u'length')-Js(1.0)), var.get(u'last').callprop(u'withText', (var.get(u'last').get(u'text')+var.get(u'first').get(u'text'))))
            var.put(u'i', Js(1.0))
        #for JS loop
        
        while (var.get(u'i')<var.get(u'other').get(u'content').get(u'length')):
            try:
                var.get(u'content').callprop(u'push', var.get(u'other').get(u'content').get(var.get(u'i')))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return var.get(u'Fragment').create(var.get(u'content'), (var.get(u"this").get(u'size')+var.get(u'other').get(u'size')))
    PyJs_append_31_._set_name(u'append')
    var.get(u'Fragment').get(u'prototype').put(u'append', PyJs_append_31_)
    @Js
    def PyJs_cut_32_(PyJsArg_66726f6d_, to, this, arguments, var=var):
        var = Scope({u'this':this, u'to':to, u'cut':PyJs_cut_32_, u'from':PyJsArg_66726f6d_, u'arguments':arguments}, var)
        var.registers([u'end', u'i', u'this$1', u'pos', u'to', u'result', u'child', u'from', u'size'])
        var.put(u'this$1', var.get(u"this"))
        if (var.get(u'to')==var.get(u"null")):
            var.put(u'to', var.get(u"this").get(u'size'))
        if ((var.get(u'from')==Js(0.0)) and (var.get(u'to')==var.get(u"this").get(u'size'))):
            return var.get(u"this")
        var.put(u'result', Js([]))
        var.put(u'size', Js(0.0))
        if (var.get(u'to')>var.get(u'from')):
            #for JS loop
            var.put(u'i', Js(0.0))
            var.put(u'pos', Js(0.0))
            while (var.get(u'pos')<var.get(u'to')):
                try:
                    var.put(u'child', var.get(u'this$1').get(u'content').get(var.get(u'i')))
                    var.put(u'end', (var.get(u'pos')+var.get(u'child').get(u'nodeSize')))
                    if (var.get(u'end')>var.get(u'from')):
                        if ((var.get(u'pos')<var.get(u'from')) or (var.get(u'end')>var.get(u'to'))):
                            if var.get(u'child').get(u'isText'):
                                var.put(u'child', var.get(u'child').callprop(u'cut', var.get(u'Math').callprop(u'max', Js(0.0), (var.get(u'from')-var.get(u'pos'))), var.get(u'Math').callprop(u'min', var.get(u'child').get(u'text').get(u'length'), (var.get(u'to')-var.get(u'pos')))))
                            else:
                                var.put(u'child', var.get(u'child').callprop(u'cut', var.get(u'Math').callprop(u'max', Js(0.0), ((var.get(u'from')-var.get(u'pos'))-Js(1.0))), var.get(u'Math').callprop(u'min', var.get(u'child').get(u'content').get(u'size'), ((var.get(u'to')-var.get(u'pos'))-Js(1.0)))))
                        var.get(u'result').callprop(u'push', var.get(u'child'))
                        var.put(u'size', var.get(u'child').get(u'nodeSize'), u'+')
                    var.put(u'pos', var.get(u'end'))
                finally:
                        (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return var.get(u'Fragment').create(var.get(u'result'), var.get(u'size'))
    PyJs_cut_32_._set_name(u'cut')
    var.get(u'Fragment').get(u'prototype').put(u'cut', PyJs_cut_32_)
    @Js
    def PyJs_cutByIndex_33_(PyJsArg_66726f6d_, to, this, arguments, var=var):
        var = Scope({u'this':this, u'to':to, u'cutByIndex':PyJs_cutByIndex_33_, u'from':PyJsArg_66726f6d_, u'arguments':arguments}, var)
        var.registers([u'to', u'from'])
        if (var.get(u'from')==var.get(u'to')):
            return var.get(u'Fragment').get(u'empty')
        if ((var.get(u'from')==Js(0.0)) and (var.get(u'to')==var.get(u"this").get(u'content').get(u'length'))):
            return var.get(u"this")
        return var.get(u'Fragment').create(var.get(u"this").get(u'content').callprop(u'slice', var.get(u'from'), var.get(u'to')))
    PyJs_cutByIndex_33_._set_name(u'cutByIndex')
    var.get(u'Fragment').get(u'prototype').put(u'cutByIndex', PyJs_cutByIndex_33_)
    @Js
    def PyJs_replaceChild_34_(index, node, this, arguments, var=var):
        var = Scope({u'node':node, u'index':index, u'this':this, u'arguments':arguments, u'replaceChild':PyJs_replaceChild_34_}, var)
        var.registers([u'current', u'index', u'copy', u'node', u'size'])
        var.put(u'current', var.get(u"this").get(u'content').get(var.get(u'index')))
        if (var.get(u'current')==var.get(u'node')):
            return var.get(u"this")
        var.put(u'copy', var.get(u"this").get(u'content').callprop(u'slice'))
        var.put(u'size', ((var.get(u"this").get(u'size')+var.get(u'node').get(u'nodeSize'))-var.get(u'current').get(u'nodeSize')))
        var.get(u'copy').put(var.get(u'index'), var.get(u'node'))
        return var.get(u'Fragment').create(var.get(u'copy'), var.get(u'size'))
    PyJs_replaceChild_34_._set_name(u'replaceChild')
    var.get(u'Fragment').get(u'prototype').put(u'replaceChild', PyJs_replaceChild_34_)
    @Js
    def PyJs_addToStart_35_(node, this, arguments, var=var):
        var = Scope({u'node':node, u'this':this, u'arguments':arguments, u'addToStart':PyJs_addToStart_35_}, var)
        var.registers([u'node'])
        return var.get(u'Fragment').create(Js([var.get(u'node')]).callprop(u'concat', var.get(u"this").get(u'content')), (var.get(u"this").get(u'size')+var.get(u'node').get(u'nodeSize')))
    PyJs_addToStart_35_._set_name(u'addToStart')
    var.get(u'Fragment').get(u'prototype').put(u'addToStart', PyJs_addToStart_35_)
    @Js
    def PyJs_addToEnd_36_(node, this, arguments, var=var):
        var = Scope({u'node':node, u'this':this, u'arguments':arguments, u'addToEnd':PyJs_addToEnd_36_}, var)
        var.registers([u'node'])
        return var.get(u'Fragment').create(var.get(u"this").get(u'content').callprop(u'concat', var.get(u'node')), (var.get(u"this").get(u'size')+var.get(u'node').get(u'nodeSize')))
    PyJs_addToEnd_36_._set_name(u'addToEnd')
    var.get(u'Fragment').get(u'prototype').put(u'addToEnd', PyJs_addToEnd_36_)
    @Js
    def PyJs_eq_37_(other, this, arguments, var=var):
        var = Scope({u'this':this, u'other':other, u'eq':PyJs_eq_37_, u'arguments':arguments}, var)
        var.registers([u'i', u'other', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        if (var.get(u"this").get(u'content').get(u'length')!=var.get(u'other').get(u'content').get(u'length')):
            return Js(False)
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u"this").get(u'content').get(u'length')):
            try:
                if var.get(u'this$1').get(u'content').get(var.get(u'i')).callprop(u'eq', var.get(u'other').get(u'content').get(var.get(u'i'))).neg():
                    return Js(False)
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return Js(True)
    PyJs_eq_37_._set_name(u'eq')
    var.get(u'Fragment').get(u'prototype').put(u'eq', PyJs_eq_37_)
    @Js
    def PyJs_anonymous_38_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return (var.get(u"this").get(u'content').get(u'0') if var.get(u"this").get(u'content').get(u'length') else var.get(u"null"))
    PyJs_anonymous_38_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$1').get(u'firstChild').put(u'get', PyJs_anonymous_38_)
    @Js
    def PyJs_anonymous_39_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return (var.get(u"this").get(u'content').get((var.get(u"this").get(u'content').get(u'length')-Js(1.0))) if var.get(u"this").get(u'content').get(u'length') else var.get(u"null"))
    PyJs_anonymous_39_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$1').get(u'lastChild').put(u'get', PyJs_anonymous_39_)
    @Js
    def PyJs_anonymous_40_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get(u'content').get(u'length')
    PyJs_anonymous_40_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$1').get(u'childCount').put(u'get', PyJs_anonymous_40_)
    @Js
    def PyJs_child_41_(index, this, arguments, var=var):
        var = Scope({u'this':this, u'index':index, u'arguments':arguments, u'child':PyJs_child_41_}, var)
        var.registers([u'found', u'index'])
        var.put(u'found', var.get(u"this").get(u'content').get(var.get(u'index')))
        if var.get(u'found').neg():
            PyJsTempException = JsToPyException(var.get(u'RangeError').create((((Js(u'Index ')+var.get(u'index'))+Js(u' out of range for '))+var.get(u"this"))))
            raise PyJsTempException
        return var.get(u'found')
    PyJs_child_41_._set_name(u'child')
    var.get(u'Fragment').get(u'prototype').put(u'child', PyJs_child_41_)
    @Js
    def PyJs_maybeChild_42_(index, this, arguments, var=var):
        var = Scope({u'this':this, u'index':index, u'maybeChild':PyJs_maybeChild_42_, u'arguments':arguments}, var)
        var.registers([u'index'])
        return var.get(u"this").get(u'content').get(var.get(u'index'))
    PyJs_maybeChild_42_._set_name(u'maybeChild')
    var.get(u'Fragment').get(u'prototype').put(u'maybeChild', PyJs_maybeChild_42_)
    @Js
    def PyJs_forEach_43_(f, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'forEach':PyJs_forEach_43_, u'f':f}, var)
        var.registers([u'i', u'p', u'child', u'f', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        #for JS loop
        var.put(u'i', Js(0.0))
        var.put(u'p', Js(0.0))
        while (var.get(u'i')<var.get(u"this").get(u'content').get(u'length')):
            try:
                var.put(u'child', var.get(u'this$1').get(u'content').get(var.get(u'i')))
                var.get(u'f')(var.get(u'child'), var.get(u'p'), var.get(u'i'))
                var.put(u'p', var.get(u'child').get(u'nodeSize'), u'+')
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
    PyJs_forEach_43_._set_name(u'forEach')
    var.get(u'Fragment').get(u'prototype').put(u'forEach', PyJs_forEach_43_)
    @Js
    def PyJs_InlineNonPyName_44_(other, pos, this, arguments, var=var):
        var = Scope({u'this':this, u'other':other, u'pos':pos, u'findDiffStart$1':PyJs_InlineNonPyName_44_, u'arguments':arguments}, var)
        var.registers([u'other', u'pos'])
        if PyJsStrictEq(var.get(u'pos'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'pos', Js(0.0))
        return var.get(u'findDiffStart')(var.get(u"this"), var.get(u'other'), var.get(u'pos'))
    PyJs_InlineNonPyName_44_._set_name(u'findDiffStart$1')
    var.get(u'Fragment').get(u'prototype').put(u'findDiffStart', PyJs_InlineNonPyName_44_)
    @Js
    def PyJs_InlineNonPyName_45_(other, pos, otherPos, this, arguments, var=var):
        var = Scope({u'this':this, u'pos':pos, u'otherPos':otherPos, u'other':other, u'arguments':arguments, u'findDiffEnd$1':PyJs_InlineNonPyName_45_}, var)
        var.registers([u'otherPos', u'other', u'pos'])
        if PyJsStrictEq(var.get(u'pos'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'pos', var.get(u"this").get(u'size'))
        if PyJsStrictEq(var.get(u'otherPos'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'otherPos', var.get(u'other').get(u'size'))
        return var.get(u'findDiffEnd')(var.get(u"this"), var.get(u'other'), var.get(u'pos'), var.get(u'otherPos'))
    PyJs_InlineNonPyName_45_._set_name(u'findDiffEnd$1')
    var.get(u'Fragment').get(u'prototype').put(u'findDiffEnd', PyJs_InlineNonPyName_45_)
    @Js
    def PyJs_findIndex_46_(pos, round, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'findIndex':PyJs_findIndex_46_, u'pos':pos, u'round':round}, var)
        var.registers([u'end', u'cur', u'i', u'pos', u'curPos', u'this$1', u'round'])
        var.put(u'this$1', var.get(u"this"))
        if PyJsStrictEq(var.get(u'round'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'round', (-Js(1.0)))
        if (var.get(u'pos')==Js(0.0)):
            return var.get(u'retIndex')(Js(0.0), var.get(u'pos'))
        if (var.get(u'pos')==var.get(u"this").get(u'size')):
            return var.get(u'retIndex')(var.get(u"this").get(u'content').get(u'length'), var.get(u'pos'))
        if ((var.get(u'pos')>var.get(u"this").get(u'size')) or (var.get(u'pos')<Js(0.0))):
            PyJsTempException = JsToPyException(var.get(u'RangeError').create(((((Js(u'Position ')+var.get(u'pos'))+Js(u' outside of fragment ('))+var.get(u"this"))+Js(u')'))))
            raise PyJsTempException
        #for JS loop
        var.put(u'i', Js(0.0))
        var.put(u'curPos', Js(0.0))
        while 1:
            try:
                var.put(u'cur', var.get(u'this$1').callprop(u'child', var.get(u'i')))
                var.put(u'end', (var.get(u'curPos')+var.get(u'cur').get(u'nodeSize')))
                if (var.get(u'end')>=var.get(u'pos')):
                    if ((var.get(u'end')==var.get(u'pos')) or (var.get(u'round')>Js(0.0))):
                        return var.get(u'retIndex')((var.get(u'i')+Js(1.0)), var.get(u'end'))
                    return var.get(u'retIndex')(var.get(u'i'), var.get(u'curPos'))
                var.put(u'curPos', var.get(u'end'))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
    PyJs_findIndex_46_._set_name(u'findIndex')
    var.get(u'Fragment').get(u'prototype').put(u'findIndex', PyJs_findIndex_46_)
    @Js
    def PyJs_toString_47_(this, arguments, var=var):
        var = Scope({u'this':this, u'toString':PyJs_toString_47_, u'arguments':arguments}, var)
        var.registers([])
        return ((Js(u'<')+var.get(u"this").callprop(u'toStringInner'))+Js(u'>'))
    PyJs_toString_47_._set_name(u'toString')
    var.get(u'Fragment').get(u'prototype').put(u'toString', PyJs_toString_47_)
    @Js
    def PyJs_toStringInner_48_(this, arguments, var=var):
        var = Scope({u'this':this, u'toStringInner':PyJs_toStringInner_48_, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get(u'content').callprop(u'join', Js(u', '))
    PyJs_toStringInner_48_._set_name(u'toStringInner')
    var.get(u'Fragment').get(u'prototype').put(u'toStringInner', PyJs_toStringInner_48_)
    @Js
    def PyJs_toJSON_49_(this, arguments, var=var):
        var = Scope({u'this':this, u'toJSON':PyJs_toJSON_49_, u'arguments':arguments}, var)
        var.registers([])
        @Js
        def PyJs_anonymous_50_(n, this, arguments, var=var):
            var = Scope({u'this':this, u'arguments':arguments, u'n':n}, var)
            var.registers([u'n'])
            return var.get(u'n').callprop(u'toJSON')
        PyJs_anonymous_50_._set_name(u'anonymous')
        return (var.get(u"this").get(u'content').callprop(u'map', PyJs_anonymous_50_) if var.get(u"this").get(u'content').get(u'length') else var.get(u"null"))
    PyJs_toJSON_49_._set_name(u'toJSON')
    var.get(u'Fragment').get(u'prototype').put(u'toJSON', PyJs_toJSON_49_)
    @Js
    def PyJs_fromJSON_51_(schema, value, this, arguments, var=var):
        var = Scope({u'this':this, u'fromJSON':PyJs_fromJSON_51_, u'arguments':arguments, u'value':value, u'schema':schema}, var)
        var.registers([u'value', u'schema'])
        if var.get(u'value').neg():
            return var.get(u'Fragment').get(u'empty')
        if var.get(u'Array').callprop(u'isArray', var.get(u'value')).neg():
            PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'Invalid input for Fragment.fromJSON')))
            raise PyJsTempException
        return var.get(u'Fragment').create(var.get(u'value').callprop(u'map', var.get(u'schema').get(u'nodeFromJSON')))
    PyJs_fromJSON_51_._set_name(u'fromJSON')
    var.get(u'Fragment').put(u'fromJSON', PyJs_fromJSON_51_)
    @Js
    def PyJs_fromArray_52_(array, this, arguments, var=var):
        var = Scope({u'this':this, u'array':array, u'arguments':arguments, u'fromArray':PyJs_fromArray_52_}, var)
        var.registers([u'i', u'node', u'array', u'joined', u'size'])
        if var.get(u'array').get(u'length').neg():
            return var.get(u'Fragment').get(u'empty')
        var.put(u'size', Js(0.0))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u'array').get(u'length')):
            try:
                var.put(u'node', var.get(u'array').get(var.get(u'i')))
                var.put(u'size', var.get(u'node').get(u'nodeSize'), u'+')
                if ((var.get(u'i') and var.get(u'node').get(u'isText')) and var.get(u'array').get((var.get(u'i')-Js(1.0))).callprop(u'sameMarkup', var.get(u'node'))):
                    if var.get(u'joined').neg():
                        var.put(u'joined', var.get(u'array').callprop(u'slice', Js(0.0), var.get(u'i')))
                    var.get(u'joined').put((var.get(u'joined').get(u'length')-Js(1.0)), var.get(u'node').callprop(u'withText', (var.get(u'joined').get((var.get(u'joined').get(u'length')-Js(1.0))).get(u'text')+var.get(u'node').get(u'text'))))
                else:
                    if var.get(u'joined'):
                        var.get(u'joined').callprop(u'push', var.get(u'node'))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return var.get(u'Fragment').create((var.get(u'joined') or var.get(u'array')), var.get(u'size'))
    PyJs_fromArray_52_._set_name(u'fromArray')
    var.get(u'Fragment').put(u'fromArray', PyJs_fromArray_52_)
    @Js
    def PyJs_InlineNonPyName_53_(nodes, this, arguments, var=var):
        var = Scope({u'this':this, u'nodes':nodes, u'from':PyJs_InlineNonPyName_53_, u'arguments':arguments}, var)
        var.registers([u'nodes'])
        if var.get(u'nodes').neg():
            return var.get(u'Fragment').get(u'empty')
        if var.get(u'nodes').instanceof(var.get(u'Fragment')):
            return var.get(u'nodes')
        if var.get(u'Array').callprop(u'isArray', var.get(u'nodes')):
            return var.get(u"this").callprop(u'fromArray', var.get(u'nodes'))
        return var.get(u'Fragment').create(Js([var.get(u'nodes')]), var.get(u'nodes').get(u'nodeSize'))
    PyJs_InlineNonPyName_53_._set_name(u'from')
    var.get(u'Fragment').put(u'from', PyJs_InlineNonPyName_53_)
    var.get(u'Object').callprop(u'defineProperties', var.get(u'Fragment').get(u'prototype'), var.get(u'prototypeAccessors$1'))
    PyJs_Object_54_ = Js({u'index':Js(0.0),u'offset':Js(0.0)})
    var.put(u'found', PyJs_Object_54_)
    pass
    var.get(u'Fragment').put(u'empty', var.get(u'Fragment').create(Js([]), Js(0.0)))
    pass
    @Js
    def PyJs_Mark_55_(type, attrs, this, arguments, var=var):
        var = Scope({u'this':this, u'Mark':PyJs_Mark_55_, u'type':type, u'attrs':attrs, u'arguments':arguments}, var)
        var.registers([u'type', u'attrs'])
        var.get(u"this").put(u'type', var.get(u'type'))
        var.get(u"this").put(u'attrs', var.get(u'attrs'))
    PyJs_Mark_55_._set_name(u'Mark')
    var.put(u'Mark', PyJs_Mark_55_)
    @Js
    def PyJs_addToSet_56_(set, this, arguments, var=var):
        var = Scope({u'this':this, u'addToSet':PyJs_addToSet_56_, u'set':set, u'arguments':arguments}, var)
        var.registers([u'set', u'i', u'placed', u'other', u'this$1', u'copy'])
        var.put(u'this$1', var.get(u"this"))
        var.put(u'placed', Js(False))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u'set').get(u'length')):
            try:
                var.put(u'other', var.get(u'set').get(var.get(u'i')))
                if var.get(u'this$1').callprop(u'eq', var.get(u'other')):
                    return var.get(u'set')
                if var.get(u'this$1').get(u'type').callprop(u'excludes', var.get(u'other').get(u'type')):
                    if var.get(u'copy').neg():
                        var.put(u'copy', var.get(u'set').callprop(u'slice', Js(0.0), var.get(u'i')))
                else:
                    if var.get(u'other').get(u'type').callprop(u'excludes', var.get(u'this$1').get(u'type')):
                        return var.get(u'set')
                    else:
                        if (var.get(u'placed').neg() and (var.get(u'other').get(u'type').get(u'rank')>var.get(u'this$1').get(u'type').get(u'rank'))):
                            if var.get(u'copy').neg():
                                var.put(u'copy', var.get(u'set').callprop(u'slice', Js(0.0), var.get(u'i')))
                            var.get(u'copy').callprop(u'push', var.get(u'this$1'))
                            var.put(u'placed', Js(True))
                        if var.get(u'copy'):
                            var.get(u'copy').callprop(u'push', var.get(u'other'))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        if var.get(u'copy').neg():
            var.put(u'copy', var.get(u'set').callprop(u'slice'))
        if var.get(u'placed').neg():
            var.get(u'copy').callprop(u'push', var.get(u"this"))
        return var.get(u'copy')
    PyJs_addToSet_56_._set_name(u'addToSet')
    var.get(u'Mark').get(u'prototype').put(u'addToSet', PyJs_addToSet_56_)
    @Js
    def PyJs_removeFromSet_57_(set, this, arguments, var=var):
        var = Scope({u'this':this, u'set':set, u'arguments':arguments, u'removeFromSet':PyJs_removeFromSet_57_}, var)
        var.registers([u'i', u'set', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u'set').get(u'length')):
            try:
                if var.get(u'this$1').callprop(u'eq', var.get(u'set').get(var.get(u'i'))):
                    return var.get(u'set').callprop(u'slice', Js(0.0), var.get(u'i')).callprop(u'concat', var.get(u'set').callprop(u'slice', (var.get(u'i')+Js(1.0))))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return var.get(u'set')
    PyJs_removeFromSet_57_._set_name(u'removeFromSet')
    var.get(u'Mark').get(u'prototype').put(u'removeFromSet', PyJs_removeFromSet_57_)
    @Js
    def PyJs_isInSet_58_(set, this, arguments, var=var):
        var = Scope({u'this':this, u'isInSet':PyJs_isInSet_58_, u'set':set, u'arguments':arguments}, var)
        var.registers([u'i', u'set', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u'set').get(u'length')):
            try:
                if var.get(u'this$1').callprop(u'eq', var.get(u'set').get(var.get(u'i'))):
                    return Js(True)
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return Js(False)
    PyJs_isInSet_58_._set_name(u'isInSet')
    var.get(u'Mark').get(u'prototype').put(u'isInSet', PyJs_isInSet_58_)
    @Js
    def PyJs_eq_59_(other, this, arguments, var=var):
        var = Scope({u'this':this, u'other':other, u'eq':PyJs_eq_59_, u'arguments':arguments}, var)
        var.registers([u'other'])
        return ((var.get(u"this")==var.get(u'other')) or ((var.get(u"this").get(u'type')==var.get(u'other').get(u'type')) and var.get(u'compareDeep')(var.get(u"this").get(u'attrs'), var.get(u'other').get(u'attrs'))))
    PyJs_eq_59_._set_name(u'eq')
    var.get(u'Mark').get(u'prototype').put(u'eq', PyJs_eq_59_)
    @Js
    def PyJs_toJSON_60_(this, arguments, var=var):
        var = Scope({u'this':this, u'toJSON':PyJs_toJSON_60_, u'arguments':arguments}, var)
        var.registers([u'obj', u'_', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        PyJs_Object_61_ = Js({u'type':var.get(u"this").get(u'type').get(u'name')})
        var.put(u'obj', PyJs_Object_61_)
        for PyJsTemp in var.get(u'this$1').get(u'attrs'):
            var.put(u'_', PyJsTemp)
            var.get(u'obj').put(u'attrs', var.get(u'this$1').get(u'attrs'))
            break
        return var.get(u'obj')
    PyJs_toJSON_60_._set_name(u'toJSON')
    var.get(u'Mark').get(u'prototype').put(u'toJSON', PyJs_toJSON_60_)
    @Js
    def PyJs_fromJSON_62_(schema, json, this, arguments, var=var):
        var = Scope({u'this':this, u'json':json, u'arguments':arguments, u'fromJSON':PyJs_fromJSON_62_, u'schema':schema}, var)
        var.registers([u'json', u'type', u'schema'])
        if var.get(u'json').neg():
            PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'Invalid input for Mark.fromJSON')))
            raise PyJsTempException
        var.put(u'type', var.get(u'schema').get(u'marks').get(var.get(u'json').get(u'type')))
        if var.get(u'type').neg():
            PyJsTempException = JsToPyException(var.get(u'RangeError').create(((Js(u'There is no mark type ')+var.get(u'json').get(u'type'))+Js(u' in this schema'))))
            raise PyJsTempException
        return var.get(u'type').callprop(u'create', var.get(u'json').get(u'attrs'))
    PyJs_fromJSON_62_._set_name(u'fromJSON')
    var.get(u'Mark').put(u'fromJSON', PyJs_fromJSON_62_)
    @Js
    def PyJs_sameSet_63_(a, b, this, arguments, var=var):
        var = Scope({u'a':a, u'this':this, u'b':b, u'arguments':arguments, u'sameSet':PyJs_sameSet_63_}, var)
        var.registers([u'i', u'a', u'b'])
        if (var.get(u'a')==var.get(u'b')):
            return Js(True)
        if (var.get(u'a').get(u'length')!=var.get(u'b').get(u'length')):
            return Js(False)
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u'a').get(u'length')):
            try:
                if var.get(u'a').get(var.get(u'i')).callprop(u'eq', var.get(u'b').get(var.get(u'i'))).neg():
                    return Js(False)
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return Js(True)
    PyJs_sameSet_63_._set_name(u'sameSet')
    var.get(u'Mark').put(u'sameSet', PyJs_sameSet_63_)
    @Js
    def PyJs_setFrom_64_(marks, this, arguments, var=var):
        var = Scope({u'this':this, u'setFrom':PyJs_setFrom_64_, u'arguments':arguments, u'marks':marks}, var)
        var.registers([u'copy', u'marks'])
        if (var.get(u'marks').neg() or (var.get(u'marks').get(u'length')==Js(0.0))):
            return var.get(u'Mark').get(u'none')
        if var.get(u'marks').instanceof(var.get(u'Mark')):
            return Js([var.get(u'marks')])
        var.put(u'copy', var.get(u'marks').callprop(u'slice'))
        @Js
        def PyJs_anonymous_65_(a, b, this, arguments, var=var):
            var = Scope({u'a':a, u'this':this, u'b':b, u'arguments':arguments}, var)
            var.registers([u'a', u'b'])
            return (var.get(u'a').get(u'type').get(u'rank')-var.get(u'b').get(u'type').get(u'rank'))
        PyJs_anonymous_65_._set_name(u'anonymous')
        var.get(u'copy').callprop(u'sort', PyJs_anonymous_65_)
        return var.get(u'copy')
    PyJs_setFrom_64_._set_name(u'setFrom')
    var.get(u'Mark').put(u'setFrom', PyJs_setFrom_64_)
    var.get(u'Mark').put(u'none', Js([]))
    pass
    var.get(u'ReplaceError').put(u'prototype', var.get(u'Object').callprop(u'create', var.get(u'Error').get(u'prototype')))
    var.get(u'ReplaceError').get(u'prototype').put(u'constructor', var.get(u'ReplaceError'))
    var.get(u'ReplaceError').get(u'prototype').put(u'name', Js(u'ReplaceError'))
    @Js
    def PyJs_Slice_66_(content, openStart, openEnd, this, arguments, var=var):
        var = Scope({u'Slice':PyJs_Slice_66_, u'this':this, u'content':content, u'openStart':openStart, u'openEnd':openEnd, u'arguments':arguments}, var)
        var.registers([u'content', u'openEnd', u'openStart'])
        var.get(u"this").put(u'content', var.get(u'content'))
        var.get(u"this").put(u'openStart', var.get(u'openStart'))
        var.get(u"this").put(u'openEnd', var.get(u'openEnd'))
    PyJs_Slice_66_._set_name(u'Slice')
    var.put(u'Slice', PyJs_Slice_66_)
    PyJs_Object_68_ = Js({})
    PyJs_Object_67_ = Js({u'size':PyJs_Object_68_})
    var.put(u'prototypeAccessors$2', PyJs_Object_67_)
    @Js
    def PyJs_anonymous_69_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return ((var.get(u"this").get(u'content').get(u'size')-var.get(u"this").get(u'openStart'))-var.get(u"this").get(u'openEnd'))
    PyJs_anonymous_69_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$2').get(u'size').put(u'get', PyJs_anonymous_69_)
    @Js
    def PyJs_insertAt_70_(pos, fragment, this, arguments, var=var):
        var = Scope({u'fragment':fragment, u'this':this, u'insertAt':PyJs_insertAt_70_, u'pos':pos, u'arguments':arguments}, var)
        var.registers([u'content', u'fragment', u'pos'])
        var.put(u'content', var.get(u'insertInto')(var.get(u"this").get(u'content'), (var.get(u'pos')+var.get(u"this").get(u'openStart')), var.get(u'fragment'), var.get(u"null")))
        return (var.get(u'content') and var.get(u'Slice').create(var.get(u'content'), var.get(u"this").get(u'openStart'), var.get(u"this").get(u'openEnd')))
    PyJs_insertAt_70_._set_name(u'insertAt')
    var.get(u'Slice').get(u'prototype').put(u'insertAt', PyJs_insertAt_70_)
    @Js
    def PyJs_removeBetween_71_(PyJsArg_66726f6d_, to, this, arguments, var=var):
        var = Scope({u'this':this, u'to':to, u'from':PyJsArg_66726f6d_, u'arguments':arguments, u'removeBetween':PyJs_removeBetween_71_}, var)
        var.registers([u'to', u'from'])
        return var.get(u'Slice').create(var.get(u'removeRange')(var.get(u"this").get(u'content'), (var.get(u'from')+var.get(u"this").get(u'openStart')), (var.get(u'to')+var.get(u"this").get(u'openStart'))), var.get(u"this").get(u'openStart'), var.get(u"this").get(u'openEnd'))
    PyJs_removeBetween_71_._set_name(u'removeBetween')
    var.get(u'Slice').get(u'prototype').put(u'removeBetween', PyJs_removeBetween_71_)
    @Js
    def PyJs_eq_72_(other, this, arguments, var=var):
        var = Scope({u'this':this, u'other':other, u'eq':PyJs_eq_72_, u'arguments':arguments}, var)
        var.registers([u'other'])
        return ((var.get(u"this").get(u'content').callprop(u'eq', var.get(u'other').get(u'content')) and (var.get(u"this").get(u'openStart')==var.get(u'other').get(u'openStart'))) and (var.get(u"this").get(u'openEnd')==var.get(u'other').get(u'openEnd')))
    PyJs_eq_72_._set_name(u'eq')
    var.get(u'Slice').get(u'prototype').put(u'eq', PyJs_eq_72_)
    @Js
    def PyJs_toString_73_(this, arguments, var=var):
        var = Scope({u'this':this, u'toString':PyJs_toString_73_, u'arguments':arguments}, var)
        var.registers([])
        return (((((var.get(u"this").get(u'content')+Js(u'('))+var.get(u"this").get(u'openStart'))+Js(u','))+var.get(u"this").get(u'openEnd'))+Js(u')'))
    PyJs_toString_73_._set_name(u'toString')
    var.get(u'Slice').get(u'prototype').put(u'toString', PyJs_toString_73_)
    @Js
    def PyJs_toJSON_74_(this, arguments, var=var):
        var = Scope({u'this':this, u'toJSON':PyJs_toJSON_74_, u'arguments':arguments}, var)
        var.registers([u'json'])
        if var.get(u"this").get(u'content').get(u'size').neg():
            return var.get(u"null")
        PyJs_Object_75_ = Js({u'content':var.get(u"this").get(u'content').callprop(u'toJSON')})
        var.put(u'json', PyJs_Object_75_)
        if (var.get(u"this").get(u'openStart')>Js(0.0)):
            var.get(u'json').put(u'openStart', var.get(u"this").get(u'openStart'))
        if (var.get(u"this").get(u'openEnd')>Js(0.0)):
            var.get(u'json').put(u'openEnd', var.get(u"this").get(u'openEnd'))
        return var.get(u'json')
    PyJs_toJSON_74_._set_name(u'toJSON')
    var.get(u'Slice').get(u'prototype').put(u'toJSON', PyJs_toJSON_74_)
    @Js
    def PyJs_fromJSON_76_(schema, json, this, arguments, var=var):
        var = Scope({u'this':this, u'json':json, u'arguments':arguments, u'fromJSON':PyJs_fromJSON_76_, u'schema':schema}, var)
        var.registers([u'openEnd', u'json', u'openStart', u'schema'])
        if var.get(u'json').neg():
            return var.get(u'Slice').get(u'empty')
        var.put(u'openStart', (var.get(u'json').get(u'openStart') or Js(0.0)))
        var.put(u'openEnd', (var.get(u'json').get(u'openEnd') or Js(0.0)))
        if ((var.get(u'openStart',throw=False).typeof()!=Js(u'number')) or (var.get(u'openEnd',throw=False).typeof()!=Js(u'number'))):
            PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'Invalid input for Slice.fromJSON')))
            raise PyJsTempException
        return var.get(u'Slice').create(var.get(u'Fragment').callprop(u'fromJSON', var.get(u'schema'), var.get(u'json').get(u'content')), (var.get(u'json').get(u'openStart') or Js(0.0)), (var.get(u'json').get(u'openEnd') or Js(0.0)))
    PyJs_fromJSON_76_._set_name(u'fromJSON')
    var.get(u'Slice').put(u'fromJSON', PyJs_fromJSON_76_)
    @Js
    def PyJs_maxOpen_77_(fragment, openIsolating, this, arguments, var=var):
        var = Scope({u'fragment':fragment, u'this':this, u'openIsolating':openIsolating, u'arguments':arguments, u'maxOpen':PyJs_maxOpen_77_}, var)
        var.registers([u'openIsolating', u'fragment', u'n', u'n$1', u'openStart', u'openEnd'])
        if PyJsStrictEq(var.get(u'openIsolating'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'openIsolating', Js(True))
        var.put(u'openStart', Js(0.0))
        var.put(u'openEnd', Js(0.0))
        #for JS loop
        var.put(u'n', var.get(u'fragment').get(u'firstChild'))
        while ((var.get(u'n') and var.get(u'n').get(u'isLeaf').neg()) and (var.get(u'openIsolating') or var.get(u'n').get(u'type').get(u'spec').get(u'isolating').neg())):
            try:
                (var.put(u'openStart',Js(var.get(u'openStart').to_number())+Js(1))-Js(1))
            finally:
                    var.put(u'n', var.get(u'n').get(u'firstChild'))
        #for JS loop
        var.put(u'n$1', var.get(u'fragment').get(u'lastChild'))
        while ((var.get(u'n$1') and var.get(u'n$1').get(u'isLeaf').neg()) and (var.get(u'openIsolating') or var.get(u'n$1').get(u'type').get(u'spec').get(u'isolating').neg())):
            try:
                (var.put(u'openEnd',Js(var.get(u'openEnd').to_number())+Js(1))-Js(1))
            finally:
                    var.put(u'n$1', var.get(u'n$1').get(u'lastChild'))
        return var.get(u'Slice').create(var.get(u'fragment'), var.get(u'openStart'), var.get(u'openEnd'))
    PyJs_maxOpen_77_._set_name(u'maxOpen')
    var.get(u'Slice').put(u'maxOpen', PyJs_maxOpen_77_)
    var.get(u'Object').callprop(u'defineProperties', var.get(u'Slice').get(u'prototype'), var.get(u'prototypeAccessors$2'))
    pass
    pass
    var.get(u'Slice').put(u'empty', var.get(u'Slice').create(var.get(u'Fragment').get(u'empty'), Js(0.0), Js(0.0)))
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    @Js
    def PyJs_ResolvedPos_79_(pos, path, parentOffset, this, arguments, var=var):
        var = Scope({u'this':this, u'pos':pos, u'parentOffset':parentOffset, u'arguments':arguments, u'path':path, u'ResolvedPos':PyJs_ResolvedPos_79_}, var)
        var.registers([u'path', u'pos', u'parentOffset'])
        var.get(u"this").put(u'pos', var.get(u'pos'))
        var.get(u"this").put(u'path', var.get(u'path'))
        var.get(u"this").put(u'depth', ((var.get(u'path').get(u'length')/Js(3.0))-Js(1.0)))
        var.get(u"this").put(u'parentOffset', var.get(u'parentOffset'))
    PyJs_ResolvedPos_79_._set_name(u'ResolvedPos')
    var.put(u'ResolvedPos', PyJs_ResolvedPos_79_)
    PyJs_Object_81_ = Js({})
    PyJs_Object_82_ = Js({})
    PyJs_Object_83_ = Js({})
    PyJs_Object_84_ = Js({})
    PyJs_Object_85_ = Js({})
    PyJs_Object_80_ = Js({u'parent':PyJs_Object_81_,u'doc':PyJs_Object_82_,u'textOffset':PyJs_Object_83_,u'nodeAfter':PyJs_Object_84_,u'nodeBefore':PyJs_Object_85_})
    var.put(u'prototypeAccessors$3', PyJs_Object_80_)
    @Js
    def PyJs_resolveDepth_86_(val, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'val':val, u'resolveDepth':PyJs_resolveDepth_86_}, var)
        var.registers([u'val'])
        if (var.get(u'val')==var.get(u"null")):
            return var.get(u"this").get(u'depth')
        if (var.get(u'val')<Js(0.0)):
            return (var.get(u"this").get(u'depth')+var.get(u'val'))
        return var.get(u'val')
    PyJs_resolveDepth_86_._set_name(u'resolveDepth')
    var.get(u'ResolvedPos').get(u'prototype').put(u'resolveDepth', PyJs_resolveDepth_86_)
    @Js
    def PyJs_anonymous_87_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").callprop(u'node', var.get(u"this").get(u'depth'))
    PyJs_anonymous_87_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$3').get(u'parent').put(u'get', PyJs_anonymous_87_)
    @Js
    def PyJs_anonymous_88_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").callprop(u'node', Js(0.0))
    PyJs_anonymous_88_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$3').get(u'doc').put(u'get', PyJs_anonymous_88_)
    @Js
    def PyJs_node_89_(depth, this, arguments, var=var):
        var = Scope({u'this':this, u'node':PyJs_node_89_, u'depth':depth, u'arguments':arguments}, var)
        var.registers([u'depth'])
        return var.get(u"this").get(u'path').get((var.get(u"this").callprop(u'resolveDepth', var.get(u'depth'))*Js(3.0)))
    PyJs_node_89_._set_name(u'node')
    var.get(u'ResolvedPos').get(u'prototype').put(u'node', PyJs_node_89_)
    @Js
    def PyJs_index_90_(depth, this, arguments, var=var):
        var = Scope({u'this':this, u'index':PyJs_index_90_, u'depth':depth, u'arguments':arguments}, var)
        var.registers([u'depth'])
        return var.get(u"this").get(u'path').get(((var.get(u"this").callprop(u'resolveDepth', var.get(u'depth'))*Js(3.0))+Js(1.0)))
    PyJs_index_90_._set_name(u'index')
    var.get(u'ResolvedPos').get(u'prototype').put(u'index', PyJs_index_90_)
    @Js
    def PyJs_indexAfter_91_(depth, this, arguments, var=var):
        var = Scope({u'this':this, u'indexAfter':PyJs_indexAfter_91_, u'depth':depth, u'arguments':arguments}, var)
        var.registers([u'depth'])
        var.put(u'depth', var.get(u"this").callprop(u'resolveDepth', var.get(u'depth')))
        return (var.get(u"this").callprop(u'index', var.get(u'depth'))+(Js(0.0) if ((var.get(u'depth')==var.get(u"this").get(u'depth')) and var.get(u"this").get(u'textOffset').neg()) else Js(1.0)))
    PyJs_indexAfter_91_._set_name(u'indexAfter')
    var.get(u'ResolvedPos').get(u'prototype').put(u'indexAfter', PyJs_indexAfter_91_)
    @Js
    def PyJs_start_92_(depth, this, arguments, var=var):
        var = Scope({u'this':this, u'start':PyJs_start_92_, u'depth':depth, u'arguments':arguments}, var)
        var.registers([u'depth'])
        var.put(u'depth', var.get(u"this").callprop(u'resolveDepth', var.get(u'depth')))
        return (Js(0.0) if (var.get(u'depth')==Js(0.0)) else (var.get(u"this").get(u'path').get(((var.get(u'depth')*Js(3.0))-Js(1.0)))+Js(1.0)))
    PyJs_start_92_._set_name(u'start')
    var.get(u'ResolvedPos').get(u'prototype').put(u'start', PyJs_start_92_)
    @Js
    def PyJs_end_93_(depth, this, arguments, var=var):
        var = Scope({u'this':this, u'depth':depth, u'end':PyJs_end_93_, u'arguments':arguments}, var)
        var.registers([u'depth'])
        var.put(u'depth', var.get(u"this").callprop(u'resolveDepth', var.get(u'depth')))
        return (var.get(u"this").callprop(u'start', var.get(u'depth'))+var.get(u"this").callprop(u'node', var.get(u'depth')).get(u'content').get(u'size'))
    PyJs_end_93_._set_name(u'end')
    var.get(u'ResolvedPos').get(u'prototype').put(u'end', PyJs_end_93_)
    @Js
    def PyJs_before_94_(depth, this, arguments, var=var):
        var = Scope({u'this':this, u'depth':depth, u'arguments':arguments, u'before':PyJs_before_94_}, var)
        var.registers([u'depth'])
        var.put(u'depth', var.get(u"this").callprop(u'resolveDepth', var.get(u'depth')))
        if var.get(u'depth').neg():
            PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'There is no position before the top-level node')))
            raise PyJsTempException
        return (var.get(u"this").get(u'pos') if (var.get(u'depth')==(var.get(u"this").get(u'depth')+Js(1.0))) else var.get(u"this").get(u'path').get(((var.get(u'depth')*Js(3.0))-Js(1.0))))
    PyJs_before_94_._set_name(u'before')
    var.get(u'ResolvedPos').get(u'prototype').put(u'before', PyJs_before_94_)
    @Js
    def PyJs_after_95_(depth, this, arguments, var=var):
        var = Scope({u'this':this, u'depth':depth, u'after':PyJs_after_95_, u'arguments':arguments}, var)
        var.registers([u'depth'])
        var.put(u'depth', var.get(u"this").callprop(u'resolveDepth', var.get(u'depth')))
        if var.get(u'depth').neg():
            PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'There is no position after the top-level node')))
            raise PyJsTempException
        return (var.get(u"this").get(u'pos') if (var.get(u'depth')==(var.get(u"this").get(u'depth')+Js(1.0))) else (var.get(u"this").get(u'path').get(((var.get(u'depth')*Js(3.0))-Js(1.0)))+var.get(u"this").get(u'path').get((var.get(u'depth')*Js(3.0))).get(u'nodeSize')))
    PyJs_after_95_._set_name(u'after')
    var.get(u'ResolvedPos').get(u'prototype').put(u'after', PyJs_after_95_)
    @Js
    def PyJs_anonymous_96_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return (var.get(u"this").get(u'pos')-var.get(u"this").get(u'path').get((var.get(u"this").get(u'path').get(u'length')-Js(1.0))))
    PyJs_anonymous_96_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$3').get(u'textOffset').put(u'get', PyJs_anonymous_96_)
    @Js
    def PyJs_anonymous_97_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([u'index', u'child', u'parent', u'dOff'])
        var.put(u'parent', var.get(u"this").get(u'parent'))
        var.put(u'index', var.get(u"this").callprop(u'index', var.get(u"this").get(u'depth')))
        if (var.get(u'index')==var.get(u'parent').get(u'childCount')):
            return var.get(u"null")
        var.put(u'dOff', (var.get(u"this").get(u'pos')-var.get(u"this").get(u'path').get((var.get(u"this").get(u'path').get(u'length')-Js(1.0)))))
        var.put(u'child', var.get(u'parent').callprop(u'child', var.get(u'index')))
        return (var.get(u'parent').callprop(u'child', var.get(u'index')).callprop(u'cut', var.get(u'dOff')) if var.get(u'dOff') else var.get(u'child'))
    PyJs_anonymous_97_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$3').get(u'nodeAfter').put(u'get', PyJs_anonymous_97_)
    @Js
    def PyJs_anonymous_98_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([u'index', u'dOff'])
        var.put(u'index', var.get(u"this").callprop(u'index', var.get(u"this").get(u'depth')))
        var.put(u'dOff', (var.get(u"this").get(u'pos')-var.get(u"this").get(u'path').get((var.get(u"this").get(u'path').get(u'length')-Js(1.0)))))
        if var.get(u'dOff'):
            return var.get(u"this").get(u'parent').callprop(u'child', var.get(u'index')).callprop(u'cut', Js(0.0), var.get(u'dOff'))
        return (var.get(u"null") if (var.get(u'index')==Js(0.0)) else var.get(u"this").get(u'parent').callprop(u'child', (var.get(u'index')-Js(1.0))))
    PyJs_anonymous_98_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$3').get(u'nodeBefore').put(u'get', PyJs_anonymous_98_)
    @Js
    def PyJs_marks_99_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'marks':PyJs_marks_99_}, var)
        var.registers([u'tmp', u'index', u'parent', u'i', u'other', u'marks', u'main'])
        var.put(u'parent', var.get(u"this").get(u'parent'))
        var.put(u'index', var.get(u"this").callprop(u'index'))
        if (var.get(u'parent').get(u'content').get(u'size')==Js(0.0)):
            return var.get(u'Mark').get(u'none')
        if var.get(u"this").get(u'textOffset'):
            return var.get(u'parent').callprop(u'child', var.get(u'index')).get(u'marks')
        var.put(u'main', var.get(u'parent').callprop(u'maybeChild', (var.get(u'index')-Js(1.0))))
        var.put(u'other', var.get(u'parent').callprop(u'maybeChild', var.get(u'index')))
        if var.get(u'main').neg():
            var.put(u'tmp', var.get(u'main'))
            var.put(u'main', var.get(u'other'))
            var.put(u'other', var.get(u'tmp'))
        var.put(u'marks', var.get(u'main').get(u'marks'))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u'marks').get(u'length')):
            try:
                if (PyJsStrictEq(var.get(u'marks').get(var.get(u'i')).get(u'type').get(u'spec').get(u'inclusive'),Js(False)) and (var.get(u'other').neg() or var.get(u'marks').get(var.get(u'i')).callprop(u'isInSet', var.get(u'other').get(u'marks')).neg())):
                    var.put(u'marks', var.get(u'marks').get((var.put(u'i',Js(var.get(u'i').to_number())-Js(1))+Js(1))).callprop(u'removeFromSet', var.get(u'marks')))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return var.get(u'marks')
    PyJs_marks_99_._set_name(u'marks')
    var.get(u'ResolvedPos').get(u'prototype').put(u'marks', PyJs_marks_99_)
    @Js
    def PyJs_marksAcross_100_(PyJsArg_24656e64_, this, arguments, var=var):
        var = Scope({u'this':this, u'marksAcross':PyJs_marksAcross_100_, u'arguments':arguments, u'$end':PyJsArg_24656e64_}, var)
        var.registers([u'i', u'next', u'after', u'$end', u'marks'])
        var.put(u'after', var.get(u"this").get(u'parent').callprop(u'maybeChild', var.get(u"this").callprop(u'index')))
        if (var.get(u'after').neg() or var.get(u'after').get(u'isInline').neg()):
            return var.get(u"null")
        var.put(u'marks', var.get(u'after').get(u'marks'))
        var.put(u'next', var.get(u'$end').get(u'parent').callprop(u'maybeChild', var.get(u'$end').callprop(u'index')))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u'marks').get(u'length')):
            try:
                if (PyJsStrictEq(var.get(u'marks').get(var.get(u'i')).get(u'type').get(u'spec').get(u'inclusive'),Js(False)) and (var.get(u'next').neg() or var.get(u'marks').get(var.get(u'i')).callprop(u'isInSet', var.get(u'next').get(u'marks')).neg())):
                    var.put(u'marks', var.get(u'marks').get((var.put(u'i',Js(var.get(u'i').to_number())-Js(1))+Js(1))).callprop(u'removeFromSet', var.get(u'marks')))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return var.get(u'marks')
    PyJs_marksAcross_100_._set_name(u'marksAcross')
    var.get(u'ResolvedPos').get(u'prototype').put(u'marksAcross', PyJs_marksAcross_100_)
    @Js
    def PyJs_sharedDepth_101_(pos, this, arguments, var=var):
        var = Scope({u'this':this, u'sharedDepth':PyJs_sharedDepth_101_, u'pos':pos, u'arguments':arguments}, var)
        var.registers([u'depth', u'pos', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        #for JS loop
        var.put(u'depth', var.get(u"this").get(u'depth'))
        while (var.get(u'depth')>Js(0.0)):
            try:
                if ((var.get(u'this$1').callprop(u'start', var.get(u'depth'))<=var.get(u'pos')) and (var.get(u'this$1').callprop(u'end', var.get(u'depth'))>=var.get(u'pos'))):
                    return var.get(u'depth')
            finally:
                    (var.put(u'depth',Js(var.get(u'depth').to_number())-Js(1))+Js(1))
        return Js(0.0)
    PyJs_sharedDepth_101_._set_name(u'sharedDepth')
    var.get(u'ResolvedPos').get(u'prototype').put(u'sharedDepth', PyJs_sharedDepth_101_)
    @Js
    def PyJs_blockRange_102_(other, pred, this, arguments, var=var):
        var = Scope({u'this':this, u'pred':pred, u'other':other, u'blockRange':PyJs_blockRange_102_, u'arguments':arguments}, var)
        var.registers([u'pred', u'other', u'd', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        if PyJsStrictEq(var.get(u'other'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'other', var.get(u"this"))
        if (var.get(u'other').get(u'pos')<var.get(u"this").get(u'pos')):
            return var.get(u'other').callprop(u'blockRange', var.get(u"this"))
        #for JS loop
        var.put(u'd', (var.get(u"this").get(u'depth')-(Js(1.0) if (var.get(u"this").get(u'parent').get(u'inlineContent') or (var.get(u"this").get(u'pos')==var.get(u'other').get(u'pos'))) else Js(0.0))))
        while (var.get(u'd')>=Js(0.0)):
            try:
                if ((var.get(u'other').get(u'pos')<=var.get(u'this$1').callprop(u'end', var.get(u'd'))) and (var.get(u'pred').neg() or var.get(u'pred')(var.get(u'this$1').callprop(u'node', var.get(u'd'))))):
                    return var.get(u'NodeRange').create(var.get(u'this$1'), var.get(u'other'), var.get(u'd'))
            finally:
                    (var.put(u'd',Js(var.get(u'd').to_number())-Js(1))+Js(1))
    PyJs_blockRange_102_._set_name(u'blockRange')
    var.get(u'ResolvedPos').get(u'prototype').put(u'blockRange', PyJs_blockRange_102_)
    @Js
    def PyJs_sameParent_103_(other, this, arguments, var=var):
        var = Scope({u'this':this, u'sameParent':PyJs_sameParent_103_, u'other':other, u'arguments':arguments}, var)
        var.registers([u'other'])
        return ((var.get(u"this").get(u'pos')-var.get(u"this").get(u'parentOffset'))==(var.get(u'other').get(u'pos')-var.get(u'other').get(u'parentOffset')))
    PyJs_sameParent_103_._set_name(u'sameParent')
    var.get(u'ResolvedPos').get(u'prototype').put(u'sameParent', PyJs_sameParent_103_)
    @Js
    def PyJs_max_104_(other, this, arguments, var=var):
        var = Scope({u'this':this, u'max':PyJs_max_104_, u'other':other, u'arguments':arguments}, var)
        var.registers([u'other'])
        return (var.get(u'other') if (var.get(u'other').get(u'pos')>var.get(u"this").get(u'pos')) else var.get(u"this"))
    PyJs_max_104_._set_name(u'max')
    var.get(u'ResolvedPos').get(u'prototype').put(u'max', PyJs_max_104_)
    @Js
    def PyJs_min_105_(other, this, arguments, var=var):
        var = Scope({u'this':this, u'other':other, u'arguments':arguments, u'min':PyJs_min_105_}, var)
        var.registers([u'other'])
        return (var.get(u'other') if (var.get(u'other').get(u'pos')<var.get(u"this").get(u'pos')) else var.get(u"this"))
    PyJs_min_105_._set_name(u'min')
    var.get(u'ResolvedPos').get(u'prototype').put(u'min', PyJs_min_105_)
    @Js
    def PyJs_toString_106_(this, arguments, var=var):
        var = Scope({u'this':this, u'toString':PyJs_toString_106_, u'arguments':arguments}, var)
        var.registers([u'i', u'str', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        var.put(u'str', Js(u''))
        #for JS loop
        var.put(u'i', Js(1.0))
        while (var.get(u'i')<=var.get(u"this").get(u'depth')):
            try:
                var.put(u'str', ((((Js(u'/') if var.get(u'str') else Js(u''))+var.get(u'this$1').callprop(u'node', var.get(u'i')).get(u'type').get(u'name'))+Js(u'_'))+var.get(u'this$1').callprop(u'index', (var.get(u'i')-Js(1.0)))), u'+')
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return ((var.get(u'str')+Js(u':'))+var.get(u"this").get(u'parentOffset'))
    PyJs_toString_106_._set_name(u'toString')
    var.get(u'ResolvedPos').get(u'prototype').put(u'toString', PyJs_toString_106_)
    @Js
    def PyJs_resolve_107_(doc, pos, this, arguments, var=var):
        var = Scope({u'this':this, u'doc':doc, u'resolve':PyJs_resolve_107_, u'pos':pos, u'arguments':arguments}, var)
        var.registers([u'node', u'index', u'doc', u'rem', u'pos', u'start', u'offset', u'path', u'ref', u'parentOffset'])
        if ((var.get(u'pos')>=Js(0.0)) and (var.get(u'pos')<=var.get(u'doc').get(u'content').get(u'size'))).neg():
            PyJsTempException = JsToPyException(var.get(u'RangeError').create(((Js(u'Position ')+var.get(u'pos'))+Js(u' out of range'))))
            raise PyJsTempException
        var.put(u'path', Js([]))
        var.put(u'start', Js(0.0))
        var.put(u'parentOffset', var.get(u'pos'))
        #for JS loop
        var.put(u'node', var.get(u'doc'))
        while 1:
            var.put(u'ref', var.get(u'node').get(u'content').callprop(u'findIndex', var.get(u'parentOffset')))
            var.put(u'index', var.get(u'ref').get(u'index'))
            var.put(u'offset', var.get(u'ref').get(u'offset'))
            var.put(u'rem', (var.get(u'parentOffset')-var.get(u'offset')))
            var.get(u'path').callprop(u'push', var.get(u'node'), var.get(u'index'), (var.get(u'start')+var.get(u'offset')))
            if var.get(u'rem').neg():
                break
            var.put(u'node', var.get(u'node').callprop(u'child', var.get(u'index')))
            if var.get(u'node').get(u'isText'):
                break
            var.put(u'parentOffset', (var.get(u'rem')-Js(1.0)))
            var.put(u'start', (var.get(u'offset')+Js(1.0)), u'+')
        
        return var.get(u'ResolvedPos').create(var.get(u'pos'), var.get(u'path'), var.get(u'parentOffset'))
    PyJs_resolve_107_._set_name(u'resolve')
    var.get(u'ResolvedPos').put(u'resolve', PyJs_resolve_107_)
    @Js
    def PyJs_resolveCached_108_(doc, pos, this, arguments, var=var):
        var = Scope({u'this':this, u'doc':doc, u'resolveCached':PyJs_resolveCached_108_, u'pos':pos, u'arguments':arguments}, var)
        var.registers([u'i', u'cached', u'pos', u'result', u'doc'])
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u'resolveCache').get(u'length')):
            try:
                var.put(u'cached', var.get(u'resolveCache').get(var.get(u'i')))
                if ((var.get(u'cached').get(u'pos')==var.get(u'pos')) and (var.get(u'cached').get(u'doc')==var.get(u'doc'))):
                    return var.get(u'cached')
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        var.put(u'result', var.get(u'resolveCache').put(var.get(u'resolveCachePos'), var.get(u'ResolvedPos').callprop(u'resolve', var.get(u'doc'), var.get(u'pos'))))
        var.put(u'resolveCachePos', ((var.get(u'resolveCachePos')+Js(1.0))%var.get(u'resolveCacheSize')))
        return var.get(u'result')
    PyJs_resolveCached_108_._set_name(u'resolveCached')
    var.get(u'ResolvedPos').put(u'resolveCached', PyJs_resolveCached_108_)
    var.get(u'Object').callprop(u'defineProperties', var.get(u'ResolvedPos').get(u'prototype'), var.get(u'prototypeAccessors$3'))
    var.put(u'resolveCache', Js([]))
    var.put(u'resolveCachePos', Js(0.0))
    var.put(u'resolveCacheSize', Js(12.0))
    @Js
    def PyJs_NodeRange_109_(PyJsArg_2466726f6d_, PyJsArg_24746f_, depth, this, arguments, var=var):
        var = Scope({u'NodeRange':PyJs_NodeRange_109_, u'$to':PyJsArg_24746f_, u'this':this, u'$from':PyJsArg_2466726f6d_, u'depth':depth, u'arguments':arguments}, var)
        var.registers([u'$from', u'depth', u'$to'])
        var.get(u"this").put(u'$from', var.get(u'$from'))
        var.get(u"this").put(u'$to', var.get(u'$to'))
        var.get(u"this").put(u'depth', var.get(u'depth'))
    PyJs_NodeRange_109_._set_name(u'NodeRange')
    var.put(u'NodeRange', PyJs_NodeRange_109_)
    PyJs_Object_111_ = Js({})
    PyJs_Object_112_ = Js({})
    PyJs_Object_113_ = Js({})
    PyJs_Object_114_ = Js({})
    PyJs_Object_115_ = Js({})
    PyJs_Object_110_ = Js({u'start':PyJs_Object_111_,u'end':PyJs_Object_112_,u'parent':PyJs_Object_113_,u'startIndex':PyJs_Object_114_,u'endIndex':PyJs_Object_115_})
    var.put(u'prototypeAccessors$1$1', PyJs_Object_110_)
    @Js
    def PyJs_anonymous_116_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get(u'$from').callprop(u'before', (var.get(u"this").get(u'depth')+Js(1.0)))
    PyJs_anonymous_116_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$1$1').get(u'start').put(u'get', PyJs_anonymous_116_)
    @Js
    def PyJs_anonymous_117_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get(u'$to').callprop(u'after', (var.get(u"this").get(u'depth')+Js(1.0)))
    PyJs_anonymous_117_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$1$1').get(u'end').put(u'get', PyJs_anonymous_117_)
    @Js
    def PyJs_anonymous_118_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get(u'$from').callprop(u'node', var.get(u"this").get(u'depth'))
    PyJs_anonymous_118_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$1$1').get(u'parent').put(u'get', PyJs_anonymous_118_)
    @Js
    def PyJs_anonymous_119_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get(u'$from').callprop(u'index', var.get(u"this").get(u'depth'))
    PyJs_anonymous_119_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$1$1').get(u'startIndex').put(u'get', PyJs_anonymous_119_)
    @Js
    def PyJs_anonymous_120_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get(u'$to').callprop(u'indexAfter', var.get(u"this").get(u'depth'))
    PyJs_anonymous_120_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$1$1').get(u'endIndex').put(u'get', PyJs_anonymous_120_)
    var.get(u'Object').callprop(u'defineProperties', var.get(u'NodeRange').get(u'prototype'), var.get(u'prototypeAccessors$1$1'))
    var.put(u'emptyAttrs', var.get(u'Object').callprop(u'create', var.get(u"null")))
    @Js
    def PyJs_Node_121_(type, attrs, content, marks, this, arguments, var=var):
        var = Scope({u'content':content, u'Node':PyJs_Node_121_, u'attrs':attrs, u'marks':marks, u'this':this, u'type':type, u'arguments':arguments}, var)
        var.registers([u'content', u'type', u'attrs', u'marks'])
        var.get(u"this").put(u'type', var.get(u'type'))
        var.get(u"this").put(u'attrs', var.get(u'attrs'))
        var.get(u"this").put(u'content', (var.get(u'content') or var.get(u'Fragment').get(u'empty')))
        var.get(u"this").put(u'marks', (var.get(u'marks') or var.get(u'Mark').get(u'none')))
    PyJs_Node_121_._set_name(u'Node')
    var.put(u'Node', PyJs_Node_121_)
    PyJs_Object_123_ = Js({})
    PyJs_Object_124_ = Js({})
    PyJs_Object_125_ = Js({})
    PyJs_Object_126_ = Js({})
    PyJs_Object_127_ = Js({})
    PyJs_Object_128_ = Js({})
    PyJs_Object_129_ = Js({})
    PyJs_Object_130_ = Js({})
    PyJs_Object_131_ = Js({})
    PyJs_Object_132_ = Js({})
    PyJs_Object_133_ = Js({})
    PyJs_Object_134_ = Js({})
    PyJs_Object_122_ = Js({u'nodeSize':PyJs_Object_123_,u'childCount':PyJs_Object_124_,u'textContent':PyJs_Object_125_,u'firstChild':PyJs_Object_126_,u'lastChild':PyJs_Object_127_,u'isBlock':PyJs_Object_128_,u'isTextblock':PyJs_Object_129_,u'inlineContent':PyJs_Object_130_,u'isInline':PyJs_Object_131_,u'isText':PyJs_Object_132_,u'isLeaf':PyJs_Object_133_,u'isAtom':PyJs_Object_134_})
    var.put(u'prototypeAccessors', PyJs_Object_122_)
    @Js
    def PyJs_anonymous_135_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return (Js(1.0) if var.get(u"this").get(u'isLeaf') else (Js(2.0)+var.get(u"this").get(u'content').get(u'size')))
    PyJs_anonymous_135_._set_name(u'anonymous')
    var.get(u'prototypeAccessors').get(u'nodeSize').put(u'get', PyJs_anonymous_135_)
    @Js
    def PyJs_anonymous_136_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get(u'content').get(u'childCount')
    PyJs_anonymous_136_._set_name(u'anonymous')
    var.get(u'prototypeAccessors').get(u'childCount').put(u'get', PyJs_anonymous_136_)
    @Js
    def PyJs_child_137_(index, this, arguments, var=var):
        var = Scope({u'this':this, u'index':index, u'arguments':arguments, u'child':PyJs_child_137_}, var)
        var.registers([u'index'])
        return var.get(u"this").get(u'content').callprop(u'child', var.get(u'index'))
    PyJs_child_137_._set_name(u'child')
    var.get(u'Node').get(u'prototype').put(u'child', PyJs_child_137_)
    @Js
    def PyJs_maybeChild_138_(index, this, arguments, var=var):
        var = Scope({u'this':this, u'index':index, u'maybeChild':PyJs_maybeChild_138_, u'arguments':arguments}, var)
        var.registers([u'index'])
        return var.get(u"this").get(u'content').callprop(u'maybeChild', var.get(u'index'))
    PyJs_maybeChild_138_._set_name(u'maybeChild')
    var.get(u'Node').get(u'prototype').put(u'maybeChild', PyJs_maybeChild_138_)
    @Js
    def PyJs_forEach_139_(f, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'forEach':PyJs_forEach_139_, u'f':f}, var)
        var.registers([u'f'])
        var.get(u"this").get(u'content').callprop(u'forEach', var.get(u'f'))
    PyJs_forEach_139_._set_name(u'forEach')
    var.get(u'Node').get(u'prototype').put(u'forEach', PyJs_forEach_139_)
    @Js
    def PyJs_nodesBetween_140_(PyJsArg_66726f6d_, to, f, startPos, this, arguments, var=var):
        var = Scope({u'to':to, u'from':PyJsArg_66726f6d_, u'arguments':arguments, u'f':f, u'this':this, u'startPos':startPos, u'nodesBetween':PyJs_nodesBetween_140_}, var)
        var.registers([u'to', u'startPos', u'from', u'f'])
        if PyJsStrictEq(var.get(u'startPos'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'startPos', Js(0.0))
        var.get(u"this").get(u'content').callprop(u'nodesBetween', var.get(u'from'), var.get(u'to'), var.get(u'f'), var.get(u'startPos'), var.get(u"this"))
    PyJs_nodesBetween_140_._set_name(u'nodesBetween')
    var.get(u'Node').get(u'prototype').put(u'nodesBetween', PyJs_nodesBetween_140_)
    @Js
    def PyJs_descendants_141_(f, this, arguments, var=var):
        var = Scope({u'this':this, u'descendants':PyJs_descendants_141_, u'arguments':arguments, u'f':f}, var)
        var.registers([u'f'])
        var.get(u"this").callprop(u'nodesBetween', Js(0.0), var.get(u"this").get(u'content').get(u'size'), var.get(u'f'))
    PyJs_descendants_141_._set_name(u'descendants')
    var.get(u'Node').get(u'prototype').put(u'descendants', PyJs_descendants_141_)
    @Js
    def PyJs_anonymous_142_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").callprop(u'textBetween', Js(0.0), var.get(u"this").get(u'content').get(u'size'), Js(u''))
    PyJs_anonymous_142_._set_name(u'anonymous')
    var.get(u'prototypeAccessors').get(u'textContent').put(u'get', PyJs_anonymous_142_)
    @Js
    def PyJs_textBetween_143_(PyJsArg_66726f6d_, to, blockSeparator, leafText, this, arguments, var=var):
        var = Scope({u'to':to, u'from':PyJsArg_66726f6d_, u'leafText':leafText, u'blockSeparator':blockSeparator, u'this':this, u'textBetween':PyJs_textBetween_143_, u'arguments':arguments}, var)
        var.registers([u'to', u'from', u'leafText', u'blockSeparator'])
        return var.get(u"this").get(u'content').callprop(u'textBetween', var.get(u'from'), var.get(u'to'), var.get(u'blockSeparator'), var.get(u'leafText'))
    PyJs_textBetween_143_._set_name(u'textBetween')
    var.get(u'Node').get(u'prototype').put(u'textBetween', PyJs_textBetween_143_)
    @Js
    def PyJs_anonymous_144_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get(u'content').get(u'firstChild')
    PyJs_anonymous_144_._set_name(u'anonymous')
    var.get(u'prototypeAccessors').get(u'firstChild').put(u'get', PyJs_anonymous_144_)
    @Js
    def PyJs_anonymous_145_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get(u'content').get(u'lastChild')
    PyJs_anonymous_145_._set_name(u'anonymous')
    var.get(u'prototypeAccessors').get(u'lastChild').put(u'get', PyJs_anonymous_145_)
    @Js
    def PyJs_eq_146_(other, this, arguments, var=var):
        var = Scope({u'this':this, u'other':other, u'eq':PyJs_eq_146_, u'arguments':arguments}, var)
        var.registers([u'other'])
        return ((var.get(u"this")==var.get(u'other')) or (var.get(u"this").callprop(u'sameMarkup', var.get(u'other')) and var.get(u"this").get(u'content').callprop(u'eq', var.get(u'other').get(u'content'))))
    PyJs_eq_146_._set_name(u'eq')
    var.get(u'Node').get(u'prototype').put(u'eq', PyJs_eq_146_)
    @Js
    def PyJs_sameMarkup_147_(other, this, arguments, var=var):
        var = Scope({u'this':this, u'other':other, u'sameMarkup':PyJs_sameMarkup_147_, u'arguments':arguments}, var)
        var.registers([u'other'])
        return var.get(u"this").callprop(u'hasMarkup', var.get(u'other').get(u'type'), var.get(u'other').get(u'attrs'), var.get(u'other').get(u'marks'))
    PyJs_sameMarkup_147_._set_name(u'sameMarkup')
    var.get(u'Node').get(u'prototype').put(u'sameMarkup', PyJs_sameMarkup_147_)
    @Js
    def PyJs_hasMarkup_148_(type, attrs, marks, this, arguments, var=var):
        var = Scope({u'this':this, u'hasMarkup':PyJs_hasMarkup_148_, u'arguments':arguments, u'marks':marks, u'type':type, u'attrs':attrs}, var)
        var.registers([u'type', u'attrs', u'marks'])
        return (((var.get(u"this").get(u'type')==var.get(u'type')) and var.get(u'compareDeep')(var.get(u"this").get(u'attrs'), ((var.get(u'attrs') or var.get(u'type').get(u'defaultAttrs')) or var.get(u'emptyAttrs')))) and var.get(u'Mark').callprop(u'sameSet', var.get(u"this").get(u'marks'), (var.get(u'marks') or var.get(u'Mark').get(u'none'))))
    PyJs_hasMarkup_148_._set_name(u'hasMarkup')
    var.get(u'Node').get(u'prototype').put(u'hasMarkup', PyJs_hasMarkup_148_)
    @Js
    def PyJs_copy_149_(content, this, arguments, var=var):
        var = Scope({u'content':content, u'this':this, u'copy':PyJs_copy_149_, u'arguments':arguments}, var)
        var.registers([u'content'])
        if PyJsStrictEq(var.get(u'content'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'content', var.get(u"null"))
        if (var.get(u'content')==var.get(u"this").get(u'content')):
            return var.get(u"this")
        return var.get(u"this").get(u'constructor').create(var.get(u"this").get(u'type'), var.get(u"this").get(u'attrs'), var.get(u'content'), var.get(u"this").get(u'marks'))
    PyJs_copy_149_._set_name(u'copy')
    var.get(u'Node').get(u'prototype').put(u'copy', PyJs_copy_149_)
    @Js
    def PyJs_mark_150_(marks, this, arguments, var=var):
        var = Scope({u'this':this, u'mark':PyJs_mark_150_, u'arguments':arguments, u'marks':marks}, var)
        var.registers([u'marks'])
        return (var.get(u"this") if (var.get(u'marks')==var.get(u"this").get(u'marks')) else var.get(u"this").get(u'constructor').create(var.get(u"this").get(u'type'), var.get(u"this").get(u'attrs'), var.get(u"this").get(u'content'), var.get(u'marks')))
    PyJs_mark_150_._set_name(u'mark')
    var.get(u'Node').get(u'prototype').put(u'mark', PyJs_mark_150_)
    @Js
    def PyJs_cut_151_(PyJsArg_66726f6d_, to, this, arguments, var=var):
        var = Scope({u'this':this, u'to':to, u'cut':PyJs_cut_151_, u'from':PyJsArg_66726f6d_, u'arguments':arguments}, var)
        var.registers([u'to', u'from'])
        if ((var.get(u'from')==Js(0.0)) and (var.get(u'to')==var.get(u"this").get(u'content').get(u'size'))):
            return var.get(u"this")
        return var.get(u"this").callprop(u'copy', var.get(u"this").get(u'content').callprop(u'cut', var.get(u'from'), var.get(u'to')))
    PyJs_cut_151_._set_name(u'cut')
    var.get(u'Node').get(u'prototype').put(u'cut', PyJs_cut_151_)
    @Js
    def PyJs_slice_152_(PyJsArg_66726f6d_, to, includeParents, this, arguments, var=var):
        var = Scope({u'includeParents':includeParents, u'slice':PyJs_slice_152_, u'from':PyJsArg_66726f6d_, u'this':this, u'to':to, u'arguments':arguments}, var)
        var.registers([u'node', u'includeParents', u'$to', u'to', u'$from', u'content', u'start', u'depth', u'from'])
        if PyJsStrictEq(var.get(u'to'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'to', var.get(u"this").get(u'content').get(u'size'))
        if PyJsStrictEq(var.get(u'includeParents'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'includeParents', Js(False))
        if (var.get(u'from')==var.get(u'to')):
            return var.get(u'Slice').get(u'empty')
        var.put(u'$from', var.get(u"this").callprop(u'resolve', var.get(u'from')))
        var.put(u'$to', var.get(u"this").callprop(u'resolve', var.get(u'to')))
        var.put(u'depth', (Js(0.0) if var.get(u'includeParents') else var.get(u'$from').callprop(u'sharedDepth', var.get(u'to'))))
        var.put(u'start', var.get(u'$from').callprop(u'start', var.get(u'depth')))
        var.put(u'node', var.get(u'$from').callprop(u'node', var.get(u'depth')))
        var.put(u'content', var.get(u'node').get(u'content').callprop(u'cut', (var.get(u'$from').get(u'pos')-var.get(u'start')), (var.get(u'$to').get(u'pos')-var.get(u'start'))))
        return var.get(u'Slice').create(var.get(u'content'), (var.get(u'$from').get(u'depth')-var.get(u'depth')), (var.get(u'$to').get(u'depth')-var.get(u'depth')))
    PyJs_slice_152_._set_name(u'slice')
    var.get(u'Node').get(u'prototype').put(u'slice', PyJs_slice_152_)
    @Js
    def PyJs_InlineNonPyName_153_(PyJsArg_66726f6d_, to, slice, this, arguments, var=var):
        var = Scope({u'slice':slice, u'from':PyJsArg_66726f6d_, u'this':this, u'replace$1':PyJs_InlineNonPyName_153_, u'to':to, u'arguments':arguments}, var)
        var.registers([u'to', u'slice', u'from'])
        return var.get(u'replace')(var.get(u"this").callprop(u'resolve', var.get(u'from')), var.get(u"this").callprop(u'resolve', var.get(u'to')), var.get(u'slice'))
    PyJs_InlineNonPyName_153_._set_name(u'replace$1')
    var.get(u'Node').get(u'prototype').put(u'replace', PyJs_InlineNonPyName_153_)
    @Js
    def PyJs_nodeAt_154_(pos, this, arguments, var=var):
        var = Scope({u'this':this, u'nodeAt':PyJs_nodeAt_154_, u'pos':pos, u'arguments':arguments}, var)
        var.registers([u'node', u'index', u'ref', u'pos', u'offset'])
        #for JS loop
        var.put(u'node', var.get(u"this"))
        while 1:
            var.put(u'ref', var.get(u'node').get(u'content').callprop(u'findIndex', var.get(u'pos')))
            var.put(u'index', var.get(u'ref').get(u'index'))
            var.put(u'offset', var.get(u'ref').get(u'offset'))
            var.put(u'node', var.get(u'node').callprop(u'maybeChild', var.get(u'index')))
            if var.get(u'node').neg():
                return var.get(u"null")
            if ((var.get(u'offset')==var.get(u'pos')) or var.get(u'node').get(u'isText')):
                return var.get(u'node')
            var.put(u'pos', (var.get(u'offset')+Js(1.0)), u'-')
        
    PyJs_nodeAt_154_._set_name(u'nodeAt')
    var.get(u'Node').get(u'prototype').put(u'nodeAt', PyJs_nodeAt_154_)
    @Js
    def PyJs_childAfter_155_(pos, this, arguments, var=var):
        var = Scope({u'this':this, u'pos':pos, u'childAfter':PyJs_childAfter_155_, u'arguments':arguments}, var)
        var.registers([u'index', u'ref', u'pos', u'offset'])
        var.put(u'ref', var.get(u"this").get(u'content').callprop(u'findIndex', var.get(u'pos')))
        var.put(u'index', var.get(u'ref').get(u'index'))
        var.put(u'offset', var.get(u'ref').get(u'offset'))
        PyJs_Object_156_ = Js({u'node':var.get(u"this").get(u'content').callprop(u'maybeChild', var.get(u'index')),u'index':var.get(u'index'),u'offset':var.get(u'offset')})
        return PyJs_Object_156_
    PyJs_childAfter_155_._set_name(u'childAfter')
    var.get(u'Node').get(u'prototype').put(u'childAfter', PyJs_childAfter_155_)
    @Js
    def PyJs_childBefore_157_(pos, this, arguments, var=var):
        var = Scope({u'this':this, u'childBefore':PyJs_childBefore_157_, u'pos':pos, u'arguments':arguments}, var)
        var.registers([u'node', u'index', u'ref', u'pos', u'offset'])
        if (var.get(u'pos')==Js(0.0)):
            PyJs_Object_158_ = Js({u'node':var.get(u"null"),u'index':Js(0.0),u'offset':Js(0.0)})
            return PyJs_Object_158_
        var.put(u'ref', var.get(u"this").get(u'content').callprop(u'findIndex', var.get(u'pos')))
        var.put(u'index', var.get(u'ref').get(u'index'))
        var.put(u'offset', var.get(u'ref').get(u'offset'))
        if (var.get(u'offset')<var.get(u'pos')):
            PyJs_Object_159_ = Js({u'node':var.get(u"this").get(u'content').callprop(u'child', var.get(u'index')),u'index':var.get(u'index'),u'offset':var.get(u'offset')})
            return PyJs_Object_159_
        var.put(u'node', var.get(u"this").get(u'content').callprop(u'child', (var.get(u'index')-Js(1.0))))
        PyJs_Object_160_ = Js({u'node':var.get(u'node'),u'index':(var.get(u'index')-Js(1.0)),u'offset':(var.get(u'offset')-var.get(u'node').get(u'nodeSize'))})
        return PyJs_Object_160_
    PyJs_childBefore_157_._set_name(u'childBefore')
    var.get(u'Node').get(u'prototype').put(u'childBefore', PyJs_childBefore_157_)
    @Js
    def PyJs_resolve_161_(pos, this, arguments, var=var):
        var = Scope({u'this':this, u'resolve':PyJs_resolve_161_, u'pos':pos, u'arguments':arguments}, var)
        var.registers([u'pos'])
        return var.get(u'ResolvedPos').callprop(u'resolveCached', var.get(u"this"), var.get(u'pos'))
    PyJs_resolve_161_._set_name(u'resolve')
    var.get(u'Node').get(u'prototype').put(u'resolve', PyJs_resolve_161_)
    @Js
    def PyJs_resolveNoCache_162_(pos, this, arguments, var=var):
        var = Scope({u'this':this, u'resolveNoCache':PyJs_resolveNoCache_162_, u'pos':pos, u'arguments':arguments}, var)
        var.registers([u'pos'])
        return var.get(u'ResolvedPos').callprop(u'resolve', var.get(u"this"), var.get(u'pos'))
    PyJs_resolveNoCache_162_._set_name(u'resolveNoCache')
    var.get(u'Node').get(u'prototype').put(u'resolveNoCache', PyJs_resolveNoCache_162_)
    @Js
    def PyJs_rangeHasMark_163_(PyJsArg_66726f6d_, to, type, this, arguments, var=var):
        var = Scope({u'from':PyJsArg_66726f6d_, u'this':this, u'to':to, u'arguments':arguments, u'type':type, u'rangeHasMark':PyJs_rangeHasMark_163_}, var)
        var.registers([u'found', u'type', u'from', u'to'])
        var.put(u'found', Js(False))
        if (var.get(u'to')>var.get(u'from')):
            @Js
            def PyJs_anonymous_164_(node, this, arguments, var=var):
                var = Scope({u'node':node, u'this':this, u'arguments':arguments}, var)
                var.registers([u'node'])
                if var.get(u'type').callprop(u'isInSet', var.get(u'node').get(u'marks')):
                    var.put(u'found', Js(True))
                return var.get(u'found').neg()
            PyJs_anonymous_164_._set_name(u'anonymous')
            var.get(u"this").callprop(u'nodesBetween', var.get(u'from'), var.get(u'to'), PyJs_anonymous_164_)
        return var.get(u'found')
    PyJs_rangeHasMark_163_._set_name(u'rangeHasMark')
    var.get(u'Node').get(u'prototype').put(u'rangeHasMark', PyJs_rangeHasMark_163_)
    @Js
    def PyJs_anonymous_165_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get(u'type').get(u'isBlock')
    PyJs_anonymous_165_._set_name(u'anonymous')
    var.get(u'prototypeAccessors').get(u'isBlock').put(u'get', PyJs_anonymous_165_)
    @Js
    def PyJs_anonymous_166_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get(u'type').get(u'isTextblock')
    PyJs_anonymous_166_._set_name(u'anonymous')
    var.get(u'prototypeAccessors').get(u'isTextblock').put(u'get', PyJs_anonymous_166_)
    @Js
    def PyJs_anonymous_167_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get(u'type').get(u'inlineContent')
    PyJs_anonymous_167_._set_name(u'anonymous')
    var.get(u'prototypeAccessors').get(u'inlineContent').put(u'get', PyJs_anonymous_167_)
    @Js
    def PyJs_anonymous_168_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get(u'type').get(u'isInline')
    PyJs_anonymous_168_._set_name(u'anonymous')
    var.get(u'prototypeAccessors').get(u'isInline').put(u'get', PyJs_anonymous_168_)
    @Js
    def PyJs_anonymous_169_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get(u'type').get(u'isText')
    PyJs_anonymous_169_._set_name(u'anonymous')
    var.get(u'prototypeAccessors').get(u'isText').put(u'get', PyJs_anonymous_169_)
    @Js
    def PyJs_anonymous_170_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get(u'type').get(u'isLeaf')
    PyJs_anonymous_170_._set_name(u'anonymous')
    var.get(u'prototypeAccessors').get(u'isLeaf').put(u'get', PyJs_anonymous_170_)
    @Js
    def PyJs_anonymous_171_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get(u'type').get(u'isAtom')
    PyJs_anonymous_171_._set_name(u'anonymous')
    var.get(u'prototypeAccessors').get(u'isAtom').put(u'get', PyJs_anonymous_171_)
    @Js
    def PyJs_toString_172_(this, arguments, var=var):
        var = Scope({u'this':this, u'toString':PyJs_toString_172_, u'arguments':arguments}, var)
        var.registers([u'name'])
        if var.get(u"this").get(u'type').get(u'spec').get(u'toDebugString'):
            return var.get(u"this").get(u'type').get(u'spec').callprop(u'toDebugString', var.get(u"this"))
        var.put(u'name', var.get(u"this").get(u'type').get(u'name'))
        if var.get(u"this").get(u'content').get(u'size'):
            var.put(u'name', ((Js(u'(')+var.get(u"this").get(u'content').callprop(u'toStringInner'))+Js(u')')), u'+')
        return var.get(u'wrapMarks')(var.get(u"this").get(u'marks'), var.get(u'name'))
    PyJs_toString_172_._set_name(u'toString')
    var.get(u'Node').get(u'prototype').put(u'toString', PyJs_toString_172_)
    @Js
    def PyJs_contentMatchAt_173_(index, this, arguments, var=var):
        var = Scope({u'this':this, u'index':index, u'arguments':arguments, u'contentMatchAt':PyJs_contentMatchAt_173_}, var)
        var.registers([u'index', u'match'])
        var.put(u'match', var.get(u"this").get(u'type').get(u'contentMatch').callprop(u'matchFragment', var.get(u"this").get(u'content'), Js(0.0), var.get(u'index')))
        if var.get(u'match').neg():
            PyJsTempException = JsToPyException(var.get(u'Error').create(Js(u'Called contentMatchAt on a node with invalid content')))
            raise PyJsTempException
        return var.get(u'match')
    PyJs_contentMatchAt_173_._set_name(u'contentMatchAt')
    var.get(u'Node').get(u'prototype').put(u'contentMatchAt', PyJs_contentMatchAt_173_)
    @Js
    def PyJs_canReplace_174_(PyJsArg_66726f6d_, to, replacement, start, end, this, arguments, var=var):
        var = Scope({u'canReplace':PyJs_canReplace_174_, u'to':to, u'end':end, u'arguments':arguments, u'start':start, u'this':this, u'from':PyJsArg_66726f6d_, u'replacement':replacement}, var)
        var.registers([u'from', u'start', u'i', u'two', u'one', u'to', u'this$1', u'end', u'replacement'])
        var.put(u'this$1', var.get(u"this"))
        if PyJsStrictEq(var.get(u'replacement'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'replacement', var.get(u'Fragment').get(u'empty'))
        if PyJsStrictEq(var.get(u'start'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'start', Js(0.0))
        if PyJsStrictEq(var.get(u'end'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'end', var.get(u'replacement').get(u'childCount'))
        var.put(u'one', var.get(u"this").callprop(u'contentMatchAt', var.get(u'from')).callprop(u'matchFragment', var.get(u'replacement'), var.get(u'start'), var.get(u'end')))
        var.put(u'two', (var.get(u'one') and var.get(u'one').callprop(u'matchFragment', var.get(u"this").get(u'content'), var.get(u'to'))))
        if (var.get(u'two').neg() or var.get(u'two').get(u'validEnd').neg()):
            return Js(False)
        #for JS loop
        var.put(u'i', var.get(u'start'))
        while (var.get(u'i')<var.get(u'end')):
            try:
                if var.get(u'this$1').get(u'type').callprop(u'allowsMarks', var.get(u'replacement').callprop(u'child', var.get(u'i')).get(u'marks')).neg():
                    return Js(False)
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return Js(True)
    PyJs_canReplace_174_._set_name(u'canReplace')
    var.get(u'Node').get(u'prototype').put(u'canReplace', PyJs_canReplace_174_)
    @Js
    def PyJs_canReplaceWith_175_(PyJsArg_66726f6d_, to, type, marks, this, arguments, var=var):
        var = Scope({u'canReplaceWith':PyJs_canReplaceWith_175_, u'to':to, u'from':PyJsArg_66726f6d_, u'arguments':arguments, u'marks':marks, u'this':this, u'type':type}, var)
        var.registers([u'end', u'to', u'start', u'marks', u'from', u'type'])
        if (var.get(u'marks') and var.get(u"this").get(u'type').callprop(u'allowsMarks', var.get(u'marks')).neg()):
            return Js(False)
        var.put(u'start', var.get(u"this").callprop(u'contentMatchAt', var.get(u'from')).callprop(u'matchType', var.get(u'type')))
        var.put(u'end', (var.get(u'start') and var.get(u'start').callprop(u'matchFragment', var.get(u"this").get(u'content'), var.get(u'to'))))
        return (var.get(u'end').get(u'validEnd') if var.get(u'end') else Js(False))
    PyJs_canReplaceWith_175_._set_name(u'canReplaceWith')
    var.get(u'Node').get(u'prototype').put(u'canReplaceWith', PyJs_canReplaceWith_175_)
    @Js
    def PyJs_canAppend_176_(other, this, arguments, var=var):
        var = Scope({u'this':this, u'other':other, u'canAppend':PyJs_canAppend_176_, u'arguments':arguments}, var)
        var.registers([u'other'])
        if var.get(u'other').get(u'content').get(u'size'):
            return var.get(u"this").callprop(u'canReplace', var.get(u"this").get(u'childCount'), var.get(u"this").get(u'childCount'), var.get(u'other').get(u'content'))
        else:
            return var.get(u"this").get(u'type').callprop(u'compatibleContent', var.get(u'other').get(u'type'))
    PyJs_canAppend_176_._set_name(u'canAppend')
    var.get(u'Node').get(u'prototype').put(u'canAppend', PyJs_canAppend_176_)
    @Js
    def PyJs_defaultContentType_177_(at, this, arguments, var=var):
        var = Scope({u'this':this, u'defaultContentType':PyJs_defaultContentType_177_, u'at':at, u'arguments':arguments}, var)
        var.registers([u'at'])
        return var.get(u"this").callprop(u'contentMatchAt', var.get(u'at')).get(u'defaultType')
    PyJs_defaultContentType_177_._set_name(u'defaultContentType')
    var.get(u'Node').get(u'prototype').put(u'defaultContentType', PyJs_defaultContentType_177_)
    @Js
    def PyJs_check_178_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'check':PyJs_check_178_}, var)
        var.registers([])
        if var.get(u"this").get(u'type').callprop(u'validContent', var.get(u"this").get(u'content')).neg():
            PyJsTempException = JsToPyException(var.get(u'RangeError').create((((Js(u'Invalid content for node ')+var.get(u"this").get(u'type').get(u'name'))+Js(u': '))+var.get(u"this").get(u'content').callprop(u'toString').callprop(u'slice', Js(0.0), Js(50.0)))))
            raise PyJsTempException
        @Js
        def PyJs_anonymous_179_(node, this, arguments, var=var):
            var = Scope({u'node':node, u'this':this, u'arguments':arguments}, var)
            var.registers([u'node'])
            return var.get(u'node').callprop(u'check')
        PyJs_anonymous_179_._set_name(u'anonymous')
        var.get(u"this").get(u'content').callprop(u'forEach', PyJs_anonymous_179_)
    PyJs_check_178_._set_name(u'check')
    var.get(u'Node').get(u'prototype').put(u'check', PyJs_check_178_)
    @Js
    def PyJs_toJSON_180_(this, arguments, var=var):
        var = Scope({u'this':this, u'toJSON':PyJs_toJSON_180_, u'arguments':arguments}, var)
        var.registers([u'obj', u'_', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        PyJs_Object_181_ = Js({u'type':var.get(u"this").get(u'type').get(u'name')})
        var.put(u'obj', PyJs_Object_181_)
        for PyJsTemp in var.get(u'this$1').get(u'attrs'):
            var.put(u'_', PyJsTemp)
            var.get(u'obj').put(u'attrs', var.get(u'this$1').get(u'attrs'))
            break
        if var.get(u"this").get(u'content').get(u'size'):
            var.get(u'obj').put(u'content', var.get(u"this").get(u'content').callprop(u'toJSON'))
        if var.get(u"this").get(u'marks').get(u'length'):
            @Js
            def PyJs_anonymous_182_(n, this, arguments, var=var):
                var = Scope({u'this':this, u'arguments':arguments, u'n':n}, var)
                var.registers([u'n'])
                return var.get(u'n').callprop(u'toJSON')
            PyJs_anonymous_182_._set_name(u'anonymous')
            var.get(u'obj').put(u'marks', var.get(u"this").get(u'marks').callprop(u'map', PyJs_anonymous_182_))
        return var.get(u'obj')
    PyJs_toJSON_180_._set_name(u'toJSON')
    var.get(u'Node').get(u'prototype').put(u'toJSON', PyJs_toJSON_180_)
    @Js
    def PyJs_fromJSON_183_(schema, json, this, arguments, var=var):
        var = Scope({u'this':this, u'json':json, u'arguments':arguments, u'fromJSON':PyJs_fromJSON_183_, u'schema':schema}, var)
        var.registers([u'content', u'json', u'schema', u'marks'])
        if var.get(u'json').neg():
            PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'Invalid input for Node.fromJSON')))
            raise PyJsTempException
        var.put(u'marks', var.get(u"null"))
        if var.get(u'json').get(u'marks'):
            if var.get(u'Array').callprop(u'isArray', var.get(u'json').get(u'marks')).neg():
                PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'Invalid mark data for Node.fromJSON')))
                raise PyJsTempException
            var.put(u'marks', var.get(u'json').get(u'marks').callprop(u'map', var.get(u'schema').get(u'markFromJSON')))
        if (var.get(u'json').get(u'type')==Js(u'text')):
            if (var.get(u'json').get(u'text').typeof()!=Js(u'string')):
                PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'Invalid text node in JSON')))
                raise PyJsTempException
            return var.get(u'schema').callprop(u'text', var.get(u'json').get(u'text'), var.get(u'marks'))
        var.put(u'content', var.get(u'Fragment').callprop(u'fromJSON', var.get(u'schema'), var.get(u'json').get(u'content')))
        return var.get(u'schema').callprop(u'nodeType', var.get(u'json').get(u'type')).callprop(u'create', var.get(u'json').get(u'attrs'), var.get(u'content'), var.get(u'marks'))
    PyJs_fromJSON_183_._set_name(u'fromJSON')
    var.get(u'Node').put(u'fromJSON', PyJs_fromJSON_183_)
    var.get(u'Object').callprop(u'defineProperties', var.get(u'Node').get(u'prototype'), var.get(u'prototypeAccessors'))
    @Js
    def PyJs_anonymous_184_(Node, this, arguments, var=var):
        var = Scope({u'Node':Node, u'this':this, u'arguments':arguments}, var)
        var.registers([u'Node', u'TextNode', u'prototypeAccessors$1'])
        @Js
        def PyJsHoisted_TextNode_(type, attrs, content, marks, this, arguments, var=var):
            var = Scope({u'content':content, u'attrs':attrs, u'marks':marks, u'this':this, u'type':type, u'arguments':arguments}, var)
            var.registers([u'content', u'type', u'attrs', u'marks'])
            var.get(u'Node').callprop(u'call', var.get(u"this"), var.get(u'type'), var.get(u'attrs'), var.get(u"null"), var.get(u'marks'))
            if var.get(u'content').neg():
                PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'Empty text nodes are not allowed')))
                raise PyJsTempException
            var.get(u"this").put(u'text', var.get(u'content'))
        PyJsHoisted_TextNode_.func_name = u'TextNode'
        var.put(u'TextNode', PyJsHoisted_TextNode_)
        pass
        if var.get(u'Node'):
            var.get(u'TextNode').put(u'__proto__', var.get(u'Node'))
        var.get(u'TextNode').put(u'prototype', var.get(u'Object').callprop(u'create', (var.get(u'Node') and var.get(u'Node').get(u'prototype'))))
        var.get(u'TextNode').get(u'prototype').put(u'constructor', var.get(u'TextNode'))
        PyJs_Object_186_ = Js({})
        PyJs_Object_187_ = Js({})
        PyJs_Object_185_ = Js({u'textContent':PyJs_Object_186_,u'nodeSize':PyJs_Object_187_})
        var.put(u'prototypeAccessors$1', PyJs_Object_185_)
        @Js
        def PyJs_toString_188_(this, arguments, var=var):
            var = Scope({u'this':this, u'toString':PyJs_toString_188_, u'arguments':arguments}, var)
            var.registers([])
            if var.get(u"this").get(u'type').get(u'spec').get(u'toDebugString'):
                return var.get(u"this").get(u'type').get(u'spec').callprop(u'toDebugString', var.get(u"this"))
            return var.get(u'wrapMarks')(var.get(u"this").get(u'marks'), var.get(u'JSON').callprop(u'stringify', var.get(u"this").get(u'text')))
        PyJs_toString_188_._set_name(u'toString')
        var.get(u'TextNode').get(u'prototype').put(u'toString', PyJs_toString_188_)
        @Js
        def PyJs_anonymous_189_(this, arguments, var=var):
            var = Scope({u'this':this, u'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get(u'text')
        PyJs_anonymous_189_._set_name(u'anonymous')
        var.get(u'prototypeAccessors$1').get(u'textContent').put(u'get', PyJs_anonymous_189_)
        @Js
        def PyJs_textBetween_190_(PyJsArg_66726f6d_, to, this, arguments, var=var):
            var = Scope({u'this':this, u'to':to, u'textBetween':PyJs_textBetween_190_, u'from':PyJsArg_66726f6d_, u'arguments':arguments}, var)
            var.registers([u'to', u'from'])
            return var.get(u"this").get(u'text').callprop(u'slice', var.get(u'from'), var.get(u'to'))
        PyJs_textBetween_190_._set_name(u'textBetween')
        var.get(u'TextNode').get(u'prototype').put(u'textBetween', PyJs_textBetween_190_)
        @Js
        def PyJs_anonymous_191_(this, arguments, var=var):
            var = Scope({u'this':this, u'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get(u'text').get(u'length')
        PyJs_anonymous_191_._set_name(u'anonymous')
        var.get(u'prototypeAccessors$1').get(u'nodeSize').put(u'get', PyJs_anonymous_191_)
        @Js
        def PyJs_mark_192_(marks, this, arguments, var=var):
            var = Scope({u'this':this, u'mark':PyJs_mark_192_, u'arguments':arguments, u'marks':marks}, var)
            var.registers([u'marks'])
            return (var.get(u"this") if (var.get(u'marks')==var.get(u"this").get(u'marks')) else var.get(u'TextNode').create(var.get(u"this").get(u'type'), var.get(u"this").get(u'attrs'), var.get(u"this").get(u'text'), var.get(u'marks')))
        PyJs_mark_192_._set_name(u'mark')
        var.get(u'TextNode').get(u'prototype').put(u'mark', PyJs_mark_192_)
        @Js
        def PyJs_withText_193_(text, this, arguments, var=var):
            var = Scope({u'this':this, u'text':text, u'arguments':arguments, u'withText':PyJs_withText_193_}, var)
            var.registers([u'text'])
            if (var.get(u'text')==var.get(u"this").get(u'text')):
                return var.get(u"this")
            return var.get(u'TextNode').create(var.get(u"this").get(u'type'), var.get(u"this").get(u'attrs'), var.get(u'text'), var.get(u"this").get(u'marks'))
        PyJs_withText_193_._set_name(u'withText')
        var.get(u'TextNode').get(u'prototype').put(u'withText', PyJs_withText_193_)
        @Js
        def PyJs_cut_194_(PyJsArg_66726f6d_, to, this, arguments, var=var):
            var = Scope({u'this':this, u'to':to, u'cut':PyJs_cut_194_, u'from':PyJsArg_66726f6d_, u'arguments':arguments}, var)
            var.registers([u'to', u'from'])
            if PyJsStrictEq(var.get(u'from'),PyJsComma(Js(0.0), Js(None))):
                var.put(u'from', Js(0.0))
            if PyJsStrictEq(var.get(u'to'),PyJsComma(Js(0.0), Js(None))):
                var.put(u'to', var.get(u"this").get(u'text').get(u'length'))
            if ((var.get(u'from')==Js(0.0)) and (var.get(u'to')==var.get(u"this").get(u'text').get(u'length'))):
                return var.get(u"this")
            return var.get(u"this").callprop(u'withText', var.get(u"this").get(u'text').callprop(u'slice', var.get(u'from'), var.get(u'to')))
        PyJs_cut_194_._set_name(u'cut')
        var.get(u'TextNode').get(u'prototype').put(u'cut', PyJs_cut_194_)
        @Js
        def PyJs_eq_195_(other, this, arguments, var=var):
            var = Scope({u'this':this, u'other':other, u'eq':PyJs_eq_195_, u'arguments':arguments}, var)
            var.registers([u'other'])
            return (var.get(u"this").callprop(u'sameMarkup', var.get(u'other')) and (var.get(u"this").get(u'text')==var.get(u'other').get(u'text')))
        PyJs_eq_195_._set_name(u'eq')
        var.get(u'TextNode').get(u'prototype').put(u'eq', PyJs_eq_195_)
        @Js
        def PyJs_toJSON_196_(this, arguments, var=var):
            var = Scope({u'this':this, u'toJSON':PyJs_toJSON_196_, u'arguments':arguments}, var)
            var.registers([u'base'])
            var.put(u'base', var.get(u'Node').get(u'prototype').get(u'toJSON').callprop(u'call', var.get(u"this")))
            var.get(u'base').put(u'text', var.get(u"this").get(u'text'))
            return var.get(u'base')
        PyJs_toJSON_196_._set_name(u'toJSON')
        var.get(u'TextNode').get(u'prototype').put(u'toJSON', PyJs_toJSON_196_)
        var.get(u'Object').callprop(u'defineProperties', var.get(u'TextNode').get(u'prototype'), var.get(u'prototypeAccessors$1'))
        return var.get(u'TextNode')
    PyJs_anonymous_184_._set_name(u'anonymous')
    var.put(u'TextNode', PyJs_anonymous_184_(var.get(u'Node')))
    pass
    @Js
    def PyJs_ContentMatch_197_(validEnd, this, arguments, var=var):
        var = Scope({u'this':this, u'validEnd':validEnd, u'ContentMatch':PyJs_ContentMatch_197_, u'arguments':arguments}, var)
        var.registers([u'validEnd'])
        var.get(u"this").put(u'validEnd', var.get(u'validEnd'))
        var.get(u"this").put(u'next', Js([]))
        var.get(u"this").put(u'wrapCache', Js([]))
    PyJs_ContentMatch_197_._set_name(u'ContentMatch')
    var.put(u'ContentMatch', PyJs_ContentMatch_197_)
    PyJs_Object_199_ = Js({})
    PyJs_Object_200_ = Js({})
    PyJs_Object_201_ = Js({})
    PyJs_Object_198_ = Js({u'inlineContent':PyJs_Object_199_,u'defaultType':PyJs_Object_200_,u'edgeCount':PyJs_Object_201_})
    var.put(u'prototypeAccessors$5', PyJs_Object_198_)
    @Js
    def PyJs_parse_202_(string, nodeTypes, this, arguments, var=var):
        var = Scope({u'this':this, u'parse':PyJs_parse_202_, u'string':string, u'nodeTypes':nodeTypes, u'arguments':arguments}, var)
        var.registers([u'expr', u'nodeTypes', u'match', u'stream', u'string'])
        var.put(u'stream', var.get(u'TokenStream').create(var.get(u'string'), var.get(u'nodeTypes')))
        if (var.get(u'stream').get(u'next')==var.get(u"null")):
            return var.get(u'ContentMatch').get(u'empty')
        var.put(u'expr', var.get(u'parseExpr')(var.get(u'stream')))
        if var.get(u'stream').get(u'next'):
            var.get(u'stream').callprop(u'err', Js(u'Unexpected trailing text'))
        var.put(u'match', var.get(u'dfa')(var.get(u'nfa')(var.get(u'expr'))))
        var.get(u'checkForDeadEnds')(var.get(u'match'), var.get(u'stream'))
        return var.get(u'match')
    PyJs_parse_202_._set_name(u'parse')
    var.get(u'ContentMatch').put(u'parse', PyJs_parse_202_)
    @Js
    def PyJs_matchType_203_(type, this, arguments, var=var):
        var = Scope({u'this':this, u'matchType':PyJs_matchType_203_, u'type':type, u'arguments':arguments}, var)
        var.registers([u'i', u'type', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u"this").get(u'next').get(u'length')):
            try:
                if (var.get(u'this$1').get(u'next').get(var.get(u'i'))==var.get(u'type')):
                    return var.get(u'this$1').get(u'next').get((var.get(u'i')+Js(1.0)))
            finally:
                    var.put(u'i', Js(2.0), u'+')
        return var.get(u"null")
    PyJs_matchType_203_._set_name(u'matchType')
    var.get(u'ContentMatch').get(u'prototype').put(u'matchType', PyJs_matchType_203_)
    @Js
    def PyJs_matchFragment_204_(frag, start, end, this, arguments, var=var):
        var = Scope({u'frag':frag, u'end':end, u'this':this, u'start':start, u'arguments':arguments, u'matchFragment':PyJs_matchFragment_204_}, var)
        var.registers([u'i', u'frag', u'end', u'cur', u'start'])
        if PyJsStrictEq(var.get(u'start'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'start', Js(0.0))
        if PyJsStrictEq(var.get(u'end'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'end', var.get(u'frag').get(u'childCount'))
        var.put(u'cur', var.get(u"this"))
        #for JS loop
        var.put(u'i', var.get(u'start'))
        while (var.get(u'cur') and (var.get(u'i')<var.get(u'end'))):
            try:
                var.put(u'cur', var.get(u'cur').callprop(u'matchType', var.get(u'frag').callprop(u'child', var.get(u'i')).get(u'type')))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return var.get(u'cur')
    PyJs_matchFragment_204_._set_name(u'matchFragment')
    var.get(u'ContentMatch').get(u'prototype').put(u'matchFragment', PyJs_matchFragment_204_)
    @Js
    def PyJs_anonymous_205_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([u'first'])
        var.put(u'first', var.get(u"this").get(u'next').get(u'0'))
        return (var.get(u'first').get(u'isInline') if var.get(u'first') else Js(False))
    PyJs_anonymous_205_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$5').get(u'inlineContent').put(u'get', PyJs_anonymous_205_)
    @Js
    def PyJs_anonymous_206_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([u'i', u'type', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u"this").get(u'next').get(u'length')):
            try:
                var.put(u'type', var.get(u'this$1').get(u'next').get(var.get(u'i')))
                if (var.get(u'type').get(u'isText') or var.get(u'type').callprop(u'hasRequiredAttrs')).neg():
                    return var.get(u'type')
            finally:
                    var.put(u'i', Js(2.0), u'+')
    PyJs_anonymous_206_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$5').get(u'defaultType').put(u'get', PyJs_anonymous_206_)
    @Js
    def PyJs_compatible_207_(other, this, arguments, var=var):
        var = Scope({u'this':this, u'compatible':PyJs_compatible_207_, u'other':other, u'arguments':arguments}, var)
        var.registers([u'i', u'j', u'other', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u"this").get(u'next').get(u'length')):
            try:
                #for JS loop
                var.put(u'j', Js(0.0))
                while (var.get(u'j')<var.get(u'other').get(u'next').get(u'length')):
                    try:
                        if (var.get(u'this$1').get(u'next').get(var.get(u'i'))==var.get(u'other').get(u'next').get(var.get(u'j'))):
                            return Js(True)
                    finally:
                            var.put(u'j', Js(2.0), u'+')
            finally:
                    var.put(u'i', Js(2.0), u'+')
        return Js(False)
    PyJs_compatible_207_._set_name(u'compatible')
    var.get(u'ContentMatch').get(u'prototype').put(u'compatible', PyJs_compatible_207_)
    @Js
    def PyJs_fillBefore_208_(after, toEnd, startIndex, this, arguments, var=var):
        var = Scope({u'fillBefore':PyJs_fillBefore_208_, u'this':this, u'after':after, u'toEnd':toEnd, u'startIndex':startIndex, u'arguments':arguments}, var)
        var.registers([u'seen', u'search', u'after', u'startIndex', u'toEnd'])
        @Js
        def PyJsHoisted_search_(match, types, this, arguments, var=var):
            var = Scope({u'this':this, u'types':types, u'match':match, u'arguments':arguments}, var)
            var.registers([u'i', u'next', u'finished', u'types', u'found', u'type', u'match'])
            var.put(u'finished', var.get(u'match').callprop(u'matchFragment', var.get(u'after'), var.get(u'startIndex')))
            if (var.get(u'finished') and (var.get(u'toEnd').neg() or var.get(u'finished').get(u'validEnd'))):
                @Js
                def PyJs_anonymous_209_(tp, this, arguments, var=var):
                    var = Scope({u'this':this, u'arguments':arguments, u'tp':tp}, var)
                    var.registers([u'tp'])
                    return var.get(u'tp').callprop(u'createAndFill')
                PyJs_anonymous_209_._set_name(u'anonymous')
                return var.get(u'Fragment').callprop(u'from', var.get(u'types').callprop(u'map', PyJs_anonymous_209_))
            #for JS loop
            var.put(u'i', Js(0.0))
            while (var.get(u'i')<var.get(u'match').get(u'next').get(u'length')):
                try:
                    var.put(u'type', var.get(u'match').get(u'next').get(var.get(u'i')))
                    var.put(u'next', var.get(u'match').get(u'next').get((var.get(u'i')+Js(1.0))))
                    if ((var.get(u'type').get(u'isText') or var.get(u'type').callprop(u'hasRequiredAttrs')).neg() and (var.get(u'seen').callprop(u'indexOf', var.get(u'next'))==(-Js(1.0)))):
                        var.get(u'seen').callprop(u'push', var.get(u'next'))
                        var.put(u'found', var.get(u'search')(var.get(u'next'), var.get(u'types').callprop(u'concat', var.get(u'type'))))
                        if var.get(u'found'):
                            return var.get(u'found')
                finally:
                        var.put(u'i', Js(2.0), u'+')
        PyJsHoisted_search_.func_name = u'search'
        var.put(u'search', PyJsHoisted_search_)
        if PyJsStrictEq(var.get(u'toEnd'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'toEnd', Js(False))
        if PyJsStrictEq(var.get(u'startIndex'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'startIndex', Js(0.0))
        var.put(u'seen', Js([var.get(u"this")]))
        pass
        return var.get(u'search')(var.get(u"this"), Js([]))
    PyJs_fillBefore_208_._set_name(u'fillBefore')
    var.get(u'ContentMatch').get(u'prototype').put(u'fillBefore', PyJs_fillBefore_208_)
    @Js
    def PyJs_findWrapping_210_(target, this, arguments, var=var):
        var = Scope({u'this':this, u'findWrapping':PyJs_findWrapping_210_, u'target':target, u'arguments':arguments}, var)
        var.registers([u'i', u'target', u'computed', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u"this").get(u'wrapCache').get(u'length')):
            try:
                if (var.get(u'this$1').get(u'wrapCache').get(var.get(u'i'))==var.get(u'target')):
                    return var.get(u'this$1').get(u'wrapCache').get((var.get(u'i')+Js(1.0)))
            finally:
                    var.put(u'i', Js(2.0), u'+')
        var.put(u'computed', var.get(u"this").callprop(u'computeWrapping', var.get(u'target')))
        var.get(u"this").get(u'wrapCache').callprop(u'push', var.get(u'target'), var.get(u'computed'))
        return var.get(u'computed')
    PyJs_findWrapping_210_._set_name(u'findWrapping')
    var.get(u'ContentMatch').get(u'prototype').put(u'findWrapping', PyJs_findWrapping_210_)
    @Js
    def PyJs_computeWrapping_211_(target, this, arguments, var=var):
        var = Scope({u'this':this, u'computeWrapping':PyJs_computeWrapping_211_, u'target':target, u'arguments':arguments}, var)
        var.registers([u'obj', u'target', u'i', u'current', u'result', u'active', u'seen', u'type', u'match'])
        var.put(u'seen', var.get(u'Object').callprop(u'create', var.get(u"null")))
        PyJs_Object_212_ = Js({u'match':var.get(u"this"),u'type':var.get(u"null"),u'via':var.get(u"null")})
        var.put(u'active', Js([PyJs_Object_212_]))
        while var.get(u'active').get(u'length'):
            var.put(u'current', var.get(u'active').callprop(u'shift'))
            var.put(u'match', var.get(u'current').get(u'match'))
            if var.get(u'match').callprop(u'matchType', var.get(u'target')):
                var.put(u'result', Js([]))
                #for JS loop
                var.put(u'obj', var.get(u'current'))
                while var.get(u'obj').get(u'type'):
                    try:
                        var.get(u'result').callprop(u'push', var.get(u'obj').get(u'type'))
                    finally:
                            var.put(u'obj', var.get(u'obj').get(u'via'))
                return var.get(u'result').callprop(u'reverse')
            #for JS loop
            var.put(u'i', Js(0.0))
            while (var.get(u'i')<var.get(u'match').get(u'next').get(u'length')):
                try:
                    var.put(u'type', var.get(u'match').get(u'next').get(var.get(u'i')))
                    if (((var.get(u'type').get(u'isLeaf').neg() and var.get(u'type').callprop(u'hasRequiredAttrs').neg()) and var.get(u'seen').contains(var.get(u'type').get(u'name')).neg()) and (var.get(u'current').get(u'type').neg() or var.get(u'match').get(u'next').get((var.get(u'i')+Js(1.0))).get(u'validEnd'))):
                        PyJs_Object_213_ = Js({u'match':var.get(u'type').get(u'contentMatch'),u'type':var.get(u'type'),u'via':var.get(u'current')})
                        var.get(u'active').callprop(u'push', PyJs_Object_213_)
                        var.get(u'seen').put(var.get(u'type').get(u'name'), Js(True))
                finally:
                        var.put(u'i', Js(2.0), u'+')
    PyJs_computeWrapping_211_._set_name(u'computeWrapping')
    var.get(u'ContentMatch').get(u'prototype').put(u'computeWrapping', PyJs_computeWrapping_211_)
    @Js
    def PyJs_anonymous_214_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return (var.get(u"this").get(u'next').get(u'length')>>Js(1.0))
    PyJs_anonymous_214_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$5').get(u'edgeCount').put(u'get', PyJs_anonymous_214_)
    @Js
    def PyJs_edge_215_(n, this, arguments, var=var):
        var = Scope({u'this':this, u'edge':PyJs_edge_215_, u'arguments':arguments, u'n':n}, var)
        var.registers([u'i', u'n'])
        var.put(u'i', (var.get(u'n')<<Js(1.0)))
        if (var.get(u'i')>var.get(u"this").get(u'next').get(u'length')):
            PyJsTempException = JsToPyException(var.get(u'RangeError').create(((Js(u"There's no ")+var.get(u'n'))+Js(u'th edge in this content match'))))
            raise PyJsTempException
        PyJs_Object_216_ = Js({u'type':var.get(u"this").get(u'next').get(var.get(u'i')),u'next':var.get(u"this").get(u'next').get((var.get(u'i')+Js(1.0)))})
        return PyJs_Object_216_
    PyJs_edge_215_._set_name(u'edge')
    var.get(u'ContentMatch').get(u'prototype').put(u'edge', PyJs_edge_215_)
    @Js
    def PyJs_toString_217_(this, arguments, var=var):
        var = Scope({u'this':this, u'toString':PyJs_toString_217_, u'arguments':arguments}, var)
        var.registers([u'seen', u'scan'])
        @Js
        def PyJsHoisted_scan_(m, this, arguments, var=var):
            var = Scope({u'this':this, u'm':m, u'arguments':arguments}, var)
            var.registers([u'i', u'm'])
            var.get(u'seen').callprop(u'push', var.get(u'm'))
            #for JS loop
            var.put(u'i', Js(1.0))
            while (var.get(u'i')<var.get(u'm').get(u'next').get(u'length')):
                try:
                    if (var.get(u'seen').callprop(u'indexOf', var.get(u'm').get(u'next').get(var.get(u'i')))==(-Js(1.0))):
                        var.get(u'scan')(var.get(u'm').get(u'next').get(var.get(u'i')))
                finally:
                        var.put(u'i', Js(2.0), u'+')
        PyJsHoisted_scan_.func_name = u'scan'
        var.put(u'scan', PyJsHoisted_scan_)
        var.put(u'seen', Js([]))
        pass
        var.get(u'scan')(var.get(u"this"))
        @Js
        def PyJs_anonymous_218_(m, i, this, arguments, var=var):
            var = Scope({u'i':i, u'this':this, u'm':m, u'arguments':arguments}, var)
            var.registers([u'i', u'i$1', u'm', u'out'])
            var.put(u'out', ((var.get(u'i')+(Js(u'*') if var.get(u'm').get(u'validEnd') else Js(u' ')))+Js(u' ')))
            #for JS loop
            var.put(u'i$1', Js(0.0))
            while (var.get(u'i$1')<var.get(u'm').get(u'next').get(u'length')):
                try:
                    var.put(u'out', ((((Js(u', ') if var.get(u'i$1') else Js(u''))+var.get(u'm').get(u'next').get(var.get(u'i$1')).get(u'name'))+Js(u'->'))+var.get(u'seen').callprop(u'indexOf', var.get(u'm').get(u'next').get((var.get(u'i$1')+Js(1.0))))), u'+')
                finally:
                        var.put(u'i$1', Js(2.0), u'+')
            return var.get(u'out')
        PyJs_anonymous_218_._set_name(u'anonymous')
        return var.get(u'seen').callprop(u'map', PyJs_anonymous_218_).callprop(u'join', Js(u'\n'))
    PyJs_toString_217_._set_name(u'toString')
    var.get(u'ContentMatch').get(u'prototype').put(u'toString', PyJs_toString_217_)
    var.get(u'Object').callprop(u'defineProperties', var.get(u'ContentMatch').get(u'prototype'), var.get(u'prototypeAccessors$5'))
    var.get(u'ContentMatch').put(u'empty', var.get(u'ContentMatch').create(Js(True)))
    @Js
    def PyJs_TokenStream_219_(string, nodeTypes, this, arguments, var=var):
        var = Scope({u'this':this, u'TokenStream':PyJs_TokenStream_219_, u'string':string, u'nodeTypes':nodeTypes, u'arguments':arguments}, var)
        var.registers([u'string', u'nodeTypes'])
        var.get(u"this").put(u'string', var.get(u'string'))
        var.get(u"this").put(u'nodeTypes', var.get(u'nodeTypes'))
        var.get(u"this").put(u'inline', var.get(u"null"))
        var.get(u"this").put(u'pos', Js(0.0))
        var.get(u"this").put(u'tokens', var.get(u'string').callprop(u'split', JsRegExp(u'/\\s*(?=\\b|\\W|$)/')))
        if (var.get(u"this").get(u'tokens').get((var.get(u"this").get(u'tokens').get(u'length')-Js(1.0)))==Js(u'')):
            var.get(u"this").get(u'tokens').callprop(u'pop')
        if (var.get(u"this").get(u'tokens').get(u'0')==Js(u'')):
            var.get(u"this").get(u'tokens').callprop(u'unshift')
    PyJs_TokenStream_219_._set_name(u'TokenStream')
    var.put(u'TokenStream', PyJs_TokenStream_219_)
    PyJs_Object_221_ = Js({})
    PyJs_Object_220_ = Js({u'next':PyJs_Object_221_})
    var.put(u'prototypeAccessors$1$3', PyJs_Object_220_)
    @Js
    def PyJs_anonymous_222_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get(u'tokens').get(var.get(u"this").get(u'pos'))
    PyJs_anonymous_222_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$1$3').get(u'next').put(u'get', PyJs_anonymous_222_)
    @Js
    def PyJs_eat_223_(tok, this, arguments, var=var):
        var = Scope({u'this':this, u'tok':tok, u'arguments':arguments, u'eat':PyJs_eat_223_}, var)
        var.registers([u'tok'])
        return ((var.get(u"this").get(u'next')==var.get(u'tok')) and ((var.get(u"this").put(u'pos',Js(var.get(u"this").get(u'pos').to_number())+Js(1))-Js(1)) or Js(True)))
    PyJs_eat_223_._set_name(u'eat')
    var.get(u'TokenStream').get(u'prototype').put(u'eat', PyJs_eat_223_)
    @Js
    def PyJs_err_224_(str, this, arguments, var=var):
        var = Scope({u'this':this, u'err':PyJs_err_224_, u'arguments':arguments, u'str':str}, var)
        var.registers([u'str'])
        PyJsTempException = JsToPyException(var.get(u'SyntaxError').create((((var.get(u'str')+Js(u" (in content expression '"))+var.get(u"this").get(u'string'))+Js(u"')"))))
        raise PyJsTempException
    PyJs_err_224_._set_name(u'err')
    var.get(u'TokenStream').get(u'prototype').put(u'err', PyJs_err_224_)
    var.get(u'Object').callprop(u'defineProperties', var.get(u'TokenStream').get(u'prototype'), var.get(u'prototypeAccessors$1$3'))
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    @Js
    def PyJs_NodeType_240_(name, schema, spec, this, arguments, var=var):
        var = Scope({u'NodeType':PyJs_NodeType_240_, u'name':name, u'this':this, u'arguments':arguments, u'spec':spec, u'schema':schema}, var)
        var.registers([u'spec', u'name', u'schema'])
        var.get(u"this").put(u'name', var.get(u'name'))
        var.get(u"this").put(u'schema', var.get(u'schema'))
        var.get(u"this").put(u'spec', var.get(u'spec'))
        var.get(u"this").put(u'groups', (var.get(u'spec').get(u'group').callprop(u'split', Js(u' ')) if var.get(u'spec').get(u'group') else Js([])))
        var.get(u"this").put(u'attrs', var.get(u'initAttrs')(var.get(u'spec').get(u'attrs')))
        var.get(u"this").put(u'defaultAttrs', var.get(u'defaultAttrs')(var.get(u"this").get(u'attrs')))
        var.get(u"this").put(u'contentMatch', var.get(u"null"))
        var.get(u"this").put(u'markSet', var.get(u"null"))
        var.get(u"this").put(u'inlineContent', var.get(u"null"))
        var.get(u"this").put(u'isBlock', (var.get(u'spec').get(u'inline') or (var.get(u'name')==Js(u'text'))).neg())
        var.get(u"this").put(u'isText', (var.get(u'name')==Js(u'text')))
    PyJs_NodeType_240_._set_name(u'NodeType')
    var.put(u'NodeType', PyJs_NodeType_240_)
    PyJs_Object_242_ = Js({})
    PyJs_Object_243_ = Js({})
    PyJs_Object_244_ = Js({})
    PyJs_Object_245_ = Js({})
    PyJs_Object_241_ = Js({u'isInline':PyJs_Object_242_,u'isTextblock':PyJs_Object_243_,u'isLeaf':PyJs_Object_244_,u'isAtom':PyJs_Object_245_})
    var.put(u'prototypeAccessors$4', PyJs_Object_241_)
    @Js
    def PyJs_anonymous_246_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get(u'isBlock').neg()
    PyJs_anonymous_246_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$4').get(u'isInline').put(u'get', PyJs_anonymous_246_)
    @Js
    def PyJs_anonymous_247_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return (var.get(u"this").get(u'isBlock') and var.get(u"this").get(u'inlineContent'))
    PyJs_anonymous_247_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$4').get(u'isTextblock').put(u'get', PyJs_anonymous_247_)
    @Js
    def PyJs_anonymous_248_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return (var.get(u"this").get(u'contentMatch')==var.get(u'ContentMatch').get(u'empty'))
    PyJs_anonymous_248_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$4').get(u'isLeaf').put(u'get', PyJs_anonymous_248_)
    @Js
    def PyJs_anonymous_249_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return (var.get(u"this").get(u'isLeaf') or var.get(u"this").get(u'spec').get(u'atom'))
    PyJs_anonymous_249_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$4').get(u'isAtom').put(u'get', PyJs_anonymous_249_)
    @Js
    def PyJs_hasRequiredAttrs_250_(ignore, this, arguments, var=var):
        var = Scope({u'ignore':ignore, u'this':this, u'arguments':arguments, u'hasRequiredAttrs':PyJs_hasRequiredAttrs_250_}, var)
        var.registers([u'ignore', u'n', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        for PyJsTemp in var.get(u'this$1').get(u'attrs'):
            var.put(u'n', PyJsTemp)
            if (var.get(u'this$1').get(u'attrs').get(var.get(u'n')).get(u'isRequired') and (var.get(u'ignore').neg() or var.get(u'ignore').contains(var.get(u'n')).neg())):
                return Js(True)
        return Js(False)
    PyJs_hasRequiredAttrs_250_._set_name(u'hasRequiredAttrs')
    var.get(u'NodeType').get(u'prototype').put(u'hasRequiredAttrs', PyJs_hasRequiredAttrs_250_)
    @Js
    def PyJs_compatibleContent_251_(other, this, arguments, var=var):
        var = Scope({u'this':this, u'other':other, u'compatibleContent':PyJs_compatibleContent_251_, u'arguments':arguments}, var)
        var.registers([u'other'])
        return ((var.get(u"this")==var.get(u'other')) or var.get(u"this").get(u'contentMatch').callprop(u'compatible', var.get(u'other').get(u'contentMatch')))
    PyJs_compatibleContent_251_._set_name(u'compatibleContent')
    var.get(u'NodeType').get(u'prototype').put(u'compatibleContent', PyJs_compatibleContent_251_)
    @Js
    def PyJs_InlineNonPyName_252_(attrs, this, arguments, var=var):
        var = Scope({u'this':this, u'attrs':attrs, u'computeAttrs$1':PyJs_InlineNonPyName_252_, u'arguments':arguments}, var)
        var.registers([u'attrs'])
        if (var.get(u'attrs').neg() and var.get(u"this").get(u'defaultAttrs')):
            return var.get(u"this").get(u'defaultAttrs')
        else:
            return var.get(u'computeAttrs')(var.get(u"this").get(u'attrs'), var.get(u'attrs'))
    PyJs_InlineNonPyName_252_._set_name(u'computeAttrs$1')
    var.get(u'NodeType').get(u'prototype').put(u'computeAttrs', PyJs_InlineNonPyName_252_)
    @Js
    def PyJs_create_253_(attrs, content, marks, this, arguments, var=var):
        var = Scope({u'this':this, u'create':PyJs_create_253_, u'content':content, u'attrs':attrs, u'marks':marks, u'arguments':arguments}, var)
        var.registers([u'content', u'attrs', u'marks'])
        if var.get(u"this").get(u'isText'):
            PyJsTempException = JsToPyException(var.get(u'Error').create(Js(u"NodeType.create can't construct text nodes")))
            raise PyJsTempException
        return var.get(u'Node').create(var.get(u"this"), var.get(u"this").callprop(u'computeAttrs', var.get(u'attrs')), var.get(u'Fragment').callprop(u'from', var.get(u'content')), var.get(u'Mark').callprop(u'setFrom', var.get(u'marks')))
    PyJs_create_253_._set_name(u'create')
    var.get(u'NodeType').get(u'prototype').put(u'create', PyJs_create_253_)
    @Js
    def PyJs_createChecked_254_(attrs, content, marks, this, arguments, var=var):
        var = Scope({u'createChecked':PyJs_createChecked_254_, u'this':this, u'content':content, u'attrs':attrs, u'marks':marks, u'arguments':arguments}, var)
        var.registers([u'content', u'attrs', u'marks'])
        var.put(u'content', var.get(u'Fragment').callprop(u'from', var.get(u'content')))
        if var.get(u"this").callprop(u'validContent', var.get(u'content')).neg():
            PyJsTempException = JsToPyException(var.get(u'RangeError').create((Js(u'Invalid content for node ')+var.get(u"this").get(u'name'))))
            raise PyJsTempException
        return var.get(u'Node').create(var.get(u"this"), var.get(u"this").callprop(u'computeAttrs', var.get(u'attrs')), var.get(u'content'), var.get(u'Mark').callprop(u'setFrom', var.get(u'marks')))
    PyJs_createChecked_254_._set_name(u'createChecked')
    var.get(u'NodeType').get(u'prototype').put(u'createChecked', PyJs_createChecked_254_)
    @Js
    def PyJs_createAndFill_255_(attrs, content, marks, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'content':content, u'createAndFill':PyJs_createAndFill_255_, u'marks':marks, u'attrs':attrs}, var)
        var.registers([u'content', u'marks', u'after', u'attrs', u'before'])
        var.put(u'attrs', var.get(u"this").callprop(u'computeAttrs', var.get(u'attrs')))
        var.put(u'content', var.get(u'Fragment').callprop(u'from', var.get(u'content')))
        if var.get(u'content').get(u'size'):
            var.put(u'before', var.get(u"this").get(u'contentMatch').callprop(u'fillBefore', var.get(u'content')))
            if var.get(u'before').neg():
                return var.get(u"null")
            var.put(u'content', var.get(u'before').callprop(u'append', var.get(u'content')))
        var.put(u'after', var.get(u"this").get(u'contentMatch').callprop(u'matchFragment', var.get(u'content')).callprop(u'fillBefore', var.get(u'Fragment').get(u'empty'), Js(True)))
        if var.get(u'after').neg():
            return var.get(u"null")
        return var.get(u'Node').create(var.get(u"this"), var.get(u'attrs'), var.get(u'content').callprop(u'append', var.get(u'after')), var.get(u'Mark').callprop(u'setFrom', var.get(u'marks')))
    PyJs_createAndFill_255_._set_name(u'createAndFill')
    var.get(u'NodeType').get(u'prototype').put(u'createAndFill', PyJs_createAndFill_255_)
    @Js
    def PyJs_validContent_256_(content, this, arguments, var=var):
        var = Scope({u'content':content, u'this':this, u'arguments':arguments, u'validContent':PyJs_validContent_256_}, var)
        var.registers([u'i', u'content', u'result', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        var.put(u'result', var.get(u"this").get(u'contentMatch').callprop(u'matchFragment', var.get(u'content')))
        if (var.get(u'result').neg() or var.get(u'result').get(u'validEnd').neg()):
            return Js(False)
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u'content').get(u'childCount')):
            try:
                if var.get(u'this$1').callprop(u'allowsMarks', var.get(u'content').callprop(u'child', var.get(u'i')).get(u'marks')).neg():
                    return Js(False)
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return Js(True)
    PyJs_validContent_256_._set_name(u'validContent')
    var.get(u'NodeType').get(u'prototype').put(u'validContent', PyJs_validContent_256_)
    @Js
    def PyJs_allowsMarkType_257_(markType, this, arguments, var=var):
        var = Scope({u'this':this, u'markType':markType, u'allowsMarkType':PyJs_allowsMarkType_257_, u'arguments':arguments}, var)
        var.registers([u'markType'])
        return ((var.get(u"this").get(u'markSet')==var.get(u"null")) or (var.get(u"this").get(u'markSet').callprop(u'indexOf', var.get(u'markType'))>(-Js(1.0))))
    PyJs_allowsMarkType_257_._set_name(u'allowsMarkType')
    var.get(u'NodeType').get(u'prototype').put(u'allowsMarkType', PyJs_allowsMarkType_257_)
    @Js
    def PyJs_allowsMarks_258_(marks, this, arguments, var=var):
        var = Scope({u'this':this, u'allowsMarks':PyJs_allowsMarks_258_, u'arguments':arguments, u'marks':marks}, var)
        var.registers([u'i', u'marks', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        if (var.get(u"this").get(u'markSet')==var.get(u"null")):
            return Js(True)
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u'marks').get(u'length')):
            try:
                if var.get(u'this$1').callprop(u'allowsMarkType', var.get(u'marks').get(var.get(u'i')).get(u'type')).neg():
                    return Js(False)
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return Js(True)
    PyJs_allowsMarks_258_._set_name(u'allowsMarks')
    var.get(u'NodeType').get(u'prototype').put(u'allowsMarks', PyJs_allowsMarks_258_)
    @Js
    def PyJs_allowedMarks_259_(marks, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'allowedMarks':PyJs_allowedMarks_259_, u'marks':marks}, var)
        var.registers([u'i', u'marks', u'copy', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        if (var.get(u"this").get(u'markSet')==var.get(u"null")):
            return var.get(u'marks')
        pass
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u'marks').get(u'length')):
            try:
                if var.get(u'this$1').callprop(u'allowsMarkType', var.get(u'marks').get(var.get(u'i')).get(u'type')).neg():
                    if var.get(u'copy').neg():
                        var.put(u'copy', var.get(u'marks').callprop(u'slice', Js(0.0), var.get(u'i')))
                else:
                    if var.get(u'copy'):
                        var.get(u'copy').callprop(u'push', var.get(u'marks').get(var.get(u'i')))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return (var.get(u'marks') if var.get(u'copy').neg() else (var.get(u'copy') if var.get(u'copy').get(u'length') else var.get(u'Mark').get(u'empty')))
    PyJs_allowedMarks_259_._set_name(u'allowedMarks')
    var.get(u'NodeType').get(u'prototype').put(u'allowedMarks', PyJs_allowedMarks_259_)
    @Js
    def PyJs_compile_260_(nodes, schema, this, arguments, var=var):
        var = Scope({u'this':this, u'compile':PyJs_compile_260_, u'nodes':nodes, u'arguments':arguments, u'schema':schema}, var)
        var.registers([u'_', u'nodes', u'result', u'topType', u'schema'])
        var.put(u'result', var.get(u'Object').callprop(u'create', var.get(u"null")))
        @Js
        def PyJs_anonymous_261_(name, spec, this, arguments, var=var):
            var = Scope({u'this':this, u'arguments':arguments, u'name':name, u'spec':spec}, var)
            var.registers([u'name', u'spec'])
            return var.get(u'result').put(var.get(u'name'), var.get(u'NodeType').create(var.get(u'name'), var.get(u'schema'), var.get(u'spec')))
        PyJs_anonymous_261_._set_name(u'anonymous')
        var.get(u'nodes').callprop(u'forEach', PyJs_anonymous_261_)
        var.put(u'topType', (var.get(u'schema').get(u'spec').get(u'topNode') or Js(u'doc')))
        if var.get(u'result').get(var.get(u'topType')).neg():
            PyJsTempException = JsToPyException(var.get(u'RangeError').create(((Js(u"Schema is missing its top node type ('")+var.get(u'topType'))+Js(u"')"))))
            raise PyJsTempException
        if var.get(u'result').get(u'text').neg():
            PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u"Every schema needs a 'text' type")))
            raise PyJsTempException
        for PyJsTemp in var.get(u'result').get(u'text').get(u'attrs'):
            var.put(u'_', PyJsTemp)
            PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'The text node type should not have attributes')))
            raise PyJsTempException
        return var.get(u'result')
    PyJs_compile_260_._set_name(u'compile')
    var.get(u'NodeType').put(u'compile', PyJs_compile_260_)
    var.get(u'Object').callprop(u'defineProperties', var.get(u'NodeType').get(u'prototype'), var.get(u'prototypeAccessors$4'))
    @Js
    def PyJs_Attribute_262_(options, this, arguments, var=var):
        var = Scope({u'this':this, u'Attribute':PyJs_Attribute_262_, u'options':options, u'arguments':arguments}, var)
        var.registers([u'options'])
        var.get(u"this").put(u'hasDefault', var.get(u'Object').get(u'prototype').get(u'hasOwnProperty').callprop(u'call', var.get(u'options'), Js(u'default')))
        var.get(u"this").put(u'default', var.get(u'options').get(u'default'))
    PyJs_Attribute_262_._set_name(u'Attribute')
    var.put(u'Attribute', PyJs_Attribute_262_)
    PyJs_Object_264_ = Js({})
    PyJs_Object_263_ = Js({u'isRequired':PyJs_Object_264_})
    var.put(u'prototypeAccessors$1$2', PyJs_Object_263_)
    @Js
    def PyJs_anonymous_265_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get(u'hasDefault').neg()
    PyJs_anonymous_265_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$1$2').get(u'isRequired').put(u'get', PyJs_anonymous_265_)
    var.get(u'Object').callprop(u'defineProperties', var.get(u'Attribute').get(u'prototype'), var.get(u'prototypeAccessors$1$2'))
    @Js
    def PyJs_MarkType_266_(name, rank, schema, spec, this, arguments, var=var):
        var = Scope({u'name':name, u'this':this, u'arguments':arguments, u'MarkType':PyJs_MarkType_266_, u'spec':spec, u'rank':rank, u'schema':schema}, var)
        var.registers([u'spec', u'rank', u'name', u'defaults', u'schema'])
        var.get(u"this").put(u'name', var.get(u'name'))
        var.get(u"this").put(u'schema', var.get(u'schema'))
        var.get(u"this").put(u'spec', var.get(u'spec'))
        var.get(u"this").put(u'attrs', var.get(u'initAttrs')(var.get(u'spec').get(u'attrs')))
        var.get(u"this").put(u'rank', var.get(u'rank'))
        var.get(u"this").put(u'excluded', var.get(u"null"))
        var.put(u'defaults', var.get(u'defaultAttrs')(var.get(u"this").get(u'attrs')))
        var.get(u"this").put(u'instance', (var.get(u'defaults') and var.get(u'Mark').create(var.get(u"this"), var.get(u'defaults'))))
    PyJs_MarkType_266_._set_name(u'MarkType')
    var.put(u'MarkType', PyJs_MarkType_266_)
    @Js
    def PyJs_create_267_(attrs, this, arguments, var=var):
        var = Scope({u'this':this, u'create':PyJs_create_267_, u'attrs':attrs, u'arguments':arguments}, var)
        var.registers([u'attrs'])
        if (var.get(u'attrs').neg() and var.get(u"this").get(u'instance')):
            return var.get(u"this").get(u'instance')
        return var.get(u'Mark').create(var.get(u"this"), var.get(u'computeAttrs')(var.get(u"this").get(u'attrs'), var.get(u'attrs')))
    PyJs_create_267_._set_name(u'create')
    var.get(u'MarkType').get(u'prototype').put(u'create', PyJs_create_267_)
    @Js
    def PyJs_compile_268_(marks, schema, this, arguments, var=var):
        var = Scope({u'this':this, u'compile':PyJs_compile_268_, u'schema':schema, u'arguments':arguments, u'marks':marks}, var)
        var.registers([u'schema', u'result', u'rank', u'marks'])
        var.put(u'result', var.get(u'Object').callprop(u'create', var.get(u"null")))
        var.put(u'rank', Js(0.0))
        @Js
        def PyJs_anonymous_269_(name, spec, this, arguments, var=var):
            var = Scope({u'this':this, u'arguments':arguments, u'name':name, u'spec':spec}, var)
            var.registers([u'name', u'spec'])
            return var.get(u'result').put(var.get(u'name'), var.get(u'MarkType').create(var.get(u'name'), (var.put(u'rank',Js(var.get(u'rank').to_number())+Js(1))-Js(1)), var.get(u'schema'), var.get(u'spec')))
        PyJs_anonymous_269_._set_name(u'anonymous')
        var.get(u'marks').callprop(u'forEach', PyJs_anonymous_269_)
        return var.get(u'result')
    PyJs_compile_268_._set_name(u'compile')
    var.get(u'MarkType').put(u'compile', PyJs_compile_268_)
    @Js
    def PyJs_removeFromSet_270_(set, this, arguments, var=var):
        var = Scope({u'this':this, u'set':set, u'arguments':arguments, u'removeFromSet':PyJs_removeFromSet_270_}, var)
        var.registers([u'i', u'set', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u'set').get(u'length')):
            try:
                if (var.get(u'set').get(var.get(u'i')).get(u'type')==var.get(u'this$1')):
                    return var.get(u'set').callprop(u'slice', Js(0.0), var.get(u'i')).callprop(u'concat', var.get(u'set').callprop(u'slice', (var.get(u'i')+Js(1.0))))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return var.get(u'set')
    PyJs_removeFromSet_270_._set_name(u'removeFromSet')
    var.get(u'MarkType').get(u'prototype').put(u'removeFromSet', PyJs_removeFromSet_270_)
    @Js
    def PyJs_isInSet_271_(set, this, arguments, var=var):
        var = Scope({u'this':this, u'isInSet':PyJs_isInSet_271_, u'set':set, u'arguments':arguments}, var)
        var.registers([u'i', u'set', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u'set').get(u'length')):
            try:
                if (var.get(u'set').get(var.get(u'i')).get(u'type')==var.get(u'this$1')):
                    return var.get(u'set').get(var.get(u'i'))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
    PyJs_isInSet_271_._set_name(u'isInSet')
    var.get(u'MarkType').get(u'prototype').put(u'isInSet', PyJs_isInSet_271_)
    @Js
    def PyJs_excludes_272_(other, this, arguments, var=var):
        var = Scope({u'this':this, u'excludes':PyJs_excludes_272_, u'other':other, u'arguments':arguments}, var)
        var.registers([u'other'])
        return (var.get(u"this").get(u'excluded').callprop(u'indexOf', var.get(u'other'))>(-Js(1.0)))
    PyJs_excludes_272_._set_name(u'excludes')
    var.get(u'MarkType').get(u'prototype').put(u'excludes', PyJs_excludes_272_)
    @Js
    def PyJs_Schema_273_(spec, this, arguments, var=var):
        var = Scope({u'this':this, u'Schema':PyJs_Schema_273_, u'spec':spec, u'arguments':arguments}, var)
        var.registers([u'contentExprCache', u'prop', u'contentExpr', u'type$1', u'this$1', u'prop$1', u'excl', u'prop$2', u'type', u'spec', u'markExpr'])
        var.put(u'this$1', var.get(u"this"))
        PyJs_Object_274_ = Js({})
        var.get(u"this").put(u'spec', PyJs_Object_274_)
        for PyJsTemp in var.get(u'spec'):
            var.put(u'prop', PyJsTemp)
            var.get(u'this$1').get(u'spec').put(var.get(u'prop'), var.get(u'spec').get(var.get(u'prop')))
        var.get(u"this").get(u'spec').put(u'nodes', var.get(u'OrderedMap').callprop(u'from', var.get(u'spec').get(u'nodes')))
        var.get(u"this").get(u'spec').put(u'marks', var.get(u'OrderedMap').callprop(u'from', var.get(u'spec').get(u'marks')))
        var.get(u"this").put(u'nodes', var.get(u'NodeType').callprop(u'compile', var.get(u"this").get(u'spec').get(u'nodes'), var.get(u"this")))
        var.get(u"this").put(u'marks', var.get(u'MarkType').callprop(u'compile', var.get(u"this").get(u'spec').get(u'marks'), var.get(u"this")))
        var.put(u'contentExprCache', var.get(u'Object').callprop(u'create', var.get(u"null")))
        for PyJsTemp in var.get(u'this$1').get(u'nodes'):
            var.put(u'prop$1', PyJsTemp)
            if var.get(u'this$1').get(u'marks').contains(var.get(u'prop$1')):
                PyJsTempException = JsToPyException(var.get(u'RangeError').create((var.get(u'prop$1')+Js(u' can not be both a node and a mark'))))
                raise PyJsTempException
            var.put(u'type', var.get(u'this$1').get(u'nodes').get(var.get(u'prop$1')))
            var.put(u'contentExpr', (var.get(u'type').get(u'spec').get(u'content') or Js(u'')))
            var.put(u'markExpr', var.get(u'type').get(u'spec').get(u'marks'))
            var.get(u'type').put(u'contentMatch', (var.get(u'contentExprCache').get(var.get(u'contentExpr')) or var.get(u'contentExprCache').put(var.get(u'contentExpr'), var.get(u'ContentMatch').callprop(u'parse', var.get(u'contentExpr'), var.get(u'this$1').get(u'nodes')))))
            var.get(u'type').put(u'inlineContent', var.get(u'type').get(u'contentMatch').get(u'inlineContent'))
            var.get(u'type').put(u'markSet', (var.get(u"null") if (var.get(u'markExpr')==Js(u'_')) else (var.get(u'gatherMarks')(var.get(u'this$1'), var.get(u'markExpr').callprop(u'split', Js(u' '))) if var.get(u'markExpr') else (Js([]) if ((var.get(u'markExpr')==Js(u'')) or var.get(u'type').get(u'inlineContent').neg()) else var.get(u"null")))))
        for PyJsTemp in var.get(u'this$1').get(u'marks'):
            var.put(u'prop$2', PyJsTemp)
            var.put(u'type$1', var.get(u'this$1').get(u'marks').get(var.get(u'prop$2')))
            var.put(u'excl', var.get(u'type$1').get(u'spec').get(u'excludes'))
            var.get(u'type$1').put(u'excluded', (Js([var.get(u'type$1')]) if (var.get(u'excl')==var.get(u"null")) else (Js([]) if (var.get(u'excl')==Js(u'')) else var.get(u'gatherMarks')(var.get(u'this$1'), var.get(u'excl').callprop(u'split', Js(u' '))))))
        var.get(u"this").put(u'nodeFromJSON', var.get(u"this").get(u'nodeFromJSON').callprop(u'bind', var.get(u"this")))
        var.get(u"this").put(u'markFromJSON', var.get(u"this").get(u'markFromJSON').callprop(u'bind', var.get(u"this")))
        var.get(u"this").put(u'topNodeType', var.get(u"this").get(u'nodes').get((var.get(u"this").get(u'spec').get(u'topNode') or Js(u'doc'))))
        var.get(u"this").put(u'cached', var.get(u'Object').callprop(u'create', var.get(u"null")))
        var.get(u"this").get(u'cached').put(u'wrappings', var.get(u'Object').callprop(u'create', var.get(u"null")))
    PyJs_Schema_273_._set_name(u'Schema')
    var.put(u'Schema', PyJs_Schema_273_)
    @Js
    def PyJs_node_275_(type, attrs, content, marks, this, arguments, var=var):
        var = Scope({u'content':content, u'node':PyJs_node_275_, u'attrs':attrs, u'marks':marks, u'this':this, u'type':type, u'arguments':arguments}, var)
        var.registers([u'content', u'type', u'attrs', u'marks'])
        if (var.get(u'type',throw=False).typeof()==Js(u'string')):
            var.put(u'type', var.get(u"this").callprop(u'nodeType', var.get(u'type')))
        else:
            if var.get(u'type').instanceof(var.get(u'NodeType')).neg():
                PyJsTempException = JsToPyException(var.get(u'RangeError').create((Js(u'Invalid node type: ')+var.get(u'type'))))
                raise PyJsTempException
            else:
                if (var.get(u'type').get(u'schema')!=var.get(u"this")):
                    PyJsTempException = JsToPyException(var.get(u'RangeError').create(((Js(u'Node type from different schema used (')+var.get(u'type').get(u'name'))+Js(u')'))))
                    raise PyJsTempException
        return var.get(u'type').callprop(u'createChecked', var.get(u'attrs'), var.get(u'content'), var.get(u'marks'))
    PyJs_node_275_._set_name(u'node')
    var.get(u'Schema').get(u'prototype').put(u'node', PyJs_node_275_)
    @Js
    def PyJs_text_276_(PyJsArg_746578742431_, marks, this, arguments, var=var):
        var = Scope({u'this':this, u'text':PyJs_text_276_, u'arguments':arguments, u'text$1':PyJsArg_746578742431_, u'marks':marks}, var)
        var.registers([u'type', u'text$1', u'marks'])
        var.put(u'type', var.get(u"this").get(u'nodes').get(u'text'))
        return var.get(u'TextNode').create(var.get(u'type'), var.get(u'type').get(u'defaultAttrs'), var.get(u'text$1'), var.get(u'Mark').callprop(u'setFrom', var.get(u'marks')))
    PyJs_text_276_._set_name(u'text')
    var.get(u'Schema').get(u'prototype').put(u'text', PyJs_text_276_)
    @Js
    def PyJs_mark_277_(type, attrs, this, arguments, var=var):
        var = Scope({u'this':this, u'mark':PyJs_mark_277_, u'type':type, u'attrs':attrs, u'arguments':arguments}, var)
        var.registers([u'type', u'attrs'])
        if (var.get(u'type',throw=False).typeof()==Js(u'string')):
            var.put(u'type', var.get(u"this").get(u'marks').get(var.get(u'type')))
        return var.get(u'type').callprop(u'create', var.get(u'attrs'))
    PyJs_mark_277_._set_name(u'mark')
    var.get(u'Schema').get(u'prototype').put(u'mark', PyJs_mark_277_)
    @Js
    def PyJs_nodeFromJSON_278_(json, this, arguments, var=var):
        var = Scope({u'this':this, u'json':json, u'arguments':arguments, u'nodeFromJSON':PyJs_nodeFromJSON_278_}, var)
        var.registers([u'json'])
        return var.get(u'Node').callprop(u'fromJSON', var.get(u"this"), var.get(u'json'))
    PyJs_nodeFromJSON_278_._set_name(u'nodeFromJSON')
    var.get(u'Schema').get(u'prototype').put(u'nodeFromJSON', PyJs_nodeFromJSON_278_)
    @Js
    def PyJs_markFromJSON_279_(json, this, arguments, var=var):
        var = Scope({u'this':this, u'markFromJSON':PyJs_markFromJSON_279_, u'json':json, u'arguments':arguments}, var)
        var.registers([u'json'])
        return var.get(u'Mark').callprop(u'fromJSON', var.get(u"this"), var.get(u'json'))
    PyJs_markFromJSON_279_._set_name(u'markFromJSON')
    var.get(u'Schema').get(u'prototype').put(u'markFromJSON', PyJs_markFromJSON_279_)
    @Js
    def PyJs_nodeType_280_(name, this, arguments, var=var):
        var = Scope({u'this':this, u'nodeType':PyJs_nodeType_280_, u'name':name, u'arguments':arguments}, var)
        var.registers([u'found', u'name'])
        var.put(u'found', var.get(u"this").get(u'nodes').get(var.get(u'name')))
        if var.get(u'found').neg():
            PyJsTempException = JsToPyException(var.get(u'RangeError').create((Js(u'Unknown node type: ')+var.get(u'name'))))
            raise PyJsTempException
        return var.get(u'found')
    PyJs_nodeType_280_._set_name(u'nodeType')
    var.get(u'Schema').get(u'prototype').put(u'nodeType', PyJs_nodeType_280_)
    pass
    @Js
    def PyJs_DOMParser_281_(schema, rules, this, arguments, var=var):
        var = Scope({u'rules':rules, u'this':this, u'DOMParser':PyJs_DOMParser_281_, u'arguments':arguments, u'schema':schema}, var)
        var.registers([u'rules', u'schema', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        var.get(u"this").put(u'schema', var.get(u'schema'))
        var.get(u"this").put(u'rules', var.get(u'rules'))
        var.get(u"this").put(u'tags', Js([]))
        var.get(u"this").put(u'styles', Js([]))
        @Js
        def PyJs_anonymous_282_(rule, this, arguments, var=var):
            var = Scope({u'this':this, u'arguments':arguments, u'rule':rule}, var)
            var.registers([u'rule'])
            if var.get(u'rule').get(u'tag'):
                var.get(u'this$1').get(u'tags').callprop(u'push', var.get(u'rule'))
            else:
                if var.get(u'rule').get(u'style'):
                    var.get(u'this$1').get(u'styles').callprop(u'push', var.get(u'rule'))
        PyJs_anonymous_282_._set_name(u'anonymous')
        var.get(u'rules').callprop(u'forEach', PyJs_anonymous_282_)
    PyJs_DOMParser_281_._set_name(u'DOMParser')
    var.put(u'DOMParser', PyJs_DOMParser_281_)
    @Js
    def PyJs_parse_283_(dom, options, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'parse':PyJs_parse_283_, u'options':options, u'dom':dom}, var)
        var.registers([u'options', u'context', u'dom'])
        if PyJsStrictEq(var.get(u'options'),PyJsComma(Js(0.0), Js(None))):
            PyJs_Object_284_ = Js({})
            var.put(u'options', PyJs_Object_284_)
        var.put(u'context', var.get(u'ParseContext').create(var.get(u"this"), var.get(u'options'), Js(False)))
        var.get(u'context').callprop(u'addAll', var.get(u'dom'), var.get(u"null"), var.get(u'options').get(u'from'), var.get(u'options').get(u'to'))
        return var.get(u'context').callprop(u'finish')
    PyJs_parse_283_._set_name(u'parse')
    var.get(u'DOMParser').get(u'prototype').put(u'parse', PyJs_parse_283_)
    @Js
    def PyJs_parseSlice_285_(dom, options, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'parseSlice':PyJs_parseSlice_285_, u'options':options, u'dom':dom}, var)
        var.registers([u'options', u'context', u'dom'])
        if PyJsStrictEq(var.get(u'options'),PyJsComma(Js(0.0), Js(None))):
            PyJs_Object_286_ = Js({})
            var.put(u'options', PyJs_Object_286_)
        var.put(u'context', var.get(u'ParseContext').create(var.get(u"this"), var.get(u'options'), Js(True)))
        var.get(u'context').callprop(u'addAll', var.get(u'dom'), var.get(u"null"), var.get(u'options').get(u'from'), var.get(u'options').get(u'to'))
        return var.get(u'Slice').callprop(u'maxOpen', var.get(u'context').callprop(u'finish'))
    PyJs_parseSlice_285_._set_name(u'parseSlice')
    var.get(u'DOMParser').get(u'prototype').put(u'parseSlice', PyJs_parseSlice_285_)
    @Js
    def PyJs_matchTag_287_(dom, context, this, arguments, var=var):
        var = Scope({u'this':this, u'matchTag':PyJs_matchTag_287_, u'arguments':arguments, u'context':context, u'dom':dom}, var)
        var.registers([u'dom', u'i', u'rule', u'result', u'context', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u"this").get(u'tags').get(u'length')):
            try:
                var.put(u'rule', var.get(u'this$1').get(u'tags').get(var.get(u'i')))
                if ((var.get(u'matches')(var.get(u'dom'), var.get(u'rule').get(u'tag')) and (PyJsStrictEq(var.get(u'rule').get(u'namespace'),var.get(u'undefined')) or (var.get(u'dom').get(u'namespaceURI')==var.get(u'rule').get(u'namespace')))) and (var.get(u'rule').get(u'context').neg() or var.get(u'context').callprop(u'matchesContext', var.get(u'rule').get(u'context')))):
                    if var.get(u'rule').get(u'getAttrs'):
                        var.put(u'result', var.get(u'rule').callprop(u'getAttrs', var.get(u'dom')))
                        if PyJsStrictEq(var.get(u'result'),Js(False)):
                            continue
                        var.get(u'rule').put(u'attrs', var.get(u'result'))
                    return var.get(u'rule')
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
    PyJs_matchTag_287_._set_name(u'matchTag')
    var.get(u'DOMParser').get(u'prototype').put(u'matchTag', PyJs_matchTag_287_)
    @Js
    def PyJs_matchStyle_288_(prop, value, context, this, arguments, var=var):
        var = Scope({u'this':this, u'matchStyle':PyJs_matchStyle_288_, u'value':value, u'prop':prop, u'arguments':arguments, u'context':context}, var)
        var.registers([u'i', u'rule', u'value', u'prop', u'result', u'context', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u"this").get(u'styles').get(u'length')):
            try:
                var.put(u'rule', var.get(u'this$1').get(u'styles').get(var.get(u'i')))
                def PyJs_LONG_289_(var=var):
                    return (((var.get(u'rule').get(u'style').callprop(u'indexOf', var.get(u'prop'))!=Js(0.0)) or (var.get(u'rule').get(u'context') and var.get(u'context').callprop(u'matchesContext', var.get(u'rule').get(u'context')).neg())) or ((var.get(u'rule').get(u'style').get(u'length')>var.get(u'prop').get(u'length')) and ((var.get(u'rule').get(u'style').callprop(u'charCodeAt', var.get(u'prop').get(u'length'))!=Js(61.0)) or (var.get(u'rule').get(u'style').callprop(u'slice', (var.get(u'prop').get(u'length')+Js(1.0)))!=var.get(u'value')))))
                if PyJs_LONG_289_():
                    continue
                if var.get(u'rule').get(u'getAttrs'):
                    var.put(u'result', var.get(u'rule').callprop(u'getAttrs', var.get(u'value')))
                    if PyJsStrictEq(var.get(u'result'),Js(False)):
                        continue
                    var.get(u'rule').put(u'attrs', var.get(u'result'))
                return var.get(u'rule')
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
    PyJs_matchStyle_288_._set_name(u'matchStyle')
    var.get(u'DOMParser').get(u'prototype').put(u'matchStyle', PyJs_matchStyle_288_)
    @Js
    def PyJs_schemaRules_290_(schema, this, arguments, var=var):
        var = Scope({u'this':this, u'schemaRules':PyJs_schemaRules_290_, u'arguments':arguments, u'schema':schema}, var)
        var.registers([u'insert', u'name$1', u'name', u'loop$1', u'result', u'loop', u'schema'])
        @Js
        def PyJsHoisted_insert_(rule, this, arguments, var=var):
            var = Scope({u'this':this, u'arguments':arguments, u'rule':rule}, var)
            var.registers([u'priority', u'i', u'nextPriority', u'rule', u'next'])
            var.put(u'priority', (Js(50.0) if (var.get(u'rule').get(u'priority')==var.get(u"null")) else var.get(u'rule').get(u'priority')))
            var.put(u'i', Js(0.0))
            #for JS loop
            
            while (var.get(u'i')<var.get(u'result').get(u'length')):
                try:
                    var.put(u'next', var.get(u'result').get(var.get(u'i')))
                    var.put(u'nextPriority', (Js(50.0) if (var.get(u'next').get(u'priority')==var.get(u"null")) else var.get(u'next').get(u'priority')))
                    if (var.get(u'nextPriority')<var.get(u'priority')):
                        break
                finally:
                        (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
            var.get(u'result').callprop(u'splice', var.get(u'i'), Js(0.0), var.get(u'rule'))
        PyJsHoisted_insert_.func_name = u'insert'
        var.put(u'insert', PyJsHoisted_insert_)
        var.put(u'result', Js([]))
        pass
        @Js
        def PyJs_anonymous_291_(name, this, arguments, var=var):
            var = Scope({u'this':this, u'name':name, u'arguments':arguments}, var)
            var.registers([u'rules', u'name'])
            var.put(u'rules', var.get(u'schema').get(u'marks').get(var.get(u'name')).get(u'spec').get(u'parseDOM'))
            if var.get(u'rules'):
                @Js
                def PyJs_anonymous_292_(rule, this, arguments, var=var):
                    var = Scope({u'this':this, u'arguments':arguments, u'rule':rule}, var)
                    var.registers([u'rule'])
                    var.get(u'insert')(var.put(u'rule', var.get(u'copy')(var.get(u'rule'))))
                    var.get(u'rule').put(u'mark', var.get(u'name'))
                PyJs_anonymous_292_._set_name(u'anonymous')
                var.get(u'rules').callprop(u'forEach', PyJs_anonymous_292_)
        PyJs_anonymous_291_._set_name(u'anonymous')
        var.put(u'loop', PyJs_anonymous_291_)
        for PyJsTemp in var.get(u'schema').get(u'marks'):
            var.put(u'name', PyJsTemp)
            var.get(u'loop')(var.get(u'name'))
        @Js
        def PyJs_anonymous_293_(name, this, arguments, var=var):
            var = Scope({u'this':this, u'name':name, u'arguments':arguments}, var)
            var.registers([u'name', u'rules$1'])
            var.put(u'rules$1', var.get(u'schema').get(u'nodes').get(var.get(u'name$1')).get(u'spec').get(u'parseDOM'))
            if var.get(u'rules$1'):
                @Js
                def PyJs_anonymous_294_(rule, this, arguments, var=var):
                    var = Scope({u'this':this, u'arguments':arguments, u'rule':rule}, var)
                    var.registers([u'rule'])
                    var.get(u'insert')(var.put(u'rule', var.get(u'copy')(var.get(u'rule'))))
                    var.get(u'rule').put(u'node', var.get(u'name$1'))
                PyJs_anonymous_294_._set_name(u'anonymous')
                var.get(u'rules$1').callprop(u'forEach', PyJs_anonymous_294_)
        PyJs_anonymous_293_._set_name(u'anonymous')
        var.put(u'loop$1', PyJs_anonymous_293_)
        for PyJsTemp in var.get(u'schema').get(u'nodes'):
            var.put(u'name$1', PyJsTemp)
            var.get(u'loop$1')(var.get(u'name'))
        return var.get(u'result')
    PyJs_schemaRules_290_._set_name(u'schemaRules')
    var.get(u'DOMParser').put(u'schemaRules', PyJs_schemaRules_290_)
    @Js
    def PyJs_fromSchema_295_(schema, this, arguments, var=var):
        var = Scope({u'this':this, u'fromSchema':PyJs_fromSchema_295_, u'arguments':arguments, u'schema':schema}, var)
        var.registers([u'schema'])
        return (var.get(u'schema').get(u'cached').get(u'domParser') or var.get(u'schema').get(u'cached').put(u'domParser', var.get(u'DOMParser').create(var.get(u'schema'), var.get(u'DOMParser').callprop(u'schemaRules', var.get(u'schema')))))
    PyJs_fromSchema_295_._set_name(u'fromSchema')
    var.get(u'DOMParser').put(u'fromSchema', PyJs_fromSchema_295_)
    PyJs_Object_296_ = Js({u'address':Js(True),u'article':Js(True),u'aside':Js(True),u'blockquote':Js(True),u'canvas':Js(True),u'dd':Js(True),u'div':Js(True),u'dl':Js(True),u'fieldset':Js(True),u'figcaption':Js(True),u'figure':Js(True),u'footer':Js(True),u'form':Js(True),u'h1':Js(True),u'h2':Js(True),u'h3':Js(True),u'h4':Js(True),u'h5':Js(True),u'h6':Js(True),u'header':Js(True),u'hgroup':Js(True),u'hr':Js(True),u'li':Js(True),u'noscript':Js(True),u'ol':Js(True),u'output':Js(True),u'p':Js(True),u'pre':Js(True),u'section':Js(True),u'table':Js(True),u'tfoot':Js(True),u'ul':Js(True)})
    var.put(u'blockTags', PyJs_Object_296_)
    PyJs_Object_297_ = Js({u'head':Js(True),u'noscript':Js(True),u'object':Js(True),u'script':Js(True),u'style':Js(True),u'title':Js(True)})
    var.put(u'ignoreTags', PyJs_Object_297_)
    PyJs_Object_298_ = Js({u'ol':Js(True),u'ul':Js(True)})
    var.put(u'listTags', PyJs_Object_298_)
    var.put(u'OPT_PRESERVE_WS', Js(1.0))
    var.put(u'OPT_PRESERVE_WS_FULL', Js(2.0))
    var.put(u'OPT_OPEN_LEFT', Js(4.0))
    pass
    @Js
    def PyJs_NodeContext_299_(type, attrs, marks, solid, match, options, this, arguments, var=var):
        var = Scope({u'solid':solid, u'NodeContext':PyJs_NodeContext_299_, u'this':this, u'attrs':attrs, u'marks':marks, u'type':type, u'options':options, u'match':match, u'arguments':arguments}, var)
        var.registers([u'solid', u'attrs', u'marks', u'type', u'options', u'match'])
        var.get(u"this").put(u'type', var.get(u'type'))
        var.get(u"this").put(u'attrs', var.get(u'attrs'))
        var.get(u"this").put(u'solid', var.get(u'solid'))
        var.get(u"this").put(u'match', (var.get(u'match') or (var.get(u"null") if (var.get(u'options')&var.get(u'OPT_OPEN_LEFT')) else var.get(u'type').get(u'contentMatch'))))
        var.get(u"this").put(u'options', var.get(u'options'))
        var.get(u"this").put(u'content', Js([]))
        var.get(u"this").put(u'marks', var.get(u'marks'))
        var.get(u"this").put(u'activeMarks', var.get(u'Mark').get(u'none'))
    PyJs_NodeContext_299_._set_name(u'NodeContext')
    var.put(u'NodeContext', PyJs_NodeContext_299_)
    @Js
    def PyJs_findWrapping_300_(node, this, arguments, var=var):
        var = Scope({u'node':node, u'this':this, u'arguments':arguments, u'findWrapping':PyJs_findWrapping_300_}, var)
        var.registers([u'wrap', u'start', u'node', u'fill'])
        if var.get(u"this").get(u'match').neg():
            if var.get(u"this").get(u'type').neg():
                return Js([])
            var.put(u'fill', var.get(u"this").get(u'type').get(u'contentMatch').callprop(u'fillBefore', var.get(u'Fragment').callprop(u'from', var.get(u'node'))))
            if var.get(u'fill'):
                var.get(u"this").put(u'match', var.get(u"this").get(u'type').get(u'contentMatch').callprop(u'matchFragment', var.get(u'fill')))
            else:
                var.put(u'start', var.get(u"this").get(u'type').get(u'contentMatch'))
                if var.put(u'wrap', var.get(u'start').callprop(u'findWrapping', var.get(u'node').get(u'type'))):
                    var.get(u"this").put(u'match', var.get(u'start'))
                    return var.get(u'wrap')
                else:
                    return var.get(u"null")
        return var.get(u"this").get(u'match').callprop(u'findWrapping', var.get(u'node').get(u'type'))
    PyJs_findWrapping_300_._set_name(u'findWrapping')
    var.get(u'NodeContext').get(u'prototype').put(u'findWrapping', PyJs_findWrapping_300_)
    @Js
    def PyJs_finish_301_(openEnd, this, arguments, var=var):
        var = Scope({u'openEnd':openEnd, u'this':this, u'finish':PyJs_finish_301_, u'arguments':arguments}, var)
        var.registers([u'content', u'm', u'last', u'openEnd'])
        if (var.get(u"this").get(u'options')&var.get(u'OPT_PRESERVE_WS')).neg():
            var.put(u'last', var.get(u"this").get(u'content').get((var.get(u"this").get(u'content').get(u'length')-Js(1.0))))
            if ((var.get(u'last') and var.get(u'last').get(u'isText')) and var.put(u'm', JsRegExp(u'/\\s+$/').callprop(u'exec', var.get(u'last').get(u'text')))):
                if (var.get(u'last').get(u'text').get(u'length')==var.get(u'm').get(u'0').get(u'length')):
                    var.get(u"this").get(u'content').callprop(u'pop')
                else:
                    var.get(u"this").get(u'content').put((var.get(u"this").get(u'content').get(u'length')-Js(1.0)), var.get(u'last').callprop(u'withText', var.get(u'last').get(u'text').callprop(u'slice', Js(0.0), (var.get(u'last').get(u'text').get(u'length')-var.get(u'm').get(u'0').get(u'length')))))
        var.put(u'content', var.get(u'Fragment').callprop(u'from', var.get(u"this").get(u'content')))
        if (var.get(u'openEnd').neg() and var.get(u"this").get(u'match')):
            var.put(u'content', var.get(u'content').callprop(u'append', var.get(u"this").get(u'match').callprop(u'fillBefore', var.get(u'Fragment').get(u'empty'), Js(True))))
        return (var.get(u"this").get(u'type').callprop(u'create', var.get(u"this").get(u'attrs'), var.get(u'content'), var.get(u"this").get(u'marks')) if var.get(u"this").get(u'type') else var.get(u'content'))
    PyJs_finish_301_._set_name(u'finish')
    var.get(u'NodeContext').get(u'prototype').put(u'finish', PyJs_finish_301_)
    @Js
    def PyJs_ParseContext_302_(parser, options, open, this, arguments, var=var):
        var = Scope({u'this':this, u'parser':parser, u'arguments':arguments, u'open':open, u'options':options, u'ParseContext':PyJs_ParseContext_302_}, var)
        var.registers([u'parser', u'topContext', u'open', u'options', u'topNode', u'topOptions'])
        var.get(u"this").put(u'parser', var.get(u'parser'))
        var.get(u"this").put(u'options', var.get(u'options'))
        var.get(u"this").put(u'isOpen', var.get(u'open'))
        var.get(u"this").put(u'pendingMarks', Js([]))
        var.put(u'topNode', var.get(u'options').get(u'topNode'))
        var.put(u'topOptions', (var.get(u'wsOptionsFor')(var.get(u'options').get(u'preserveWhitespace'))|(var.get(u'OPT_OPEN_LEFT') if var.get(u'open') else Js(0.0))))
        if var.get(u'topNode'):
            var.put(u'topContext', var.get(u'NodeContext').create(var.get(u'topNode').get(u'type'), var.get(u'topNode').get(u'attrs'), var.get(u'Mark').get(u'none'), Js(True), (var.get(u'options').get(u'topMatch') or var.get(u'topNode').get(u'type').get(u'contentMatch')), var.get(u'topOptions')))
        else:
            if var.get(u'open'):
                var.put(u'topContext', var.get(u'NodeContext').create(var.get(u"null"), var.get(u"null"), var.get(u'Mark').get(u'none'), Js(True), var.get(u"null"), var.get(u'topOptions')))
            else:
                var.put(u'topContext', var.get(u'NodeContext').create(var.get(u'parser').get(u'schema').get(u'topNodeType'), var.get(u"null"), var.get(u'Mark').get(u'none'), Js(True), var.get(u"null"), var.get(u'topOptions')))
        var.get(u"this").put(u'nodes', Js([var.get(u'topContext')]))
        var.get(u"this").put(u'open', Js(0.0))
        var.get(u"this").put(u'find', var.get(u'options').get(u'findPositions'))
        var.get(u"this").put(u'needsBlock', Js(False))
    PyJs_ParseContext_302_._set_name(u'ParseContext')
    var.put(u'ParseContext', PyJs_ParseContext_302_)
    PyJs_Object_304_ = Js({})
    PyJs_Object_305_ = Js({})
    PyJs_Object_303_ = Js({u'top':PyJs_Object_304_,u'currentPos':PyJs_Object_305_})
    var.put(u'prototypeAccessors$6', PyJs_Object_303_)
    @Js
    def PyJs_anonymous_306_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u"this").get(u'nodes').get(var.get(u"this").get(u'open'))
    PyJs_anonymous_306_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$6').get(u'top').put(u'get', PyJs_anonymous_306_)
    @Js
    def PyJs_addDOM_307_(dom, this, arguments, var=var):
        var = Scope({u'this':this, u'addDOM':PyJs_addDOM_307_, u'arguments':arguments, u'dom':dom}, var)
        var.registers([u'style', u'dom', u'i', u'this$1', u'i$1', u'marks'])
        var.put(u'this$1', var.get(u"this"))
        if (var.get(u'dom').get(u'nodeType')==Js(3.0)):
            var.get(u"this").callprop(u'addTextNode', var.get(u'dom'))
        else:
            if (var.get(u'dom').get(u'nodeType')==Js(1.0)):
                var.put(u'style', var.get(u'dom').callprop(u'getAttribute', Js(u'style')))
                var.put(u'marks', (var.get(u"this").callprop(u'readStyles', var.get(u'parseStyles')(var.get(u'style'))) if var.get(u'style') else var.get(u"null")))
                if (var.get(u'marks')!=var.get(u"null")):
                    #for JS loop
                    var.put(u'i', Js(0.0))
                    while (var.get(u'i')<var.get(u'marks').get(u'length')):
                        try:
                            var.get(u'this$1').callprop(u'addPendingMark', var.get(u'marks').get(var.get(u'i')))
                        finally:
                                (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
                var.get(u"this").callprop(u'addElement', var.get(u'dom'))
                if (var.get(u'marks')!=var.get(u"null")):
                    #for JS loop
                    var.put(u'i$1', Js(0.0))
                    while (var.get(u'i$1')<var.get(u'marks').get(u'length')):
                        try:
                            var.get(u'this$1').callprop(u'removePendingMark', var.get(u'marks').get(var.get(u'i$1')))
                        finally:
                                (var.put(u'i$1',Js(var.get(u'i$1').to_number())+Js(1))-Js(1))
    PyJs_addDOM_307_._set_name(u'addDOM')
    var.get(u'ParseContext').get(u'prototype').put(u'addDOM', PyJs_addDOM_307_)
    @Js
    def PyJs_addTextNode_308_(dom, this, arguments, var=var):
        var = Scope({u'this':this, u'addTextNode':PyJs_addTextNode_308_, u'arguments':arguments, u'dom':dom}, var)
        var.registers([u'top', u'dom', u'domNodeBefore', u'value', u'nodeBefore'])
        var.put(u'value', var.get(u'dom').get(u'nodeValue'))
        var.put(u'top', var.get(u"this").get(u'top'))
        if ((var.get(u'top').get(u'type').get(u'inlineContent') if var.get(u'top').get(u'type') else (var.get(u'top').get(u'content').get(u'length') and var.get(u'top').get(u'content').get(u'0').get(u'isInline'))) or JsRegExp(u'/\\S/').callprop(u'test', var.get(u'value'))):
            if (var.get(u'top').get(u'options')&var.get(u'OPT_PRESERVE_WS')).neg():
                var.put(u'value', var.get(u'value').callprop(u'replace', JsRegExp(u'/\\s+/g'), Js(u' ')))
                if (JsRegExp(u'/^\\s/').callprop(u'test', var.get(u'value')) and (var.get(u"this").get(u'open')==(var.get(u"this").get(u'nodes').get(u'length')-Js(1.0)))):
                    var.put(u'nodeBefore', var.get(u'top').get(u'content').get((var.get(u'top').get(u'content').get(u'length')-Js(1.0))))
                    var.put(u'domNodeBefore', var.get(u'dom').get(u'previousSibling'))
                    if ((var.get(u'nodeBefore').neg() or (var.get(u'domNodeBefore') and (var.get(u'domNodeBefore').get(u'nodeName')==Js(u'BR')))) or (var.get(u'nodeBefore').get(u'isText') and JsRegExp(u'/\\s$/').callprop(u'test', var.get(u'nodeBefore').get(u'text')))):
                        var.put(u'value', var.get(u'value').callprop(u'slice', Js(1.0)))
            else:
                if (var.get(u'top').get(u'options')&var.get(u'OPT_PRESERVE_WS_FULL')).neg():
                    var.put(u'value', var.get(u'value').callprop(u'replace', JsRegExp(u'/\\r?\\n|\\r/g'), Js(u' ')))
            if var.get(u'value'):
                var.get(u"this").callprop(u'insertNode', var.get(u"this").get(u'parser').get(u'schema').callprop(u'text', var.get(u'value')))
            var.get(u"this").callprop(u'findInText', var.get(u'dom'))
        else:
            var.get(u"this").callprop(u'findInside', var.get(u'dom'))
    PyJs_addTextNode_308_._set_name(u'addTextNode')
    var.get(u'ParseContext').get(u'prototype').put(u'addTextNode', PyJs_addTextNode_308_)
    @Js
    def PyJs_addElement_309_(dom, this, arguments, var=var):
        var = Scope({u'this':this, u'addElement':PyJs_addElement_309_, u'arguments':arguments, u'dom':dom}, var)
        var.registers([u'name', u'dom', u'top', u'sync', u'rule', u'oldNeedsBlock'])
        var.put(u'name', var.get(u'dom').get(u'nodeName').callprop(u'toLowerCase'))
        if var.get(u'listTags').callprop(u'hasOwnProperty', var.get(u'name')):
            var.get(u'normalizeList')(var.get(u'dom'))
        var.put(u'rule', ((var.get(u"this").get(u'options').get(u'ruleFromNode') and var.get(u"this").get(u'options').callprop(u'ruleFromNode', var.get(u'dom'))) or var.get(u"this").get(u'parser').callprop(u'matchTag', var.get(u'dom'), var.get(u"this"))))
        if (var.get(u'rule').get(u'ignore') if var.get(u'rule') else var.get(u'ignoreTags').callprop(u'hasOwnProperty', var.get(u'name'))):
            var.get(u"this").callprop(u'findInside', var.get(u'dom'))
        else:
            if (var.get(u'rule').neg() or var.get(u'rule').get(u'skip')):
                if (var.get(u'rule') and var.get(u'rule').get(u'skip').get(u'nodeType')):
                    var.put(u'dom', var.get(u'rule').get(u'skip'))
                var.put(u'top', var.get(u"this").get(u'top'))
                var.put(u'oldNeedsBlock', var.get(u"this").get(u'needsBlock'))
                if var.get(u'blockTags').callprop(u'hasOwnProperty', var.get(u'name')):
                    var.put(u'sync', Js(True))
                    if var.get(u'top').get(u'type').neg():
                        var.get(u"this").put(u'needsBlock', Js(True))
                var.get(u"this").callprop(u'addAll', var.get(u'dom'))
                if var.get(u'sync'):
                    var.get(u"this").callprop(u'sync', var.get(u'top'))
                var.get(u"this").put(u'needsBlock', var.get(u'oldNeedsBlock'))
            else:
                var.get(u"this").callprop(u'addElementByRule', var.get(u'dom'), var.get(u'rule'))
    PyJs_addElement_309_._set_name(u'addElement')
    var.get(u'ParseContext').get(u'prototype').put(u'addElement', PyJs_addElement_309_)
    @Js
    def PyJs_readStyles_310_(styles, this, arguments, var=var):
        var = Scope({u'styles':styles, u'this':this, u'readStyles':PyJs_readStyles_310_, u'arguments':arguments}, var)
        var.registers([u'i', u'styles', u'marks', u'rule', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        var.put(u'marks', var.get(u'Mark').get(u'none'))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u'styles').get(u'length')):
            try:
                var.put(u'rule', var.get(u'this$1').get(u'parser').callprop(u'matchStyle', var.get(u'styles').get(var.get(u'i')), var.get(u'styles').get((var.get(u'i')+Js(1.0))), var.get(u'this$1')))
                if var.get(u'rule').neg():
                    continue
                if var.get(u'rule').get(u'ignore'):
                    return var.get(u"null")
                var.put(u'marks', var.get(u'this$1').get(u'parser').get(u'schema').get(u'marks').get(var.get(u'rule').get(u'mark')).callprop(u'create', var.get(u'rule').get(u'attrs')).callprop(u'addToSet', var.get(u'marks')))
            finally:
                    var.put(u'i', Js(2.0), u'+')
        return var.get(u'marks')
    PyJs_readStyles_310_._set_name(u'readStyles')
    var.get(u'ParseContext').get(u'prototype').put(u'readStyles', PyJs_readStyles_310_)
    @Js
    def PyJs_addElementByRule_311_(dom, rule, this, arguments, var=var):
        var = Scope({u'this':this, u'addElementByRule':PyJs_addElementByRule_311_, u'arguments':arguments, u'rule':rule, u'dom':dom}, var)
        var.registers([u'contentDOM', u'nodeType', u'dom', u'markType', u'sync', u'rule', u'mark', u'startIn', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        pass
        if var.get(u'rule').get(u'node'):
            var.put(u'nodeType', var.get(u"this").get(u'parser').get(u'schema').get(u'nodes').get(var.get(u'rule').get(u'node')))
            if var.get(u'nodeType').get(u'isLeaf'):
                var.get(u"this").callprop(u'insertNode', var.get(u'nodeType').callprop(u'create', var.get(u'rule').get(u'attrs')))
            else:
                var.put(u'sync', var.get(u"this").callprop(u'enter', var.get(u'nodeType'), var.get(u'rule').get(u'attrs'), var.get(u'rule').get(u'preserveWhitespace')))
        else:
            var.put(u'markType', var.get(u"this").get(u'parser').get(u'schema').get(u'marks').get(var.get(u'rule').get(u'mark')))
            var.put(u'mark', var.get(u'markType').callprop(u'create', var.get(u'rule').get(u'attrs')))
            var.get(u"this").callprop(u'addPendingMark', var.get(u'mark'))
        var.put(u'startIn', var.get(u"this").get(u'top'))
        if (var.get(u'nodeType') and var.get(u'nodeType').get(u'isLeaf')):
            var.get(u"this").callprop(u'findInside', var.get(u'dom'))
        else:
            if var.get(u'rule').get(u'getContent'):
                var.get(u"this").callprop(u'findInside', var.get(u'dom'))
                @Js
                def PyJs_anonymous_312_(node, this, arguments, var=var):
                    var = Scope({u'node':node, u'this':this, u'arguments':arguments}, var)
                    var.registers([u'node'])
                    return var.get(u'this$1').callprop(u'insertNode', var.get(u'node'))
                PyJs_anonymous_312_._set_name(u'anonymous')
                var.get(u'rule').callprop(u'getContent', var.get(u'dom'), var.get(u"this").get(u'parser').get(u'schema')).callprop(u'forEach', PyJs_anonymous_312_)
            else:
                var.put(u'contentDOM', var.get(u'rule').get(u'contentElement'))
                if (var.get(u'contentDOM',throw=False).typeof()==Js(u'string')):
                    var.put(u'contentDOM', var.get(u'dom').callprop(u'querySelector', var.get(u'contentDOM')))
                else:
                    if (var.get(u'contentDOM',throw=False).typeof()==Js(u'function')):
                        var.put(u'contentDOM', var.get(u'contentDOM')(var.get(u'dom')))
                if var.get(u'contentDOM').neg():
                    var.put(u'contentDOM', var.get(u'dom'))
                var.get(u"this").callprop(u'findAround', var.get(u'dom'), var.get(u'contentDOM'), Js(True))
                var.get(u"this").callprop(u'addAll', var.get(u'contentDOM'), var.get(u'sync'))
        if var.get(u'sync'):
            var.get(u"this").callprop(u'sync', var.get(u'startIn'))
            (var.get(u"this").put(u'open',Js(var.get(u"this").get(u'open').to_number())-Js(1))+Js(1))
        if var.get(u'mark'):
            var.get(u"this").callprop(u'removePendingMark', var.get(u'mark'))
        return Js(True)
    PyJs_addElementByRule_311_._set_name(u'addElementByRule')
    var.get(u'ParseContext').get(u'prototype').put(u'addElementByRule', PyJs_addElementByRule_311_)
    @Js
    def PyJs_addAll_313_(parent, sync, startIndex, endIndex, this, arguments, var=var):
        var = Scope({u'endIndex':endIndex, u'startIndex':startIndex, u'addAll':PyJs_addAll_313_, u'arguments':arguments, u'parent':parent, u'this':this, u'sync':sync}, var)
        var.registers([u'index', u'endIndex', u'end', u'parent', u'dom', u'sync', u'startIndex', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        var.put(u'index', (var.get(u'startIndex') or Js(0.0)))
        #for JS loop
        var.put(u'dom', (var.get(u'parent').get(u'childNodes').get(var.get(u'startIndex')) if var.get(u'startIndex') else var.get(u'parent').get(u'firstChild')))
        var.put(u'end', (var.get(u"null") if (var.get(u'endIndex')==var.get(u"null")) else var.get(u'parent').get(u'childNodes').get(var.get(u'endIndex'))))
        while (var.get(u'dom')!=var.get(u'end')):
            try:
                var.get(u'this$1').callprop(u'findAtPoint', var.get(u'parent'), var.get(u'index'))
                var.get(u'this$1').callprop(u'addDOM', var.get(u'dom'))
                if (var.get(u'sync') and var.get(u'blockTags').callprop(u'hasOwnProperty', var.get(u'dom').get(u'nodeName').callprop(u'toLowerCase'))):
                    var.get(u'this$1').callprop(u'sync', var.get(u'sync'))
            finally:
                    PyJsComma(var.put(u'dom', var.get(u'dom').get(u'nextSibling')),var.put(u'index',Js(var.get(u'index').to_number())+Js(1)))
        var.get(u"this").callprop(u'findAtPoint', var.get(u'parent'), var.get(u'index'))
    PyJs_addAll_313_._set_name(u'addAll')
    var.get(u'ParseContext').get(u'prototype').put(u'addAll', PyJs_addAll_313_)
    @Js
    def PyJs_findPlace_314_(node, this, arguments, var=var):
        var = Scope({u'node':node, u'this':this, u'arguments':arguments, u'findPlace':PyJs_findPlace_314_}, var)
        var.registers([u'node', u'i', u'route', u'sync', u'depth', u'cx', u'this$1', u'found'])
        var.put(u'this$1', var.get(u"this"))
        pass
        #for JS loop
        var.put(u'depth', var.get(u"this").get(u'open'))
        while (var.get(u'depth')>=Js(0.0)):
            try:
                var.put(u'cx', var.get(u'this$1').get(u'nodes').get(var.get(u'depth')))
                var.put(u'found', var.get(u'cx').callprop(u'findWrapping', var.get(u'node')))
                if (var.get(u'found') and (var.get(u'route').neg() or (var.get(u'route').get(u'length')>var.get(u'found').get(u'length')))):
                    var.put(u'route', var.get(u'found'))
                    var.put(u'sync', var.get(u'cx'))
                    if var.get(u'found').get(u'length').neg():
                        break
                if var.get(u'cx').get(u'solid'):
                    break
            finally:
                    (var.put(u'depth',Js(var.get(u'depth').to_number())-Js(1))+Js(1))
        if var.get(u'route').neg():
            return Js(False)
        var.get(u"this").callprop(u'sync', var.get(u'sync'))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u'route').get(u'length')):
            try:
                var.get(u'this$1').callprop(u'enterInner', var.get(u'route').get(var.get(u'i')), var.get(u"null"), Js(False))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return Js(True)
    PyJs_findPlace_314_._set_name(u'findPlace')
    var.get(u'ParseContext').get(u'prototype').put(u'findPlace', PyJs_findPlace_314_)
    @Js
    def PyJs_insertNode_315_(node, this, arguments, var=var):
        var = Scope({u'node':node, u'this':this, u'arguments':arguments, u'insertNode':PyJs_insertNode_315_}, var)
        var.registers([u'i', u'node', u'top', u'block', u'marks'])
        if ((var.get(u'node').get(u'isInline') and var.get(u"this").get(u'needsBlock')) and var.get(u"this").get(u'top').get(u'type').neg()):
            var.put(u'block', var.get(u"this").callprop(u'textblockFromContext'))
            if var.get(u'block'):
                var.get(u"this").callprop(u'enterInner', var.get(u'block'))
        if var.get(u"this").callprop(u'findPlace', var.get(u'node')):
            var.get(u"this").callprop(u'closeExtra')
            var.put(u'top', var.get(u"this").get(u'top'))
            var.get(u"this").callprop(u'applyPendingMarks', var.get(u'top'))
            if var.get(u'top').get(u'match'):
                var.get(u'top').put(u'match', var.get(u'top').get(u'match').callprop(u'matchType', var.get(u'node').get(u'type')))
            var.put(u'marks', var.get(u'top').get(u'activeMarks'))
            #for JS loop
            var.put(u'i', Js(0.0))
            while (var.get(u'i')<var.get(u'node').get(u'marks').get(u'length')):
                try:
                    if (var.get(u'top').get(u'type').neg() or var.get(u'top').get(u'type').callprop(u'allowsMarkType', var.get(u'node').get(u'marks').get(var.get(u'i')).get(u'type'))):
                        var.put(u'marks', var.get(u'node').get(u'marks').get(var.get(u'i')).callprop(u'addToSet', var.get(u'marks')))
                finally:
                        (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
            var.get(u'top').get(u'content').callprop(u'push', var.get(u'node').callprop(u'mark', var.get(u'marks')))
    PyJs_insertNode_315_._set_name(u'insertNode')
    var.get(u'ParseContext').get(u'prototype').put(u'insertNode', PyJs_insertNode_315_)
    @Js
    def PyJs_applyPendingMarks_316_(top, this, arguments, var=var):
        var = Scope({u'this':this, u'applyPendingMarks':PyJs_applyPendingMarks_316_, u'top':top, u'arguments':arguments}, var)
        var.registers([u'i', u'top', u'mark', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u"this").get(u'pendingMarks').get(u'length')):
            try:
                var.put(u'mark', var.get(u'this$1').get(u'pendingMarks').get(var.get(u'i')))
                if ((var.get(u'top').get(u'type').neg() or var.get(u'top').get(u'type').callprop(u'allowsMarkType', var.get(u'mark').get(u'type'))) and var.get(u'mark').get(u'type').callprop(u'isInSet', var.get(u'top').get(u'activeMarks')).neg()):
                    var.get(u'top').put(u'activeMarks', var.get(u'mark').callprop(u'addToSet', var.get(u'top').get(u'activeMarks')))
                    var.get(u'this$1').get(u'pendingMarks').callprop(u'splice', (var.put(u'i',Js(var.get(u'i').to_number())-Js(1))+Js(1)), Js(1.0))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
    PyJs_applyPendingMarks_316_._set_name(u'applyPendingMarks')
    var.get(u'ParseContext').get(u'prototype').put(u'applyPendingMarks', PyJs_applyPendingMarks_316_)
    @Js
    def PyJs_enter_317_(type, attrs, preserveWS, this, arguments, var=var):
        var = Scope({u'this':this, u'preserveWS':preserveWS, u'attrs':attrs, u'enter':PyJs_enter_317_, u'type':type, u'arguments':arguments}, var)
        var.registers([u'type', u'preserveWS', u'ok', u'attrs'])
        var.put(u'ok', var.get(u"this").callprop(u'findPlace', var.get(u'type').callprop(u'create', var.get(u'attrs'))))
        if var.get(u'ok'):
            var.get(u"this").callprop(u'applyPendingMarks', var.get(u"this").get(u'top'))
            var.get(u"this").callprop(u'enterInner', var.get(u'type'), var.get(u'attrs'), Js(True), var.get(u'preserveWS'))
        return var.get(u'ok')
    PyJs_enter_317_._set_name(u'enter')
    var.get(u'ParseContext').get(u'prototype').put(u'enter', PyJs_enter_317_)
    @Js
    def PyJs_enterInner_318_(type, attrs, solid, preserveWS, this, arguments, var=var):
        var = Scope({u'this':this, u'enterInner':PyJs_enterInner_318_, u'preserveWS':preserveWS, u'attrs':attrs, u'solid':solid, u'type':type, u'arguments':arguments}, var)
        var.registers([u'solid', u'top', u'preserveWS', u'attrs', u'type', u'options'])
        var.get(u"this").callprop(u'closeExtra')
        var.put(u'top', var.get(u"this").get(u'top'))
        var.get(u'top').put(u'match', (var.get(u'top').get(u'match') and var.get(u'top').get(u'match').callprop(u'matchType', var.get(u'type'), var.get(u'attrs'))))
        var.put(u'options', ((var.get(u'top').get(u'options')&(~var.get(u'OPT_OPEN_LEFT'))) if (var.get(u'preserveWS')==var.get(u"null")) else var.get(u'wsOptionsFor')(var.get(u'preserveWS'))))
        if ((var.get(u'top').get(u'options')&var.get(u'OPT_OPEN_LEFT')) and (var.get(u'top').get(u'content').get(u'length')==Js(0.0))):
            var.put(u'options', var.get(u'OPT_OPEN_LEFT'), u'|')
        var.get(u"this").get(u'nodes').callprop(u'push', var.get(u'NodeContext').create(var.get(u'type'), var.get(u'attrs'), var.get(u'top').get(u'activeMarks'), var.get(u'solid'), var.get(u"null"), var.get(u'options')))
        (var.get(u"this").put(u'open',Js(var.get(u"this").get(u'open').to_number())+Js(1))-Js(1))
    PyJs_enterInner_318_._set_name(u'enterInner')
    var.get(u'ParseContext').get(u'prototype').put(u'enterInner', PyJs_enterInner_318_)
    @Js
    def PyJs_closeExtra_319_(openEnd, this, arguments, var=var):
        var = Scope({u'openEnd':openEnd, u'this':this, u'closeExtra':PyJs_closeExtra_319_, u'arguments':arguments}, var)
        var.registers([u'i', u'openEnd', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        var.put(u'i', (var.get(u"this").get(u'nodes').get(u'length')-Js(1.0)))
        if (var.get(u'i')>var.get(u"this").get(u'open')):
            #for JS loop
            
            while (var.get(u'i')>var.get(u"this").get(u'open')):
                try:
                    var.get(u'this$1').get(u'nodes').get((var.get(u'i')-Js(1.0))).get(u'content').callprop(u'push', var.get(u'this$1').get(u'nodes').get(var.get(u'i')).callprop(u'finish', var.get(u'openEnd')))
                finally:
                        (var.put(u'i',Js(var.get(u'i').to_number())-Js(1))+Js(1))
            var.get(u"this").get(u'nodes').put(u'length', (var.get(u"this").get(u'open')+Js(1.0)))
    PyJs_closeExtra_319_._set_name(u'closeExtra')
    var.get(u'ParseContext').get(u'prototype').put(u'closeExtra', PyJs_closeExtra_319_)
    @Js
    def PyJs_finish_320_(this, arguments, var=var):
        var = Scope({u'this':this, u'finish':PyJs_finish_320_, u'arguments':arguments}, var)
        var.registers([])
        var.get(u"this").put(u'open', Js(0.0))
        var.get(u"this").callprop(u'closeExtra', var.get(u"this").get(u'isOpen'))
        return var.get(u"this").get(u'nodes').get(u'0').callprop(u'finish', (var.get(u"this").get(u'isOpen') or var.get(u"this").get(u'options').get(u'topOpen')))
    PyJs_finish_320_._set_name(u'finish')
    var.get(u'ParseContext').get(u'prototype').put(u'finish', PyJs_finish_320_)
    @Js
    def PyJs_sync_321_(to, this, arguments, var=var):
        var = Scope({u'this':this, u'to':to, u'arguments':arguments, u'sync':PyJs_sync_321_}, var)
        var.registers([u'i', u'to', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        #for JS loop
        var.put(u'i', var.get(u"this").get(u'open'))
        while (var.get(u'i')>=Js(0.0)):
            try:
                if (var.get(u'this$1').get(u'nodes').get(var.get(u'i'))==var.get(u'to')):
                    var.get(u'this$1').put(u'open', var.get(u'i'))
                    return var.get('undefined')
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())-Js(1))+Js(1))
    PyJs_sync_321_._set_name(u'sync')
    var.get(u'ParseContext').get(u'prototype').put(u'sync', PyJs_sync_321_)
    @Js
    def PyJs_addPendingMark_322_(mark, this, arguments, var=var):
        var = Scope({u'this':this, u'addPendingMark':PyJs_addPendingMark_322_, u'arguments':arguments, u'mark':mark}, var)
        var.registers([u'mark'])
        var.get(u"this").get(u'pendingMarks').callprop(u'push', var.get(u'mark'))
    PyJs_addPendingMark_322_._set_name(u'addPendingMark')
    var.get(u'ParseContext').get(u'prototype').put(u'addPendingMark', PyJs_addPendingMark_322_)
    @Js
    def PyJs_removePendingMark_323_(mark, this, arguments, var=var):
        var = Scope({u'this':this, u'removePendingMark':PyJs_removePendingMark_323_, u'arguments':arguments, u'mark':mark}, var)
        var.registers([u'found', u'top', u'mark'])
        var.put(u'found', var.get(u"this").get(u'pendingMarks').callprop(u'lastIndexOf', var.get(u'mark')))
        if (var.get(u'found')>(-Js(1.0))):
            var.get(u"this").get(u'pendingMarks').callprop(u'splice', var.get(u'found'), Js(1.0))
        else:
            var.put(u'top', var.get(u"this").get(u'top'))
            var.get(u'top').put(u'activeMarks', var.get(u'mark').callprop(u'removeFromSet', var.get(u'top').get(u'activeMarks')))
    PyJs_removePendingMark_323_._set_name(u'removePendingMark')
    var.get(u'ParseContext').get(u'prototype').put(u'removePendingMark', PyJs_removePendingMark_323_)
    @Js
    def PyJs_anonymous_324_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([u'i', u'content', u'j', u'pos', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        var.get(u"this").callprop(u'closeExtra')
        var.put(u'pos', Js(0.0))
        #for JS loop
        var.put(u'i', var.get(u"this").get(u'open'))
        while (var.get(u'i')>=Js(0.0)):
            try:
                var.put(u'content', var.get(u'this$1').get(u'nodes').get(var.get(u'i')).get(u'content'))
                #for JS loop
                var.put(u'j', (var.get(u'content').get(u'length')-Js(1.0)))
                while (var.get(u'j')>=Js(0.0)):
                    try:
                        var.put(u'pos', var.get(u'content').get(var.get(u'j')).get(u'nodeSize'), u'+')
                    finally:
                            (var.put(u'j',Js(var.get(u'j').to_number())-Js(1))+Js(1))
                if var.get(u'i'):
                    (var.put(u'pos',Js(var.get(u'pos').to_number())+Js(1))-Js(1))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())-Js(1))+Js(1))
        return var.get(u'pos')
    PyJs_anonymous_324_._set_name(u'anonymous')
    var.get(u'prototypeAccessors$6').get(u'currentPos').put(u'get', PyJs_anonymous_324_)
    @Js
    def PyJs_findAtPoint_325_(parent, offset, this, arguments, var=var):
        var = Scope({u'this':this, u'findAtPoint':PyJs_findAtPoint_325_, u'arguments':arguments, u'parent':parent, u'offset':offset}, var)
        var.registers([u'i', u'offset', u'parent', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        if var.get(u"this").get(u'find'):
            #for JS loop
            var.put(u'i', Js(0.0))
            while (var.get(u'i')<var.get(u"this").get(u'find').get(u'length')):
                try:
                    if ((var.get(u'this$1').get(u'find').get(var.get(u'i')).get(u'node')==var.get(u'parent')) and (var.get(u'this$1').get(u'find').get(var.get(u'i')).get(u'offset')==var.get(u'offset'))):
                        var.get(u'this$1').get(u'find').get(var.get(u'i')).put(u'pos', var.get(u'this$1').get(u'currentPos'))
                finally:
                        (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
    PyJs_findAtPoint_325_._set_name(u'findAtPoint')
    var.get(u'ParseContext').get(u'prototype').put(u'findAtPoint', PyJs_findAtPoint_325_)
    @Js
    def PyJs_findInside_326_(parent, this, arguments, var=var):
        var = Scope({u'this':this, u'findInside':PyJs_findInside_326_, u'arguments':arguments, u'parent':parent}, var)
        var.registers([u'i', u'parent', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        if var.get(u"this").get(u'find'):
            #for JS loop
            var.put(u'i', Js(0.0))
            while (var.get(u'i')<var.get(u"this").get(u'find').get(u'length')):
                try:
                    if (((var.get(u'this$1').get(u'find').get(var.get(u'i')).get(u'pos')==var.get(u"null")) and (var.get(u'parent').get(u'nodeType')==Js(1.0))) and var.get(u'parent').callprop(u'contains', var.get(u'this$1').get(u'find').get(var.get(u'i')).get(u'node'))):
                        var.get(u'this$1').get(u'find').get(var.get(u'i')).put(u'pos', var.get(u'this$1').get(u'currentPos'))
                finally:
                        (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
    PyJs_findInside_326_._set_name(u'findInside')
    var.get(u'ParseContext').get(u'prototype').put(u'findInside', PyJs_findInside_326_)
    @Js
    def PyJs_findAround_327_(parent, content, before, this, arguments, var=var):
        var = Scope({u'parent':parent, u'this':this, u'content':content, u'arguments':arguments, u'findAround':PyJs_findAround_327_, u'before':before}, var)
        var.registers([u'parent', u'i', u'pos', u'content', u'this$1', u'before'])
        var.put(u'this$1', var.get(u"this"))
        if ((var.get(u'parent')!=var.get(u'content')) and var.get(u"this").get(u'find')):
            #for JS loop
            var.put(u'i', Js(0.0))
            while (var.get(u'i')<var.get(u"this").get(u'find').get(u'length')):
                try:
                    if (((var.get(u'this$1').get(u'find').get(var.get(u'i')).get(u'pos')==var.get(u"null")) and (var.get(u'parent').get(u'nodeType')==Js(1.0))) and var.get(u'parent').callprop(u'contains', var.get(u'this$1').get(u'find').get(var.get(u'i')).get(u'node'))):
                        var.put(u'pos', var.get(u'content').callprop(u'compareDocumentPosition', var.get(u'this$1').get(u'find').get(var.get(u'i')).get(u'node')))
                        if (var.get(u'pos')&(Js(2.0) if var.get(u'before') else Js(4.0))):
                            var.get(u'this$1').get(u'find').get(var.get(u'i')).put(u'pos', var.get(u'this$1').get(u'currentPos'))
                finally:
                        (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
    PyJs_findAround_327_._set_name(u'findAround')
    var.get(u'ParseContext').get(u'prototype').put(u'findAround', PyJs_findAround_327_)
    @Js
    def PyJs_findInText_328_(textNode, this, arguments, var=var):
        var = Scope({u'this':this, u'findInText':PyJs_findInText_328_, u'textNode':textNode, u'arguments':arguments}, var)
        var.registers([u'i', u'textNode', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        if var.get(u"this").get(u'find'):
            #for JS loop
            var.put(u'i', Js(0.0))
            while (var.get(u'i')<var.get(u"this").get(u'find').get(u'length')):
                try:
                    if (var.get(u'this$1').get(u'find').get(var.get(u'i')).get(u'node')==var.get(u'textNode')):
                        var.get(u'this$1').get(u'find').get(var.get(u'i')).put(u'pos', (var.get(u'this$1').get(u'currentPos')-(var.get(u'textNode').get(u'nodeValue').get(u'length')-var.get(u'this$1').get(u'find').get(var.get(u'i')).get(u'offset'))))
                finally:
                        (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
    PyJs_findInText_328_._set_name(u'findInText')
    var.get(u'ParseContext').get(u'prototype').put(u'findInText', PyJs_findInText_328_)
    @Js
    def PyJs_matchesContext_329_(context, this, arguments, var=var):
        var = Scope({u'this':this, u'matchesContext':PyJs_matchesContext_329_, u'arguments':arguments, u'context':context}, var)
        var.registers([u'useRoot', u'minDepth', u'option', u'parts', u'context', u'this$1', u'match'])
        var.put(u'this$1', var.get(u"this"))
        if (var.get(u'context').callprop(u'indexOf', Js(u'|'))>(-Js(1.0))):
            return var.get(u'context').callprop(u'split', JsRegExp(u'/\\s*\\|\\s*/')).callprop(u'some', var.get(u"this").get(u'matchesContext'), var.get(u"this"))
        var.put(u'parts', var.get(u'context').callprop(u'split', Js(u'/')))
        var.put(u'option', var.get(u"this").get(u'options').get(u'context'))
        var.put(u'useRoot', (var.get(u"this").get(u'isOpen').neg() and (var.get(u'option').neg() or (var.get(u'option').get(u'parent').get(u'type')==var.get(u"this").get(u'nodes').get(u'0').get(u'type')))))
        var.put(u'minDepth', ((-((var.get(u'option').get(u'depth')+Js(1.0)) if var.get(u'option') else Js(0.0)))+(Js(0.0) if var.get(u'useRoot') else Js(1.0))))
        @Js
        def PyJs_anonymous_330_(i, depth, this, arguments, var=var):
            var = Scope({u'i':i, u'this':this, u'depth':depth, u'arguments':arguments}, var)
            var.registers([u'i', u'depth', u'part', u'next'])
            #for JS loop
            
            while (var.get(u'i')>=Js(0.0)):
                try:
                    var.put(u'part', var.get(u'parts').get(var.get(u'i')))
                    if (var.get(u'part')==Js(u'')):
                        if ((var.get(u'i')==(var.get(u'parts').get(u'length')-Js(1.0))) or (var.get(u'i')==Js(0.0))):
                            continue
                        #for JS loop
                        
                        while (var.get(u'depth')>=var.get(u'minDepth')):
                            try:
                                if var.get(u'match')((var.get(u'i')-Js(1.0)), var.get(u'depth')):
                                    return Js(True)
                            finally:
                                    (var.put(u'depth',Js(var.get(u'depth').to_number())-Js(1))+Js(1))
                        return Js(False)
                    else:
                        var.put(u'next', (var.get(u'this$1').get(u'nodes').get(var.get(u'depth')).get(u'type') if ((var.get(u'depth')>Js(0.0)) or ((var.get(u'depth')==Js(0.0)) and var.get(u'useRoot'))) else (var.get(u'option').callprop(u'node', (var.get(u'depth')-var.get(u'minDepth'))).get(u'type') if (var.get(u'option') and (var.get(u'depth')>=var.get(u'minDepth'))) else var.get(u"null"))))
                        if (var.get(u'next').neg() or ((var.get(u'next').get(u'name')!=var.get(u'part')) and (var.get(u'next').get(u'groups').callprop(u'indexOf', var.get(u'part'))==(-Js(1.0))))):
                            return Js(False)
                        (var.put(u'depth',Js(var.get(u'depth').to_number())-Js(1))+Js(1))
                finally:
                        (var.put(u'i',Js(var.get(u'i').to_number())-Js(1))+Js(1))
            return Js(True)
        PyJs_anonymous_330_._set_name(u'anonymous')
        var.put(u'match', PyJs_anonymous_330_)
        return var.get(u'match')((var.get(u'parts').get(u'length')-Js(1.0)), var.get(u"this").get(u'open'))
    PyJs_matchesContext_329_._set_name(u'matchesContext')
    var.get(u'ParseContext').get(u'prototype').put(u'matchesContext', PyJs_matchesContext_329_)
    @Js
    def PyJs_textblockFromContext_331_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'textblockFromContext':PyJs_textblockFromContext_331_}, var)
        var.registers([u'deflt', u'd', u'$context', u'this$1', u'type', u'name'])
        var.put(u'this$1', var.get(u"this"))
        var.put(u'$context', var.get(u"this").get(u'options').get(u'context'))
        if var.get(u'$context'):
            #for JS loop
            var.put(u'd', var.get(u'$context').get(u'depth'))
            while (var.get(u'd')>=Js(0.0)):
                try:
                    var.put(u'deflt', var.get(u'$context').callprop(u'node', var.get(u'd')).callprop(u'contentMatchAt', var.get(u'$context').callprop(u'indexAfter', var.get(u'd'))).get(u'defaultType'))
                    if ((var.get(u'deflt') and var.get(u'deflt').get(u'isTextblock')) and var.get(u'deflt').get(u'defaultAttrs')):
                        return var.get(u'deflt')
                finally:
                        (var.put(u'd',Js(var.get(u'd').to_number())-Js(1))+Js(1))
        for PyJsTemp in var.get(u'this$1').get(u'parser').get(u'schema').get(u'nodes'):
            var.put(u'name', PyJsTemp)
            var.put(u'type', var.get(u'this$1').get(u'parser').get(u'schema').get(u'nodes').get(var.get(u'name')))
            if (var.get(u'type').get(u'isTextblock') and var.get(u'type').get(u'defaultAttrs')):
                return var.get(u'type')
    PyJs_textblockFromContext_331_._set_name(u'textblockFromContext')
    var.get(u'ParseContext').get(u'prototype').put(u'textblockFromContext', PyJs_textblockFromContext_331_)
    var.get(u'Object').callprop(u'defineProperties', var.get(u'ParseContext').get(u'prototype'), var.get(u'prototypeAccessors$6'))
    pass
    pass
    pass
    pass
    @Js
    def PyJs_DOMSerializer_333_(nodes, marks, this, arguments, var=var):
        var = Scope({u'this':this, u'nodes':nodes, u'DOMSerializer':PyJs_DOMSerializer_333_, u'arguments':arguments, u'marks':marks}, var)
        var.registers([u'nodes', u'marks'])
        PyJs_Object_334_ = Js({})
        var.get(u"this").put(u'nodes', (var.get(u'nodes') or PyJs_Object_334_))
        PyJs_Object_335_ = Js({})
        var.get(u"this").put(u'marks', (var.get(u'marks') or PyJs_Object_335_))
    PyJs_DOMSerializer_333_._set_name(u'DOMSerializer')
    var.put(u'DOMSerializer', PyJs_DOMSerializer_333_)
    @Js
    def PyJs_serializeFragment_336_(fragment, options, target, this, arguments, var=var):
        var = Scope({u'serializeFragment':PyJs_serializeFragment_336_, u'target':target, u'fragment':fragment, u'this':this, u'arguments':arguments, u'options':options}, var)
        var.registers([u'target', u'fragment', u'top', u'this$1', u'active', u'options'])
        var.put(u'this$1', var.get(u"this"))
        if PyJsStrictEq(var.get(u'options'),PyJsComma(Js(0.0), Js(None))):
            PyJs_Object_337_ = Js({})
            var.put(u'options', PyJs_Object_337_)
        if var.get(u'target').neg():
            var.put(u'target', var.get(u'doc')(var.get(u'options')).callprop(u'createDocumentFragment'))
        var.put(u'top', var.get(u'target'))
        var.put(u'active', var.get(u"null"))
        @Js
        def PyJs_anonymous_338_(node, this, arguments, var=var):
            var = Scope({u'node':node, u'this':this, u'arguments':arguments}, var)
            var.registers([u'node', u'rendered', u'markDOM', u'next', u'add', u'keep'])
            if (var.get(u'active') or var.get(u'node').get(u'marks').get(u'length')):
                if var.get(u'active').neg():
                    var.put(u'active', Js([]))
                var.put(u'keep', Js(0.0))
                var.put(u'rendered', Js(0.0))
                while ((var.get(u'keep')<var.get(u'active').get(u'length')) and (var.get(u'rendered')<var.get(u'node').get(u'marks').get(u'length'))):
                    var.put(u'next', var.get(u'node').get(u'marks').get(var.get(u'rendered')))
                    if var.get(u'this$1').get(u'marks').get(var.get(u'next').get(u'type').get(u'name')).neg():
                        (var.put(u'rendered',Js(var.get(u'rendered').to_number())+Js(1))-Js(1))
                        continue
                    if var.get(u'next').callprop(u'eq', var.get(u'active').get(var.get(u'keep'))).neg():
                        break
                    var.put(u'keep', Js(2.0), u'+')
                    (var.put(u'rendered',Js(var.get(u'rendered').to_number())+Js(1))-Js(1))
                while (var.get(u'keep')<var.get(u'active').get(u'length')):
                    var.put(u'top', var.get(u'active').callprop(u'pop'))
                    var.get(u'active').callprop(u'pop')
                while (var.get(u'rendered')<var.get(u'node').get(u'marks').get(u'length')):
                    var.put(u'add', var.get(u'node').get(u'marks').get((var.put(u'rendered',Js(var.get(u'rendered').to_number())+Js(1))-Js(1))))
                    var.put(u'markDOM', var.get(u'this$1').callprop(u'serializeMark', var.get(u'add'), var.get(u'node').get(u'isInline'), var.get(u'options')))
                    if var.get(u'markDOM'):
                        var.get(u'active').callprop(u'push', var.get(u'add'), var.get(u'top'))
                        var.get(u'top').callprop(u'appendChild', var.get(u'markDOM').get(u'dom'))
                        var.put(u'top', (var.get(u'markDOM').get(u'contentDOM') or var.get(u'markDOM').get(u'dom')))
            var.get(u'top').callprop(u'appendChild', var.get(u'this$1').callprop(u'serializeNode', var.get(u'node'), var.get(u'options')))
        PyJs_anonymous_338_._set_name(u'anonymous')
        var.get(u'fragment').callprop(u'forEach', PyJs_anonymous_338_)
        return var.get(u'target')
    PyJs_serializeFragment_336_._set_name(u'serializeFragment')
    var.get(u'DOMSerializer').get(u'prototype').put(u'serializeFragment', PyJs_serializeFragment_336_)
    @Js
    def PyJs_serializeNode_339_(node, options, this, arguments, var=var):
        var = Scope({u'node':node, u'this':this, u'serializeNode':PyJs_serializeNode_339_, u'options':options, u'arguments':arguments}, var)
        var.registers([u'node', u'contentDOM', u'ref', u'options', u'dom'])
        if PyJsStrictEq(var.get(u'options'),PyJsComma(Js(0.0), Js(None))):
            PyJs_Object_340_ = Js({})
            var.put(u'options', PyJs_Object_340_)
        var.put(u'ref', var.get(u'DOMSerializer').callprop(u'renderSpec', var.get(u'doc')(var.get(u'options')), var.get(u"this").get(u'nodes').callprop(var.get(u'node').get(u'type').get(u'name'), var.get(u'node'))))
        var.put(u'dom', var.get(u'ref').get(u'dom'))
        var.put(u'contentDOM', var.get(u'ref').get(u'contentDOM'))
        if var.get(u'contentDOM'):
            if var.get(u'node').get(u'isLeaf'):
                PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'Content hole not allowed in a leaf node spec')))
                raise PyJsTempException
            if var.get(u'options').get(u'onContent'):
                var.get(u'options').callprop(u'onContent', var.get(u'node'), var.get(u'contentDOM'), var.get(u'options'))
            else:
                var.get(u"this").callprop(u'serializeFragment', var.get(u'node').get(u'content'), var.get(u'options'), var.get(u'contentDOM'))
        return var.get(u'dom')
    PyJs_serializeNode_339_._set_name(u'serializeNode')
    var.get(u'DOMSerializer').get(u'prototype').put(u'serializeNode', PyJs_serializeNode_339_)
    @Js
    def PyJs_serializeNodeAndMarks_341_(node, options, this, arguments, var=var):
        var = Scope({u'node':node, u'this':this, u'options':options, u'serializeNodeAndMarks':PyJs_serializeNodeAndMarks_341_, u'arguments':arguments}, var)
        var.registers([u'node', u'dom', u'i', u'this$1', u'wrap', u'options'])
        var.put(u'this$1', var.get(u"this"))
        if PyJsStrictEq(var.get(u'options'),PyJsComma(Js(0.0), Js(None))):
            PyJs_Object_342_ = Js({})
            var.put(u'options', PyJs_Object_342_)
        var.put(u'dom', var.get(u"this").callprop(u'serializeNode', var.get(u'node'), var.get(u'options')))
        #for JS loop
        var.put(u'i', (var.get(u'node').get(u'marks').get(u'length')-Js(1.0)))
        while (var.get(u'i')>=Js(0.0)):
            try:
                var.put(u'wrap', var.get(u'this$1').callprop(u'serializeMark', var.get(u'node').get(u'marks').get(var.get(u'i')), var.get(u'node').get(u'isInline'), var.get(u'options')))
                if var.get(u'wrap'):
                    (var.get(u'wrap').get(u'contentDOM') or var.get(u'wrap').get(u'dom')).callprop(u'appendChild', var.get(u'dom'))
                    var.put(u'dom', var.get(u'wrap').get(u'dom'))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())-Js(1))+Js(1))
        return var.get(u'dom')
    PyJs_serializeNodeAndMarks_341_._set_name(u'serializeNodeAndMarks')
    var.get(u'DOMSerializer').get(u'prototype').put(u'serializeNodeAndMarks', PyJs_serializeNodeAndMarks_341_)
    @Js
    def PyJs_serializeMark_343_(mark, inline, options, this, arguments, var=var):
        var = Scope({u'this':this, u'mark':mark, u'serializeMark':PyJs_serializeMark_343_, u'arguments':arguments, u'inline':inline, u'options':options}, var)
        var.registers([u'toDOM', u'inline', u'options', u'mark'])
        if PyJsStrictEq(var.get(u'options'),PyJsComma(Js(0.0), Js(None))):
            PyJs_Object_344_ = Js({})
            var.put(u'options', PyJs_Object_344_)
        var.put(u'toDOM', var.get(u"this").get(u'marks').get(var.get(u'mark').get(u'type').get(u'name')))
        return (var.get(u'toDOM') and var.get(u'DOMSerializer').callprop(u'renderSpec', var.get(u'doc')(var.get(u'options')), var.get(u'toDOM')(var.get(u'mark'), var.get(u'inline'))))
    PyJs_serializeMark_343_._set_name(u'serializeMark')
    var.get(u'DOMSerializer').get(u'prototype').put(u'serializeMark', PyJs_serializeMark_343_)
    @Js
    def PyJs_renderSpec_345_(doc, structure, this, arguments, var=var):
        var = Scope({u'this':this, u'doc':doc, u'renderSpec':PyJs_renderSpec_345_, u'arguments':arguments, u'structure':structure}, var)
        var.registers([u'contentDOM', u'name', u'dom', u'i', u'doc', u'innerContent', u'start', u'attrs', u'child', u'ref', u'structure', u'inner'])
        if (var.get(u'structure',throw=False).typeof()==Js(u'string')):
            PyJs_Object_346_ = Js({u'dom':var.get(u'doc').callprop(u'createTextNode', var.get(u'structure'))})
            return PyJs_Object_346_
        if (var.get(u'structure').get(u'nodeType')!=var.get(u"null")):
            PyJs_Object_347_ = Js({u'dom':var.get(u'structure')})
            return PyJs_Object_347_
        var.put(u'dom', var.get(u'doc').callprop(u'createElement', var.get(u'structure').get(u'0')))
        var.put(u'contentDOM', var.get(u"null"))
        var.put(u'attrs', var.get(u'structure').get(u'1'))
        var.put(u'start', Js(1.0))
        if (((var.get(u'attrs') and (var.get(u'attrs',throw=False).typeof()==Js(u'object'))) and (var.get(u'attrs').get(u'nodeType')==var.get(u"null"))) and var.get(u'Array').callprop(u'isArray', var.get(u'attrs')).neg()):
            var.put(u'start', Js(2.0))
            for PyJsTemp in var.get(u'attrs'):
                var.put(u'name', PyJsTemp)
                if (var.get(u'name')==Js(u'style')):
                    var.get(u'dom').get(u'style').put(u'cssText', var.get(u'attrs').get(var.get(u'name')))
                else:
                    if (var.get(u'attrs').get(var.get(u'name'))!=var.get(u"null")):
                        var.get(u'dom').callprop(u'setAttribute', var.get(u'name'), var.get(u'attrs').get(var.get(u'name')))
        #for JS loop
        var.put(u'i', var.get(u'start'))
        while (var.get(u'i')<var.get(u'structure').get(u'length')):
            try:
                var.put(u'child', var.get(u'structure').get(var.get(u'i')))
                if PyJsStrictEq(var.get(u'child'),Js(0.0)):
                    if ((var.get(u'i')<(var.get(u'structure').get(u'length')-Js(1.0))) or (var.get(u'i')>var.get(u'start'))):
                        PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'Content hole must be the only child of its parent node')))
                        raise PyJsTempException
                    PyJs_Object_348_ = Js({u'dom':var.get(u'dom'),u'contentDOM':var.get(u'dom')})
                    return PyJs_Object_348_
                else:
                    var.put(u'ref', var.get(u'DOMSerializer').callprop(u'renderSpec', var.get(u'doc'), var.get(u'child')))
                    var.put(u'inner', var.get(u'ref').get(u'dom'))
                    var.put(u'innerContent', var.get(u'ref').get(u'contentDOM'))
                    var.get(u'dom').callprop(u'appendChild', var.get(u'inner'))
                    if var.get(u'innerContent'):
                        if var.get(u'contentDOM'):
                            PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'Multiple content holes')))
                            raise PyJsTempException
                        var.put(u'contentDOM', var.get(u'innerContent'))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        PyJs_Object_349_ = Js({u'dom':var.get(u'dom'),u'contentDOM':var.get(u'contentDOM')})
        return PyJs_Object_349_
    PyJs_renderSpec_345_._set_name(u'renderSpec')
    var.get(u'DOMSerializer').put(u'renderSpec', PyJs_renderSpec_345_)
    @Js
    def PyJs_fromSchema_350_(schema, this, arguments, var=var):
        var = Scope({u'this':this, u'fromSchema':PyJs_fromSchema_350_, u'arguments':arguments, u'schema':schema}, var)
        var.registers([u'schema'])
        return (var.get(u'schema').get(u'cached').get(u'domSerializer') or var.get(u'schema').get(u'cached').put(u'domSerializer', var.get(u'DOMSerializer').create(var.get(u"this").callprop(u'nodesFromSchema', var.get(u'schema')), var.get(u"this").callprop(u'marksFromSchema', var.get(u'schema')))))
    PyJs_fromSchema_350_._set_name(u'fromSchema')
    var.get(u'DOMSerializer').put(u'fromSchema', PyJs_fromSchema_350_)
    @Js
    def PyJs_nodesFromSchema_351_(schema, this, arguments, var=var):
        var = Scope({u'this':this, u'nodesFromSchema':PyJs_nodesFromSchema_351_, u'arguments':arguments, u'schema':schema}, var)
        var.registers([u'result', u'schema'])
        var.put(u'result', var.get(u'gatherToDOM')(var.get(u'schema').get(u'nodes')))
        if var.get(u'result').get(u'text').neg():
            @Js
            def PyJs_anonymous_352_(node, this, arguments, var=var):
                var = Scope({u'node':node, u'this':this, u'arguments':arguments}, var)
                var.registers([u'node'])
                return var.get(u'node').get(u'text')
            PyJs_anonymous_352_._set_name(u'anonymous')
            var.get(u'result').put(u'text', PyJs_anonymous_352_)
        return var.get(u'result')
    PyJs_nodesFromSchema_351_._set_name(u'nodesFromSchema')
    var.get(u'DOMSerializer').put(u'nodesFromSchema', PyJs_nodesFromSchema_351_)
    @Js
    def PyJs_marksFromSchema_353_(schema, this, arguments, var=var):
        var = Scope({u'this':this, u'marksFromSchema':PyJs_marksFromSchema_353_, u'arguments':arguments, u'schema':schema}, var)
        var.registers([u'schema'])
        return var.get(u'gatherToDOM')(var.get(u'schema').get(u'marks'))
    PyJs_marksFromSchema_353_._set_name(u'marksFromSchema')
    var.get(u'DOMSerializer').put(u'marksFromSchema', PyJs_marksFromSchema_353_)
    pass
    pass
    var.get(u'exports').put(u'Node', var.get(u'Node'))
    var.get(u'exports').put(u'ResolvedPos', var.get(u'ResolvedPos'))
    var.get(u'exports').put(u'NodeRange', var.get(u'NodeRange'))
    var.get(u'exports').put(u'Fragment', var.get(u'Fragment'))
    var.get(u'exports').put(u'Slice', var.get(u'Slice'))
    var.get(u'exports').put(u'ReplaceError', var.get(u'ReplaceError'))
    var.get(u'exports').put(u'Mark', var.get(u'Mark'))
    var.get(u'exports').put(u'Schema', var.get(u'Schema'))
    var.get(u'exports').put(u'NodeType', var.get(u'NodeType'))
    var.get(u'exports').put(u'MarkType', var.get(u'MarkType'))
    var.get(u'exports').put(u'ContentMatch', var.get(u'ContentMatch'))
    var.get(u'exports').put(u'DOMParser', var.get(u'DOMParser'))
    var.get(u'exports').put(u'DOMSerializer', var.get(u'DOMSerializer'))
PyJs_anonymous_17_._set_name(u'anonymous')
var.put(u'dist', var.get(u'createCommonjsModule')(PyJs_anonymous_17_))
var.get(u'unwrapExports')(var.get(u'dist'))
var.put(u'dist_1', var.get(u'dist').get(u'Node'))
var.put(u'dist_2', var.get(u'dist').get(u'ResolvedPos'))
var.put(u'dist_3', var.get(u'dist').get(u'NodeRange'))
var.put(u'dist_4', var.get(u'dist').get(u'Fragment'))
var.put(u'dist_5', var.get(u'dist').get(u'Slice'))
var.put(u'dist_6', var.get(u'dist').get(u'ReplaceError'))
var.put(u'dist_7', var.get(u'dist').get(u'Mark'))
var.put(u'dist_8', var.get(u'dist').get(u'Schema'))
var.put(u'dist_9', var.get(u'dist').get(u'NodeType'))
var.put(u'dist_10', var.get(u'dist').get(u'MarkType'))
var.put(u'dist_11', var.get(u'dist').get(u'ContentMatch'))
var.put(u'dist_12', var.get(u'dist').get(u'DOMParser'))
var.put(u'dist_13', var.get(u'dist').get(u'DOMSerializer'))
@Js
def PyJs_anonymous_355_(module, exports, this, arguments, var=var):
    var = Scope({u'this':this, u'exports':exports, u'arguments':arguments, u'module':module}, var)
    var.registers([u'joinable', u'canMoveText', u'nodeRight', u'Frontier', u'recoverIndex', u'joinPoint', u'Transform', u'module', u'canJoin', u'factor16', u'liftTarget', u'placeSlice', u'ReplaceStep', u'recoverOffset', u'closeNodeEnd', u'findWrappingOutside', u'canChangeType', u'fitRight', u'mustOverride', u'fitRightClosed', u'MapResult', u'Mapping', u'withAttrs', u'Step', u'StepMap', u'fitLeft', u'mapFragment', u'fitsTrivially', u'fitRightJoin', u'insertPoint', u'closeFragment', u'exports', u'StepResult', u'stepsByID', u'fitRightSeparate', u'canSplit', u'RemoveMarkStep', u'closeFragmentEnd', u'findWrappingInside', u'TransformError', u'ReplaceAroundStep', u'findWrapping', u'closeNodeStart', u'contentBetween', u'coveredDepths', u'canCut', u'makeRecover', u'replaceStep', u'AddMarkStep', u'dropPoint', u'normalizeSlice', u'prototypeAccessors', u'lower16', u'fitLeftInner'])
    @Js
    def PyJsHoisted_joinable_(a, b, this, arguments, var=var):
        var = Scope({u'a':a, u'this':this, u'b':b, u'arguments':arguments}, var)
        var.registers([u'a', u'b'])
        return (((var.get(u'a') and var.get(u'b')) and var.get(u'a').get(u'isLeaf').neg()) and var.get(u'a').callprop(u'canAppend', var.get(u'b')))
    PyJsHoisted_joinable_.func_name = u'joinable'
    var.put(u'joinable', PyJsHoisted_joinable_)
    @Js
    def PyJsHoisted_canMoveText_(PyJsArg_2466726f6d_, PyJsArg_24746f_, slice, this, arguments, var=var):
        var = Scope({u'this':this, u'$from':PyJsArg_2466726f6d_, u'slice':slice, u'$to':PyJsArg_24746f_, u'arguments':arguments}, var)
        var.registers([u'slice', u'$to', u'parent', u'i', u'$from', u'match'])
        if var.get(u'$to').get(u'parent').get(u'isTextblock').neg():
            return Js(False)
        var.put(u'parent', (var.get(u'nodeRight')(var.get(u'slice').get(u'content'), var.get(u'slice').get(u'openEnd')) if var.get(u'slice').get(u'openEnd') else var.get(u'$from').callprop(u'node', (var.get(u'$from').get(u'depth')-(var.get(u'slice').get(u'openStart')-var.get(u'slice').get(u'openEnd'))))))
        if var.get(u'parent').get(u'isTextblock').neg():
            return Js(False)
        #for JS loop
        var.put(u'i', var.get(u'$to').callprop(u'index'))
        while (var.get(u'i')<var.get(u'$to').get(u'parent').get(u'childCount')):
            try:
                if var.get(u'parent').get(u'type').callprop(u'allowsMarks', var.get(u'$to').get(u'parent').callprop(u'child', var.get(u'i')).get(u'marks')).neg():
                    return Js(False)
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        pass
        if var.get(u'slice').get(u'openEnd'):
            var.put(u'match', var.get(u'parent').callprop(u'contentMatchAt', var.get(u'parent').get(u'childCount')))
        else:
            var.put(u'match', var.get(u'parent').callprop(u'contentMatchAt', var.get(u'parent').get(u'childCount')))
            if var.get(u'slice').get(u'size'):
                var.put(u'match', var.get(u'match').callprop(u'matchFragment', var.get(u'slice').get(u'content'), (Js(1.0) if var.get(u'slice').get(u'openStart') else Js(0.0))))
        var.put(u'match', var.get(u'match').callprop(u'matchFragment', var.get(u'$to').get(u'parent').get(u'content'), var.get(u'$to').callprop(u'index')))
        return (var.get(u'match') and var.get(u'match').get(u'validEnd'))
    PyJsHoisted_canMoveText_.func_name = u'canMoveText'
    var.put(u'canMoveText', PyJsHoisted_canMoveText_)
    @Js
    def PyJsHoisted_joinPoint_(doc, pos, dir, this, arguments, var=var):
        var = Scope({u'this':this, u'doc':doc, u'pos':pos, u'dir':dir, u'arguments':arguments}, var)
        var.registers([u'd', u'$pos', u'doc', u'after', u'pos', u'dir', u'before'])
        if PyJsStrictEq(var.get(u'dir'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'dir', (-Js(1.0)))
        var.put(u'$pos', var.get(u'doc').callprop(u'resolve', var.get(u'pos')))
        #for JS loop
        var.put(u'd', var.get(u'$pos').get(u'depth'))
        while 1:
            try:
                var.put(u'before', PyJsComma(Js(0.0), Js(None)))
                var.put(u'after', PyJsComma(Js(0.0), Js(None)))
                if (var.get(u'd')==var.get(u'$pos').get(u'depth')):
                    var.put(u'before', var.get(u'$pos').get(u'nodeBefore'))
                    var.put(u'after', var.get(u'$pos').get(u'nodeAfter'))
                else:
                    if (var.get(u'dir')>Js(0.0)):
                        var.put(u'before', var.get(u'$pos').callprop(u'node', (var.get(u'd')+Js(1.0))))
                        var.put(u'after', var.get(u'$pos').callprop(u'node', var.get(u'd')).callprop(u'maybeChild', (var.get(u'$pos').callprop(u'index', var.get(u'd'))+Js(1.0))))
                    else:
                        var.put(u'before', var.get(u'$pos').callprop(u'node', var.get(u'd')).callprop(u'maybeChild', (var.get(u'$pos').callprop(u'index', var.get(u'd'))-Js(1.0))))
                        var.put(u'after', var.get(u'$pos').callprop(u'node', (var.get(u'd')+Js(1.0))))
                if ((var.get(u'before') and var.get(u'before').get(u'isTextblock').neg()) and var.get(u'joinable')(var.get(u'before'), var.get(u'after'))):
                    return var.get(u'pos')
                if (var.get(u'd')==Js(0.0)):
                    break
                var.put(u'pos', (var.get(u'$pos').callprop(u'before', var.get(u'd')) if (var.get(u'dir')<Js(0.0)) else var.get(u'$pos').callprop(u'after', var.get(u'd'))))
            finally:
                    (var.put(u'd',Js(var.get(u'd').to_number())-Js(1))+Js(1))
    PyJsHoisted_joinPoint_.func_name = u'joinPoint'
    var.put(u'joinPoint', PyJsHoisted_joinPoint_)
    @Js
    def PyJsHoisted_liftTarget_(range, this, arguments, var=var):
        var = Scope({u'this':this, u'range':range, u'arguments':arguments}, var)
        var.registers([u'node', u'endIndex', u'parent', u'index', u'range', u'content', u'depth'])
        var.put(u'parent', var.get(u'range').get(u'parent'))
        var.put(u'content', var.get(u'parent').get(u'content').callprop(u'cutByIndex', var.get(u'range').get(u'startIndex'), var.get(u'range').get(u'endIndex')))
        #for JS loop
        var.put(u'depth', var.get(u'range').get(u'depth'))
        while 1:
            try:
                var.put(u'node', var.get(u'range').get(u'$from').callprop(u'node', var.get(u'depth')))
                var.put(u'index', var.get(u'range').get(u'$from').callprop(u'index', var.get(u'depth')))
                var.put(u'endIndex', var.get(u'range').get(u'$to').callprop(u'indexAfter', var.get(u'depth')))
                if ((var.get(u'depth')<var.get(u'range').get(u'depth')) and var.get(u'node').callprop(u'canReplace', var.get(u'index'), var.get(u'endIndex'), var.get(u'content'))):
                    return var.get(u'depth')
                if (((var.get(u'depth')==Js(0.0)) or var.get(u'node').get(u'type').get(u'spec').get(u'isolating')) or var.get(u'canCut')(var.get(u'node'), var.get(u'index'), var.get(u'endIndex')).neg()):
                    break
            finally:
                    var.put(u'depth',Js(var.get(u'depth').to_number())-Js(1))
    PyJsHoisted_liftTarget_.func_name = u'liftTarget'
    var.put(u'liftTarget', PyJsHoisted_liftTarget_)
    @Js
    def PyJsHoisted_placeSlice_(PyJsArg_2466726f6d_, slice, this, arguments, var=var):
        var = Scope({u'this':this, u'$from':PyJsArg_2466726f6d_, u'slice':slice, u'arguments':arguments}, var)
        var.registers([u'$from', u'pass', u'slice', u'frontier'])
        var.put(u'frontier', var.get(u'Frontier').create(var.get(u'$from')))
        #for JS loop
        var.put(u'pass', Js(1.0))
        while (var.get(u'slice').get(u'size') and (var.get(u'pass')<=Js(3.0))):
            try:
                var.put(u'slice', var.get(u'frontier').callprop(u'placeSlice', var.get(u'slice').get(u'content'), var.get(u'slice').get(u'openStart'), var.get(u'slice').get(u'openEnd'), var.get(u'pass')))
            finally:
                    (var.put(u'pass',Js(var.get(u'pass').to_number())+Js(1))-Js(1))
        while var.get(u'frontier').get(u'open').get(u'length'):
            var.get(u'frontier').callprop(u'closeNode')
        return var.get(u'frontier').get(u'placed')
    PyJsHoisted_placeSlice_.func_name = u'placeSlice'
    var.put(u'placeSlice', PyJsHoisted_placeSlice_)
    @Js
    def PyJsHoisted_recoverOffset_(value, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'value':value}, var)
        var.registers([u'value'])
        return ((var.get(u'value')-(var.get(u'value')&var.get(u'lower16')))/var.get(u'factor16'))
    PyJsHoisted_recoverOffset_.func_name = u'recoverOffset'
    var.put(u'recoverOffset', PyJsHoisted_recoverOffset_)
    @Js
    def PyJsHoisted_closeNodeEnd_(node, depth, this, arguments, var=var):
        var = Scope({u'node':node, u'this':this, u'depth':depth, u'arguments':arguments}, var)
        var.registers([u'content', u'node', u'depth', u'last', u'fill'])
        var.put(u'content', var.get(u'node').get(u'content'))
        if (var.get(u'depth')>Js(1.0)):
            var.put(u'last', var.get(u'closeNodeEnd')(var.get(u'node').get(u'lastChild'), (var.get(u'depth')-Js(1.0))))
            var.put(u'content', var.get(u'node').get(u'content').callprop(u'replaceChild', (var.get(u'node').get(u'childCount')-Js(1.0)), var.get(u'last')))
        var.put(u'fill', var.get(u'node').callprop(u'contentMatchAt', var.get(u'node').get(u'childCount')).callprop(u'fillBefore', var.get(u'dist').get(u'Fragment').get(u'empty'), Js(True)))
        return var.get(u'node').callprop(u'copy', var.get(u'content').callprop(u'append', var.get(u'fill')))
    PyJsHoisted_closeNodeEnd_.func_name = u'closeNodeEnd'
    var.put(u'closeNodeEnd', PyJsHoisted_closeNodeEnd_)
    @Js
    def PyJsHoisted_findWrappingOutside_(range, type, this, arguments, var=var):
        var = Scope({u'this':this, u'range':range, u'type':type, u'arguments':arguments}, var)
        var.registers([u'endIndex', u'outer', u'around', u'parent', u'range', u'startIndex', u'type'])
        var.put(u'parent', var.get(u'range').get(u'parent'))
        var.put(u'startIndex', var.get(u'range').get(u'startIndex'))
        var.put(u'endIndex', var.get(u'range').get(u'endIndex'))
        var.put(u'around', var.get(u'parent').callprop(u'contentMatchAt', var.get(u'startIndex')).callprop(u'findWrapping', var.get(u'type')))
        if var.get(u'around').neg():
            return var.get(u"null")
        var.put(u'outer', (var.get(u'around').get(u'0') if var.get(u'around').get(u'length') else var.get(u'type')))
        return (var.get(u'around') if var.get(u'parent').callprop(u'canReplaceWith', var.get(u'startIndex'), var.get(u'endIndex'), var.get(u'outer')) else var.get(u"null"))
    PyJsHoisted_findWrappingOutside_.func_name = u'findWrappingOutside'
    var.put(u'findWrappingOutside', PyJsHoisted_findWrappingOutside_)
    @Js
    def PyJsHoisted_canChangeType_(doc, pos, type, this, arguments, var=var):
        var = Scope({u'this':this, u'doc':doc, u'type':type, u'pos':pos, u'arguments':arguments}, var)
        var.registers([u'index', u'type', u'pos', u'$pos', u'doc'])
        var.put(u'$pos', var.get(u'doc').callprop(u'resolve', var.get(u'pos')))
        var.put(u'index', var.get(u'$pos').callprop(u'index'))
        return var.get(u'$pos').get(u'parent').callprop(u'canReplaceWith', var.get(u'index'), (var.get(u'index')+Js(1.0)), var.get(u'type'))
    PyJsHoisted_canChangeType_.func_name = u'canChangeType'
    var.put(u'canChangeType', PyJsHoisted_canChangeType_)
    @Js
    def PyJsHoisted_fitRight_(PyJsArg_2466726f6d_, PyJsArg_24746f_, slice, this, arguments, var=var):
        var = Scope({u'this':this, u'$from':PyJsArg_2466726f6d_, u'slice':slice, u'$to':PyJsArg_24746f_, u'arguments':arguments}, var)
        var.registers([u'$from', u'slice', u'$to', u'fitted'])
        var.put(u'fitted', var.get(u'fitRightJoin')(var.get(u'slice').get(u'content'), var.get(u'$from').callprop(u'node', Js(0.0)), var.get(u'$from'), var.get(u'$to'), Js(0.0), var.get(u'slice').get(u'openStart'), var.get(u'slice').get(u'openEnd')))
        if var.get(u'fitted').neg():
            return var.get(u"null")
        return var.get(u'normalizeSlice')(var.get(u'fitted'), var.get(u'slice').get(u'openStart'), var.get(u'$to').get(u'depth'))
    PyJsHoisted_fitRight_.func_name = u'fitRight'
    var.put(u'fitRight', PyJsHoisted_fitRight_)
    @Js
    def PyJsHoisted_mustOverride_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        PyJsTempException = JsToPyException(var.get(u'Error').create(Js(u'Override me')))
        raise PyJsTempException
    PyJsHoisted_mustOverride_.func_name = u'mustOverride'
    var.put(u'mustOverride', PyJsHoisted_mustOverride_)
    @Js
    def PyJsHoisted_fitRightClosed_(node, openEnd, PyJsArg_2466726f6d_, depth, openStart, this, arguments, var=var):
        var = Scope({u'node':node, u'this':this, u'depth':depth, u'openStart':openStart, u'openEnd':openEnd, u'$from':PyJsArg_2466726f6d_, u'arguments':arguments}, var)
        var.registers([u'count', u'node', u'$from', u'content', u'depth', u'openStart', u'closed', u'openEnd', u'match'])
        var.put(u'content', var.get(u'node').get(u'content'))
        var.put(u'count', var.get(u'content').get(u'childCount'))
        if (var.get(u'openStart')>=Js(0.0)):
            var.put(u'match', var.get(u'$from').callprop(u'node', var.get(u'depth')).callprop(u'contentMatchAt', var.get(u'$from').callprop(u'indexAfter', var.get(u'depth'))).callprop(u'matchFragment', var.get(u'content'), (Js(1.0) if (var.get(u'openStart')>Js(0.0)) else Js(0.0)), var.get(u'count')))
        else:
            var.put(u'match', var.get(u'node').callprop(u'contentMatchAt', var.get(u'count')))
        if (var.get(u'openEnd')>Js(0.0)):
            var.put(u'closed', var.get(u'fitRightClosed')(var.get(u'content').get(u'lastChild'), (var.get(u'openEnd')-Js(1.0)), var.get(u'$from'), (var.get(u'depth')+Js(1.0)), ((var.get(u'openStart')-Js(1.0)) if (var.get(u'count')==Js(1.0)) else (-Js(1.0)))))
            var.put(u'content', var.get(u'content').callprop(u'replaceChild', (var.get(u'count')-Js(1.0)), var.get(u'closed')))
        return var.get(u'node').callprop(u'copy', var.get(u'content').callprop(u'append', var.get(u'match').callprop(u'fillBefore', var.get(u'dist').get(u'Fragment').get(u'empty'), Js(True))))
    PyJsHoisted_fitRightClosed_.func_name = u'fitRightClosed'
    var.put(u'fitRightClosed', PyJsHoisted_fitRightClosed_)
    @Js
    def PyJsHoisted_recoverIndex_(value, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'value':value}, var)
        var.registers([u'value'])
        return (var.get(u'value')&var.get(u'lower16'))
    PyJsHoisted_recoverIndex_.func_name = u'recoverIndex'
    var.put(u'recoverIndex', PyJsHoisted_recoverIndex_)
    @Js
    def PyJsHoisted_canJoin_(doc, pos, this, arguments, var=var):
        var = Scope({u'this':this, u'doc':doc, u'pos':pos, u'arguments':arguments}, var)
        var.registers([u'index', u'pos', u'$pos', u'doc'])
        var.put(u'$pos', var.get(u'doc').callprop(u'resolve', var.get(u'pos')))
        var.put(u'index', var.get(u'$pos').callprop(u'index'))
        return (var.get(u'joinable')(var.get(u'$pos').get(u'nodeBefore'), var.get(u'$pos').get(u'nodeAfter')) and var.get(u'$pos').get(u'parent').callprop(u'canReplace', var.get(u'index'), (var.get(u'index')+Js(1.0))))
    PyJsHoisted_canJoin_.func_name = u'canJoin'
    var.put(u'canJoin', PyJsHoisted_canJoin_)
    @Js
    def PyJsHoisted_withAttrs_(type, this, arguments, var=var):
        var = Scope({u'this':this, u'type':type, u'arguments':arguments}, var)
        var.registers([u'type'])
        PyJs_Object_424_ = Js({u'type':var.get(u'type'),u'attrs':var.get(u"null")})
        return PyJs_Object_424_
    PyJsHoisted_withAttrs_.func_name = u'withAttrs'
    var.put(u'withAttrs', PyJsHoisted_withAttrs_)
    @Js
    def PyJsHoisted_fitLeft_(PyJsArg_2466726f6d_, placed, this, arguments, var=var):
        var = Scope({u'this':this, u'$from':PyJsArg_2466726f6d_, u'arguments':arguments, u'placed':placed}, var)
        var.registers([u'content', u'openEnd', u'placed', u'ref', u'$from'])
        var.put(u'ref', var.get(u'fitLeftInner')(var.get(u'$from'), Js(0.0), var.get(u'placed'), Js(False)))
        var.put(u'content', var.get(u'ref').get(u'content'))
        var.put(u'openEnd', var.get(u'ref').get(u'openEnd'))
        return var.get(u'dist').get(u'Slice').create(var.get(u'content'), var.get(u'$from').get(u'depth'), (var.get(u'openEnd') or Js(0.0)))
    PyJsHoisted_fitLeft_.func_name = u'fitLeft'
    var.put(u'fitLeft', PyJsHoisted_fitLeft_)
    @Js
    def PyJsHoisted_mapFragment_(fragment, f, parent, this, arguments, var=var):
        var = Scope({u'fragment':fragment, u'this':this, u'arguments':arguments, u'parent':parent, u'f':f}, var)
        var.registers([u'parent', u'f', u'i', u'mapped', u'fragment', u'child'])
        var.put(u'mapped', Js([]))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u'fragment').get(u'childCount')):
            try:
                var.put(u'child', var.get(u'fragment').callprop(u'child', var.get(u'i')))
                if var.get(u'child').get(u'content').get(u'size'):
                    var.put(u'child', var.get(u'child').callprop(u'copy', var.get(u'mapFragment')(var.get(u'child').get(u'content'), var.get(u'f'), var.get(u'child'))))
                if var.get(u'child').get(u'isInline'):
                    var.put(u'child', var.get(u'f')(var.get(u'child'), var.get(u'parent'), var.get(u'i')))
                var.get(u'mapped').callprop(u'push', var.get(u'child'))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return var.get(u'dist').get(u'Fragment').callprop(u'fromArray', var.get(u'mapped'))
    PyJsHoisted_mapFragment_.func_name = u'mapFragment'
    var.put(u'mapFragment', PyJsHoisted_mapFragment_)
    @Js
    def PyJsHoisted_fitsTrivially_(PyJsArg_2466726f6d_, PyJsArg_24746f_, slice, this, arguments, var=var):
        var = Scope({u'this':this, u'$from':PyJsArg_2466726f6d_, u'slice':slice, u'$to':PyJsArg_24746f_, u'arguments':arguments}, var)
        var.registers([u'$from', u'slice', u'$to'])
        return (((var.get(u'slice').get(u'openStart').neg() and var.get(u'slice').get(u'openEnd').neg()) and (var.get(u'$from').callprop(u'start')==var.get(u'$to').callprop(u'start'))) and var.get(u'$from').get(u'parent').callprop(u'canReplace', var.get(u'$from').callprop(u'index'), var.get(u'$to').callprop(u'index'), var.get(u'slice').get(u'content')))
    PyJsHoisted_fitsTrivially_.func_name = u'fitsTrivially'
    var.put(u'fitsTrivially', PyJsHoisted_fitsTrivially_)
    @Js
    def PyJsHoisted_fitRightJoin_(content, parent, PyJsArg_2466726f6d_, PyJsArg_24746f_, depth, openStart, openEnd, this, arguments, var=var):
        var = Scope({u'$to':PyJsArg_24746f_, u'parent':parent, u'this':this, u'$from':PyJsArg_2466726f6d_, u'content':content, u'depth':depth, u'openStart':openStart, u'openEnd':openEnd, u'arguments':arguments}, var)
        var.registers([u'count', u'joinable', u'matchCount', u'last', u'parent', u'i', u'$from', u'after', u'toNode', u'parentNode', u'joinable$1', u'content', u'depth', u'inner', u'closed', u'openEnd', u'$to', u'toIndex', u'match', u'openStart'])
        var.put(u'count', var.get(u'content').get(u'childCount'))
        var.put(u'matchCount', (var.get(u'count')-(Js(1.0) if (var.get(u'openEnd')>Js(0.0)) else Js(0.0))))
        var.put(u'parentNode', (var.get(u'parent') if (var.get(u'openStart')<Js(0.0)) else var.get(u'$from').callprop(u'node', var.get(u'depth'))))
        if (var.get(u'openStart')<Js(0.0)):
            var.put(u'match', var.get(u'parentNode').callprop(u'contentMatchAt', var.get(u'matchCount')))
        else:
            if ((var.get(u'count')==Js(1.0)) and (var.get(u'openEnd')>Js(0.0))):
                var.put(u'match', var.get(u'parentNode').callprop(u'contentMatchAt', (var.get(u'$from').callprop(u'index', var.get(u'depth')) if var.get(u'openStart') else var.get(u'$from').callprop(u'indexAfter', var.get(u'depth')))))
            else:
                var.put(u'match', var.get(u'parentNode').callprop(u'contentMatchAt', var.get(u'$from').callprop(u'indexAfter', var.get(u'depth'))).callprop(u'matchFragment', var.get(u'content'), (Js(1.0) if ((var.get(u'count')>Js(0.0)) and var.get(u'openStart')) else Js(0.0)), var.get(u'matchCount')))
        var.put(u'toNode', var.get(u'$to').callprop(u'node', var.get(u'depth')))
        if ((var.get(u'openEnd')>Js(0.0)) and (var.get(u'depth')<var.get(u'$to').get(u'depth'))):
            var.put(u'after', var.get(u'toNode').get(u'content').callprop(u'cutByIndex', var.get(u'$to').callprop(u'indexAfter', var.get(u'depth'))).callprop(u'addToStart', var.get(u'content').get(u'lastChild')))
            var.put(u'joinable$1', var.get(u'match').callprop(u'fillBefore', var.get(u'after'), Js(True)))
            if (((var.get(u'joinable$1') and var.get(u'joinable$1').get(u'size')) and (var.get(u'openStart')>Js(0.0))) and (var.get(u'count')==Js(1.0))):
                var.put(u'joinable$1', var.get(u"null"))
            if var.get(u'joinable$1'):
                var.put(u'inner', var.get(u'fitRightJoin')(var.get(u'content').get(u'lastChild').get(u'content'), var.get(u'content').get(u'lastChild'), var.get(u'$from'), var.get(u'$to'), (var.get(u'depth')+Js(1.0)), ((var.get(u'openStart')-Js(1.0)) if (var.get(u'count')==Js(1.0)) else (-Js(1.0))), (var.get(u'openEnd')-Js(1.0))))
                if var.get(u'inner'):
                    var.put(u'last', var.get(u'content').get(u'lastChild').callprop(u'copy', var.get(u'inner')))
                    if var.get(u'joinable$1').get(u'size'):
                        return var.get(u'content').callprop(u'cutByIndex', Js(0.0), (var.get(u'count')-Js(1.0))).callprop(u'append', var.get(u'joinable$1')).callprop(u'addToEnd', var.get(u'last'))
                    else:
                        return var.get(u'content').callprop(u'replaceChild', (var.get(u'count')-Js(1.0)), var.get(u'last'))
        if (var.get(u'openEnd')>Js(0.0)):
            var.put(u'match', var.get(u'match').callprop(u'matchType', (var.get(u'$from').callprop(u'node', (var.get(u'depth')+Js(1.0))) if ((var.get(u'count')==Js(1.0)) and (var.get(u'openStart')>Js(0.0))) else var.get(u'content').get(u'lastChild')).get(u'type')))
        var.put(u'toIndex', var.get(u'$to').callprop(u'index', var.get(u'depth')))
        if ((var.get(u'toIndex')==var.get(u'toNode').get(u'childCount')) and var.get(u'toNode').get(u'type').callprop(u'compatibleContent', var.get(u'parent').get(u'type')).neg()):
            return var.get(u"null")
        var.put(u'joinable', var.get(u'match').callprop(u'fillBefore', var.get(u'toNode').get(u'content'), Js(True), var.get(u'toIndex')))
        #for JS loop
        var.put(u'i', var.get(u'toIndex'))
        while (var.get(u'joinable') and (var.get(u'i')<var.get(u'toNode').get(u'content').get(u'childCount'))):
            try:
                if var.get(u'parentNode').get(u'type').callprop(u'allowsMarks', var.get(u'toNode').get(u'content').callprop(u'child', var.get(u'i')).get(u'marks')).neg():
                    var.put(u'joinable', var.get(u"null"))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        if var.get(u'joinable').neg():
            return var.get(u"null")
        if (var.get(u'openEnd')>Js(0.0)):
            var.put(u'closed', var.get(u'fitRightClosed')(var.get(u'content').get(u'lastChild'), (var.get(u'openEnd')-Js(1.0)), var.get(u'$from'), (var.get(u'depth')+Js(1.0)), ((var.get(u'openStart')-Js(1.0)) if (var.get(u'count')==Js(1.0)) else (-Js(1.0)))))
            var.put(u'content', var.get(u'content').callprop(u'replaceChild', (var.get(u'count')-Js(1.0)), var.get(u'closed')))
        var.put(u'content', var.get(u'content').callprop(u'append', var.get(u'joinable')))
        if (var.get(u'$to').get(u'depth')>var.get(u'depth')):
            var.put(u'content', var.get(u'content').callprop(u'addToEnd', var.get(u'fitRightSeparate')(var.get(u'$to'), (var.get(u'depth')+Js(1.0)))))
        return var.get(u'content')
    PyJsHoisted_fitRightJoin_.func_name = u'fitRightJoin'
    var.put(u'fitRightJoin', PyJsHoisted_fitRightJoin_)
    @Js
    def PyJsHoisted_insertPoint_(doc, pos, nodeType, this, arguments, var=var):
        var = Scope({u'this':this, u'doc':doc, u'nodeType':nodeType, u'pos':pos, u'arguments':arguments}, var)
        var.registers([u'index', u'nodeType', u'd', u'$pos', u'doc', u'd$1', u'pos', u'index$1'])
        var.put(u'$pos', var.get(u'doc').callprop(u'resolve', var.get(u'pos')))
        if var.get(u'$pos').get(u'parent').callprop(u'canReplaceWith', var.get(u'$pos').callprop(u'index'), var.get(u'$pos').callprop(u'index'), var.get(u'nodeType')):
            return var.get(u'pos')
        if (var.get(u'$pos').get(u'parentOffset')==Js(0.0)):
            #for JS loop
            var.put(u'd', (var.get(u'$pos').get(u'depth')-Js(1.0)))
            while (var.get(u'd')>=Js(0.0)):
                try:
                    var.put(u'index', var.get(u'$pos').callprop(u'index', var.get(u'd')))
                    if var.get(u'$pos').callprop(u'node', var.get(u'd')).callprop(u'canReplaceWith', var.get(u'index'), var.get(u'index'), var.get(u'nodeType')):
                        return var.get(u'$pos').callprop(u'before', (var.get(u'd')+Js(1.0)))
                    if (var.get(u'index')>Js(0.0)):
                        return var.get(u"null")
                finally:
                        (var.put(u'd',Js(var.get(u'd').to_number())-Js(1))+Js(1))
        if (var.get(u'$pos').get(u'parentOffset')==var.get(u'$pos').get(u'parent').get(u'content').get(u'size')):
            #for JS loop
            var.put(u'd$1', (var.get(u'$pos').get(u'depth')-Js(1.0)))
            while (var.get(u'd$1')>=Js(0.0)):
                try:
                    var.put(u'index$1', var.get(u'$pos').callprop(u'indexAfter', var.get(u'd$1')))
                    if var.get(u'$pos').callprop(u'node', var.get(u'd$1')).callprop(u'canReplaceWith', var.get(u'index$1'), var.get(u'index$1'), var.get(u'nodeType')):
                        return var.get(u'$pos').callprop(u'after', (var.get(u'd$1')+Js(1.0)))
                    if (var.get(u'index$1')<var.get(u'$pos').callprop(u'node', var.get(u'd$1')).get(u'childCount')):
                        return var.get(u"null")
                finally:
                        (var.put(u'd$1',Js(var.get(u'd$1').to_number())-Js(1))+Js(1))
    PyJsHoisted_insertPoint_.func_name = u'insertPoint'
    var.put(u'insertPoint', PyJsHoisted_insertPoint_)
    @Js
    def PyJsHoisted_closeFragment_(fragment, depth, oldOpen, newOpen, parent, this, arguments, var=var):
        var = Scope({u'this':this, u'depth':depth, u'oldOpen':oldOpen, u'arguments':arguments, u'parent':parent, u'fragment':fragment, u'newOpen':newOpen}, var)
        var.registers([u'parent', u'fragment', u'depth', u'oldOpen', u'newOpen', u'first'])
        if (var.get(u'depth')<var.get(u'oldOpen')):
            var.put(u'first', var.get(u'fragment').get(u'firstChild'))
            var.put(u'fragment', var.get(u'fragment').callprop(u'replaceChild', Js(0.0), var.get(u'first').callprop(u'copy', var.get(u'closeFragment')(var.get(u'first').get(u'content'), (var.get(u'depth')+Js(1.0)), var.get(u'oldOpen'), var.get(u'newOpen'), var.get(u'first')))))
        if (var.get(u'depth')>var.get(u'newOpen')):
            var.put(u'fragment', var.get(u'parent').callprop(u'contentMatchAt', Js(0.0)).callprop(u'fillBefore', var.get(u'fragment'), Js(True)).callprop(u'append', var.get(u'fragment')))
        return var.get(u'fragment')
    PyJsHoisted_closeFragment_.func_name = u'closeFragment'
    var.put(u'closeFragment', PyJsHoisted_closeFragment_)
    @Js
    def PyJsHoisted_nodeRight_(content, depth, this, arguments, var=var):
        var = Scope({u'content':content, u'this':this, u'depth':depth, u'arguments':arguments}, var)
        var.registers([u'i', u'content', u'depth'])
        #for JS loop
        var.put(u'i', Js(1.0))
        while (var.get(u'i')<var.get(u'depth')):
            try:
                var.put(u'content', var.get(u'content').get(u'lastChild').get(u'content'))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return var.get(u'content').get(u'lastChild')
    PyJsHoisted_nodeRight_.func_name = u'nodeRight'
    var.put(u'nodeRight', PyJsHoisted_nodeRight_)
    @Js
    def PyJsHoisted_fitRightSeparate_(PyJsArg_24746f_, depth, this, arguments, var=var):
        var = Scope({u'this':this, u'depth':depth, u'$to':PyJsArg_24746f_, u'arguments':arguments}, var)
        var.registers([u'node', u'depth', u'$to', u'fill'])
        var.put(u'node', var.get(u'$to').callprop(u'node', var.get(u'depth')))
        var.put(u'fill', var.get(u'node').callprop(u'contentMatchAt', Js(0.0)).callprop(u'fillBefore', var.get(u'node').get(u'content'), Js(True), var.get(u'$to').callprop(u'index', var.get(u'depth'))))
        if (var.get(u'$to').get(u'depth')>var.get(u'depth')):
            var.put(u'fill', var.get(u'fill').callprop(u'addToEnd', var.get(u'fitRightSeparate')(var.get(u'$to'), (var.get(u'depth')+Js(1.0)))))
        return var.get(u'node').callprop(u'copy', var.get(u'fill'))
    PyJsHoisted_fitRightSeparate_.func_name = u'fitRightSeparate'
    var.put(u'fitRightSeparate', PyJsHoisted_fitRightSeparate_)
    @Js
    def PyJsHoisted_canSplit_(doc, pos, depth, typesAfter, this, arguments, var=var):
        var = Scope({u'depth':depth, u'arguments':arguments, u'this':this, u'doc':doc, u'pos':pos, u'typesAfter':typesAfter}, var)
        var.registers([u'node', u'innerType', u'd', u'$pos', u'index', u'i', u'baseType', u'after', u'pos', u'index$1', u'typesAfter', u'depth', u'base', u'rest', u'doc'])
        if PyJsStrictEq(var.get(u'depth'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'depth', Js(1.0))
        var.put(u'$pos', var.get(u'doc').callprop(u'resolve', var.get(u'pos')))
        var.put(u'base', (var.get(u'$pos').get(u'depth')-var.get(u'depth')))
        var.put(u'innerType', ((var.get(u'typesAfter') and var.get(u'typesAfter').get((var.get(u'typesAfter').get(u'length')-Js(1.0)))) or var.get(u'$pos').get(u'parent')))
        def PyJs_LONG_430_(var=var):
            return ((((var.get(u'base')<Js(0.0)) or var.get(u'$pos').get(u'parent').get(u'type').get(u'spec').get(u'isolating')) or var.get(u'$pos').get(u'parent').callprop(u'canReplace', var.get(u'$pos').callprop(u'index'), var.get(u'$pos').get(u'parent').get(u'childCount')).neg()) or var.get(u'innerType').get(u'type').callprop(u'validContent', var.get(u'$pos').get(u'parent').get(u'content').callprop(u'cutByIndex', var.get(u'$pos').callprop(u'index'), var.get(u'$pos').get(u'parent').get(u'childCount'))).neg())
        if PyJs_LONG_430_():
            return Js(False)
        #for JS loop
        var.put(u'd', (var.get(u'$pos').get(u'depth')-Js(1.0)))
        var.put(u'i', (var.get(u'depth')-Js(2.0)))
        while (var.get(u'd')>var.get(u'base')):
            try:
                var.put(u'node', var.get(u'$pos').callprop(u'node', var.get(u'd')))
                var.put(u'index$1', var.get(u'$pos').callprop(u'index', var.get(u'd')))
                if var.get(u'node').get(u'type').get(u'spec').get(u'isolating'):
                    return Js(False)
                var.put(u'rest', var.get(u'node').get(u'content').callprop(u'cutByIndex', var.get(u'index$1'), var.get(u'node').get(u'childCount')))
                var.put(u'after', ((var.get(u'typesAfter') and var.get(u'typesAfter').get(var.get(u'i'))) or var.get(u'node')))
                if (var.get(u'after')!=var.get(u'node')):
                    var.put(u'rest', var.get(u'rest').callprop(u'replaceChild', Js(0.0), var.get(u'after').get(u'type').callprop(u'create', var.get(u'after').get(u'attrs'))))
                if (var.get(u'node').callprop(u'canReplace', (var.get(u'index$1')+Js(1.0)), var.get(u'node').get(u'childCount')).neg() or var.get(u'after').get(u'type').callprop(u'validContent', var.get(u'rest')).neg()):
                    return Js(False)
            finally:
                    PyJsComma((var.put(u'd',Js(var.get(u'd').to_number())-Js(1))+Js(1)),(var.put(u'i',Js(var.get(u'i').to_number())-Js(1))+Js(1)))
        var.put(u'index', var.get(u'$pos').callprop(u'indexAfter', var.get(u'base')))
        var.put(u'baseType', (var.get(u'typesAfter') and var.get(u'typesAfter').get(u'0')))
        return var.get(u'$pos').callprop(u'node', var.get(u'base')).callprop(u'canReplaceWith', var.get(u'index'), var.get(u'index'), (var.get(u'baseType').get(u'type') if var.get(u'baseType') else var.get(u'$pos').callprop(u'node', (var.get(u'base')+Js(1.0))).get(u'type')))
    PyJsHoisted_canSplit_.func_name = u'canSplit'
    var.put(u'canSplit', PyJsHoisted_canSplit_)
    @Js
    def PyJsHoisted_closeFragmentEnd_(fragment, depth, this, arguments, var=var):
        var = Scope({u'fragment':fragment, u'this':this, u'depth':depth, u'arguments':arguments}, var)
        var.registers([u'fragment', u'depth'])
        return (var.get(u'fragment').callprop(u'replaceChild', (var.get(u'fragment').get(u'childCount')-Js(1.0)), var.get(u'closeNodeEnd')(var.get(u'fragment').get(u'lastChild'), var.get(u'depth'))) if var.get(u'depth') else var.get(u'fragment'))
    PyJsHoisted_closeFragmentEnd_.func_name = u'closeFragmentEnd'
    var.put(u'closeFragmentEnd', PyJsHoisted_closeFragmentEnd_)
    @Js
    def PyJsHoisted_findWrappingInside_(range, type, this, arguments, var=var):
        var = Scope({u'this':this, u'range':range, u'type':type, u'arguments':arguments}, var)
        var.registers([u'endIndex', u'parent', u'innerMatch', u'i', u'inside', u'range', u'lastType', u'startIndex', u'inner', u'type'])
        var.put(u'parent', var.get(u'range').get(u'parent'))
        var.put(u'startIndex', var.get(u'range').get(u'startIndex'))
        var.put(u'endIndex', var.get(u'range').get(u'endIndex'))
        var.put(u'inner', var.get(u'parent').callprop(u'child', var.get(u'startIndex')))
        var.put(u'inside', var.get(u'type').get(u'contentMatch').callprop(u'findWrapping', var.get(u'inner').get(u'type')))
        if var.get(u'inside').neg():
            return var.get(u"null")
        var.put(u'lastType', (var.get(u'inside').get((var.get(u'inside').get(u'length')-Js(1.0))) if var.get(u'inside').get(u'length') else var.get(u'type')))
        var.put(u'innerMatch', var.get(u'lastType').get(u'contentMatch'))
        #for JS loop
        var.put(u'i', var.get(u'startIndex'))
        while (var.get(u'innerMatch') and (var.get(u'i')<var.get(u'endIndex'))):
            try:
                var.put(u'innerMatch', var.get(u'innerMatch').callprop(u'matchType', var.get(u'parent').callprop(u'child', var.get(u'i')).get(u'type')))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        if (var.get(u'innerMatch').neg() or var.get(u'innerMatch').get(u'validEnd').neg()):
            return var.get(u"null")
        return var.get(u'inside')
    PyJsHoisted_findWrappingInside_.func_name = u'findWrappingInside'
    var.put(u'findWrappingInside', PyJsHoisted_findWrappingInside_)
    @Js
    def PyJsHoisted_TransformError_(message, this, arguments, var=var):
        var = Scope({u'this':this, u'message':message, u'arguments':arguments}, var)
        var.registers([u'message', u'err'])
        var.put(u'err', var.get(u'Error').callprop(u'call', var.get(u"this"), var.get(u'message')))
        var.get(u'err').put(u'__proto__', var.get(u'TransformError').get(u'prototype'))
        return var.get(u'err')
    PyJsHoisted_TransformError_.func_name = u'TransformError'
    var.put(u'TransformError', PyJsHoisted_TransformError_)
    @Js
    def PyJsHoisted_findWrapping_(range, nodeType, attrs, innerRange, this, arguments, var=var):
        var = Scope({u'range':range, u'nodeType':nodeType, u'attrs':attrs, u'this':this, u'innerRange':innerRange, u'arguments':arguments}, var)
        var.registers([u'nodeType', u'around', u'innerRange', u'range', u'attrs', u'inner'])
        if PyJsStrictEq(var.get(u'innerRange'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'innerRange', var.get(u'range'))
        var.put(u'around', var.get(u'findWrappingOutside')(var.get(u'range'), var.get(u'nodeType')))
        var.put(u'inner', (var.get(u'around') and var.get(u'findWrappingInside')(var.get(u'innerRange'), var.get(u'nodeType'))))
        if var.get(u'inner').neg():
            return var.get(u"null")
        PyJs_Object_423_ = Js({u'type':var.get(u'nodeType'),u'attrs':var.get(u'attrs')})
        return var.get(u'around').callprop(u'map', var.get(u'withAttrs')).callprop(u'concat', PyJs_Object_423_).callprop(u'concat', var.get(u'inner').callprop(u'map', var.get(u'withAttrs')))
    PyJsHoisted_findWrapping_.func_name = u'findWrapping'
    var.put(u'findWrapping', PyJsHoisted_findWrapping_)
    @Js
    def PyJsHoisted_closeNodeStart_(node, openStart, openEnd, this, arguments, var=var):
        var = Scope({u'node':node, u'openEnd':openEnd, u'this':this, u'openStart':openStart, u'arguments':arguments}, var)
        var.registers([u'node', u'content', u'openStart', u'openEnd', u'first', u'fill'])
        var.put(u'content', var.get(u'node').get(u'content'))
        if (var.get(u'openStart')>Js(1.0)):
            var.put(u'first', var.get(u'closeNodeStart')(var.get(u'node').get(u'firstChild'), (var.get(u'openStart')-Js(1.0)), ((var.get(u'openEnd')-Js(1.0)) if (var.get(u'node').get(u'childCount')==Js(1.0)) else Js(0.0))))
            var.put(u'content', var.get(u'node').get(u'content').callprop(u'replaceChild', Js(0.0), var.get(u'first')))
        var.put(u'fill', var.get(u'node').get(u'type').get(u'contentMatch').callprop(u'fillBefore', var.get(u'content'), (var.get(u'openEnd')==Js(0.0))))
        return var.get(u'node').callprop(u'copy', var.get(u'fill').callprop(u'append', var.get(u'content')))
    PyJsHoisted_closeNodeStart_.func_name = u'closeNodeStart'
    var.put(u'closeNodeStart', PyJsHoisted_closeNodeStart_)
    @Js
    def PyJsHoisted_contentBetween_(doc, PyJsArg_66726f6d_, to, this, arguments, var=var):
        var = Scope({u'this':this, u'doc':doc, u'from':PyJsArg_66726f6d_, u'arguments':arguments, u'to':to}, var)
        var.registers([u'from', u'$from', u'dist$$1', u'next', u'to', u'depth', u'doc'])
        var.put(u'$from', var.get(u'doc').callprop(u'resolve', var.get(u'from')))
        var.put(u'dist$$1', (var.get(u'to')-var.get(u'from')))
        var.put(u'depth', var.get(u'$from').get(u'depth'))
        while (((var.get(u'dist$$1')>Js(0.0)) and (var.get(u'depth')>Js(0.0))) and (var.get(u'$from').callprop(u'indexAfter', var.get(u'depth'))==var.get(u'$from').callprop(u'node', var.get(u'depth')).get(u'childCount'))):
            (var.put(u'depth',Js(var.get(u'depth').to_number())-Js(1))+Js(1))
            (var.put(u'dist$$1',Js(var.get(u'dist$$1').to_number())-Js(1))+Js(1))
        if (var.get(u'dist$$1')>Js(0.0)):
            var.put(u'next', var.get(u'$from').callprop(u'node', var.get(u'depth')).callprop(u'maybeChild', var.get(u'$from').callprop(u'indexAfter', var.get(u'depth'))))
            while (var.get(u'dist$$1')>Js(0.0)):
                if (var.get(u'next').neg() or var.get(u'next').get(u'isLeaf')):
                    return Js(True)
                var.put(u'next', var.get(u'next').get(u'firstChild'))
                (var.put(u'dist$$1',Js(var.get(u'dist$$1').to_number())-Js(1))+Js(1))
        return Js(False)
    PyJsHoisted_contentBetween_.func_name = u'contentBetween'
    var.put(u'contentBetween', PyJsHoisted_contentBetween_)
    @Js
    def PyJsHoisted_coveredDepths_(PyJsArg_2466726f6d_, PyJsArg_24746f_, this, arguments, var=var):
        var = Scope({u'this':this, u'$from':PyJsArg_2466726f6d_, u'$to':PyJsArg_24746f_, u'arguments':arguments}, var)
        var.registers([u'minDepth', u'$to', u'd', u'$from', u'start', u'result'])
        var.put(u'result', Js([]))
        var.put(u'minDepth', var.get(u'Math').callprop(u'min', var.get(u'$from').get(u'depth'), var.get(u'$to').get(u'depth')))
        #for JS loop
        var.put(u'd', var.get(u'minDepth'))
        while (var.get(u'd')>=Js(0.0)):
            try:
                var.put(u'start', var.get(u'$from').callprop(u'start', var.get(u'd')))
                def PyJs_LONG_478_(var=var):
                    return ((((var.get(u'start')<(var.get(u'$from').get(u'pos')-(var.get(u'$from').get(u'depth')-var.get(u'd')))) or (var.get(u'$to').callprop(u'end', var.get(u'd'))>(var.get(u'$to').get(u'pos')+(var.get(u'$to').get(u'depth')-var.get(u'd'))))) or var.get(u'$from').callprop(u'node', var.get(u'd')).get(u'type').get(u'spec').get(u'isolating')) or var.get(u'$to').callprop(u'node', var.get(u'd')).get(u'type').get(u'spec').get(u'isolating'))
                if PyJs_LONG_478_():
                    break
                if (var.get(u'start')==var.get(u'$to').callprop(u'start', var.get(u'd'))):
                    var.get(u'result').callprop(u'push', var.get(u'd'))
            finally:
                    (var.put(u'd',Js(var.get(u'd').to_number())-Js(1))+Js(1))
        return var.get(u'result')
    PyJsHoisted_coveredDepths_.func_name = u'coveredDepths'
    var.put(u'coveredDepths', PyJsHoisted_coveredDepths_)
    @Js
    def PyJsHoisted_canCut_(node, start, end, this, arguments, var=var):
        var = Scope({u'node':node, u'start':start, u'this':this, u'end':end, u'arguments':arguments}, var)
        var.registers([u'node', u'start', u'end'])
        return (((var.get(u'start')==Js(0.0)) or var.get(u'node').callprop(u'canReplace', var.get(u'start'), var.get(u'node').get(u'childCount'))) and ((var.get(u'end')==var.get(u'node').get(u'childCount')) or var.get(u'node').callprop(u'canReplace', Js(0.0), var.get(u'end'))))
    PyJsHoisted_canCut_.func_name = u'canCut'
    var.put(u'canCut', PyJsHoisted_canCut_)
    @Js
    def PyJsHoisted_makeRecover_(index, offset, this, arguments, var=var):
        var = Scope({u'this':this, u'index':index, u'arguments':arguments, u'offset':offset}, var)
        var.registers([u'index', u'offset'])
        return (var.get(u'index')+(var.get(u'offset')*var.get(u'factor16')))
    PyJsHoisted_makeRecover_.func_name = u'makeRecover'
    var.put(u'makeRecover', PyJsHoisted_makeRecover_)
    @Js
    def PyJsHoisted_replaceStep_(doc, PyJsArg_66726f6d_, to, slice, this, arguments, var=var):
        var = Scope({u'to':to, u'slice':slice, u'from':PyJsArg_66726f6d_, u'arguments':arguments, u'this':this, u'doc':doc}, var)
        var.registers([u'slice', u'$to', u'd', u'to', u'fittedLeft', u'after', u'placed', u'doc', u'$from', u'from', u'fittedAfter', u'fitted'])
        if PyJsStrictEq(var.get(u'to'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'to', var.get(u'from'))
        if PyJsStrictEq(var.get(u'slice'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'slice', var.get(u'dist').get(u'Slice').get(u'empty'))
        if ((var.get(u'from')==var.get(u'to')) and var.get(u'slice').get(u'size').neg()):
            return var.get(u"null")
        var.put(u'$from', var.get(u'doc').callprop(u'resolve', var.get(u'from')))
        var.put(u'$to', var.get(u'doc').callprop(u'resolve', var.get(u'to')))
        if var.get(u'fitsTrivially')(var.get(u'$from'), var.get(u'$to'), var.get(u'slice')):
            return var.get(u'ReplaceStep').create(var.get(u'from'), var.get(u'to'), var.get(u'slice'))
        var.put(u'placed', var.get(u'placeSlice')(var.get(u'$from'), var.get(u'slice')))
        var.put(u'fittedLeft', var.get(u'fitLeft')(var.get(u'$from'), var.get(u'placed')))
        var.put(u'fitted', var.get(u'fitRight')(var.get(u'$from'), var.get(u'$to'), var.get(u'fittedLeft')))
        if var.get(u'fitted').neg():
            return var.get(u"null")
        if ((var.get(u'fittedLeft').get(u'size')!=var.get(u'fitted').get(u'size')) and var.get(u'canMoveText')(var.get(u'$from'), var.get(u'$to'), var.get(u'fittedLeft'))):
            var.put(u'd', var.get(u'$to').get(u'depth'))
            var.put(u'after', var.get(u'$to').callprop(u'after', var.get(u'd')))
            while ((var.get(u'd')>Js(1.0)) and (var.get(u'after')==var.get(u'$to').callprop(u'end', var.put(u'd',Js(var.get(u'd').to_number())-Js(1))))):
                var.put(u'after',Js(var.get(u'after').to_number())+Js(1))
            var.put(u'fittedAfter', var.get(u'fitRight')(var.get(u'$from'), var.get(u'doc').callprop(u'resolve', var.get(u'after')), var.get(u'fittedLeft')))
            if var.get(u'fittedAfter'):
                return var.get(u'ReplaceAroundStep').create(var.get(u'from'), var.get(u'after'), var.get(u'to'), var.get(u'$to').callprop(u'end'), var.get(u'fittedAfter'), var.get(u'fittedLeft').get(u'size'))
        return (var.get(u'ReplaceStep').create(var.get(u'from'), var.get(u'to'), var.get(u'fitted')) if (var.get(u'fitted').get(u'size') or (var.get(u'from')!=var.get(u'to'))) else var.get(u"null"))
    PyJsHoisted_replaceStep_.func_name = u'replaceStep'
    var.put(u'replaceStep', PyJsHoisted_replaceStep_)
    @Js
    def PyJsHoisted_dropPoint_(doc, pos, slice, this, arguments, var=var):
        var = Scope({u'this':this, u'doc':doc, u'slice':slice, u'pos':pos, u'arguments':arguments}, var)
        var.registers([u'slice', u'd', u'$pos', u'i', u'doc', u'pos', u'content', u'bias', u'pass', u'insertPos'])
        var.put(u'$pos', var.get(u'doc').callprop(u'resolve', var.get(u'pos')))
        if var.get(u'slice').get(u'content').get(u'size').neg():
            return var.get(u'pos')
        var.put(u'content', var.get(u'slice').get(u'content'))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u'slice').get(u'openStart')):
            try:
                var.put(u'content', var.get(u'content').get(u'firstChild').get(u'content'))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        #for JS loop
        var.put(u'pass', Js(1.0))
        while (var.get(u'pass')<=(Js(2.0) if ((var.get(u'slice').get(u'openStart')==Js(0.0)) and var.get(u'slice').get(u'size')) else Js(1.0))):
            try:
                #for JS loop
                var.put(u'd', var.get(u'$pos').get(u'depth'))
                while (var.get(u'd')>=Js(0.0)):
                    try:
                        var.put(u'bias', (Js(0.0) if (var.get(u'd')==var.get(u'$pos').get(u'depth')) else ((-Js(1.0)) if (var.get(u'$pos').get(u'pos')<=((var.get(u'$pos').callprop(u'start', (var.get(u'd')+Js(1.0)))+var.get(u'$pos').callprop(u'end', (var.get(u'd')+Js(1.0))))/Js(2.0))) else Js(1.0))))
                        var.put(u'insertPos', (var.get(u'$pos').callprop(u'index', var.get(u'd'))+(Js(1.0) if (var.get(u'bias')>Js(0.0)) else Js(0.0))))
                        if (var.get(u'$pos').callprop(u'node', var.get(u'd')).callprop(u'canReplace', var.get(u'insertPos'), var.get(u'insertPos'), var.get(u'content')) if (var.get(u'pass')==Js(1.0)) else var.get(u'$pos').callprop(u'node', var.get(u'd')).callprop(u'contentMatchAt', var.get(u'insertPos')).callprop(u'findWrapping', var.get(u'content').get(u'firstChild').get(u'type'))):
                            return (var.get(u'$pos').get(u'pos') if (var.get(u'bias')==Js(0.0)) else (var.get(u'$pos').callprop(u'before', (var.get(u'd')+Js(1.0))) if (var.get(u'bias')<Js(0.0)) else var.get(u'$pos').callprop(u'after', (var.get(u'd')+Js(1.0)))))
                    finally:
                            (var.put(u'd',Js(var.get(u'd').to_number())-Js(1))+Js(1))
            finally:
                    (var.put(u'pass',Js(var.get(u'pass').to_number())+Js(1))-Js(1))
        return var.get(u"null")
    PyJsHoisted_dropPoint_.func_name = u'dropPoint'
    var.put(u'dropPoint', PyJsHoisted_dropPoint_)
    @Js
    def PyJsHoisted_normalizeSlice_(content, openStart, openEnd, this, arguments, var=var):
        var = Scope({u'content':content, u'openEnd':openEnd, u'this':this, u'openStart':openStart, u'arguments':arguments}, var)
        var.registers([u'content', u'openEnd', u'openStart'])
        while (((var.get(u'openStart')>Js(0.0)) and (var.get(u'openEnd')>Js(0.0))) and (var.get(u'content').get(u'childCount')==Js(1.0))):
            var.put(u'content', var.get(u'content').get(u'firstChild').get(u'content'))
            (var.put(u'openStart',Js(var.get(u'openStart').to_number())-Js(1))+Js(1))
            (var.put(u'openEnd',Js(var.get(u'openEnd').to_number())-Js(1))+Js(1))
        return var.get(u'dist').get(u'Slice').create(var.get(u'content'), var.get(u'openStart'), var.get(u'openEnd'))
    PyJsHoisted_normalizeSlice_.func_name = u'normalizeSlice'
    var.put(u'normalizeSlice', PyJsHoisted_normalizeSlice_)
    @Js
    def PyJsHoisted_fitLeftInner_(PyJsArg_2466726f6d_, depth, placed, placedBelow, this, arguments, var=var):
        var = Scope({u'placed':placed, u'depth':depth, u'arguments':arguments, u'this':this, u'$from':PyJsArg_2466726f6d_, u'placedBelow':placedBelow}, var)
        var.registers([u'$from', u'placedBelow', u'content', u'placed', u'depth', u'placedHere', u'inner', u'openEnd'])
        var.put(u'content', var.get(u'dist').get(u'Fragment').get(u'empty'))
        var.put(u'openEnd', Js(0.0))
        var.put(u'placedHere', var.get(u'placed').get(var.get(u'depth')))
        if (var.get(u'$from').get(u'depth')>var.get(u'depth')):
            var.put(u'inner', var.get(u'fitLeftInner')(var.get(u'$from'), (var.get(u'depth')+Js(1.0)), var.get(u'placed'), (var.get(u'placedBelow') or var.get(u'placedHere'))))
            var.put(u'openEnd', (var.get(u'inner').get(u'openEnd')+Js(1.0)))
            var.put(u'content', var.get(u'dist').get(u'Fragment').callprop(u'from', var.get(u'$from').callprop(u'node', (var.get(u'depth')+Js(1.0))).callprop(u'copy', var.get(u'inner').get(u'content'))))
        if var.get(u'placedHere'):
            var.put(u'content', var.get(u'content').callprop(u'append', var.get(u'placedHere').get(u'content')))
            var.put(u'openEnd', var.get(u'placedHere').get(u'openEnd'))
        if var.get(u'placedBelow'):
            var.put(u'content', var.get(u'content').callprop(u'append', var.get(u'$from').callprop(u'node', var.get(u'depth')).callprop(u'contentMatchAt', var.get(u'$from').callprop(u'indexAfter', var.get(u'depth'))).callprop(u'fillBefore', var.get(u'dist').get(u'Fragment').get(u'empty'), Js(True))))
            var.put(u'openEnd', Js(0.0))
        PyJs_Object_464_ = Js({u'content':var.get(u'content'),u'openEnd':var.get(u'openEnd')})
        return PyJs_Object_464_
    PyJsHoisted_fitLeftInner_.func_name = u'fitLeftInner'
    var.put(u'fitLeftInner', PyJsHoisted_fitLeftInner_)
    PyJs_Object_356_ = Js({u'value':Js(True)})
    var.get(u'Object').callprop(u'defineProperty', var.get(u'exports'), Js(u'__esModule'), PyJs_Object_356_)
    var.put(u'lower16', Js(65535))
    var.put(u'factor16', var.get(u'Math').callprop(u'pow', Js(2.0), Js(16.0)))
    pass
    pass
    pass
    @Js
    def PyJs_MapResult_357_(pos, deleted, recover, this, arguments, var=var):
        var = Scope({u'deleted':deleted, u'MapResult':PyJs_MapResult_357_, u'pos':pos, u'this':this, u'arguments':arguments, u'recover':recover}, var)
        var.registers([u'deleted', u'recover', u'pos'])
        if PyJsStrictEq(var.get(u'deleted'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'deleted', Js(False))
        if PyJsStrictEq(var.get(u'recover'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'recover', var.get(u"null"))
        var.get(u"this").put(u'pos', var.get(u'pos'))
        var.get(u"this").put(u'deleted', var.get(u'deleted'))
        var.get(u"this").put(u'recover', var.get(u'recover'))
    PyJs_MapResult_357_._set_name(u'MapResult')
    var.put(u'MapResult', PyJs_MapResult_357_)
    @Js
    def PyJs_StepMap_358_(ranges, inverted, this, arguments, var=var):
        var = Scope({u'ranges':ranges, u'this':this, u'StepMap':PyJs_StepMap_358_, u'arguments':arguments, u'inverted':inverted}, var)
        var.registers([u'ranges', u'inverted'])
        if PyJsStrictEq(var.get(u'inverted'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'inverted', Js(False))
        var.get(u"this").put(u'ranges', var.get(u'ranges'))
        var.get(u"this").put(u'inverted', var.get(u'inverted'))
    PyJs_StepMap_358_._set_name(u'StepMap')
    var.put(u'StepMap', PyJs_StepMap_358_)
    @Js
    def PyJs_recover_359_(value, this, arguments, var=var):
        var = Scope({u'this':this, u'recover':PyJs_recover_359_, u'arguments':arguments, u'value':value}, var)
        var.registers([u'i', u'diff', u'index', u'value', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        var.put(u'diff', Js(0.0))
        var.put(u'index', var.get(u'recoverIndex')(var.get(u'value')))
        if var.get(u"this").get(u'inverted').neg():
            #for JS loop
            var.put(u'i', Js(0.0))
            while (var.get(u'i')<var.get(u'index')):
                try:
                    var.put(u'diff', (var.get(u'this$1').get(u'ranges').get(((var.get(u'i')*Js(3.0))+Js(2.0)))-var.get(u'this$1').get(u'ranges').get(((var.get(u'i')*Js(3.0))+Js(1.0)))), u'+')
                finally:
                        (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return ((var.get(u"this").get(u'ranges').get((var.get(u'index')*Js(3.0)))+var.get(u'diff'))+var.get(u'recoverOffset')(var.get(u'value')))
    PyJs_recover_359_._set_name(u'recover')
    var.get(u'StepMap').get(u'prototype').put(u'recover', PyJs_recover_359_)
    @Js
    def PyJs_mapResult_360_(pos, assoc, this, arguments, var=var):
        var = Scope({u'this':this, u'mapResult':PyJs_mapResult_360_, u'assoc':assoc, u'pos':pos, u'arguments':arguments}, var)
        var.registers([u'assoc', u'pos'])
        if PyJsStrictEq(var.get(u'assoc'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'assoc', Js(1.0))
        return var.get(u"this").callprop(u'_map', var.get(u'pos'), var.get(u'assoc'), Js(False))
    PyJs_mapResult_360_._set_name(u'mapResult')
    var.get(u'StepMap').get(u'prototype').put(u'mapResult', PyJs_mapResult_360_)
    @Js
    def PyJs_map_361_(pos, assoc, this, arguments, var=var):
        var = Scope({u'this':this, u'map':PyJs_map_361_, u'assoc':assoc, u'pos':pos, u'arguments':arguments}, var)
        var.registers([u'assoc', u'pos'])
        if PyJsStrictEq(var.get(u'assoc'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'assoc', Js(1.0))
        return var.get(u"this").callprop(u'_map', var.get(u'pos'), var.get(u'assoc'), Js(True))
    PyJs_map_361_._set_name(u'map')
    var.get(u'StepMap').get(u'prototype').put(u'map', PyJs_map_361_)
    @Js
    def PyJs__map_362_(pos, assoc, simple, this, arguments, var=var):
        var = Scope({u'_map':PyJs__map_362_, u'simple':simple, u'pos':pos, u'this':this, u'assoc':assoc, u'arguments':arguments}, var)
        var.registers([u'oldIndex', u'newSize', u'oldSize', u'end', u'i', u'simple', u'pos', u'start', u'assoc', u'result', u'this$1', u'diff', u'recover', u'side', u'newIndex'])
        var.put(u'this$1', var.get(u"this"))
        var.put(u'diff', Js(0.0))
        var.put(u'oldIndex', (Js(2.0) if var.get(u"this").get(u'inverted') else Js(1.0)))
        var.put(u'newIndex', (Js(1.0) if var.get(u"this").get(u'inverted') else Js(2.0)))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u"this").get(u'ranges').get(u'length')):
            try:
                var.put(u'start', (var.get(u'this$1').get(u'ranges').get(var.get(u'i'))-(var.get(u'diff') if var.get(u'this$1').get(u'inverted') else Js(0.0))))
                if (var.get(u'start')>var.get(u'pos')):
                    break
                var.put(u'oldSize', var.get(u'this$1').get(u'ranges').get((var.get(u'i')+var.get(u'oldIndex'))))
                var.put(u'newSize', var.get(u'this$1').get(u'ranges').get((var.get(u'i')+var.get(u'newIndex'))))
                var.put(u'end', (var.get(u'start')+var.get(u'oldSize')))
                if (var.get(u'pos')<=var.get(u'end')):
                    var.put(u'side', (var.get(u'assoc') if var.get(u'oldSize').neg() else ((-Js(1.0)) if (var.get(u'pos')==var.get(u'start')) else (Js(1.0) if (var.get(u'pos')==var.get(u'end')) else var.get(u'assoc')))))
                    var.put(u'result', ((var.get(u'start')+var.get(u'diff'))+(Js(0.0) if (var.get(u'side')<Js(0.0)) else var.get(u'newSize'))))
                    if var.get(u'simple'):
                        return var.get(u'result')
                    var.put(u'recover', var.get(u'makeRecover')((var.get(u'i')/Js(3.0)), (var.get(u'pos')-var.get(u'start'))))
                    return var.get(u'MapResult').create(var.get(u'result'), ((var.get(u'pos')!=var.get(u'start')) if (var.get(u'assoc')<Js(0.0)) else (var.get(u'pos')!=var.get(u'end'))), var.get(u'recover'))
                var.put(u'diff', (var.get(u'newSize')-var.get(u'oldSize')), u'+')
            finally:
                    var.put(u'i', Js(3.0), u'+')
        return ((var.get(u'pos')+var.get(u'diff')) if var.get(u'simple') else var.get(u'MapResult').create((var.get(u'pos')+var.get(u'diff'))))
    PyJs__map_362_._set_name(u'_map')
    var.get(u'StepMap').get(u'prototype').put(u'_map', PyJs__map_362_)
    @Js
    def PyJs_touches_363_(pos, recover, this, arguments, var=var):
        var = Scope({u'this':this, u'touches':PyJs_touches_363_, u'recover':recover, u'pos':pos, u'arguments':arguments}, var)
        var.registers([u'oldIndex', u'oldSize', u'end', u'index', u'i', u'pos', u'start', u'this$1', u'diff', u'recover', u'newIndex'])
        var.put(u'this$1', var.get(u"this"))
        var.put(u'diff', Js(0.0))
        var.put(u'index', var.get(u'recoverIndex')(var.get(u'recover')))
        var.put(u'oldIndex', (Js(2.0) if var.get(u"this").get(u'inverted') else Js(1.0)))
        var.put(u'newIndex', (Js(1.0) if var.get(u"this").get(u'inverted') else Js(2.0)))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u"this").get(u'ranges').get(u'length')):
            try:
                var.put(u'start', (var.get(u'this$1').get(u'ranges').get(var.get(u'i'))-(var.get(u'diff') if var.get(u'this$1').get(u'inverted') else Js(0.0))))
                if (var.get(u'start')>var.get(u'pos')):
                    break
                var.put(u'oldSize', var.get(u'this$1').get(u'ranges').get((var.get(u'i')+var.get(u'oldIndex'))))
                var.put(u'end', (var.get(u'start')+var.get(u'oldSize')))
                if ((var.get(u'pos')<=var.get(u'end')) and (var.get(u'i')==(var.get(u'index')*Js(3.0)))):
                    return Js(True)
                var.put(u'diff', (var.get(u'this$1').get(u'ranges').get((var.get(u'i')+var.get(u'newIndex')))-var.get(u'oldSize')), u'+')
            finally:
                    var.put(u'i', Js(3.0), u'+')
        return Js(False)
    PyJs_touches_363_._set_name(u'touches')
    var.get(u'StepMap').get(u'prototype').put(u'touches', PyJs_touches_363_)
    @Js
    def PyJs_forEach_364_(f, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'forEach':PyJs_forEach_364_, u'f':f}, var)
        var.registers([u'oldIndex', u'newStart', u'oldSize', u'f', u'i', u'newSize', u'start', u'this$1', u'diff', u'oldStart', u'newIndex'])
        var.put(u'this$1', var.get(u"this"))
        var.put(u'oldIndex', (Js(2.0) if var.get(u"this").get(u'inverted') else Js(1.0)))
        var.put(u'newIndex', (Js(1.0) if var.get(u"this").get(u'inverted') else Js(2.0)))
        #for JS loop
        var.put(u'i', Js(0.0))
        var.put(u'diff', Js(0.0))
        while (var.get(u'i')<var.get(u"this").get(u'ranges').get(u'length')):
            try:
                var.put(u'start', var.get(u'this$1').get(u'ranges').get(var.get(u'i')))
                var.put(u'oldStart', (var.get(u'start')-(var.get(u'diff') if var.get(u'this$1').get(u'inverted') else Js(0.0))))
                var.put(u'newStart', (var.get(u'start')+(Js(0.0) if var.get(u'this$1').get(u'inverted') else var.get(u'diff'))))
                var.put(u'oldSize', var.get(u'this$1').get(u'ranges').get((var.get(u'i')+var.get(u'oldIndex'))))
                var.put(u'newSize', var.get(u'this$1').get(u'ranges').get((var.get(u'i')+var.get(u'newIndex'))))
                var.get(u'f')(var.get(u'oldStart'), (var.get(u'oldStart')+var.get(u'oldSize')), var.get(u'newStart'), (var.get(u'newStart')+var.get(u'newSize')))
                var.put(u'diff', (var.get(u'newSize')-var.get(u'oldSize')), u'+')
            finally:
                    var.put(u'i', Js(3.0), u'+')
    PyJs_forEach_364_._set_name(u'forEach')
    var.get(u'StepMap').get(u'prototype').put(u'forEach', PyJs_forEach_364_)
    @Js
    def PyJs_invert_365_(this, arguments, var=var):
        var = Scope({u'this':this, u'invert':PyJs_invert_365_, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u'StepMap').create(var.get(u"this").get(u'ranges'), var.get(u"this").get(u'inverted').neg())
    PyJs_invert_365_._set_name(u'invert')
    var.get(u'StepMap').get(u'prototype').put(u'invert', PyJs_invert_365_)
    @Js
    def PyJs_toString_366_(this, arguments, var=var):
        var = Scope({u'this':this, u'toString':PyJs_toString_366_, u'arguments':arguments}, var)
        var.registers([])
        return ((Js(u'-') if var.get(u"this").get(u'inverted') else Js(u''))+var.get(u'JSON').callprop(u'stringify', var.get(u"this").get(u'ranges')))
    PyJs_toString_366_._set_name(u'toString')
    var.get(u'StepMap').get(u'prototype').put(u'toString', PyJs_toString_366_)
    @Js
    def PyJs_offset_367_(n, this, arguments, var=var):
        var = Scope({u'this':this, u'offset':PyJs_offset_367_, u'arguments':arguments, u'n':n}, var)
        var.registers([u'n'])
        return (var.get(u'StepMap').get(u'empty') if (var.get(u'n')==Js(0.0)) else var.get(u'StepMap').create((Js([Js(0.0), (-var.get(u'n')), Js(0.0)]) if (var.get(u'n')<Js(0.0)) else Js([Js(0.0), Js(0.0), var.get(u'n')]))))
    PyJs_offset_367_._set_name(u'offset')
    var.get(u'StepMap').put(u'offset', PyJs_offset_367_)
    var.get(u'StepMap').put(u'empty', var.get(u'StepMap').create(Js([])))
    @Js
    def PyJs_Mapping_368_(maps, mirror, PyJsArg_66726f6d_, to, this, arguments, var=var):
        var = Scope({u'maps':maps, u'from':PyJsArg_66726f6d_, u'arguments':arguments, u'to':to, u'this':this, u'mirror':mirror, u'Mapping':PyJs_Mapping_368_}, var)
        var.registers([u'maps', u'from', u'to', u'mirror'])
        var.get(u"this").put(u'maps', (var.get(u'maps') or Js([])))
        var.get(u"this").put(u'from', (var.get(u'from') or Js(0.0)))
        var.get(u"this").put(u'to', (var.get(u"this").get(u'maps').get(u'length') if (var.get(u'to')==var.get(u"null")) else var.get(u'to')))
        var.get(u"this").put(u'mirror', var.get(u'mirror'))
    PyJs_Mapping_368_._set_name(u'Mapping')
    var.put(u'Mapping', PyJs_Mapping_368_)
    @Js
    def PyJs_slice_369_(PyJsArg_66726f6d_, to, this, arguments, var=var):
        var = Scope({u'this':this, u'to':to, u'slice':PyJs_slice_369_, u'from':PyJsArg_66726f6d_, u'arguments':arguments}, var)
        var.registers([u'to', u'from'])
        if PyJsStrictEq(var.get(u'from'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'from', Js(0.0))
        if PyJsStrictEq(var.get(u'to'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'to', var.get(u"this").get(u'maps').get(u'length'))
        return var.get(u'Mapping').create(var.get(u"this").get(u'maps'), var.get(u"this").get(u'mirror'), var.get(u'from'), var.get(u'to'))
    PyJs_slice_369_._set_name(u'slice')
    var.get(u'Mapping').get(u'prototype').put(u'slice', PyJs_slice_369_)
    @Js
    def PyJs_copy_370_(this, arguments, var=var):
        var = Scope({u'this':this, u'copy':PyJs_copy_370_, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u'Mapping').create(var.get(u"this").get(u'maps').callprop(u'slice'), (var.get(u"this").get(u'mirror') and var.get(u"this").get(u'mirror').callprop(u'slice')), var.get(u"this").get(u'from'), var.get(u"this").get(u'to'))
    PyJs_copy_370_._set_name(u'copy')
    var.get(u'Mapping').get(u'prototype').put(u'copy', PyJs_copy_370_)
    @Js
    def PyJs_appendMap_371_(map, mirrors, this, arguments, var=var):
        var = Scope({u'this':this, u'map':map, u'appendMap':PyJs_appendMap_371_, u'arguments':arguments, u'mirrors':mirrors}, var)
        var.registers([u'map', u'mirrors'])
        var.get(u"this").put(u'to', var.get(u"this").get(u'maps').callprop(u'push', var.get(u'map')))
        if (var.get(u'mirrors')!=var.get(u"null")):
            var.get(u"this").callprop(u'setMirror', (var.get(u"this").get(u'maps').get(u'length')-Js(1.0)), var.get(u'mirrors'))
    PyJs_appendMap_371_._set_name(u'appendMap')
    var.get(u'Mapping').get(u'prototype').put(u'appendMap', PyJs_appendMap_371_)
    @Js
    def PyJs_appendMapping_372_(mapping, this, arguments, var=var):
        var = Scope({u'this':this, u'appendMapping':PyJs_appendMapping_372_, u'mapping':mapping, u'arguments':arguments}, var)
        var.registers([u'i', u'mapping', u'mirr', u'startSize', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        #for JS loop
        var.put(u'i', Js(0.0))
        var.put(u'startSize', var.get(u"this").get(u'maps').get(u'length'))
        while (var.get(u'i')<var.get(u'mapping').get(u'maps').get(u'length')):
            try:
                var.put(u'mirr', var.get(u'mapping').callprop(u'getMirror', var.get(u'i')))
                var.get(u'this$1').callprop(u'appendMap', var.get(u'mapping').get(u'maps').get(var.get(u'i')), ((var.get(u'startSize')+var.get(u'mirr')) if ((var.get(u'mirr')!=var.get(u"null")) and (var.get(u'mirr')<var.get(u'i'))) else var.get(u"null")))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
    PyJs_appendMapping_372_._set_name(u'appendMapping')
    var.get(u'Mapping').get(u'prototype').put(u'appendMapping', PyJs_appendMapping_372_)
    @Js
    def PyJs_getMirror_373_(n, this, arguments, var=var):
        var = Scope({u'this':this, u'getMirror':PyJs_getMirror_373_, u'arguments':arguments, u'n':n}, var)
        var.registers([u'i', u'n', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        if var.get(u"this").get(u'mirror'):
            #for JS loop
            var.put(u'i', Js(0.0))
            while (var.get(u'i')<var.get(u"this").get(u'mirror').get(u'length')):
                try:
                    if (var.get(u'this$1').get(u'mirror').get(var.get(u'i'))==var.get(u'n')):
                        return var.get(u'this$1').get(u'mirror').get((var.get(u'i')+((-Js(1.0)) if (var.get(u'i')%Js(2.0)) else Js(1.0))))
                finally:
                        (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
    PyJs_getMirror_373_._set_name(u'getMirror')
    var.get(u'Mapping').get(u'prototype').put(u'getMirror', PyJs_getMirror_373_)
    @Js
    def PyJs_setMirror_374_(n, m, this, arguments, var=var):
        var = Scope({u'this':this, u'setMirror':PyJs_setMirror_374_, u'm':m, u'arguments':arguments, u'n':n}, var)
        var.registers([u'm', u'n'])
        if var.get(u"this").get(u'mirror').neg():
            var.get(u"this").put(u'mirror', Js([]))
        var.get(u"this").get(u'mirror').callprop(u'push', var.get(u'n'), var.get(u'm'))
    PyJs_setMirror_374_._set_name(u'setMirror')
    var.get(u'Mapping').get(u'prototype').put(u'setMirror', PyJs_setMirror_374_)
    @Js
    def PyJs_appendMappingInverted_375_(mapping, this, arguments, var=var):
        var = Scope({u'this':this, u'appendMappingInverted':PyJs_appendMappingInverted_375_, u'mapping':mapping, u'arguments':arguments}, var)
        var.registers([u'i', u'totalSize', u'mapping', u'mirr', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        #for JS loop
        var.put(u'i', (var.get(u'mapping').get(u'maps').get(u'length')-Js(1.0)))
        var.put(u'totalSize', (var.get(u"this").get(u'maps').get(u'length')+var.get(u'mapping').get(u'maps').get(u'length')))
        while (var.get(u'i')>=Js(0.0)):
            try:
                var.put(u'mirr', var.get(u'mapping').callprop(u'getMirror', var.get(u'i')))
                var.get(u'this$1').callprop(u'appendMap', var.get(u'mapping').get(u'maps').get(var.get(u'i')).callprop(u'invert'), (((var.get(u'totalSize')-var.get(u'mirr'))-Js(1.0)) if ((var.get(u'mirr')!=var.get(u"null")) and (var.get(u'mirr')>var.get(u'i'))) else var.get(u"null")))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())-Js(1))+Js(1))
    PyJs_appendMappingInverted_375_._set_name(u'appendMappingInverted')
    var.get(u'Mapping').get(u'prototype').put(u'appendMappingInverted', PyJs_appendMappingInverted_375_)
    @Js
    def PyJs_invert_376_(this, arguments, var=var):
        var = Scope({u'this':this, u'invert':PyJs_invert_376_, u'arguments':arguments}, var)
        var.registers([u'inverse'])
        var.put(u'inverse', var.get(u'Mapping').create())
        var.get(u'inverse').callprop(u'appendMappingInverted', var.get(u"this"))
        return var.get(u'inverse')
    PyJs_invert_376_._set_name(u'invert')
    var.get(u'Mapping').get(u'prototype').put(u'invert', PyJs_invert_376_)
    @Js
    def PyJs_map_377_(pos, assoc, this, arguments, var=var):
        var = Scope({u'this':this, u'map':PyJs_map_377_, u'assoc':assoc, u'pos':pos, u'arguments':arguments}, var)
        var.registers([u'i', u'assoc', u'pos', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        if PyJsStrictEq(var.get(u'assoc'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'assoc', Js(1.0))
        if var.get(u"this").get(u'mirror'):
            return var.get(u"this").callprop(u'_map', var.get(u'pos'), var.get(u'assoc'), Js(True))
        #for JS loop
        var.put(u'i', var.get(u"this").get(u'from'))
        while (var.get(u'i')<var.get(u"this").get(u'to')):
            try:
                var.put(u'pos', var.get(u'this$1').get(u'maps').get(var.get(u'i')).callprop(u'map', var.get(u'pos'), var.get(u'assoc')))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return var.get(u'pos')
    PyJs_map_377_._set_name(u'map')
    var.get(u'Mapping').get(u'prototype').put(u'map', PyJs_map_377_)
    @Js
    def PyJs_mapResult_378_(pos, assoc, this, arguments, var=var):
        var = Scope({u'this':this, u'mapResult':PyJs_mapResult_378_, u'assoc':assoc, u'pos':pos, u'arguments':arguments}, var)
        var.registers([u'assoc', u'pos'])
        if PyJsStrictEq(var.get(u'assoc'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'assoc', Js(1.0))
        return var.get(u"this").callprop(u'_map', var.get(u'pos'), var.get(u'assoc'), Js(False))
    PyJs_mapResult_378_._set_name(u'mapResult')
    var.get(u'Mapping').get(u'prototype').put(u'mapResult', PyJs_mapResult_378_)
    @Js
    def PyJs__map_379_(pos, assoc, simple, this, arguments, var=var):
        var = Scope({u'_map':PyJs__map_379_, u'simple':simple, u'pos':pos, u'this':this, u'assoc':assoc, u'arguments':arguments}, var)
        var.registers([u'map', u'recoverables', u'deleted', u'pos', u'i', u'assoc', u'result', u'corr', u'this$1', u'rec', u'simple'])
        var.put(u'this$1', var.get(u"this"))
        var.put(u'deleted', Js(False))
        var.put(u'recoverables', var.get(u"null"))
        #for JS loop
        var.put(u'i', var.get(u"this").get(u'from'))
        while (var.get(u'i')<var.get(u"this").get(u'to')):
            try:
                var.put(u'map', var.get(u'this$1').get(u'maps').get(var.get(u'i')))
                var.put(u'rec', (var.get(u'recoverables') and var.get(u'recoverables').get(var.get(u'i'))))
                if ((var.get(u'rec')!=var.get(u"null")) and var.get(u'map').callprop(u'touches', var.get(u'pos'), var.get(u'rec'))):
                    var.put(u'pos', var.get(u'map').callprop(u'recover', var.get(u'rec')))
                    continue
                var.put(u'result', var.get(u'map').callprop(u'mapResult', var.get(u'pos'), var.get(u'assoc')))
                if (var.get(u'result').get(u'recover')!=var.get(u"null")):
                    var.put(u'corr', var.get(u'this$1').callprop(u'getMirror', var.get(u'i')))
                    if (((var.get(u'corr')!=var.get(u"null")) and (var.get(u'corr')>var.get(u'i'))) and (var.get(u'corr')<var.get(u'this$1').get(u'to'))):
                        if var.get(u'result').get(u'deleted'):
                            var.put(u'i', var.get(u'corr'))
                            var.put(u'pos', var.get(u'this$1').get(u'maps').get(var.get(u'corr')).callprop(u'recover', var.get(u'result').get(u'recover')))
                            continue
                        else:
                            (var.get(u'recoverables') or var.put(u'recoverables', var.get(u'Object').callprop(u'create', var.get(u"null")))).put(var.get(u'corr'), var.get(u'result').get(u'recover'))
                if var.get(u'result').get(u'deleted'):
                    var.put(u'deleted', Js(True))
                var.put(u'pos', var.get(u'result').get(u'pos'))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        return (var.get(u'pos') if var.get(u'simple') else var.get(u'MapResult').create(var.get(u'pos'), var.get(u'deleted')))
    PyJs__map_379_._set_name(u'_map')
    var.get(u'Mapping').get(u'prototype').put(u'_map', PyJs__map_379_)
    pass
    var.get(u'TransformError').put(u'prototype', var.get(u'Object').callprop(u'create', var.get(u'Error').get(u'prototype')))
    var.get(u'TransformError').get(u'prototype').put(u'constructor', var.get(u'TransformError'))
    var.get(u'TransformError').get(u'prototype').put(u'name', Js(u'TransformError'))
    @Js
    def PyJs_Transform_380_(doc, this, arguments, var=var):
        var = Scope({u'this':this, u'doc':doc, u'arguments':arguments, u'Transform':PyJs_Transform_380_}, var)
        var.registers([u'doc'])
        var.get(u"this").put(u'doc', var.get(u'doc'))
        var.get(u"this").put(u'steps', Js([]))
        var.get(u"this").put(u'docs', Js([]))
        var.get(u"this").put(u'mapping', var.get(u'Mapping').create())
    PyJs_Transform_380_._set_name(u'Transform')
    var.put(u'Transform', PyJs_Transform_380_)
    PyJs_Object_382_ = Js({})
    PyJs_Object_383_ = Js({})
    PyJs_Object_381_ = Js({u'before':PyJs_Object_382_,u'docChanged':PyJs_Object_383_})
    var.put(u'prototypeAccessors', PyJs_Object_381_)
    @Js
    def PyJs_anonymous_384_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return (var.get(u"this").get(u'docs').get(u'0') if var.get(u"this").get(u'docs').get(u'length') else var.get(u"this").get(u'doc'))
    PyJs_anonymous_384_._set_name(u'anonymous')
    var.get(u'prototypeAccessors').get(u'before').put(u'get', PyJs_anonymous_384_)
    @Js
    def PyJs_step_385_(object, this, arguments, var=var):
        var = Scope({u'this':this, u'step':PyJs_step_385_, u'object':object, u'arguments':arguments}, var)
        var.registers([u'object', u'result'])
        var.put(u'result', var.get(u"this").callprop(u'maybeStep', var.get(u'object')))
        if var.get(u'result').get(u'failed'):
            PyJsTempException = JsToPyException(var.get(u'TransformError').create(var.get(u'result').get(u'failed')))
            raise PyJsTempException
        return var.get(u"this")
    PyJs_step_385_._set_name(u'step')
    var.get(u'Transform').get(u'prototype').put(u'step', PyJs_step_385_)
    @Js
    def PyJs_maybeStep_386_(step, this, arguments, var=var):
        var = Scope({u'this':this, u'step':step, u'maybeStep':PyJs_maybeStep_386_, u'arguments':arguments}, var)
        var.registers([u'step', u'result'])
        var.put(u'result', var.get(u'step').callprop(u'apply', var.get(u"this").get(u'doc')))
        if var.get(u'result').get(u'failed').neg():
            var.get(u"this").callprop(u'addStep', var.get(u'step'), var.get(u'result').get(u'doc'))
        return var.get(u'result')
    PyJs_maybeStep_386_._set_name(u'maybeStep')
    var.get(u'Transform').get(u'prototype').put(u'maybeStep', PyJs_maybeStep_386_)
    @Js
    def PyJs_anonymous_387_(this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments}, var)
        var.registers([])
        return (var.get(u"this").get(u'steps').get(u'length')>Js(0.0))
    PyJs_anonymous_387_._set_name(u'anonymous')
    var.get(u'prototypeAccessors').get(u'docChanged').put(u'get', PyJs_anonymous_387_)
    @Js
    def PyJs_addStep_388_(step, doc, this, arguments, var=var):
        var = Scope({u'this':this, u'doc':doc, u'step':step, u'addStep':PyJs_addStep_388_, u'arguments':arguments}, var)
        var.registers([u'doc', u'step'])
        var.get(u"this").get(u'docs').callprop(u'push', var.get(u"this").get(u'doc'))
        var.get(u"this").get(u'steps').callprop(u'push', var.get(u'step'))
        var.get(u"this").get(u'mapping').callprop(u'appendMap', var.get(u'step').callprop(u'getMap'))
        var.get(u"this").put(u'doc', var.get(u'doc'))
    PyJs_addStep_388_._set_name(u'addStep')
    var.get(u'Transform').get(u'prototype').put(u'addStep', PyJs_addStep_388_)
    var.get(u'Object').callprop(u'defineProperties', var.get(u'Transform').get(u'prototype'), var.get(u'prototypeAccessors'))
    pass
    var.put(u'stepsByID', var.get(u'Object').callprop(u'create', var.get(u"null")))
    @Js
    def PyJs_Step_389_(this, arguments, var=var):
        var = Scope({u'this':this, u'Step':PyJs_Step_389_, u'arguments':arguments}, var)
        var.registers([])
        pass
    PyJs_Step_389_._set_name(u'Step')
    var.put(u'Step', PyJs_Step_389_)
    @Js
    def PyJs_apply_390_(_doc, this, arguments, var=var):
        var = Scope({u'this':this, u'apply':PyJs_apply_390_, u'_doc':_doc, u'arguments':arguments}, var)
        var.registers([u'_doc'])
        return var.get(u'mustOverride')()
    PyJs_apply_390_._set_name(u'apply')
    var.get(u'Step').get(u'prototype').put(u'apply', PyJs_apply_390_)
    @Js
    def PyJs_getMap_391_(this, arguments, var=var):
        var = Scope({u'this':this, u'getMap':PyJs_getMap_391_, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u'StepMap').get(u'empty')
    PyJs_getMap_391_._set_name(u'getMap')
    var.get(u'Step').get(u'prototype').put(u'getMap', PyJs_getMap_391_)
    @Js
    def PyJs_invert_392_(_doc, this, arguments, var=var):
        var = Scope({u'this':this, u'invert':PyJs_invert_392_, u'_doc':_doc, u'arguments':arguments}, var)
        var.registers([u'_doc'])
        return var.get(u'mustOverride')()
    PyJs_invert_392_._set_name(u'invert')
    var.get(u'Step').get(u'prototype').put(u'invert', PyJs_invert_392_)
    @Js
    def PyJs_map_393_(_mapping, this, arguments, var=var):
        var = Scope({u'this':this, u'map':PyJs_map_393_, u'arguments':arguments, u'_mapping':_mapping}, var)
        var.registers([u'_mapping'])
        return var.get(u'mustOverride')()
    PyJs_map_393_._set_name(u'map')
    var.get(u'Step').get(u'prototype').put(u'map', PyJs_map_393_)
    @Js
    def PyJs_merge_394_(_other, this, arguments, var=var):
        var = Scope({u'this':this, u'_other':_other, u'arguments':arguments, u'merge':PyJs_merge_394_}, var)
        var.registers([u'_other'])
        return var.get(u"null")
    PyJs_merge_394_._set_name(u'merge')
    var.get(u'Step').get(u'prototype').put(u'merge', PyJs_merge_394_)
    @Js
    def PyJs_toJSON_395_(this, arguments, var=var):
        var = Scope({u'this':this, u'toJSON':PyJs_toJSON_395_, u'arguments':arguments}, var)
        var.registers([])
        return var.get(u'mustOverride')()
    PyJs_toJSON_395_._set_name(u'toJSON')
    var.get(u'Step').get(u'prototype').put(u'toJSON', PyJs_toJSON_395_)
    @Js
    def PyJs_fromJSON_396_(schema, json, this, arguments, var=var):
        var = Scope({u'this':this, u'json':json, u'arguments':arguments, u'fromJSON':PyJs_fromJSON_396_, u'schema':schema}, var)
        var.registers([u'json', u'type', u'schema'])
        if (var.get(u'json').neg() or var.get(u'json').get(u'stepType').neg()):
            PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'Invalid input for Step.fromJSON')))
            raise PyJsTempException
        var.put(u'type', var.get(u'stepsByID').get(var.get(u'json').get(u'stepType')))
        if var.get(u'type').neg():
            PyJsTempException = JsToPyException(var.get(u'RangeError').create(((Js(u'No step type ')+var.get(u'json').get(u'stepType'))+Js(u' defined'))))
            raise PyJsTempException
        return var.get(u'type').callprop(u'fromJSON', var.get(u'schema'), var.get(u'json'))
    PyJs_fromJSON_396_._set_name(u'fromJSON')
    var.get(u'Step').put(u'fromJSON', PyJs_fromJSON_396_)
    @Js
    def PyJs_jsonID_397_(id, stepClass, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'jsonID':PyJs_jsonID_397_, u'id':id, u'stepClass':stepClass}, var)
        var.registers([u'id', u'stepClass'])
        if var.get(u'stepsByID').contains(var.get(u'id')):
            PyJsTempException = JsToPyException(var.get(u'RangeError').create((Js(u'Duplicate use of step JSON ID ')+var.get(u'id'))))
            raise PyJsTempException
        var.get(u'stepsByID').put(var.get(u'id'), var.get(u'stepClass'))
        var.get(u'stepClass').get(u'prototype').put(u'jsonID', var.get(u'id'))
        return var.get(u'stepClass')
    PyJs_jsonID_397_._set_name(u'jsonID')
    var.get(u'Step').put(u'jsonID', PyJs_jsonID_397_)
    @Js
    def PyJs_StepResult_398_(doc, failed, this, arguments, var=var):
        var = Scope({u'this':this, u'doc':doc, u'StepResult':PyJs_StepResult_398_, u'arguments':arguments, u'failed':failed}, var)
        var.registers([u'doc', u'failed'])
        var.get(u"this").put(u'doc', var.get(u'doc'))
        var.get(u"this").put(u'failed', var.get(u'failed'))
    PyJs_StepResult_398_._set_name(u'StepResult')
    var.put(u'StepResult', PyJs_StepResult_398_)
    @Js
    def PyJs_ok_399_(doc, this, arguments, var=var):
        var = Scope({u'this':this, u'doc':doc, u'ok':PyJs_ok_399_, u'arguments':arguments}, var)
        var.registers([u'doc'])
        return var.get(u'StepResult').create(var.get(u'doc'), var.get(u"null"))
    PyJs_ok_399_._set_name(u'ok')
    var.get(u'StepResult').put(u'ok', PyJs_ok_399_)
    @Js
    def PyJs_fail_400_(message, this, arguments, var=var):
        var = Scope({u'this':this, u'fail':PyJs_fail_400_, u'message':message, u'arguments':arguments}, var)
        var.registers([u'message'])
        return var.get(u'StepResult').create(var.get(u"null"), var.get(u'message'))
    PyJs_fail_400_._set_name(u'fail')
    var.get(u'StepResult').put(u'fail', PyJs_fail_400_)
    @Js
    def PyJs_fromReplace_401_(doc, PyJsArg_66726f6d_, to, slice, this, arguments, var=var):
        var = Scope({u'to':to, u'slice':slice, u'from':PyJsArg_66726f6d_, u'arguments':arguments, u'this':this, u'doc':doc, u'fromReplace':PyJs_fromReplace_401_}, var)
        var.registers([u'doc', u'slice', u'from', u'to'])
        try:
            return var.get(u'StepResult').callprop(u'ok', var.get(u'doc').callprop(u'replace', var.get(u'from'), var.get(u'to'), var.get(u'slice')))
        except PyJsException as PyJsTempException:
            PyJsHolder_65_47444503 = var.own.get(u'e')
            var.force_own_put(u'e', PyExceptionToJs(PyJsTempException))
            try:
                if var.get(u'e').instanceof(var.get(u'dist').get(u'ReplaceError')):
                    return var.get(u'StepResult').callprop(u'fail', var.get(u'e').get(u'message'))
                PyJsTempException = JsToPyException(var.get(u'e'))
                raise PyJsTempException
            finally:
                if PyJsHolder_65_47444503 is not None:
                    var.own[u'e'] = PyJsHolder_65_47444503
                else:
                    del var.own[u'e']
                del PyJsHolder_65_47444503
    PyJs_fromReplace_401_._set_name(u'fromReplace')
    var.get(u'StepResult').put(u'fromReplace', PyJs_fromReplace_401_)
    @Js
    def PyJs_anonymous_402_(PyJsArg_53746570242431_, this, arguments, var=var):
        var = Scope({u'this':this, u'Step$$1':PyJsArg_53746570242431_, u'arguments':arguments}, var)
        var.registers([u'Step$$1', u'ReplaceStep'])
        @Js
        def PyJsHoisted_ReplaceStep_(PyJsArg_66726f6d_, to, slice, structure, this, arguments, var=var):
            var = Scope({u'to':to, u'slice':slice, u'from':PyJsArg_66726f6d_, u'arguments':arguments, u'this':this, u'structure':structure}, var)
            var.registers([u'to', u'slice', u'from', u'structure'])
            var.get(u'Step$$1').callprop(u'call', var.get(u"this"))
            var.get(u"this").put(u'from', var.get(u'from'))
            var.get(u"this").put(u'to', var.get(u'to'))
            var.get(u"this").put(u'slice', var.get(u'slice'))
            var.get(u"this").put(u'structure', var.get(u'structure').neg().neg())
        PyJsHoisted_ReplaceStep_.func_name = u'ReplaceStep'
        var.put(u'ReplaceStep', PyJsHoisted_ReplaceStep_)
        pass
        if var.get(u'Step$$1'):
            var.get(u'ReplaceStep').put(u'__proto__', var.get(u'Step$$1'))
        var.get(u'ReplaceStep').put(u'prototype', var.get(u'Object').callprop(u'create', (var.get(u'Step$$1') and var.get(u'Step$$1').get(u'prototype'))))
        var.get(u'ReplaceStep').get(u'prototype').put(u'constructor', var.get(u'ReplaceStep'))
        @Js
        def PyJs_apply_403_(doc, this, arguments, var=var):
            var = Scope({u'this':this, u'doc':doc, u'arguments':arguments, u'apply':PyJs_apply_403_}, var)
            var.registers([u'doc'])
            if (var.get(u"this").get(u'structure') and var.get(u'contentBetween')(var.get(u'doc'), var.get(u"this").get(u'from'), var.get(u"this").get(u'to'))):
                return var.get(u'StepResult').callprop(u'fail', Js(u'Structure replace would overwrite content'))
            return var.get(u'StepResult').callprop(u'fromReplace', var.get(u'doc'), var.get(u"this").get(u'from'), var.get(u"this").get(u'to'), var.get(u"this").get(u'slice'))
        PyJs_apply_403_._set_name(u'apply')
        var.get(u'ReplaceStep').get(u'prototype').put(u'apply', PyJs_apply_403_)
        @Js
        def PyJs_getMap_404_(this, arguments, var=var):
            var = Scope({u'this':this, u'getMap':PyJs_getMap_404_, u'arguments':arguments}, var)
            var.registers([])
            return var.get(u'StepMap').create(Js([var.get(u"this").get(u'from'), (var.get(u"this").get(u'to')-var.get(u"this").get(u'from')), var.get(u"this").get(u'slice').get(u'size')]))
        PyJs_getMap_404_._set_name(u'getMap')
        var.get(u'ReplaceStep').get(u'prototype').put(u'getMap', PyJs_getMap_404_)
        @Js
        def PyJs_invert_405_(doc, this, arguments, var=var):
            var = Scope({u'this':this, u'doc':doc, u'invert':PyJs_invert_405_, u'arguments':arguments}, var)
            var.registers([u'doc'])
            return var.get(u'ReplaceStep').create(var.get(u"this").get(u'from'), (var.get(u"this").get(u'from')+var.get(u"this").get(u'slice').get(u'size')), var.get(u'doc').callprop(u'slice', var.get(u"this").get(u'from'), var.get(u"this").get(u'to')))
        PyJs_invert_405_._set_name(u'invert')
        var.get(u'ReplaceStep').get(u'prototype').put(u'invert', PyJs_invert_405_)
        @Js
        def PyJs_map_406_(mapping, this, arguments, var=var):
            var = Scope({u'this':this, u'map':PyJs_map_406_, u'mapping':mapping, u'arguments':arguments}, var)
            var.registers([u'to', u'from', u'mapping'])
            var.put(u'from', var.get(u'mapping').callprop(u'mapResult', var.get(u"this").get(u'from'), Js(1.0)))
            var.put(u'to', var.get(u'mapping').callprop(u'mapResult', var.get(u"this").get(u'to'), (-Js(1.0))))
            if (var.get(u'from').get(u'deleted') and var.get(u'to').get(u'deleted')):
                return var.get(u"null")
            return var.get(u'ReplaceStep').create(var.get(u'from').get(u'pos'), var.get(u'Math').callprop(u'max', var.get(u'from').get(u'pos'), var.get(u'to').get(u'pos')), var.get(u"this").get(u'slice'))
        PyJs_map_406_._set_name(u'map')
        var.get(u'ReplaceStep').get(u'prototype').put(u'map', PyJs_map_406_)
        @Js
        def PyJs_merge_407_(other, this, arguments, var=var):
            var = Scope({u'this':this, u'merge':PyJs_merge_407_, u'other':other, u'arguments':arguments}, var)
            var.registers([u'slice', u'slice$1', u'other'])
            if (var.get(u'other').instanceof(var.get(u'ReplaceStep')).neg() or (var.get(u'other').get(u'structure')!=var.get(u"this").get(u'structure'))):
                return var.get(u"null")
            if ((((var.get(u"this").get(u'from')+var.get(u"this").get(u'slice').get(u'size'))==var.get(u'other').get(u'from')) and var.get(u"this").get(u'slice').get(u'openEnd').neg()) and var.get(u'other').get(u'slice').get(u'openStart').neg()):
                def PyJs_LONG_408_(var=var):
                    return (var.get(u'dist').get(u'Slice').get(u'empty') if ((var.get(u"this").get(u'slice').get(u'size')+var.get(u'other').get(u'slice').get(u'size'))==Js(0.0)) else var.get(u'dist').get(u'Slice').create(var.get(u"this").get(u'slice').get(u'content').callprop(u'append', var.get(u'other').get(u'slice').get(u'content')), var.get(u"this").get(u'slice').get(u'openStart'), var.get(u'other').get(u'slice').get(u'openEnd')))
                var.put(u'slice', PyJs_LONG_408_())
                return var.get(u'ReplaceStep').create(var.get(u"this").get(u'from'), (var.get(u"this").get(u'to')+(var.get(u'other').get(u'to')-var.get(u'other').get(u'from'))), var.get(u'slice'), var.get(u"this").get(u'structure'))
            else:
                if (((var.get(u'other').get(u'to')==var.get(u"this").get(u'from')) and var.get(u"this").get(u'slice').get(u'openStart').neg()) and var.get(u'other').get(u'slice').get(u'openEnd').neg()):
                    def PyJs_LONG_409_(var=var):
                        return (var.get(u'dist').get(u'Slice').get(u'empty') if ((var.get(u"this").get(u'slice').get(u'size')+var.get(u'other').get(u'slice').get(u'size'))==Js(0.0)) else var.get(u'dist').get(u'Slice').create(var.get(u'other').get(u'slice').get(u'content').callprop(u'append', var.get(u"this").get(u'slice').get(u'content')), var.get(u'other').get(u'slice').get(u'openStart'), var.get(u"this").get(u'slice').get(u'openEnd')))
                    var.put(u'slice$1', PyJs_LONG_409_())
                    return var.get(u'ReplaceStep').create(var.get(u'other').get(u'from'), var.get(u"this").get(u'to'), var.get(u'slice$1'), var.get(u"this").get(u'structure'))
                else:
                    return var.get(u"null")
        PyJs_merge_407_._set_name(u'merge')
        var.get(u'ReplaceStep').get(u'prototype').put(u'merge', PyJs_merge_407_)
        @Js
        def PyJs_toJSON_410_(this, arguments, var=var):
            var = Scope({u'this':this, u'toJSON':PyJs_toJSON_410_, u'arguments':arguments}, var)
            var.registers([u'json'])
            PyJs_Object_411_ = Js({u'stepType':Js(u'replace'),u'from':var.get(u"this").get(u'from'),u'to':var.get(u"this").get(u'to')})
            var.put(u'json', PyJs_Object_411_)
            if var.get(u"this").get(u'slice').get(u'size'):
                var.get(u'json').put(u'slice', var.get(u"this").get(u'slice').callprop(u'toJSON'))
            if var.get(u"this").get(u'structure'):
                var.get(u'json').put(u'structure', Js(True))
            return var.get(u'json')
        PyJs_toJSON_410_._set_name(u'toJSON')
        var.get(u'ReplaceStep').get(u'prototype').put(u'toJSON', PyJs_toJSON_410_)
        @Js
        def PyJs_fromJSON_412_(schema, json, this, arguments, var=var):
            var = Scope({u'this':this, u'json':json, u'arguments':arguments, u'fromJSON':PyJs_fromJSON_412_, u'schema':schema}, var)
            var.registers([u'json', u'schema'])
            if ((var.get(u'json').get(u'from').typeof()!=Js(u'number')) or (var.get(u'json').get(u'to').typeof()!=Js(u'number'))):
                PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'Invalid input for ReplaceStep.fromJSON')))
                raise PyJsTempException
            return var.get(u'ReplaceStep').create(var.get(u'json').get(u'from'), var.get(u'json').get(u'to'), var.get(u'dist').get(u'Slice').callprop(u'fromJSON', var.get(u'schema'), var.get(u'json').get(u'slice')), var.get(u'json').get(u'structure').neg().neg())
        PyJs_fromJSON_412_._set_name(u'fromJSON')
        var.get(u'ReplaceStep').put(u'fromJSON', PyJs_fromJSON_412_)
        return var.get(u'ReplaceStep')
    PyJs_anonymous_402_._set_name(u'anonymous')
    var.put(u'ReplaceStep', PyJs_anonymous_402_(var.get(u'Step')))
    var.get(u'Step').callprop(u'jsonID', Js(u'replace'), var.get(u'ReplaceStep'))
    @Js
    def PyJs_anonymous_413_(PyJsArg_53746570242431_, this, arguments, var=var):
        var = Scope({u'this':this, u'Step$$1':PyJsArg_53746570242431_, u'arguments':arguments}, var)
        var.registers([u'ReplaceAroundStep', u'Step$$1'])
        @Js
        def PyJsHoisted_ReplaceAroundStep_(PyJsArg_66726f6d_, to, gapFrom, gapTo, slice, insert, structure, this, arguments, var=var):
            var = Scope({u'insert':insert, u'slice':slice, u'from':PyJsArg_66726f6d_, u'this':this, u'to':to, u'gapFrom':gapFrom, u'arguments':arguments, u'gapTo':gapTo, u'structure':structure}, var)
            var.registers([u'insert', u'slice', u'from', u'to', u'gapFrom', u'gapTo', u'structure'])
            var.get(u'Step$$1').callprop(u'call', var.get(u"this"))
            var.get(u"this").put(u'from', var.get(u'from'))
            var.get(u"this").put(u'to', var.get(u'to'))
            var.get(u"this").put(u'gapFrom', var.get(u'gapFrom'))
            var.get(u"this").put(u'gapTo', var.get(u'gapTo'))
            var.get(u"this").put(u'slice', var.get(u'slice'))
            var.get(u"this").put(u'insert', var.get(u'insert'))
            var.get(u"this").put(u'structure', var.get(u'structure').neg().neg())
        PyJsHoisted_ReplaceAroundStep_.func_name = u'ReplaceAroundStep'
        var.put(u'ReplaceAroundStep', PyJsHoisted_ReplaceAroundStep_)
        pass
        if var.get(u'Step$$1'):
            var.get(u'ReplaceAroundStep').put(u'__proto__', var.get(u'Step$$1'))
        var.get(u'ReplaceAroundStep').put(u'prototype', var.get(u'Object').callprop(u'create', (var.get(u'Step$$1') and var.get(u'Step$$1').get(u'prototype'))))
        var.get(u'ReplaceAroundStep').get(u'prototype').put(u'constructor', var.get(u'ReplaceAroundStep'))
        @Js
        def PyJs_apply_414_(doc, this, arguments, var=var):
            var = Scope({u'this':this, u'doc':doc, u'arguments':arguments, u'apply':PyJs_apply_414_}, var)
            var.registers([u'doc', u'inserted', u'gap'])
            if (var.get(u"this").get(u'structure') and (var.get(u'contentBetween')(var.get(u'doc'), var.get(u"this").get(u'from'), var.get(u"this").get(u'gapFrom')) or var.get(u'contentBetween')(var.get(u'doc'), var.get(u"this").get(u'gapTo'), var.get(u"this").get(u'to')))):
                return var.get(u'StepResult').callprop(u'fail', Js(u'Structure gap-replace would overwrite content'))
            var.put(u'gap', var.get(u'doc').callprop(u'slice', var.get(u"this").get(u'gapFrom'), var.get(u"this").get(u'gapTo')))
            if (var.get(u'gap').get(u'openStart') or var.get(u'gap').get(u'openEnd')):
                return var.get(u'StepResult').callprop(u'fail', Js(u'Gap is not a flat range'))
            var.put(u'inserted', var.get(u"this").get(u'slice').callprop(u'insertAt', var.get(u"this").get(u'insert'), var.get(u'gap').get(u'content')))
            if var.get(u'inserted').neg():
                return var.get(u'StepResult').callprop(u'fail', Js(u'Content does not fit in gap'))
            return var.get(u'StepResult').callprop(u'fromReplace', var.get(u'doc'), var.get(u"this").get(u'from'), var.get(u"this").get(u'to'), var.get(u'inserted'))
        PyJs_apply_414_._set_name(u'apply')
        var.get(u'ReplaceAroundStep').get(u'prototype').put(u'apply', PyJs_apply_414_)
        @Js
        def PyJs_getMap_415_(this, arguments, var=var):
            var = Scope({u'this':this, u'getMap':PyJs_getMap_415_, u'arguments':arguments}, var)
            var.registers([])
            return var.get(u'StepMap').create(Js([var.get(u"this").get(u'from'), (var.get(u"this").get(u'gapFrom')-var.get(u"this").get(u'from')), var.get(u"this").get(u'insert'), var.get(u"this").get(u'gapTo'), (var.get(u"this").get(u'to')-var.get(u"this").get(u'gapTo')), (var.get(u"this").get(u'slice').get(u'size')-var.get(u"this").get(u'insert'))]))
        PyJs_getMap_415_._set_name(u'getMap')
        var.get(u'ReplaceAroundStep').get(u'prototype').put(u'getMap', PyJs_getMap_415_)
        @Js
        def PyJs_invert_416_(doc, this, arguments, var=var):
            var = Scope({u'this':this, u'doc':doc, u'invert':PyJs_invert_416_, u'arguments':arguments}, var)
            var.registers([u'doc', u'gap'])
            var.put(u'gap', (var.get(u"this").get(u'gapTo')-var.get(u"this").get(u'gapFrom')))
            def PyJs_LONG_417_(var=var):
                return var.get(u'ReplaceAroundStep').create(var.get(u"this").get(u'from'), ((var.get(u"this").get(u'from')+var.get(u"this").get(u'slice').get(u'size'))+var.get(u'gap')), (var.get(u"this").get(u'from')+var.get(u"this").get(u'insert')), ((var.get(u"this").get(u'from')+var.get(u"this").get(u'insert'))+var.get(u'gap')), var.get(u'doc').callprop(u'slice', var.get(u"this").get(u'from'), var.get(u"this").get(u'to')).callprop(u'removeBetween', (var.get(u"this").get(u'gapFrom')-var.get(u"this").get(u'from')), (var.get(u"this").get(u'gapTo')-var.get(u"this").get(u'from'))), (var.get(u"this").get(u'gapFrom')-var.get(u"this").get(u'from')), var.get(u"this").get(u'structure'))
            return PyJs_LONG_417_()
        PyJs_invert_416_._set_name(u'invert')
        var.get(u'ReplaceAroundStep').get(u'prototype').put(u'invert', PyJs_invert_416_)
        @Js
        def PyJs_map_418_(mapping, this, arguments, var=var):
            var = Scope({u'this':this, u'map':PyJs_map_418_, u'mapping':mapping, u'arguments':arguments}, var)
            var.registers([u'to', u'gapTo', u'gapFrom', u'from', u'mapping'])
            var.put(u'from', var.get(u'mapping').callprop(u'mapResult', var.get(u"this").get(u'from'), Js(1.0)))
            var.put(u'to', var.get(u'mapping').callprop(u'mapResult', var.get(u"this").get(u'to'), (-Js(1.0))))
            var.put(u'gapFrom', var.get(u'mapping').callprop(u'map', var.get(u"this").get(u'gapFrom'), (-Js(1.0))))
            var.put(u'gapTo', var.get(u'mapping').callprop(u'map', var.get(u"this").get(u'gapTo'), Js(1.0)))
            if (((var.get(u'from').get(u'deleted') and var.get(u'to').get(u'deleted')) or (var.get(u'gapFrom')<var.get(u'from').get(u'pos'))) or (var.get(u'gapTo')>var.get(u'to').get(u'pos'))):
                return var.get(u"null")
            return var.get(u'ReplaceAroundStep').create(var.get(u'from').get(u'pos'), var.get(u'to').get(u'pos'), var.get(u'gapFrom'), var.get(u'gapTo'), var.get(u"this").get(u'slice'), var.get(u"this").get(u'insert'), var.get(u"this").get(u'structure'))
        PyJs_map_418_._set_name(u'map')
        var.get(u'ReplaceAroundStep').get(u'prototype').put(u'map', PyJs_map_418_)
        @Js
        def PyJs_toJSON_419_(this, arguments, var=var):
            var = Scope({u'this':this, u'toJSON':PyJs_toJSON_419_, u'arguments':arguments}, var)
            var.registers([u'json'])
            PyJs_Object_420_ = Js({u'stepType':Js(u'replaceAround'),u'from':var.get(u"this").get(u'from'),u'to':var.get(u"this").get(u'to'),u'gapFrom':var.get(u"this").get(u'gapFrom'),u'gapTo':var.get(u"this").get(u'gapTo'),u'insert':var.get(u"this").get(u'insert')})
            var.put(u'json', PyJs_Object_420_)
            if var.get(u"this").get(u'slice').get(u'size'):
                var.get(u'json').put(u'slice', var.get(u"this").get(u'slice').callprop(u'toJSON'))
            if var.get(u"this").get(u'structure'):
                var.get(u'json').put(u'structure', Js(True))
            return var.get(u'json')
        PyJs_toJSON_419_._set_name(u'toJSON')
        var.get(u'ReplaceAroundStep').get(u'prototype').put(u'toJSON', PyJs_toJSON_419_)
        @Js
        def PyJs_fromJSON_421_(schema, json, this, arguments, var=var):
            var = Scope({u'this':this, u'json':json, u'arguments':arguments, u'fromJSON':PyJs_fromJSON_421_, u'schema':schema}, var)
            var.registers([u'json', u'schema'])
            if (((((var.get(u'json').get(u'from').typeof()!=Js(u'number')) or (var.get(u'json').get(u'to').typeof()!=Js(u'number'))) or (var.get(u'json').get(u'gapFrom').typeof()!=Js(u'number'))) or (var.get(u'json').get(u'gapTo').typeof()!=Js(u'number'))) or (var.get(u'json').get(u'insert').typeof()!=Js(u'number'))):
                PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'Invalid input for ReplaceAroundStep.fromJSON')))
                raise PyJsTempException
            return var.get(u'ReplaceAroundStep').create(var.get(u'json').get(u'from'), var.get(u'json').get(u'to'), var.get(u'json').get(u'gapFrom'), var.get(u'json').get(u'gapTo'), var.get(u'dist').get(u'Slice').callprop(u'fromJSON', var.get(u'schema'), var.get(u'json').get(u'slice')), var.get(u'json').get(u'insert'), var.get(u'json').get(u'structure').neg().neg())
        PyJs_fromJSON_421_._set_name(u'fromJSON')
        var.get(u'ReplaceAroundStep').put(u'fromJSON', PyJs_fromJSON_421_)
        return var.get(u'ReplaceAroundStep')
    PyJs_anonymous_413_._set_name(u'anonymous')
    var.put(u'ReplaceAroundStep', PyJs_anonymous_413_(var.get(u'Step')))
    var.get(u'Step').callprop(u'jsonID', Js(u'replaceAround'), var.get(u'ReplaceAroundStep'))
    pass
    pass
    pass
    @Js
    def PyJs_anonymous_422_(range, target, this, arguments, var=var):
        var = Scope({u'this':this, u'range':range, u'target':target, u'arguments':arguments}, var)
        var.registers([u'splitting$1', u'$to', u'gapEnd', u'$from', u'd$1', u'after', u'splitting', u'd', u'gapStart', u'start', u'depth', u'openStart', u'target', u'openEnd', u'end', u'range', u'before'])
        var.put(u'$from', var.get(u'range').get(u'$from'))
        var.put(u'$to', var.get(u'range').get(u'$to'))
        var.put(u'depth', var.get(u'range').get(u'depth'))
        var.put(u'gapStart', var.get(u'$from').callprop(u'before', (var.get(u'depth')+Js(1.0))))
        var.put(u'gapEnd', var.get(u'$to').callprop(u'after', (var.get(u'depth')+Js(1.0))))
        var.put(u'start', var.get(u'gapStart'))
        var.put(u'end', var.get(u'gapEnd'))
        var.put(u'before', var.get(u'dist').get(u'Fragment').get(u'empty'))
        var.put(u'openStart', Js(0.0))
        #for JS loop
        var.put(u'd', var.get(u'depth'))
        var.put(u'splitting', Js(False))
        while (var.get(u'd')>var.get(u'target')):
            try:
                if (var.get(u'splitting') or (var.get(u'$from').callprop(u'index', var.get(u'd'))>Js(0.0))):
                    var.put(u'splitting', Js(True))
                    var.put(u'before', var.get(u'dist').get(u'Fragment').callprop(u'from', var.get(u'$from').callprop(u'node', var.get(u'd')).callprop(u'copy', var.get(u'before'))))
                    (var.put(u'openStart',Js(var.get(u'openStart').to_number())+Js(1))-Js(1))
                else:
                    (var.put(u'start',Js(var.get(u'start').to_number())-Js(1))+Js(1))
            finally:
                    (var.put(u'd',Js(var.get(u'd').to_number())-Js(1))+Js(1))
        var.put(u'after', var.get(u'dist').get(u'Fragment').get(u'empty'))
        var.put(u'openEnd', Js(0.0))
        #for JS loop
        var.put(u'd$1', var.get(u'depth'))
        var.put(u'splitting$1', Js(False))
        while (var.get(u'd$1')>var.get(u'target')):
            try:
                if (var.get(u'splitting$1') or (var.get(u'$to').callprop(u'after', (var.get(u'd$1')+Js(1.0)))<var.get(u'$to').callprop(u'end', var.get(u'd$1')))):
                    var.put(u'splitting$1', Js(True))
                    var.put(u'after', var.get(u'dist').get(u'Fragment').callprop(u'from', var.get(u'$to').callprop(u'node', var.get(u'd$1')).callprop(u'copy', var.get(u'after'))))
                    (var.put(u'openEnd',Js(var.get(u'openEnd').to_number())+Js(1))-Js(1))
                else:
                    (var.put(u'end',Js(var.get(u'end').to_number())+Js(1))-Js(1))
            finally:
                    (var.put(u'd$1',Js(var.get(u'd$1').to_number())-Js(1))+Js(1))
        return var.get(u"this").callprop(u'step', var.get(u'ReplaceAroundStep').create(var.get(u'start'), var.get(u'end'), var.get(u'gapStart'), var.get(u'gapEnd'), var.get(u'dist').get(u'Slice').create(var.get(u'before').callprop(u'append', var.get(u'after')), var.get(u'openStart'), var.get(u'openEnd')), (var.get(u'before').get(u'size')-var.get(u'openStart')), Js(True)))
    PyJs_anonymous_422_._set_name(u'anonymous')
    var.get(u'Transform').get(u'prototype').put(u'lift', PyJs_anonymous_422_)
    pass
    pass
    pass
    pass
    @Js
    def PyJs_anonymous_425_(range, wrappers, this, arguments, var=var):
        var = Scope({u'wrappers':wrappers, u'this':this, u'range':range, u'arguments':arguments}, var)
        var.registers([u'wrappers', u'end', u'i', u'content', u'start', u'range'])
        var.put(u'content', var.get(u'dist').get(u'Fragment').get(u'empty'))
        #for JS loop
        var.put(u'i', (var.get(u'wrappers').get(u'length')-Js(1.0)))
        while (var.get(u'i')>=Js(0.0)):
            try:
                var.put(u'content', var.get(u'dist').get(u'Fragment').callprop(u'from', var.get(u'wrappers').get(var.get(u'i')).get(u'type').callprop(u'create', var.get(u'wrappers').get(var.get(u'i')).get(u'attrs'), var.get(u'content'))))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())-Js(1))+Js(1))
        var.put(u'start', var.get(u'range').get(u'start'))
        var.put(u'end', var.get(u'range').get(u'end'))
        return var.get(u"this").callprop(u'step', var.get(u'ReplaceAroundStep').create(var.get(u'start'), var.get(u'end'), var.get(u'start'), var.get(u'end'), var.get(u'dist').get(u'Slice').create(var.get(u'content'), Js(0.0), Js(0.0)), var.get(u'wrappers').get(u'length'), Js(True)))
    PyJs_anonymous_425_._set_name(u'anonymous')
    var.get(u'Transform').get(u'prototype').put(u'wrap', PyJs_anonymous_425_)
    @Js
    def PyJs_anonymous_426_(PyJsArg_66726f6d_, to, type, attrs, this, arguments, var=var):
        var = Scope({u'to':to, u'from':PyJsArg_66726f6d_, u'attrs':attrs, u'this':this, u'type':type, u'arguments':arguments}, var)
        var.registers([u'mapFrom', u'from', u'to', u'attrs', u'this$1', u'type'])
        var.put(u'this$1', var.get(u"this"))
        if PyJsStrictEq(var.get(u'to'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'to', var.get(u'from'))
        if var.get(u'type').get(u'isTextblock').neg():
            PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'Type given to setBlockType should be a textblock')))
            raise PyJsTempException
        var.put(u'mapFrom', var.get(u"this").get(u'steps').get(u'length'))
        @Js
        def PyJs_anonymous_427_(node, pos, this, arguments, var=var):
            var = Scope({u'node':node, u'this':this, u'pos':pos, u'arguments':arguments}, var)
            var.registers([u'node', u'pos', u'endM', u'mapping', u'startM'])
            if ((var.get(u'node').get(u'isTextblock') and var.get(u'node').callprop(u'hasMarkup', var.get(u'type'), var.get(u'attrs')).neg()) and var.get(u'canChangeType')(var.get(u'this$1').get(u'doc'), var.get(u'this$1').get(u'mapping').callprop(u'slice', var.get(u'mapFrom')).callprop(u'map', var.get(u'pos')), var.get(u'type'))):
                var.get(u'this$1').callprop(u'clearIncompatible', var.get(u'this$1').get(u'mapping').callprop(u'slice', var.get(u'mapFrom')).callprop(u'map', var.get(u'pos'), Js(1.0)), var.get(u'type'))
                var.put(u'mapping', var.get(u'this$1').get(u'mapping').callprop(u'slice', var.get(u'mapFrom')))
                var.put(u'startM', var.get(u'mapping').callprop(u'map', var.get(u'pos'), Js(1.0)))
                var.put(u'endM', var.get(u'mapping').callprop(u'map', (var.get(u'pos')+var.get(u'node').get(u'nodeSize')), Js(1.0)))
                def PyJs_LONG_428_(var=var):
                    return var.get(u'this$1').callprop(u'step', var.get(u'ReplaceAroundStep').create(var.get(u'startM'), var.get(u'endM'), (var.get(u'startM')+Js(1.0)), (var.get(u'endM')-Js(1.0)), var.get(u'dist').get(u'Slice').create(var.get(u'dist').get(u'Fragment').callprop(u'from', var.get(u'type').callprop(u'create', var.get(u'attrs'), var.get(u"null"), var.get(u'node').get(u'marks'))), Js(0.0), Js(0.0)), Js(1.0), Js(True)))
                PyJs_LONG_428_()
                return Js(False)
        PyJs_anonymous_427_._set_name(u'anonymous')
        var.get(u"this").get(u'doc').callprop(u'nodesBetween', var.get(u'from'), var.get(u'to'), PyJs_anonymous_427_)
        return var.get(u"this")
    PyJs_anonymous_426_._set_name(u'anonymous')
    var.get(u'Transform').get(u'prototype').put(u'setBlockType', PyJs_anonymous_426_)
    pass
    @Js
    def PyJs_anonymous_429_(pos, type, attrs, marks, this, arguments, var=var):
        var = Scope({u'attrs':attrs, u'marks':marks, u'this':this, u'type':type, u'pos':pos, u'arguments':arguments}, var)
        var.registers([u'node', u'pos', u'attrs', u'marks', u'newNode', u'type'])
        var.put(u'node', var.get(u"this").get(u'doc').callprop(u'nodeAt', var.get(u'pos')))
        if var.get(u'node').neg():
            PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'No node at given position')))
            raise PyJsTempException
        if var.get(u'type').neg():
            var.put(u'type', var.get(u'node').get(u'type'))
        var.put(u'newNode', var.get(u'type').callprop(u'create', var.get(u'attrs'), var.get(u"null"), (var.get(u'marks') or var.get(u'node').get(u'marks'))))
        if var.get(u'node').get(u'isLeaf'):
            return var.get(u"this").callprop(u'replaceWith', var.get(u'pos'), (var.get(u'pos')+var.get(u'node').get(u'nodeSize')), var.get(u'newNode'))
        if var.get(u'type').callprop(u'validContent', var.get(u'node').get(u'content')).neg():
            PyJsTempException = JsToPyException(var.get(u'RangeError').create((Js(u'Invalid content for node type ')+var.get(u'type').get(u'name'))))
            raise PyJsTempException
        return var.get(u"this").callprop(u'step', var.get(u'ReplaceAroundStep').create(var.get(u'pos'), (var.get(u'pos')+var.get(u'node').get(u'nodeSize')), (var.get(u'pos')+Js(1.0)), ((var.get(u'pos')+var.get(u'node').get(u'nodeSize'))-Js(1.0)), var.get(u'dist').get(u'Slice').create(var.get(u'dist').get(u'Fragment').callprop(u'from', var.get(u'newNode')), Js(0.0), Js(0.0)), Js(1.0), Js(True)))
    PyJs_anonymous_429_._set_name(u'anonymous')
    var.get(u'Transform').get(u'prototype').put(u'setNodeMarkup', PyJs_anonymous_429_)
    pass
    @Js
    def PyJs_anonymous_431_(pos, depth, typesAfter, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'depth':depth, u'pos':pos, u'typesAfter':typesAfter}, var)
        var.registers([u'e', u'd', u'$pos', u'i', u'after', u'pos', u'typesAfter', u'depth', u'typeAfter', u'before'])
        if PyJsStrictEq(var.get(u'depth'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'depth', Js(1.0))
        var.put(u'$pos', var.get(u"this").get(u'doc').callprop(u'resolve', var.get(u'pos')))
        var.put(u'before', var.get(u'dist').get(u'Fragment').get(u'empty'))
        var.put(u'after', var.get(u'dist').get(u'Fragment').get(u'empty'))
        #for JS loop
        var.put(u'd', var.get(u'$pos').get(u'depth'))
        var.put(u'e', (var.get(u'$pos').get(u'depth')-var.get(u'depth')))
        var.put(u'i', (var.get(u'depth')-Js(1.0)))
        while (var.get(u'd')>var.get(u'e')):
            try:
                var.put(u'before', var.get(u'dist').get(u'Fragment').callprop(u'from', var.get(u'$pos').callprop(u'node', var.get(u'd')).callprop(u'copy', var.get(u'before'))))
                var.put(u'typeAfter', (var.get(u'typesAfter') and var.get(u'typesAfter').get(var.get(u'i'))))
                var.put(u'after', var.get(u'dist').get(u'Fragment').callprop(u'from', (var.get(u'typeAfter').get(u'type').callprop(u'create', var.get(u'typeAfter').get(u'attrs'), var.get(u'after')) if var.get(u'typeAfter') else var.get(u'$pos').callprop(u'node', var.get(u'd')).callprop(u'copy', var.get(u'after')))))
            finally:
                    PyJsComma((var.put(u'd',Js(var.get(u'd').to_number())-Js(1))+Js(1)),(var.put(u'i',Js(var.get(u'i').to_number())-Js(1))+Js(1)))
        return var.get(u"this").callprop(u'step', var.get(u'ReplaceStep').create(var.get(u'pos'), var.get(u'pos'), var.get(u'dist').get(u'Slice').create(var.get(u'before').callprop(u'append', var.get(u'after')), var.get(u'depth'), var.get(u'depth'), Js(True))))
    PyJs_anonymous_431_._set_name(u'anonymous')
    var.get(u'Transform').get(u'prototype').put(u'split', PyJs_anonymous_431_)
    pass
    pass
    pass
    @Js
    def PyJs_anonymous_432_(pos, depth, this, arguments, var=var):
        var = Scope({u'this':this, u'depth':depth, u'pos':pos, u'arguments':arguments}, var)
        var.registers([u'depth', u'step', u'pos'])
        if PyJsStrictEq(var.get(u'depth'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'depth', Js(1.0))
        var.put(u'step', var.get(u'ReplaceStep').create((var.get(u'pos')-var.get(u'depth')), (var.get(u'pos')+var.get(u'depth')), var.get(u'dist').get(u'Slice').get(u'empty'), Js(True)))
        return var.get(u"this").callprop(u'step', var.get(u'step'))
    PyJs_anonymous_432_._set_name(u'anonymous')
    var.get(u'Transform').get(u'prototype').put(u'join', PyJs_anonymous_432_)
    pass
    pass
    pass
    @Js
    def PyJs_anonymous_433_(PyJsArg_53746570242431_, this, arguments, var=var):
        var = Scope({u'this':this, u'Step$$1':PyJsArg_53746570242431_, u'arguments':arguments}, var)
        var.registers([u'Step$$1', u'AddMarkStep'])
        @Js
        def PyJsHoisted_AddMarkStep_(PyJsArg_66726f6d_, to, mark, this, arguments, var=var):
            var = Scope({u'this':this, u'to':to, u'from':PyJsArg_66726f6d_, u'arguments':arguments, u'mark':mark}, var)
            var.registers([u'to', u'from', u'mark'])
            var.get(u'Step$$1').callprop(u'call', var.get(u"this"))
            var.get(u"this").put(u'from', var.get(u'from'))
            var.get(u"this").put(u'to', var.get(u'to'))
            var.get(u"this").put(u'mark', var.get(u'mark'))
        PyJsHoisted_AddMarkStep_.func_name = u'AddMarkStep'
        var.put(u'AddMarkStep', PyJsHoisted_AddMarkStep_)
        pass
        if var.get(u'Step$$1'):
            var.get(u'AddMarkStep').put(u'__proto__', var.get(u'Step$$1'))
        var.get(u'AddMarkStep').put(u'prototype', var.get(u'Object').callprop(u'create', (var.get(u'Step$$1') and var.get(u'Step$$1').get(u'prototype'))))
        var.get(u'AddMarkStep').get(u'prototype').put(u'constructor', var.get(u'AddMarkStep'))
        @Js
        def PyJs_apply_434_(doc, this, arguments, var=var):
            var = Scope({u'this':this, u'doc':doc, u'arguments':arguments, u'apply':PyJs_apply_434_}, var)
            var.registers([u'oldSlice', u'parent', u'doc', u'this$1', u'slice', u'$from'])
            var.put(u'this$1', var.get(u"this"))
            var.put(u'oldSlice', var.get(u'doc').callprop(u'slice', var.get(u"this").get(u'from'), var.get(u"this").get(u'to')))
            var.put(u'$from', var.get(u'doc').callprop(u'resolve', var.get(u"this").get(u'from')))
            var.put(u'parent', var.get(u'$from').callprop(u'node', var.get(u'$from').callprop(u'sharedDepth', var.get(u"this").get(u'to'))))
            @Js
            def PyJs_anonymous_435_(node, parent, this, arguments, var=var):
                var = Scope({u'node':node, u'this':this, u'arguments':arguments, u'parent':parent}, var)
                var.registers([u'node', u'parent'])
                if var.get(u'parent').get(u'type').callprop(u'allowsMarkType', var.get(u'this$1').get(u'mark').get(u'type')).neg():
                    return var.get(u'node')
                return var.get(u'node').callprop(u'mark', var.get(u'this$1').get(u'mark').callprop(u'addToSet', var.get(u'node').get(u'marks')))
            PyJs_anonymous_435_._set_name(u'anonymous')
            var.put(u'slice', var.get(u'dist').get(u'Slice').create(var.get(u'mapFragment')(var.get(u'oldSlice').get(u'content'), PyJs_anonymous_435_, var.get(u'parent')), var.get(u'oldSlice').get(u'openStart'), var.get(u'oldSlice').get(u'openEnd')))
            return var.get(u'StepResult').callprop(u'fromReplace', var.get(u'doc'), var.get(u"this").get(u'from'), var.get(u"this").get(u'to'), var.get(u'slice'))
        PyJs_apply_434_._set_name(u'apply')
        var.get(u'AddMarkStep').get(u'prototype').put(u'apply', PyJs_apply_434_)
        @Js
        def PyJs_invert_436_(this, arguments, var=var):
            var = Scope({u'this':this, u'invert':PyJs_invert_436_, u'arguments':arguments}, var)
            var.registers([])
            return var.get(u'RemoveMarkStep').create(var.get(u"this").get(u'from'), var.get(u"this").get(u'to'), var.get(u"this").get(u'mark'))
        PyJs_invert_436_._set_name(u'invert')
        var.get(u'AddMarkStep').get(u'prototype').put(u'invert', PyJs_invert_436_)
        @Js
        def PyJs_map_437_(mapping, this, arguments, var=var):
            var = Scope({u'this':this, u'map':PyJs_map_437_, u'mapping':mapping, u'arguments':arguments}, var)
            var.registers([u'to', u'from', u'mapping'])
            var.put(u'from', var.get(u'mapping').callprop(u'mapResult', var.get(u"this").get(u'from'), Js(1.0)))
            var.put(u'to', var.get(u'mapping').callprop(u'mapResult', var.get(u"this").get(u'to'), (-Js(1.0))))
            if ((var.get(u'from').get(u'deleted') and var.get(u'to').get(u'deleted')) or (var.get(u'from').get(u'pos')>=var.get(u'to').get(u'pos'))):
                return var.get(u"null")
            return var.get(u'AddMarkStep').create(var.get(u'from').get(u'pos'), var.get(u'to').get(u'pos'), var.get(u"this").get(u'mark'))
        PyJs_map_437_._set_name(u'map')
        var.get(u'AddMarkStep').get(u'prototype').put(u'map', PyJs_map_437_)
        @Js
        def PyJs_merge_438_(other, this, arguments, var=var):
            var = Scope({u'this':this, u'merge':PyJs_merge_438_, u'other':other, u'arguments':arguments}, var)
            var.registers([u'other'])
            if (((var.get(u'other').instanceof(var.get(u'AddMarkStep')) and var.get(u'other').get(u'mark').callprop(u'eq', var.get(u"this").get(u'mark'))) and (var.get(u"this").get(u'from')<=var.get(u'other').get(u'to'))) and (var.get(u"this").get(u'to')>=var.get(u'other').get(u'from'))):
                return var.get(u'AddMarkStep').create(var.get(u'Math').callprop(u'min', var.get(u"this").get(u'from'), var.get(u'other').get(u'from')), var.get(u'Math').callprop(u'max', var.get(u"this").get(u'to'), var.get(u'other').get(u'to')), var.get(u"this").get(u'mark'))
        PyJs_merge_438_._set_name(u'merge')
        var.get(u'AddMarkStep').get(u'prototype').put(u'merge', PyJs_merge_438_)
        @Js
        def PyJs_toJSON_439_(this, arguments, var=var):
            var = Scope({u'this':this, u'toJSON':PyJs_toJSON_439_, u'arguments':arguments}, var)
            var.registers([])
            PyJs_Object_440_ = Js({u'stepType':Js(u'addMark'),u'mark':var.get(u"this").get(u'mark').callprop(u'toJSON'),u'from':var.get(u"this").get(u'from'),u'to':var.get(u"this").get(u'to')})
            return PyJs_Object_440_
        PyJs_toJSON_439_._set_name(u'toJSON')
        var.get(u'AddMarkStep').get(u'prototype').put(u'toJSON', PyJs_toJSON_439_)
        @Js
        def PyJs_fromJSON_441_(schema, json, this, arguments, var=var):
            var = Scope({u'this':this, u'json':json, u'arguments':arguments, u'fromJSON':PyJs_fromJSON_441_, u'schema':schema}, var)
            var.registers([u'json', u'schema'])
            if ((var.get(u'json').get(u'from').typeof()!=Js(u'number')) or (var.get(u'json').get(u'to').typeof()!=Js(u'number'))):
                PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'Invalid input for AddMarkStep.fromJSON')))
                raise PyJsTempException
            return var.get(u'AddMarkStep').create(var.get(u'json').get(u'from'), var.get(u'json').get(u'to'), var.get(u'schema').callprop(u'markFromJSON', var.get(u'json').get(u'mark')))
        PyJs_fromJSON_441_._set_name(u'fromJSON')
        var.get(u'AddMarkStep').put(u'fromJSON', PyJs_fromJSON_441_)
        return var.get(u'AddMarkStep')
    PyJs_anonymous_433_._set_name(u'anonymous')
    var.put(u'AddMarkStep', PyJs_anonymous_433_(var.get(u'Step')))
    var.get(u'Step').callprop(u'jsonID', Js(u'addMark'), var.get(u'AddMarkStep'))
    @Js
    def PyJs_anonymous_442_(PyJsArg_53746570242431_, this, arguments, var=var):
        var = Scope({u'this':this, u'Step$$1':PyJsArg_53746570242431_, u'arguments':arguments}, var)
        var.registers([u'Step$$1', u'RemoveMarkStep'])
        @Js
        def PyJsHoisted_RemoveMarkStep_(PyJsArg_66726f6d_, to, mark, this, arguments, var=var):
            var = Scope({u'this':this, u'to':to, u'from':PyJsArg_66726f6d_, u'arguments':arguments, u'mark':mark}, var)
            var.registers([u'to', u'from', u'mark'])
            var.get(u'Step$$1').callprop(u'call', var.get(u"this"))
            var.get(u"this").put(u'from', var.get(u'from'))
            var.get(u"this").put(u'to', var.get(u'to'))
            var.get(u"this").put(u'mark', var.get(u'mark'))
        PyJsHoisted_RemoveMarkStep_.func_name = u'RemoveMarkStep'
        var.put(u'RemoveMarkStep', PyJsHoisted_RemoveMarkStep_)
        pass
        if var.get(u'Step$$1'):
            var.get(u'RemoveMarkStep').put(u'__proto__', var.get(u'Step$$1'))
        var.get(u'RemoveMarkStep').put(u'prototype', var.get(u'Object').callprop(u'create', (var.get(u'Step$$1') and var.get(u'Step$$1').get(u'prototype'))))
        var.get(u'RemoveMarkStep').get(u'prototype').put(u'constructor', var.get(u'RemoveMarkStep'))
        @Js
        def PyJs_apply_443_(doc, this, arguments, var=var):
            var = Scope({u'this':this, u'doc':doc, u'arguments':arguments, u'apply':PyJs_apply_443_}, var)
            var.registers([u'doc', u'oldSlice', u'slice', u'this$1'])
            var.put(u'this$1', var.get(u"this"))
            var.put(u'oldSlice', var.get(u'doc').callprop(u'slice', var.get(u"this").get(u'from'), var.get(u"this").get(u'to')))
            @Js
            def PyJs_anonymous_444_(node, this, arguments, var=var):
                var = Scope({u'node':node, u'this':this, u'arguments':arguments}, var)
                var.registers([u'node'])
                return var.get(u'node').callprop(u'mark', var.get(u'this$1').get(u'mark').callprop(u'removeFromSet', var.get(u'node').get(u'marks')))
            PyJs_anonymous_444_._set_name(u'anonymous')
            var.put(u'slice', var.get(u'dist').get(u'Slice').create(var.get(u'mapFragment')(var.get(u'oldSlice').get(u'content'), PyJs_anonymous_444_), var.get(u'oldSlice').get(u'openStart'), var.get(u'oldSlice').get(u'openEnd')))
            return var.get(u'StepResult').callprop(u'fromReplace', var.get(u'doc'), var.get(u"this").get(u'from'), var.get(u"this").get(u'to'), var.get(u'slice'))
        PyJs_apply_443_._set_name(u'apply')
        var.get(u'RemoveMarkStep').get(u'prototype').put(u'apply', PyJs_apply_443_)
        @Js
        def PyJs_invert_445_(this, arguments, var=var):
            var = Scope({u'this':this, u'invert':PyJs_invert_445_, u'arguments':arguments}, var)
            var.registers([])
            return var.get(u'AddMarkStep').create(var.get(u"this").get(u'from'), var.get(u"this").get(u'to'), var.get(u"this").get(u'mark'))
        PyJs_invert_445_._set_name(u'invert')
        var.get(u'RemoveMarkStep').get(u'prototype').put(u'invert', PyJs_invert_445_)
        @Js
        def PyJs_map_446_(mapping, this, arguments, var=var):
            var = Scope({u'this':this, u'map':PyJs_map_446_, u'mapping':mapping, u'arguments':arguments}, var)
            var.registers([u'to', u'from', u'mapping'])
            var.put(u'from', var.get(u'mapping').callprop(u'mapResult', var.get(u"this").get(u'from'), Js(1.0)))
            var.put(u'to', var.get(u'mapping').callprop(u'mapResult', var.get(u"this").get(u'to'), (-Js(1.0))))
            if ((var.get(u'from').get(u'deleted') and var.get(u'to').get(u'deleted')) or (var.get(u'from').get(u'pos')>=var.get(u'to').get(u'pos'))):
                return var.get(u"null")
            return var.get(u'RemoveMarkStep').create(var.get(u'from').get(u'pos'), var.get(u'to').get(u'pos'), var.get(u"this").get(u'mark'))
        PyJs_map_446_._set_name(u'map')
        var.get(u'RemoveMarkStep').get(u'prototype').put(u'map', PyJs_map_446_)
        @Js
        def PyJs_merge_447_(other, this, arguments, var=var):
            var = Scope({u'this':this, u'merge':PyJs_merge_447_, u'other':other, u'arguments':arguments}, var)
            var.registers([u'other'])
            if (((var.get(u'other').instanceof(var.get(u'RemoveMarkStep')) and var.get(u'other').get(u'mark').callprop(u'eq', var.get(u"this").get(u'mark'))) and (var.get(u"this").get(u'from')<=var.get(u'other').get(u'to'))) and (var.get(u"this").get(u'to')>=var.get(u'other').get(u'from'))):
                return var.get(u'RemoveMarkStep').create(var.get(u'Math').callprop(u'min', var.get(u"this").get(u'from'), var.get(u'other').get(u'from')), var.get(u'Math').callprop(u'max', var.get(u"this").get(u'to'), var.get(u'other').get(u'to')), var.get(u"this").get(u'mark'))
        PyJs_merge_447_._set_name(u'merge')
        var.get(u'RemoveMarkStep').get(u'prototype').put(u'merge', PyJs_merge_447_)
        @Js
        def PyJs_toJSON_448_(this, arguments, var=var):
            var = Scope({u'this':this, u'toJSON':PyJs_toJSON_448_, u'arguments':arguments}, var)
            var.registers([])
            PyJs_Object_449_ = Js({u'stepType':Js(u'removeMark'),u'mark':var.get(u"this").get(u'mark').callprop(u'toJSON'),u'from':var.get(u"this").get(u'from'),u'to':var.get(u"this").get(u'to')})
            return PyJs_Object_449_
        PyJs_toJSON_448_._set_name(u'toJSON')
        var.get(u'RemoveMarkStep').get(u'prototype').put(u'toJSON', PyJs_toJSON_448_)
        @Js
        def PyJs_fromJSON_450_(schema, json, this, arguments, var=var):
            var = Scope({u'this':this, u'json':json, u'arguments':arguments, u'fromJSON':PyJs_fromJSON_450_, u'schema':schema}, var)
            var.registers([u'json', u'schema'])
            if ((var.get(u'json').get(u'from').typeof()!=Js(u'number')) or (var.get(u'json').get(u'to').typeof()!=Js(u'number'))):
                PyJsTempException = JsToPyException(var.get(u'RangeError').create(Js(u'Invalid input for RemoveMarkStep.fromJSON')))
                raise PyJsTempException
            return var.get(u'RemoveMarkStep').create(var.get(u'json').get(u'from'), var.get(u'json').get(u'to'), var.get(u'schema').callprop(u'markFromJSON', var.get(u'json').get(u'mark')))
        PyJs_fromJSON_450_._set_name(u'fromJSON')
        var.get(u'RemoveMarkStep').put(u'fromJSON', PyJs_fromJSON_450_)
        return var.get(u'RemoveMarkStep')
    PyJs_anonymous_442_._set_name(u'anonymous')
    var.put(u'RemoveMarkStep', PyJs_anonymous_442_(var.get(u'Step')))
    var.get(u'Step').callprop(u'jsonID', Js(u'removeMark'), var.get(u'RemoveMarkStep'))
    @Js
    def PyJs_anonymous_451_(PyJsArg_66726f6d_, to, mark, this, arguments, var=var):
        var = Scope({u'this':this, u'to':to, u'from':PyJsArg_66726f6d_, u'arguments':arguments, u'mark':mark}, var)
        var.registers([u'adding', u'added', u'from', u'removing', u'mark', u'to', u'this$1', u'removed'])
        var.put(u'this$1', var.get(u"this"))
        var.put(u'removed', Js([]))
        var.put(u'added', Js([]))
        var.put(u'removing', var.get(u"null"))
        var.put(u'adding', var.get(u"null"))
        @Js
        def PyJs_anonymous_452_(node, pos, parent, this, arguments, var=var):
            var = Scope({u'node':node, u'this':this, u'pos':pos, u'parent':parent, u'arguments':arguments}, var)
            var.registers([u'node', u'end', u'parent', u'i', u'pos', u'start', u'marks', u'newSet'])
            if var.get(u'node').get(u'isInline').neg():
                return var.get('undefined')
            var.put(u'marks', var.get(u'node').get(u'marks'))
            if (var.get(u'mark').callprop(u'isInSet', var.get(u'marks')).neg() and var.get(u'parent').get(u'type').callprop(u'allowsMarkType', var.get(u'mark').get(u'type'))):
                var.put(u'start', var.get(u'Math').callprop(u'max', var.get(u'pos'), var.get(u'from')))
                var.put(u'end', var.get(u'Math').callprop(u'min', (var.get(u'pos')+var.get(u'node').get(u'nodeSize')), var.get(u'to')))
                var.put(u'newSet', var.get(u'mark').callprop(u'addToSet', var.get(u'marks')))
                #for JS loop
                var.put(u'i', Js(0.0))
                while (var.get(u'i')<var.get(u'marks').get(u'length')):
                    try:
                        if var.get(u'marks').get(var.get(u'i')).callprop(u'isInSet', var.get(u'newSet')).neg():
                            if ((var.get(u'removing') and (var.get(u'removing').get(u'to')==var.get(u'start'))) and var.get(u'removing').get(u'mark').callprop(u'eq', var.get(u'marks').get(var.get(u'i')))):
                                var.get(u'removing').put(u'to', var.get(u'end'))
                            else:
                                var.get(u'removed').callprop(u'push', var.put(u'removing', var.get(u'RemoveMarkStep').create(var.get(u'start'), var.get(u'end'), var.get(u'marks').get(var.get(u'i')))))
                    finally:
                            (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
                if (var.get(u'adding') and (var.get(u'adding').get(u'to')==var.get(u'start'))):
                    var.get(u'adding').put(u'to', var.get(u'end'))
                else:
                    var.get(u'added').callprop(u'push', var.put(u'adding', var.get(u'AddMarkStep').create(var.get(u'start'), var.get(u'end'), var.get(u'mark'))))
        PyJs_anonymous_452_._set_name(u'anonymous')
        var.get(u"this").get(u'doc').callprop(u'nodesBetween', var.get(u'from'), var.get(u'to'), PyJs_anonymous_452_)
        @Js
        def PyJs_anonymous_453_(s, this, arguments, var=var):
            var = Scope({u'this':this, u's':s, u'arguments':arguments}, var)
            var.registers([u's'])
            return var.get(u'this$1').callprop(u'step', var.get(u's'))
        PyJs_anonymous_453_._set_name(u'anonymous')
        var.get(u'removed').callprop(u'forEach', PyJs_anonymous_453_)
        @Js
        def PyJs_anonymous_454_(s, this, arguments, var=var):
            var = Scope({u'this':this, u's':s, u'arguments':arguments}, var)
            var.registers([u's'])
            return var.get(u'this$1').callprop(u'step', var.get(u's'))
        PyJs_anonymous_454_._set_name(u'anonymous')
        var.get(u'added').callprop(u'forEach', PyJs_anonymous_454_)
        return var.get(u"this")
    PyJs_anonymous_451_._set_name(u'anonymous')
    var.get(u'Transform').get(u'prototype').put(u'addMark', PyJs_anonymous_451_)
    @Js
    def PyJs_anonymous_455_(PyJsArg_66726f6d_, to, mark, this, arguments, var=var):
        var = Scope({u'this':this, u'to':to, u'from':PyJsArg_66726f6d_, u'arguments':arguments, u'mark':mark}, var)
        var.registers([u'from', u'mark', u'to', u'step', u'this$1', u'matched'])
        var.put(u'this$1', var.get(u"this"))
        if PyJsStrictEq(var.get(u'mark'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'mark', var.get(u"null"))
        var.put(u'matched', Js([]))
        var.put(u'step', Js(0.0))
        @Js
        def PyJs_anonymous_456_(node, pos, this, arguments, var=var):
            var = Scope({u'node':node, u'this':this, u'pos':pos, u'arguments':arguments}, var)
            var.registers([u'node', u'style', u'end', u'found$1', u'i', u'j', u'm', u'pos', u'found', u'toRemove'])
            if var.get(u'node').get(u'isInline').neg():
                return var.get('undefined')
            (var.put(u'step',Js(var.get(u'step').to_number())+Js(1))-Js(1))
            var.put(u'toRemove', var.get(u"null"))
            if var.get(u'mark').instanceof(var.get(u'dist').get(u'MarkType')):
                var.put(u'found', var.get(u'mark').callprop(u'isInSet', var.get(u'node').get(u'marks')))
                if var.get(u'found'):
                    var.put(u'toRemove', Js([var.get(u'found')]))
            else:
                if var.get(u'mark'):
                    if var.get(u'mark').callprop(u'isInSet', var.get(u'node').get(u'marks')):
                        var.put(u'toRemove', Js([var.get(u'mark')]))
                else:
                    var.put(u'toRemove', var.get(u'node').get(u'marks'))
            if (var.get(u'toRemove') and var.get(u'toRemove').get(u'length')):
                var.put(u'end', var.get(u'Math').callprop(u'min', (var.get(u'pos')+var.get(u'node').get(u'nodeSize')), var.get(u'to')))
                #for JS loop
                var.put(u'i', Js(0.0))
                while (var.get(u'i')<var.get(u'toRemove').get(u'length')):
                    try:
                        var.put(u'style', var.get(u'toRemove').get(var.get(u'i')))
                        var.put(u'found$1', PyJsComma(Js(0.0), Js(None)))
                        #for JS loop
                        var.put(u'j', Js(0.0))
                        while (var.get(u'j')<var.get(u'matched').get(u'length')):
                            try:
                                var.put(u'm', var.get(u'matched').get(var.get(u'j')))
                                if ((var.get(u'm').get(u'step')==(var.get(u'step')-Js(1.0))) and var.get(u'style').callprop(u'eq', var.get(u'matched').get(var.get(u'j')).get(u'style'))):
                                    var.put(u'found$1', var.get(u'm'))
                            finally:
                                    (var.put(u'j',Js(var.get(u'j').to_number())+Js(1))-Js(1))
                        if var.get(u'found$1'):
                            var.get(u'found$1').put(u'to', var.get(u'end'))
                            var.get(u'found$1').put(u'step', var.get(u'step'))
                        else:
                            PyJs_Object_457_ = Js({u'style':var.get(u'style'),u'from':var.get(u'Math').callprop(u'max', var.get(u'pos'), var.get(u'from')),u'to':var.get(u'end'),u'step':var.get(u'step')})
                            var.get(u'matched').callprop(u'push', PyJs_Object_457_)
                    finally:
                            (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        PyJs_anonymous_456_._set_name(u'anonymous')
        var.get(u"this").get(u'doc').callprop(u'nodesBetween', var.get(u'from'), var.get(u'to'), PyJs_anonymous_456_)
        @Js
        def PyJs_anonymous_458_(m, this, arguments, var=var):
            var = Scope({u'this':this, u'm':m, u'arguments':arguments}, var)
            var.registers([u'm'])
            return var.get(u'this$1').callprop(u'step', var.get(u'RemoveMarkStep').create(var.get(u'm').get(u'from'), var.get(u'm').get(u'to'), var.get(u'm').get(u'style')))
        PyJs_anonymous_458_._set_name(u'anonymous')
        var.get(u'matched').callprop(u'forEach', PyJs_anonymous_458_)
        return var.get(u"this")
    PyJs_anonymous_455_._set_name(u'anonymous')
    var.get(u'Transform').get(u'prototype').put(u'removeMark', PyJs_anonymous_455_)
    @Js
    def PyJs_anonymous_459_(pos, parentType, match, this, arguments, var=var):
        var = Scope({u'this':this, u'parentType':parentType, u'pos':pos, u'match':match, u'arguments':arguments}, var)
        var.registers([u'node', u'j', u'end', u'cur', u'i', u'this$1', u'pos', u'i$1', u'parentType', u'delSteps', u'allowed', u'child', u'match', u'fill'])
        var.put(u'this$1', var.get(u"this"))
        if PyJsStrictEq(var.get(u'match'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'match', var.get(u'parentType').get(u'contentMatch'))
        var.put(u'node', var.get(u"this").get(u'doc').callprop(u'nodeAt', var.get(u'pos')))
        var.put(u'delSteps', Js([]))
        var.put(u'cur', (var.get(u'pos')+Js(1.0)))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u'node').get(u'childCount')):
            try:
                var.put(u'child', var.get(u'node').callprop(u'child', var.get(u'i')))
                var.put(u'end', (var.get(u'cur')+var.get(u'child').get(u'nodeSize')))
                var.put(u'allowed', var.get(u'match').callprop(u'matchType', var.get(u'child').get(u'type'), var.get(u'child').get(u'attrs')))
                if var.get(u'allowed').neg():
                    var.get(u'delSteps').callprop(u'push', var.get(u'ReplaceStep').create(var.get(u'cur'), var.get(u'end'), var.get(u'dist').get(u'Slice').get(u'empty')))
                else:
                    var.put(u'match', var.get(u'allowed'))
                    #for JS loop
                    var.put(u'j', Js(0.0))
                    while (var.get(u'j')<var.get(u'child').get(u'marks').get(u'length')):
                        try:
                            if var.get(u'parentType').callprop(u'allowsMarkType', var.get(u'child').get(u'marks').get(var.get(u'j')).get(u'type')).neg():
                                var.get(u'this$1').callprop(u'step', var.get(u'RemoveMarkStep').create(var.get(u'cur'), var.get(u'end'), var.get(u'child').get(u'marks').get(var.get(u'j'))))
                        finally:
                                (var.put(u'j',Js(var.get(u'j').to_number())+Js(1))-Js(1))
                var.put(u'cur', var.get(u'end'))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        if var.get(u'match').get(u'validEnd').neg():
            var.put(u'fill', var.get(u'match').callprop(u'fillBefore', var.get(u'dist').get(u'Fragment').get(u'empty'), Js(True)))
            var.get(u"this").callprop(u'replace', var.get(u'cur'), var.get(u'cur'), var.get(u'dist').get(u'Slice').create(var.get(u'fill'), Js(0.0), Js(0.0)))
        #for JS loop
        var.put(u'i$1', (var.get(u'delSteps').get(u'length')-Js(1.0)))
        while (var.get(u'i$1')>=Js(0.0)):
            try:
                var.get(u'this$1').callprop(u'step', var.get(u'delSteps').get(var.get(u'i$1')))
            finally:
                    (var.put(u'i$1',Js(var.get(u'i$1').to_number())-Js(1))+Js(1))
        return var.get(u"this")
    PyJs_anonymous_459_._set_name(u'anonymous')
    var.get(u'Transform').get(u'prototype').put(u'clearIncompatible', PyJs_anonymous_459_)
    pass
    @Js
    def PyJs_anonymous_460_(PyJsArg_66726f6d_, to, slice, this, arguments, var=var):
        var = Scope({u'this':this, u'to':to, u'slice':slice, u'from':PyJsArg_66726f6d_, u'arguments':arguments}, var)
        var.registers([u'to', u'step', u'slice', u'from'])
        if PyJsStrictEq(var.get(u'to'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'to', var.get(u'from'))
        if PyJsStrictEq(var.get(u'slice'),PyJsComma(Js(0.0), Js(None))):
            var.put(u'slice', var.get(u'dist').get(u'Slice').get(u'empty'))
        var.put(u'step', var.get(u'replaceStep')(var.get(u"this").get(u'doc'), var.get(u'from'), var.get(u'to'), var.get(u'slice')))
        if var.get(u'step'):
            var.get(u"this").callprop(u'step', var.get(u'step'))
        return var.get(u"this")
    PyJs_anonymous_460_._set_name(u'anonymous')
    var.get(u'Transform').get(u'prototype').put(u'replace', PyJs_anonymous_460_)
    @Js
    def PyJs_anonymous_461_(PyJsArg_66726f6d_, to, content, this, arguments, var=var):
        var = Scope({u'content':content, u'to':to, u'this':this, u'from':PyJsArg_66726f6d_, u'arguments':arguments}, var)
        var.registers([u'content', u'to', u'from'])
        return var.get(u"this").callprop(u'replace', var.get(u'from'), var.get(u'to'), var.get(u'dist').get(u'Slice').create(var.get(u'dist').get(u'Fragment').callprop(u'from', var.get(u'content')), Js(0.0), Js(0.0)))
    PyJs_anonymous_461_._set_name(u'anonymous')
    var.get(u'Transform').get(u'prototype').put(u'replaceWith', PyJs_anonymous_461_)
    @Js
    def PyJs_anonymous_462_(PyJsArg_66726f6d_, to, this, arguments, var=var):
        var = Scope({u'this':this, u'to':to, u'from':PyJsArg_66726f6d_, u'arguments':arguments}, var)
        var.registers([u'to', u'from'])
        return var.get(u"this").callprop(u'replace', var.get(u'from'), var.get(u'to'), var.get(u'dist').get(u'Slice').get(u'empty'))
    PyJs_anonymous_462_._set_name(u'anonymous')
    var.get(u'Transform').get(u'prototype').put(u'delete', PyJs_anonymous_462_)
    @Js
    def PyJs_anonymous_463_(pos, content, this, arguments, var=var):
        var = Scope({u'content':content, u'this':this, u'pos':pos, u'arguments':arguments}, var)
        var.registers([u'content', u'pos'])
        return var.get(u"this").callprop(u'replaceWith', var.get(u'pos'), var.get(u'pos'), var.get(u'content'))
    PyJs_anonymous_463_._set_name(u'anonymous')
    var.get(u'Transform').get(u'prototype').put(u'insert', PyJs_anonymous_463_)
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    @Js
    def PyJs_Frontier_465_(PyJsArg_24706f73_, this, arguments, var=var):
        var = Scope({u'this':this, u'arguments':arguments, u'$pos':PyJsArg_24706f73_, u'Frontier':PyJs_Frontier_465_}, var)
        var.registers([u'$pos', u'match', u'd', u'parent', u'this$1'])
        var.put(u'this$1', var.get(u"this"))
        var.get(u"this").put(u'open', Js([]))
        #for JS loop
        var.put(u'd', Js(0.0))
        while (var.get(u'd')<=var.get(u'$pos').get(u'depth')):
            try:
                var.put(u'parent', var.get(u'$pos').callprop(u'node', var.get(u'd')))
                var.put(u'match', var.get(u'parent').callprop(u'contentMatchAt', var.get(u'$pos').callprop(u'indexAfter', var.get(u'd'))))
                PyJs_Object_466_ = Js({u'parent':var.get(u'parent'),u'match':var.get(u'match'),u'content':var.get(u'dist').get(u'Fragment').get(u'empty'),u'wrapper':Js(False),u'openEnd':Js(0.0),u'depth':var.get(u'd')})
                var.get(u'this$1').get(u'open').callprop(u'push', PyJs_Object_466_)
            finally:
                    (var.put(u'd',Js(var.get(u'd').to_number())+Js(1))-Js(1))
        var.get(u"this").put(u'placed', Js([]))
    PyJs_Frontier_465_._set_name(u'Frontier')
    var.put(u'Frontier', PyJs_Frontier_465_)
    @Js
    def PyJs_placeSlice_467_(fragment, openStart, openEnd, PyJsArg_70617373_, parent, this, arguments, var=var):
        var = Scope({u'openEnd':openEnd, u'placeSlice':PyJs_placeSlice_467_, u'openStart':openStart, u'parent':parent, u'pass':PyJsArg_70617373_, u'fragment':fragment, u'this':this, u'arguments':arguments}, var)
        var.registers([u'parent', u'i', u'this$1', u'fragment', u'result', u'child', u'openEnd', u'inner', u'openStart', u'pass', u'first'])
        var.put(u'this$1', var.get(u"this"))
        if (var.get(u'openStart')>Js(0.0)):
            var.put(u'first', var.get(u'fragment').get(u'firstChild'))
            var.put(u'inner', var.get(u"this").callprop(u'placeSlice', var.get(u'first').get(u'content'), var.get(u'Math').callprop(u'max', Js(0.0), (var.get(u'openStart')-Js(1.0))), ((var.get(u'openEnd')-Js(1.0)) if (var.get(u'openEnd') and (var.get(u'fragment').get(u'childCount')==Js(1.0))) else Js(0.0)), var.get(u'pass'), var.get(u'first')))
            if (var.get(u'inner').get(u'content')!=var.get(u'first').get(u'content')):
                if var.get(u'inner').get(u'content').get(u'size'):
                    var.put(u'fragment', var.get(u'fragment').callprop(u'replaceChild', Js(0.0), var.get(u'first').callprop(u'copy', var.get(u'inner').get(u'content'))))
                    var.put(u'openStart', (var.get(u'inner').get(u'openStart')+Js(1.0)))
                else:
                    if (var.get(u'fragment').get(u'childCount')==Js(1.0)):
                        var.put(u'openEnd', Js(0.0))
                    var.put(u'fragment', var.get(u'fragment').callprop(u'cutByIndex', Js(1.0)))
                    var.put(u'openStart', Js(0.0))
        var.put(u'result', var.get(u"this").callprop(u'placeContent', var.get(u'fragment'), var.get(u'openStart'), var.get(u'openEnd'), var.get(u'pass'), var.get(u'parent')))
        if (((var.get(u'pass')>Js(2.0)) and var.get(u'result').get(u'size')) and (var.get(u'openStart')==Js(0.0))):
            #for JS loop
            var.put(u'i', Js(0.0))
            while (var.get(u'i')<var.get(u'result').get(u'content').get(u'childCount')):
                try:
                    var.put(u'child', var.get(u'result').get(u'content').callprop(u'child', var.get(u'i')))
                    var.get(u'this$1').callprop(u'placeContent', var.get(u'child').get(u'content'), Js(0.0), ((var.get(u'openEnd')-Js(1.0)) if (var.get(u'openEnd') and (var.get(u'i')==(var.get(u'result').get(u'content').get(u'childCount').get(u'length')-Js(1.0)))) else Js(0.0)), var.get(u'pass'), var.get(u'child'))
                finally:
                        (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
            var.put(u'result', var.get(u'dist').get(u'Fragment').get(u'empty'))
        return var.get(u'result')
    PyJs_placeSlice_467_._set_name(u'placeSlice')
    var.get(u'Frontier').get(u'prototype').put(u'placeSlice', PyJs_placeSlice_467_)
    @Js
    def PyJs_placeContent_468_(fragment, openStart, openEnd, PyJsArg_70617373_, parent, this, arguments, var=var):
        var = Scope({u'placeContent':PyJs_placeContent_468_, u'openEnd':openEnd, u'openStart':openStart, u'parent':parent, u'pass':PyJsArg_70617373_, u'fragment':fragment, u'this':this, u'arguments':arguments}, var)
        var.registers([u'j', u'last', u'd', u'parent', u'openEnd', u'i', u'pass', u'this$1', u'fragment', u'placed', u'ch', u'openStart', u'w', u'child', u'wrap', u'open', u'match', u'fill'])
        var.put(u'this$1', var.get(u"this"))
        var.put(u'i', Js(0.0))
        #for JS loop
        
        while (var.get(u'i')<var.get(u'fragment').get(u'childCount')):
            try:
                var.put(u'child', var.get(u'fragment').callprop(u'child', var.get(u'i')))
                var.put(u'placed', Js(False))
                var.put(u'last', (var.get(u'i')==(var.get(u'fragment').get(u'childCount')-Js(1.0))))
                #for JS loop
                var.put(u'd', (var.get(u"this").get(u'open').get(u'length')-Js(1.0)))
                while (var.get(u'd')>=Js(0.0)):
                    try:
                        var.put(u'open', var.get(u'this$1').get(u'open').get(var.get(u'd')))
                        var.put(u'wrap', PyJsComma(Js(0.0), Js(None)))
                        if (((var.get(u'pass')>Js(1.0)) and var.put(u'wrap', var.get(u'open').get(u'match').callprop(u'findWrapping', var.get(u'child').get(u'type')))) and ((var.get(u'parent') and var.get(u'wrap').get(u'length')) and (var.get(u'wrap').get((var.get(u'wrap').get(u'length')-Js(1.0)))==var.get(u'parent').get(u'type'))).neg()):
                            while ((var.get(u"this").get(u'open').get(u'length')-Js(1.0))>var.get(u'd')):
                                var.get(u'this$1').callprop(u'closeNode')
                            #for JS loop
                            var.put(u'w', Js(0.0))
                            while (var.get(u'w')<var.get(u'wrap').get(u'length')):
                                try:
                                    var.get(u'open').put(u'match', var.get(u'open').get(u'match').callprop(u'matchType', var.get(u'wrap').get(var.get(u'w'))))
                                    (var.put(u'd',Js(var.get(u'd').to_number())+Js(1))-Js(1))
                                    PyJs_Object_469_ = Js({u'parent':var.get(u'wrap').get(var.get(u'w')).callprop(u'create'),u'match':var.get(u'wrap').get(var.get(u'w')).get(u'contentMatch'),u'content':var.get(u'dist').get(u'Fragment').get(u'empty'),u'wrapper':Js(True),u'openEnd':Js(0.0),u'depth':(var.get(u'd')+var.get(u'w'))})
                                    var.put(u'open', PyJs_Object_469_)
                                    var.get(u'this$1').get(u'open').callprop(u'push', var.get(u'open'))
                                finally:
                                        (var.put(u'w',Js(var.get(u'w').to_number())+Js(1))-Js(1))
                        var.put(u'match', var.get(u'open').get(u'match').callprop(u'matchType', var.get(u'child').get(u'type')))
                        if var.get(u'match').neg():
                            var.put(u'fill', var.get(u'open').get(u'match').callprop(u'fillBefore', var.get(u'dist').get(u'Fragment').callprop(u'from', var.get(u'child'))))
                            if var.get(u'fill'):
                                #for JS loop
                                var.put(u'j', Js(0.0))
                                while (var.get(u'j')<var.get(u'fill').get(u'childCount')):
                                    try:
                                        var.put(u'ch', var.get(u'fill').callprop(u'child', var.get(u'j')))
                                        var.get(u'this$1').callprop(u'addNode', var.get(u'open'), var.get(u'ch'), Js(0.0))
                                        var.put(u'match', var.get(u'open').get(u'match').callprop(u'matchFragment', var.get(u'ch')))
                                    finally:
                                            (var.put(u'j',Js(var.get(u'j').to_number())+Js(1))-Js(1))
                            else:
                                if (var.get(u'parent') and var.get(u'open').get(u'match').callprop(u'matchType', var.get(u'parent').get(u'type'))):
                                    break
                                else:
                                    continue
                        while ((var.get(u"this").get(u'open').get(u'length')-Js(1.0))>var.get(u'd')):
                            var.get(u'this$1').callprop(u'closeNode')
                        var.put(u'child', var.get(u'child').callprop(u'mark', var.get(u'open').get(u'parent').get(u'type').callprop(u'allowedMarks', var.get(u'child').get(u'marks'))))
                        if var.get(u'openStart'):
                            var.put(u'child', var.get(u'closeNodeStart')(var.get(u'child'), var.get(u'openStart'), (var.get(u'openEnd') if var.get(u'last') else Js(0.0))))
                            var.put(u'openStart', Js(0.0))
                        var.get(u'this$1').callprop(u'addNode', var.get(u'open'), var.get(u'child'), (var.get(u'openEnd') if var.get(u'last') else Js(0.0)))
                        var.get(u'open').put(u'match', var.get(u'match'))
                        if var.get(u'last'):
                            var.put(u'openEnd', Js(0.0))
                        var.put(u'placed', Js(True))
                        break
                    finally:
                            (var.put(u'd',Js(var.get(u'd').to_number())-Js(1))+Js(1))
                if var.get(u'placed').neg():
                    break
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        if ((var.get(u"this").get(u'open').get(u'length')>Js(1.0)) and (((var.get(u'i')>Js(0.0)) and (var.get(u'i')==var.get(u'fragment').get(u'childCount'))) or (var.get(u'parent') and (var.get(u"this").get(u'open').get((var.get(u"this").get(u'open').get(u'length')-Js(1.0))).get(u'parent').get(u'type')==var.get(u'parent').get(u'type'))))):
            var.get(u"this").callprop(u'closeNode')
        return var.get(u'dist').get(u'Slice').create(var.get(u'fragment').callprop(u'cutByIndex', var.get(u'i')), var.get(u'openStart'), var.get(u'openEnd'))
    PyJs_placeContent_468_._set_name(u'placeContent')
    var.get(u'Frontier').get(u'prototype').put(u'placeContent', PyJs_placeContent_468_)
    @Js
    def PyJs_addNode_470_(open, node, openEnd, this, arguments, var=var):
        var = Scope({u'node':node, u'addNode':PyJs_addNode_470_, u'this':this, u'arguments':arguments, u'openEnd':openEnd, u'open':open}, var)
        var.registers([u'node', u'openEnd', u'open'])
        var.get(u'open').put(u'content', var.get(u'closeFragmentEnd')(var.get(u'open').get(u'content'), var.get(u'open').get(u'openEnd')).callprop(u'addToEnd', var.get(u'node')))
        var.get(u'open').put(u'openEnd', var.get(u'openEnd'))
    PyJs_addNode_470_._set_name(u'addNode')
    var.get(u'Frontier').get(u'prototype').put(u'addNode', PyJs_addNode_470_)
    @Js
    def PyJs_closeNode_471_(this, arguments, var=var):
        var = Scope({u'this':this, u'closeNode':PyJs_closeNode_471_, u'arguments':arguments}, var)
        var.registers([u'open'])
        var.put(u'open', var.get(u"this").get(u'open').callprop(u'pop'))
        if (var.get(u'open').get(u'content').get(u'size')==Js(0.0)):
            pass
        else:
            if var.get(u'open').get(u'wrapper'):
                var.get(u"this").callprop(u'addNode', var.get(u"this").get(u'open').get((var.get(u"this").get(u'open').get(u'length')-Js(1.0))), var.get(u'open').get(u'parent').callprop(u'copy', var.get(u'open').get(u'content')), (var.get(u'open').get(u'openEnd')+Js(1.0)))
            else:
                PyJs_Object_472_ = Js({u'depth':var.get(u'open').get(u'depth'),u'content':var.get(u'open').get(u'content'),u'openEnd':var.get(u'open').get(u'openEnd')})
                var.get(u"this").get(u'placed').put(var.get(u'open').get(u'depth'), PyJs_Object_472_)
    PyJs_closeNode_471_._set_name(u'closeNode')
    var.get(u'Frontier').get(u'prototype').put(u'closeNode', PyJs_closeNode_471_)
    pass
    pass
    pass
    @Js
    def PyJs_anonymous_473_(PyJsArg_66726f6d_, to, slice, this, arguments, var=var):
        var = Scope({u'this':this, u'to':to, u'slice':slice, u'from':PyJsArg_66726f6d_, u'arguments':arguments}, var)
        var.registers([u'preferredDepth', u'pos', u'this$1', u'targetDepths', u'slice', u'$to', u'preferredTarget', u'$from', u'content', u'to', u'preferredTargetIndex', u'spec', u'node', u'targetDepth', u'leftNodes', u'parent', u'index', u'from', u'expand', u'insert', u'd', u'openDepth', u'i', u'j', u'i$1'])
        var.put(u'this$1', var.get(u"this"))
        if var.get(u'slice').get(u'size').neg():
            return var.get(u"this").callprop(u'deleteRange', var.get(u'from'), var.get(u'to'))
        var.put(u'$from', var.get(u"this").get(u'doc').callprop(u'resolve', var.get(u'from')))
        var.put(u'$to', var.get(u"this").get(u'doc').callprop(u'resolve', var.get(u'to')))
        if var.get(u'fitsTrivially')(var.get(u'$from'), var.get(u'$to'), var.get(u'slice')):
            return var.get(u"this").callprop(u'step', var.get(u'ReplaceStep').create(var.get(u'from'), var.get(u'to'), var.get(u'slice')))
        var.put(u'targetDepths', var.get(u'coveredDepths')(var.get(u'$from'), var.get(u"this").get(u'doc').callprop(u'resolve', var.get(u'to'))))
        if (var.get(u'targetDepths').get((var.get(u'targetDepths').get(u'length')-Js(1.0)))==Js(0.0)):
            var.get(u'targetDepths').callprop(u'pop')
        var.put(u'preferredTarget', (-(var.get(u'$from').get(u'depth')+Js(1.0))))
        var.get(u'targetDepths').callprop(u'unshift', var.get(u'preferredTarget'))
        #for JS loop
        var.put(u'd', var.get(u'$from').get(u'depth'))
        var.put(u'pos', (var.get(u'$from').get(u'pos')-Js(1.0)))
        while (var.get(u'd')>Js(0.0)):
            try:
                var.put(u'spec', var.get(u'$from').callprop(u'node', var.get(u'd')).get(u'type').get(u'spec'))
                if (var.get(u'spec').get(u'defining') or var.get(u'spec').get(u'isolating')):
                    break
                if (var.get(u'targetDepths').callprop(u'indexOf', var.get(u'd'))>(-Js(1.0))):
                    var.put(u'preferredTarget', var.get(u'd'))
                else:
                    if (var.get(u'$from').callprop(u'before', var.get(u'd'))==var.get(u'pos')):
                        var.get(u'targetDepths').callprop(u'splice', Js(1.0), Js(0.0), (-var.get(u'd')))
            finally:
                    PyJsComma((var.put(u'd',Js(var.get(u'd').to_number())-Js(1))+Js(1)),(var.put(u'pos',Js(var.get(u'pos').to_number())-Js(1))+Js(1)))
        var.put(u'preferredTargetIndex', var.get(u'targetDepths').callprop(u'indexOf', var.get(u'preferredTarget')))
        var.put(u'leftNodes', Js([]))
        var.put(u'preferredDepth', var.get(u'slice').get(u'openStart'))
        #for JS loop
        var.put(u'content', var.get(u'slice').get(u'content'))
        var.put(u'i', Js(0.0))
        while 1:
            try:
                var.put(u'node', var.get(u'content').get(u'firstChild'))
                var.get(u'leftNodes').callprop(u'push', var.get(u'node'))
                if (var.get(u'i')==var.get(u'slice').get(u'openStart')):
                    break
                var.put(u'content', var.get(u'node').get(u'content'))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        if (((var.get(u'preferredDepth')>Js(0.0)) and var.get(u'leftNodes').get((var.get(u'preferredDepth')-Js(1.0))).get(u'type').get(u'spec').get(u'defining')) and (var.get(u'$from').callprop(u'node', var.get(u'preferredTargetIndex')).get(u'type')!=var.get(u'leftNodes').get((var.get(u'preferredDepth')-Js(1.0))).get(u'type'))):
            var.put(u'preferredDepth', Js(1.0), u'-')
        else:
            def PyJs_LONG_474_(var=var):
                return ((((var.get(u'preferredDepth')>=Js(2.0)) and var.get(u'leftNodes').get((var.get(u'preferredDepth')-Js(1.0))).get(u'isTextblock')) and var.get(u'leftNodes').get((var.get(u'preferredDepth')-Js(2.0))).get(u'type').get(u'spec').get(u'defining')) and (var.get(u'$from').callprop(u'node', var.get(u'preferredTargetIndex')).get(u'type')!=var.get(u'leftNodes').get((var.get(u'preferredDepth')-Js(2.0))).get(u'type')))
            if PyJs_LONG_474_():
                var.put(u'preferredDepth', Js(2.0), u'-')
        #for JS loop
        var.put(u'j', var.get(u'slice').get(u'openStart'))
        while (var.get(u'j')>=Js(0.0)):
            try:
                var.put(u'openDepth', (((var.get(u'j')+var.get(u'preferredDepth'))+Js(1.0))%(var.get(u'slice').get(u'openStart')+Js(1.0))))
                var.put(u'insert', var.get(u'leftNodes').get(var.get(u'openDepth')))
                if var.get(u'insert').neg():
                    continue
                #for JS loop
                var.put(u'i$1', Js(0.0))
                while (var.get(u'i$1')<var.get(u'targetDepths').get(u'length')):
                    try:
                        var.put(u'targetDepth', var.get(u'targetDepths').get(((var.get(u'i$1')+var.get(u'preferredTargetIndex'))%var.get(u'targetDepths').get(u'length'))))
                        var.put(u'expand', Js(True))
                        if (var.get(u'targetDepth')<Js(0.0)):
                            var.put(u'expand', Js(False))
                            var.put(u'targetDepth', (-var.get(u'targetDepth')))
                        var.put(u'parent', var.get(u'$from').callprop(u'node', (var.get(u'targetDepth')-Js(1.0))))
                        var.put(u'index', var.get(u'$from').callprop(u'index', (var.get(u'targetDepth')-Js(1.0))))
                        if var.get(u'parent').callprop(u'canReplaceWith', var.get(u'index'), var.get(u'index'), var.get(u'insert').get(u'type'), var.get(u'insert').get(u'marks')):
                            def PyJs_LONG_475_(var=var):
                                return var.get(u'this$1').callprop(u'replace', var.get(u'$from').callprop(u'before', var.get(u'targetDepth')), (var.get(u'$to').callprop(u'after', var.get(u'targetDepth')) if var.get(u'expand') else var.get(u'to')), var.get(u'dist').get(u'Slice').create(var.get(u'closeFragment')(var.get(u'slice').get(u'content'), Js(0.0), var.get(u'slice').get(u'openStart'), var.get(u'openDepth')), var.get(u'openDepth'), var.get(u'slice').get(u'openEnd')))
                            return PyJs_LONG_475_()
                    finally:
                            (var.put(u'i$1',Js(var.get(u'i$1').to_number())+Js(1))-Js(1))
            finally:
                    (var.put(u'j',Js(var.get(u'j').to_number())-Js(1))+Js(1))
        return var.get(u"this").callprop(u'replace', var.get(u'from'), var.get(u'to'), var.get(u'slice'))
    PyJs_anonymous_473_._set_name(u'anonymous')
    var.get(u'Transform').get(u'prototype').put(u'replaceRange', PyJs_anonymous_473_)
    pass
    @Js
    def PyJs_anonymous_476_(PyJsArg_66726f6d_, to, node, this, arguments, var=var):
        var = Scope({u'node':node, u'to':to, u'this':this, u'from':PyJsArg_66726f6d_, u'arguments':arguments}, var)
        var.registers([u'node', u'to', u'from', u'point'])
        if ((var.get(u'node').get(u'isInline').neg() and (var.get(u'from')==var.get(u'to'))) and var.get(u"this").get(u'doc').callprop(u'resolve', var.get(u'from')).get(u'parent').get(u'content').get(u'size')):
            var.put(u'point', var.get(u'insertPoint')(var.get(u"this").get(u'doc'), var.get(u'from'), var.get(u'node').get(u'type')))
            if (var.get(u'point')!=var.get(u"null")):
                var.put(u'from', var.put(u'to', var.get(u'point')))
        return var.get(u"this").callprop(u'replaceRange', var.get(u'from'), var.get(u'to'), var.get(u'dist').get(u'Slice').create(var.get(u'dist').get(u'Fragment').callprop(u'from', var.get(u'node')), Js(0.0), Js(0.0)))
    PyJs_anonymous_476_._set_name(u'anonymous')
    var.get(u'Transform').get(u'prototype').put(u'replaceRangeWith', PyJs_anonymous_476_)
    @Js
    def PyJs_anonymous_477_(PyJsArg_66726f6d_, to, this, arguments, var=var):
        var = Scope({u'this':this, u'to':to, u'from':PyJsArg_66726f6d_, u'arguments':arguments}, var)
        var.registers([u'$to', u'last', u'from', u'i', u'$from', u'to', u'depth', u'this$1', u'covered', u'd'])
        var.put(u'this$1', var.get(u"this"))
        var.put(u'$from', var.get(u"this").get(u'doc').callprop(u'resolve', var.get(u'from')))
        var.put(u'$to', var.get(u"this").get(u'doc').callprop(u'resolve', var.get(u'to')))
        var.put(u'covered', var.get(u'coveredDepths')(var.get(u'$from'), var.get(u'$to')))
        #for JS loop
        var.put(u'i', Js(0.0))
        while (var.get(u'i')<var.get(u'covered').get(u'length')):
            try:
                var.put(u'depth', var.get(u'covered').get(var.get(u'i')))
                var.put(u'last', (var.get(u'i')==(var.get(u'covered').get(u'length')-Js(1.0))))
                if ((var.get(u'last') and (var.get(u'depth')==Js(0.0))) or var.get(u'$from').callprop(u'node', var.get(u'depth')).get(u'type').get(u'contentMatch').get(u'validEnd')):
                    return var.get(u'this$1').callprop(u'delete', var.get(u'$from').callprop(u'start', var.get(u'depth')), var.get(u'$to').callprop(u'end', var.get(u'depth')))
                if ((var.get(u'depth')>Js(0.0)) and (var.get(u'last') or var.get(u'$from').callprop(u'node', (var.get(u'depth')-Js(1.0))).callprop(u'canReplace', var.get(u'$from').callprop(u'index', (var.get(u'depth')-Js(1.0))), var.get(u'$to').callprop(u'indexAfter', (var.get(u'depth')-Js(1.0)))))):
                    return var.get(u'this$1').callprop(u'delete', var.get(u'$from').callprop(u'before', var.get(u'depth')), var.get(u'$to').callprop(u'after', var.get(u'depth')))
            finally:
                    (var.put(u'i',Js(var.get(u'i').to_number())+Js(1))-Js(1))
        #for JS loop
        var.put(u'd', Js(1.0))
        while (var.get(u'd')<=var.get(u'$from').get(u'depth')):
            try:
                if (((var.get(u'from')-var.get(u'$from').callprop(u'start', var.get(u'd')))==(var.get(u'$from').get(u'depth')-var.get(u'd'))) and (var.get(u'to')>var.get(u'$from').callprop(u'end', var.get(u'd')))):
                    return var.get(u'this$1').callprop(u'delete', var.get(u'$from').callprop(u'before', var.get(u'd')), var.get(u'to'))
            finally:
                    (var.put(u'd',Js(var.get(u'd').to_number())+Js(1))-Js(1))
        return var.get(u"this").callprop(u'delete', var.get(u'from'), var.get(u'to'))
    PyJs_anonymous_477_._set_name(u'anonymous')
    var.get(u'Transform').get(u'prototype').put(u'deleteRange', PyJs_anonymous_477_)
    pass
    var.get(u'exports').put(u'Transform', var.get(u'Transform'))
    var.get(u'exports').put(u'TransformError', var.get(u'TransformError'))
    var.get(u'exports').put(u'Step', var.get(u'Step'))
    var.get(u'exports').put(u'StepResult', var.get(u'StepResult'))
    var.get(u'exports').put(u'joinPoint', var.get(u'joinPoint'))
    var.get(u'exports').put(u'canJoin', var.get(u'canJoin'))
    var.get(u'exports').put(u'canSplit', var.get(u'canSplit'))
    var.get(u'exports').put(u'insertPoint', var.get(u'insertPoint'))
    var.get(u'exports').put(u'dropPoint', var.get(u'dropPoint'))
    var.get(u'exports').put(u'liftTarget', var.get(u'liftTarget'))
    var.get(u'exports').put(u'findWrapping', var.get(u'findWrapping'))
    var.get(u'exports').put(u'StepMap', var.get(u'StepMap'))
    var.get(u'exports').put(u'MapResult', var.get(u'MapResult'))
    var.get(u'exports').put(u'Mapping', var.get(u'Mapping'))
    var.get(u'exports').put(u'AddMarkStep', var.get(u'AddMarkStep'))
    var.get(u'exports').put(u'RemoveMarkStep', var.get(u'RemoveMarkStep'))
    var.get(u'exports').put(u'ReplaceStep', var.get(u'ReplaceStep'))
    var.get(u'exports').put(u'ReplaceAroundStep', var.get(u'ReplaceAroundStep'))
    var.get(u'exports').put(u'replaceStep', var.get(u'replaceStep'))
PyJs_anonymous_355_._set_name(u'anonymous')
var.put(u'dist$1', var.get(u'createCommonjsModule')(PyJs_anonymous_355_))
var.get(u'unwrapExports')(var.get(u'dist$1'))
var.put(u'dist_1$1', var.get(u'dist$1').get(u'Transform'))
var.put(u'dist_2$1', var.get(u'dist$1').get(u'TransformError'))
var.put(u'dist_3$1', var.get(u'dist$1').get(u'Step'))
var.put(u'dist_4$1', var.get(u'dist$1').get(u'StepResult'))
var.put(u'dist_5$1', var.get(u'dist$1').get(u'joinPoint'))
var.put(u'dist_6$1', var.get(u'dist$1').get(u'canJoin'))
var.put(u'dist_7$1', var.get(u'dist$1').get(u'canSplit'))
var.put(u'dist_8$1', var.get(u'dist$1').get(u'insertPoint'))
var.put(u'dist_9$1', var.get(u'dist$1').get(u'dropPoint'))
var.put(u'dist_10$1', var.get(u'dist$1').get(u'liftTarget'))
var.put(u'dist_11$1', var.get(u'dist$1').get(u'findWrapping'))
var.put(u'dist_12$1', var.get(u'dist$1').get(u'StepMap'))
var.put(u'dist_13$1', var.get(u'dist$1').get(u'MapResult'))
var.put(u'dist_14', var.get(u'dist$1').get(u'Mapping'))
var.put(u'dist_15', var.get(u'dist$1').get(u'AddMarkStep'))
var.put(u'dist_16', var.get(u'dist$1').get(u'RemoveMarkStep'))
var.put(u'dist_17', var.get(u'dist$1').get(u'ReplaceStep'))
var.put(u'dist_18', var.get(u'dist$1').get(u'ReplaceAroundStep'))
var.put(u'dist_19', var.get(u'dist$1').get(u'replaceStep'))
@Js
def PyJs_anonymous_479_(steps_data, doc, this, arguments, var=var):
    var = Scope({u'this':this, u'doc':doc, u'arguments':arguments, u'steps_data':steps_data}, var)
    var.registers([u'doc', u'steps', u'transform', u'steps_data', u'schema'])
    var.put(u'schema', var.get(u'doc').get(u'type').get(u'schema'))
    @Js
    def PyJs_anonymous_480_(s, this, arguments, var=var):
        var = Scope({u'this':this, u's':s, u'arguments':arguments}, var)
        var.registers([u's'])
        return var.get(u'dist_3$1').callprop(u'fromJSON', var.get(u'schema'), var.get(u's'))
    PyJs_anonymous_480_._set_name(u'anonymous')
    var.put(u'steps', var.get(u'steps_data').callprop(u'map', PyJs_anonymous_480_))
    var.put(u'transform', var.get(u'dist_1$1').create(var.get(u'doc')))
    @Js
    def PyJs_anonymous_481_(step, this, arguments, var=var):
        var = Scope({u'this':this, u'step':step, u'arguments':arguments}, var)
        var.registers([u'step'])
        return var.get(u'transform').callprop(u'step', var.get(u'step'))
    PyJs_anonymous_481_._set_name(u'anonymous')
    var.get(u'steps').callprop(u'forEach', PyJs_anonymous_481_)
    return var.get(u'transform').get(u'doc')
PyJs_anonymous_479_._set_name(u'anonymous')
var.put(u'transform_doc', PyJs_anonymous_479_)
@Js
def PyJs_anonymous_482_(doc_data, schema_spec, this, arguments, var=var):
    var = Scope({u'this':this, u'doc_data':doc_data, u'arguments':arguments, u'schema_spec':schema_spec}, var)
    var.registers([u'doc_data', u'schema_spec', u'schema'])
    var.put(u'schema', var.get(u'dist_8').create(var.get(u'schema_spec')))
    return var.get(u'schema').callprop(u'nodeFromJSON', var.get(u'doc_data'))
PyJs_anonymous_482_._set_name(u'anonymous')
var.put(u'create_doc', PyJs_anonymous_482_)
var.get(u'exports').put(u'transform_doc', var.get(u'transform_doc'))
var.get(u'exports').put(u'create_doc', var.get(u'create_doc'))
pass


# Add lib to the module scope
__init__ = var.to_python()