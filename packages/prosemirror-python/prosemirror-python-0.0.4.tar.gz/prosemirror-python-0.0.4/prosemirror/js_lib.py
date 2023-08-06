__all__ = ['js_lib']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers([])
@Js
def PyJs_anonymous_0_(exports, this, arguments, var=var):
    var = Scope({'exports':exports, 'this':this, 'arguments':arguments}, var)
    var.registers(['dist_8', 'dist_9$1', 'dist_18', 'dist_10', 'dist_3$1', 'dist_12', 'transform_doc_json', 'create_doc', 'create_doc_json', 'dist_4$1', 'dist_17', 'dist$1', 'dist_15', 'dist_11', 'dist_6$1', 'transform_doc', 'dist_13$1', 'dist_12$1', 'dist_5', 'dist_13', 'dist_3', 'dist_6', 'dist_1', 'dist_10$1', 'dist_8$1', 'dist_4', 'orderedmap', 'createCommonjsModule', 'dist_11$1', 'exports', 'dist_5$1', 'dist', 'dist_16', 'dist_9', 'dist_1$1', 'dist_7', 'OrderedMap', 'unwrapExports', 'dist_2$1', 'dist_7$1', 'dist_2', 'dist_19', 'dist_14'])
    @Js
    def PyJsHoisted_unwrapExports_(x, this, arguments, var=var):
        var = Scope({'x':x, 'this':this, 'arguments':arguments}, var)
        var.registers(['x'])
        return (var.get('x').get('default') if ((var.get('x') and var.get('x').get('__esModule')) and var.get('Object').get('prototype').get('hasOwnProperty').callprop('call', var.get('x'), Js('default'))) else var.get('x'))
    PyJsHoisted_unwrapExports_.func_name = 'unwrapExports'
    var.put('unwrapExports', PyJsHoisted_unwrapExports_)
    @Js
    def PyJsHoisted_createCommonjsModule_(fn, module, this, arguments, var=var):
        var = Scope({'fn':fn, 'module':module, 'this':this, 'arguments':arguments}, var)
        var.registers(['module', 'fn'])
        PyJs_Object_2_ = Js({})
        PyJs_Object_1_ = Js({'exports':PyJs_Object_2_})
        return PyJsComma(PyJsComma(var.put('module', PyJs_Object_1_),var.get('fn')(var.get('module'), var.get('module').get('exports'))),var.get('module').get('exports'))
    PyJsHoisted_createCommonjsModule_.func_name = 'createCommonjsModule'
    var.put('createCommonjsModule', PyJsHoisted_createCommonjsModule_)
    @Js
    def PyJsHoisted_OrderedMap_(content, this, arguments, var=var):
        var = Scope({'content':content, 'this':this, 'arguments':arguments}, var)
        var.registers(['content'])
        var.get(u"this").put('content', var.get('content'))
    PyJsHoisted_OrderedMap_.func_name = 'OrderedMap'
    var.put('OrderedMap', PyJsHoisted_OrderedMap_)
    Js('use strict')
    pass
    pass
    pass
    @Js
    def PyJs_anonymous_4_(key, this, arguments, var=var):
        var = Scope({'key':key, 'this':this, 'arguments':arguments}, var)
        var.registers(['key', 'i'])
        #for JS loop
        var.put('i', Js(0.0))
        while (var.get('i')<var.get(u"this").get('content').get('length')):
            try:
                if PyJsStrictEq(var.get(u"this").get('content').get(var.get('i')),var.get('key')):
                    return var.get('i')
            finally:
                    var.put('i', Js(2.0), '+')
        return (-Js(1.0))
    PyJs_anonymous_4_._set_name('anonymous')
    @Js
    def PyJs_anonymous_5_(key, this, arguments, var=var):
        var = Scope({'key':key, 'this':this, 'arguments':arguments}, var)
        var.registers(['found', 'key'])
        var.put('found', var.get(u"this").callprop('find', var.get('key')))
        return (var.get('undefined') if (var.get('found')==(-Js(1.0))) else var.get(u"this").get('content').get((var.get('found')+Js(1.0))))
    PyJs_anonymous_5_._set_name('anonymous')
    @Js
    def PyJs_anonymous_6_(key, value, newKey, this, arguments, var=var):
        var = Scope({'key':key, 'value':value, 'newKey':newKey, 'this':this, 'arguments':arguments}, var)
        var.registers(['newKey', 'found', 'content', 'value', 'key', 'self'])
        var.put('self', (var.get(u"this").callprop('remove', var.get('newKey')) if (var.get('newKey') and (var.get('newKey')!=var.get('key'))) else var.get(u"this")))
        var.put('found', var.get('self').callprop('find', var.get('key')))
        var.put('content', var.get('self').get('content').callprop('slice'))
        if (var.get('found')==(-Js(1.0))):
            var.get('content').callprop('push', (var.get('newKey') or var.get('key')), var.get('value'))
        else:
            var.get('content').put((var.get('found')+Js(1.0)), var.get('value'))
            if var.get('newKey'):
                var.get('content').put(var.get('found'), var.get('newKey'))
        return var.get('OrderedMap').create(var.get('content'))
    PyJs_anonymous_6_._set_name('anonymous')
    @Js
    def PyJs_anonymous_7_(key, this, arguments, var=var):
        var = Scope({'key':key, 'this':this, 'arguments':arguments}, var)
        var.registers(['found', 'content', 'key'])
        var.put('found', var.get(u"this").callprop('find', var.get('key')))
        if (var.get('found')==(-Js(1.0))):
            return var.get(u"this")
        var.put('content', var.get(u"this").get('content').callprop('slice'))
        var.get('content').callprop('splice', var.get('found'), Js(2.0))
        return var.get('OrderedMap').create(var.get('content'))
    PyJs_anonymous_7_._set_name('anonymous')
    @Js
    def PyJs_anonymous_8_(key, value, this, arguments, var=var):
        var = Scope({'key':key, 'value':value, 'this':this, 'arguments':arguments}, var)
        var.registers(['value', 'key'])
        return var.get('OrderedMap').create(Js([var.get('key'), var.get('value')]).callprop('concat', var.get(u"this").callprop('remove', var.get('key')).get('content')))
    PyJs_anonymous_8_._set_name('anonymous')
    @Js
    def PyJs_anonymous_9_(key, value, this, arguments, var=var):
        var = Scope({'key':key, 'value':value, 'this':this, 'arguments':arguments}, var)
        var.registers(['content', 'value', 'key'])
        var.put('content', var.get(u"this").callprop('remove', var.get('key')).get('content').callprop('slice'))
        var.get('content').callprop('push', var.get('key'), var.get('value'))
        return var.get('OrderedMap').create(var.get('content'))
    PyJs_anonymous_9_._set_name('anonymous')
    @Js
    def PyJs_anonymous_10_(place, key, value, this, arguments, var=var):
        var = Scope({'place':place, 'key':key, 'value':value, 'this':this, 'arguments':arguments}, var)
        var.registers(['without', 'found', 'content', 'value', 'key', 'place'])
        var.put('without', var.get(u"this").callprop('remove', var.get('key')))
        var.put('content', var.get('without').get('content').callprop('slice'))
        var.put('found', var.get('without').callprop('find', var.get('place')))
        var.get('content').callprop('splice', (var.get('content').get('length') if (var.get('found')==(-Js(1.0))) else var.get('found')), Js(0.0), var.get('key'), var.get('value'))
        return var.get('OrderedMap').create(var.get('content'))
    PyJs_anonymous_10_._set_name('anonymous')
    @Js
    def PyJs_anonymous_11_(f, this, arguments, var=var):
        var = Scope({'f':f, 'this':this, 'arguments':arguments}, var)
        var.registers(['f', 'i'])
        #for JS loop
        var.put('i', Js(0.0))
        while (var.get('i')<var.get(u"this").get('content').get('length')):
            try:
                var.get('f')(var.get(u"this").get('content').get(var.get('i')), var.get(u"this").get('content').get((var.get('i')+Js(1.0))))
            finally:
                    var.put('i', Js(2.0), '+')
    PyJs_anonymous_11_._set_name('anonymous')
    @Js
    def PyJs_anonymous_12_(map, this, arguments, var=var):
        var = Scope({'map':map, 'this':this, 'arguments':arguments}, var)
        var.registers(['map'])
        var.put('map', var.get('OrderedMap').callprop('from', var.get('map')))
        if var.get('map').get('size').neg():
            return var.get(u"this")
        return var.get('OrderedMap').create(var.get('map').get('content').callprop('concat', var.get(u"this").callprop('subtract', var.get('map')).get('content')))
    PyJs_anonymous_12_._set_name('anonymous')
    @Js
    def PyJs_anonymous_13_(map, this, arguments, var=var):
        var = Scope({'map':map, 'this':this, 'arguments':arguments}, var)
        var.registers(['map'])
        var.put('map', var.get('OrderedMap').callprop('from', var.get('map')))
        if var.get('map').get('size').neg():
            return var.get(u"this")
        return var.get('OrderedMap').create(var.get(u"this").callprop('subtract', var.get('map')).get('content').callprop('concat', var.get('map').get('content')))
    PyJs_anonymous_13_._set_name('anonymous')
    @Js
    def PyJs_anonymous_14_(map, this, arguments, var=var):
        var = Scope({'map':map, 'this':this, 'arguments':arguments}, var)
        var.registers(['map', 'i', 'result'])
        var.put('result', var.get(u"this"))
        var.put('map', var.get('OrderedMap').callprop('from', var.get('map')))
        #for JS loop
        var.put('i', Js(0.0))
        while (var.get('i')<var.get('map').get('content').get('length')):
            try:
                var.put('result', var.get('result').callprop('remove', var.get('map').get('content').get(var.get('i'))))
            finally:
                    var.put('i', Js(2.0), '+')
        return var.get('result')
    PyJs_anonymous_14_._set_name('anonymous')
    PyJs_Object_3_ = Js({'constructor':var.get('OrderedMap'),'find':PyJs_anonymous_4_,'get':PyJs_anonymous_5_,'update':PyJs_anonymous_6_,'remove':PyJs_anonymous_7_,'addToStart':PyJs_anonymous_8_,'addToEnd':PyJs_anonymous_9_,'addBefore':PyJs_anonymous_10_,'forEach':PyJs_anonymous_11_,'prepend':PyJs_anonymous_12_,'append':PyJs_anonymous_13_,'subtract':PyJs_anonymous_14_})
    @Js
    def PyJs_anonymous_15_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers([])
        return (var.get(u"this").get('content').get('length')>>Js(1.0))
    PyJs_anonymous_15_._set_name('anonymous')
    PyJs_Object_3_.define_own_property('size', {"get":PyJs_anonymous_15_, "configurable":True, "enumerable":True})
    var.get('OrderedMap').put('prototype', PyJs_Object_3_)
    @Js
    def PyJs_anonymous_16_(value, this, arguments, var=var):
        var = Scope({'value':value, 'this':this, 'arguments':arguments}, var)
        var.registers(['value', 'content', 'prop'])
        if var.get('value').instanceof(var.get('OrderedMap')):
            return var.get('value')
        var.put('content', Js([]))
        if var.get('value'):
            for PyJsTemp in var.get('value'):
                var.put('prop', PyJsTemp)
                var.get('content').callprop('push', var.get('prop'), var.get('value').get(var.get('prop')))
        return var.get('OrderedMap').create(var.get('content'))
    PyJs_anonymous_16_._set_name('anonymous')
    var.get('OrderedMap').put('from', PyJs_anonymous_16_)
    var.put('orderedmap', var.get('OrderedMap'))
    @Js
    def PyJs_anonymous_17_(module, exports, this, arguments, var=var):
        var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
        var.registers(['parseExpr', 'close', 'parseExprSeq', 'ParseContext', 'prototypeAccessors$2', 'prototypeAccessors$1$3', 'listTags', 'OPT_OPEN_LEFT', 'NodeRange', 'nullFrom', 'defaultAttrs', 'Node', 'Slice', 'replaceTwoWay', 'emptyAttrs', 'prototypeAccessors$1$2', 'dfa', 'prototypeAccessors$5', 'NodeContext', 'resolveCachePos', 'normalizeList', 'DOMSerializer', 'DOMParser', 'copy', 'retIndex', 'insertInto', 'ResolvedPos', 'prototypeAccessors', 'compareDeep', 'replaceOuter', 'parseExprRange', 'replaceThreeWay', 'prepareSliceForReplace', 'ReplaceError', 'cmp', 'wrapMarks', 'prototypeAccessors$1$1', 'replace', 'ContentMatch', 'nfa', 'Schema', 'parseStyles', 'Fragment', '_interopDefault', 'TextNode', 'prototypeAccessors$3', 'TokenStream', 'doc', 'prototypeAccessors$1', 'Mark', 'gatherMarks', 'blockTags', 'resolveName', 'addNode', 'OPT_PRESERVE_WS_FULL', 'prototypeAccessors$4', 'initAttrs', 'resolveCache', 'module', 'NodeType', 'matches', 'resolveCacheSize', 'parseExprAtom', 'findDiffEnd', 'prototypeAccessors$6', 'joinable', 'MarkType', 'exports', 'checkForDeadEnds', 'ignoreTags', 'Attribute', 'wsOptionsFor', 'gatherToDOM', 'OPT_PRESERVE_WS', 'addRange', 'found', 'computeAttrs', 'OrderedMap', 'parseExprSubscript', 'parseNum', 'removeRange', 'findDiffStart', 'checkJoin'])
        @Js
        def PyJsHoisted__interopDefault_(ex, this, arguments, var=var):
            var = Scope({'ex':ex, 'this':this, 'arguments':arguments}, var)
            var.registers(['ex'])
            return (var.get('ex').get('default') if ((var.get('ex') and PyJsStrictEq(var.get('ex',throw=False).typeof(),Js('object'))) and var.get('ex').contains(Js('default'))) else var.get('ex'))
        PyJsHoisted__interopDefault_.func_name = '_interopDefault'
        var.put('_interopDefault', PyJsHoisted__interopDefault_)
        @Js
        def PyJsHoisted_findDiffStart_(a, b, pos, this, arguments, var=var):
            var = Scope({'a':a, 'b':b, 'pos':pos, 'this':this, 'arguments':arguments}, var)
            var.registers(['childB', 'childA', 'j', 'a', 'i', 'pos', 'inner', 'b'])
            #for JS loop
            var.put('i', Js(0.0))
            while 1:
                try:
                    if ((var.get('i')==var.get('a').get('childCount')) or (var.get('i')==var.get('b').get('childCount'))):
                        return (var.get(u"null") if (var.get('a').get('childCount')==var.get('b').get('childCount')) else var.get('pos'))
                    var.put('childA', var.get('a').callprop('child', var.get('i')))
                    var.put('childB', var.get('b').callprop('child', var.get('i')))
                    if (var.get('childA')==var.get('childB')):
                        var.put('pos', var.get('childA').get('nodeSize'), '+')
                        continue
                    if var.get('childA').callprop('sameMarkup', var.get('childB')).neg():
                        return var.get('pos')
                    if (var.get('childA').get('isText') and (var.get('childA').get('text')!=var.get('childB').get('text'))):
                        #for JS loop
                        var.put('j', Js(0.0))
                        while (var.get('childA').get('text').get(var.get('j'))==var.get('childB').get('text').get(var.get('j'))):
                            try:
                                (var.put('pos',Js(var.get('pos').to_number())+Js(1))-Js(1))
                            finally:
                                    (var.put('j',Js(var.get('j').to_number())+Js(1))-Js(1))
                        return var.get('pos')
                    if (var.get('childA').get('content').get('size') or var.get('childB').get('content').get('size')):
                        var.put('inner', var.get('findDiffStart')(var.get('childA').get('content'), var.get('childB').get('content'), (var.get('pos')+Js(1.0))))
                        if (var.get('inner')!=var.get(u"null")):
                            return var.get('inner')
                    var.put('pos', var.get('childA').get('nodeSize'), '+')
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        PyJsHoisted_findDiffStart_.func_name = 'findDiffStart'
        var.put('findDiffStart', PyJsHoisted_findDiffStart_)
        @Js
        def PyJsHoisted_findDiffEnd_(a, b, posA, posB, this, arguments, var=var):
            var = Scope({'a':a, 'b':b, 'posA':posA, 'posB':posB, 'this':this, 'arguments':arguments}, var)
            var.registers(['childB', 'iA', 'size', 'posA', 'inner', 'minSize', 'same', 'childA', 'a', 'iB', 'b', 'posB'])
            #for JS loop
            var.put('iA', var.get('a').get('childCount'))
            var.put('iB', var.get('b').get('childCount'))
            while 1:
                if ((var.get('iA')==Js(0.0)) or (var.get('iB')==Js(0.0))):
                    PyJs_Object_19_ = Js({'a':var.get('posA'),'b':var.get('posB')})
                    return (var.get(u"null") if (var.get('iA')==var.get('iB')) else PyJs_Object_19_)
                var.put('childA', var.get('a').callprop('child', var.put('iA',Js(var.get('iA').to_number())-Js(1))))
                var.put('childB', var.get('b').callprop('child', var.put('iB',Js(var.get('iB').to_number())-Js(1))))
                var.put('size', var.get('childA').get('nodeSize'))
                if (var.get('childA')==var.get('childB')):
                    var.put('posA', var.get('size'), '-')
                    var.put('posB', var.get('size'), '-')
                    continue
                if var.get('childA').callprop('sameMarkup', var.get('childB')).neg():
                    PyJs_Object_20_ = Js({'a':var.get('posA'),'b':var.get('posB')})
                    return PyJs_Object_20_
                if (var.get('childA').get('isText') and (var.get('childA').get('text')!=var.get('childB').get('text'))):
                    var.put('same', Js(0.0))
                    var.put('minSize', var.get('Math').callprop('min', var.get('childA').get('text').get('length'), var.get('childB').get('text').get('length')))
                    while ((var.get('same')<var.get('minSize')) and (var.get('childA').get('text').get(((var.get('childA').get('text').get('length')-var.get('same'))-Js(1.0)))==var.get('childB').get('text').get(((var.get('childB').get('text').get('length')-var.get('same'))-Js(1.0))))):
                        (var.put('same',Js(var.get('same').to_number())+Js(1))-Js(1))
                        (var.put('posA',Js(var.get('posA').to_number())-Js(1))+Js(1))
                        (var.put('posB',Js(var.get('posB').to_number())-Js(1))+Js(1))
                    PyJs_Object_21_ = Js({'a':var.get('posA'),'b':var.get('posB')})
                    return PyJs_Object_21_
                if (var.get('childA').get('content').get('size') or var.get('childB').get('content').get('size')):
                    var.put('inner', var.get('findDiffEnd')(var.get('childA').get('content'), var.get('childB').get('content'), (var.get('posA')-Js(1.0)), (var.get('posB')-Js(1.0))))
                    if var.get('inner'):
                        return var.get('inner')
                var.put('posA', var.get('size'), '-')
                var.put('posB', var.get('size'), '-')
            
        PyJsHoisted_findDiffEnd_.func_name = 'findDiffEnd'
        var.put('findDiffEnd', PyJsHoisted_findDiffEnd_)
        @Js
        def PyJsHoisted_retIndex_(index, offset, this, arguments, var=var):
            var = Scope({'index':index, 'offset':offset, 'this':this, 'arguments':arguments}, var)
            var.registers(['offset', 'index'])
            var.get('found').put('index', var.get('index'))
            var.get('found').put('offset', var.get('offset'))
            return var.get('found')
        PyJsHoisted_retIndex_.func_name = 'retIndex'
        var.put('retIndex', PyJsHoisted_retIndex_)
        @Js
        def PyJsHoisted_compareDeep_(a, b, this, arguments, var=var):
            var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
            var.registers(['a', 'p', 'i', 'p$1', 'array', 'b'])
            if PyJsStrictEq(var.get('a'),var.get('b')):
                return Js(True)
            if ((var.get('a') and (var.get('a',throw=False).typeof()==Js('object'))).neg() or (var.get('b') and (var.get('b',throw=False).typeof()==Js('object'))).neg()):
                return Js(False)
            var.put('array', var.get('Array').callprop('isArray', var.get('a')))
            if (var.get('Array').callprop('isArray', var.get('b'))!=var.get('array')):
                return Js(False)
            if var.get('array'):
                if (var.get('a').get('length')!=var.get('b').get('length')):
                    return Js(False)
                #for JS loop
                var.put('i', Js(0.0))
                while (var.get('i')<var.get('a').get('length')):
                    try:
                        if var.get('compareDeep')(var.get('a').get(var.get('i')), var.get('b').get(var.get('i'))).neg():
                            return Js(False)
                    finally:
                            (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            else:
                for PyJsTemp in var.get('a'):
                    var.put('p', PyJsTemp)
                    if (var.get('b').contains(var.get('p')).neg() or var.get('compareDeep')(var.get('a').get(var.get('p')), var.get('b').get(var.get('p'))).neg()):
                        return Js(False)
                for PyJsTemp in var.get('b'):
                    var.put('p$1', PyJsTemp)
                    if var.get('a').contains(var.get('p$1')).neg():
                        return Js(False)
            return Js(True)
        PyJsHoisted_compareDeep_.func_name = 'compareDeep'
        var.put('compareDeep', PyJsHoisted_compareDeep_)
        @Js
        def PyJsHoisted_ReplaceError_(message, this, arguments, var=var):
            var = Scope({'message':message, 'this':this, 'arguments':arguments}, var)
            var.registers(['err', 'message'])
            var.put('err', var.get('Error').callprop('call', var.get(u"this"), var.get('message')))
            var.get('err').put('__proto__', var.get('ReplaceError').get('prototype'))
            return var.get('err')
        PyJsHoisted_ReplaceError_.func_name = 'ReplaceError'
        var.put('ReplaceError', PyJsHoisted_ReplaceError_)
        @Js
        def PyJsHoisted_removeRange_(content, PyJsArg_66726f6d_, to, this, arguments, var=var):
            var = Scope({'content':content, 'from':PyJsArg_66726f6d_, 'to':to, 'this':this, 'arguments':arguments}, var)
            var.registers(['child', 'offset', 'ref$1', 'indexTo', 'ref', 'offsetTo', 'index', 'content', 'to', 'from'])
            var.put('ref', var.get('content').callprop('findIndex', var.get('from')))
            var.put('index', var.get('ref').get('index'))
            var.put('offset', var.get('ref').get('offset'))
            var.put('child', var.get('content').callprop('maybeChild', var.get('index')))
            var.put('ref$1', var.get('content').callprop('findIndex', var.get('to')))
            var.put('indexTo', var.get('ref$1').get('index'))
            var.put('offsetTo', var.get('ref$1').get('offset'))
            if ((var.get('offset')==var.get('from')) or var.get('child').get('isText')):
                if ((var.get('offsetTo')!=var.get('to')) and var.get('content').callprop('child', var.get('indexTo')).get('isText').neg()):
                    PyJsTempException = JsToPyException(var.get('RangeError').create(Js('Removing non-flat range')))
                    raise PyJsTempException
                return var.get('content').callprop('cut', Js(0.0), var.get('from')).callprop('append', var.get('content').callprop('cut', var.get('to')))
            if (var.get('index')!=var.get('indexTo')):
                PyJsTempException = JsToPyException(var.get('RangeError').create(Js('Removing non-flat range')))
                raise PyJsTempException
            return var.get('content').callprop('replaceChild', var.get('index'), var.get('child').callprop('copy', var.get('removeRange')(var.get('child').get('content'), ((var.get('from')-var.get('offset'))-Js(1.0)), ((var.get('to')-var.get('offset'))-Js(1.0)))))
        PyJsHoisted_removeRange_.func_name = 'removeRange'
        var.put('removeRange', PyJsHoisted_removeRange_)
        @Js
        def PyJsHoisted_insertInto_(content, dist, insert, parent, this, arguments, var=var):
            var = Scope({'content':content, 'dist':dist, 'insert':insert, 'parent':parent, 'this':this, 'arguments':arguments}, var)
            var.registers(['child', 'dist', 'insert', 'offset', 'ref', 'content', 'index', 'inner', 'parent'])
            var.put('ref', var.get('content').callprop('findIndex', var.get('dist')))
            var.put('index', var.get('ref').get('index'))
            var.put('offset', var.get('ref').get('offset'))
            var.put('child', var.get('content').callprop('maybeChild', var.get('index')))
            if ((var.get('offset')==var.get('dist')) or var.get('child').get('isText')):
                if (var.get('parent') and var.get('parent').callprop('canReplace', var.get('index'), var.get('index'), var.get('insert')).neg()):
                    return var.get(u"null")
                return var.get('content').callprop('cut', Js(0.0), var.get('dist')).callprop('append', var.get('insert')).callprop('append', var.get('content').callprop('cut', var.get('dist')))
            var.put('inner', var.get('insertInto')(var.get('child').get('content'), ((var.get('dist')-var.get('offset'))-Js(1.0)), var.get('insert')))
            return (var.get('inner') and var.get('content').callprop('replaceChild', var.get('index'), var.get('child').callprop('copy', var.get('inner'))))
        PyJsHoisted_insertInto_.func_name = 'insertInto'
        var.put('insertInto', PyJsHoisted_insertInto_)
        @Js
        def PyJsHoisted_replace_(PyJsArg_2466726f6d_, PyJsArg_24746f_, slice, this, arguments, var=var):
            var = Scope({'$from':PyJsArg_2466726f6d_, '$to':PyJsArg_24746f_, 'slice':slice, 'this':this, 'arguments':arguments}, var)
            var.registers(['$to', '$from', 'slice'])
            if (var.get('slice').get('openStart')>var.get('$from').get('depth')):
                PyJsTempException = JsToPyException(var.get('ReplaceError').create(Js('Inserted content deeper than insertion position')))
                raise PyJsTempException
            if ((var.get('$from').get('depth')-var.get('slice').get('openStart'))!=(var.get('$to').get('depth')-var.get('slice').get('openEnd'))):
                PyJsTempException = JsToPyException(var.get('ReplaceError').create(Js('Inconsistent open depths')))
                raise PyJsTempException
            return var.get('replaceOuter')(var.get('$from'), var.get('$to'), var.get('slice'), Js(0.0))
        PyJsHoisted_replace_.func_name = 'replace'
        var.put('replace', PyJsHoisted_replace_)
        @Js
        def PyJsHoisted_replaceOuter_(PyJsArg_2466726f6d_, PyJsArg_24746f_, slice, depth, this, arguments, var=var):
            var = Scope({'$from':PyJsArg_2466726f6d_, '$to':PyJsArg_24746f_, 'slice':slice, 'depth':depth, 'this':this, 'arguments':arguments}, var)
            var.registers(['$to', 'slice', 'node', '$from', 'end', 'depth', 'content', 'ref', 'index', 'start', 'inner', 'parent'])
            var.put('index', var.get('$from').callprop('index', var.get('depth')))
            var.put('node', var.get('$from').callprop('node', var.get('depth')))
            if ((var.get('index')==var.get('$to').callprop('index', var.get('depth'))) and (var.get('depth')<(var.get('$from').get('depth')-var.get('slice').get('openStart')))):
                var.put('inner', var.get('replaceOuter')(var.get('$from'), var.get('$to'), var.get('slice'), (var.get('depth')+Js(1.0))))
                return var.get('node').callprop('copy', var.get('node').get('content').callprop('replaceChild', var.get('index'), var.get('inner')))
            else:
                if var.get('slice').get('content').get('size').neg():
                    return var.get('close')(var.get('node'), var.get('replaceTwoWay')(var.get('$from'), var.get('$to'), var.get('depth')))
                else:
                    if (((var.get('slice').get('openStart').neg() and var.get('slice').get('openEnd').neg()) and (var.get('$from').get('depth')==var.get('depth'))) and (var.get('$to').get('depth')==var.get('depth'))):
                        var.put('parent', var.get('$from').get('parent'))
                        var.put('content', var.get('parent').get('content'))
                        return var.get('close')(var.get('parent'), var.get('content').callprop('cut', Js(0.0), var.get('$from').get('parentOffset')).callprop('append', var.get('slice').get('content')).callprop('append', var.get('content').callprop('cut', var.get('$to').get('parentOffset'))))
                    else:
                        var.put('ref', var.get('prepareSliceForReplace')(var.get('slice'), var.get('$from')))
                        var.put('start', var.get('ref').get('start'))
                        var.put('end', var.get('ref').get('end'))
                        return var.get('close')(var.get('node'), var.get('replaceThreeWay')(var.get('$from'), var.get('start'), var.get('end'), var.get('$to'), var.get('depth')))
        PyJsHoisted_replaceOuter_.func_name = 'replaceOuter'
        var.put('replaceOuter', PyJsHoisted_replaceOuter_)
        @Js
        def PyJsHoisted_checkJoin_(main, sub, this, arguments, var=var):
            var = Scope({'main':main, 'sub':sub, 'this':this, 'arguments':arguments}, var)
            var.registers(['main', 'sub'])
            if var.get('sub').get('type').callprop('compatibleContent', var.get('main').get('type')).neg():
                PyJsTempException = JsToPyException(var.get('ReplaceError').create((((Js('Cannot join ')+var.get('sub').get('type').get('name'))+Js(' onto '))+var.get('main').get('type').get('name'))))
                raise PyJsTempException
        PyJsHoisted_checkJoin_.func_name = 'checkJoin'
        var.put('checkJoin', PyJsHoisted_checkJoin_)
        @Js
        def PyJsHoisted_joinable_(PyJsArg_246265666f7265_, PyJsArg_246166746572_, depth, this, arguments, var=var):
            var = Scope({'$before':PyJsArg_246265666f7265_, '$after':PyJsArg_246166746572_, 'depth':depth, 'this':this, 'arguments':arguments}, var)
            var.registers(['depth', '$before', '$after', 'node'])
            var.put('node', var.get('$before').callprop('node', var.get('depth')))
            var.get('checkJoin')(var.get('node'), var.get('$after').callprop('node', var.get('depth')))
            return var.get('node')
        PyJsHoisted_joinable_.func_name = 'joinable'
        var.put('joinable', PyJsHoisted_joinable_)
        @Js
        def PyJsHoisted_addNode_(child, target, this, arguments, var=var):
            var = Scope({'child':child, 'target':target, 'this':this, 'arguments':arguments}, var)
            var.registers(['target', 'child', 'last'])
            var.put('last', (var.get('target').get('length')-Js(1.0)))
            if (((var.get('last')>=Js(0.0)) and var.get('child').get('isText')) and var.get('child').callprop('sameMarkup', var.get('target').get(var.get('last')))):
                var.get('target').put(var.get('last'), var.get('child').callprop('withText', (var.get('target').get(var.get('last')).get('text')+var.get('child').get('text'))))
            else:
                var.get('target').callprop('push', var.get('child'))
        PyJsHoisted_addNode_.func_name = 'addNode'
        var.put('addNode', PyJsHoisted_addNode_)
        @Js
        def PyJsHoisted_addRange_(PyJsArg_247374617274_, PyJsArg_24656e64_, depth, target, this, arguments, var=var):
            var = Scope({'$start':PyJsArg_247374617274_, '$end':PyJsArg_24656e64_, 'depth':depth, 'target':target, 'this':this, 'arguments':arguments}, var)
            var.registers(['startIndex', 'node', '$start', 'endIndex', 'depth', '$end', 'target', 'i'])
            var.put('node', (var.get('$end') or var.get('$start')).callprop('node', var.get('depth')))
            var.put('startIndex', Js(0.0))
            var.put('endIndex', (var.get('$end').callprop('index', var.get('depth')) if var.get('$end') else var.get('node').get('childCount')))
            if var.get('$start'):
                var.put('startIndex', var.get('$start').callprop('index', var.get('depth')))
                if (var.get('$start').get('depth')>var.get('depth')):
                    (var.put('startIndex',Js(var.get('startIndex').to_number())+Js(1))-Js(1))
                else:
                    if var.get('$start').get('textOffset'):
                        var.get('addNode')(var.get('$start').get('nodeAfter'), var.get('target'))
                        (var.put('startIndex',Js(var.get('startIndex').to_number())+Js(1))-Js(1))
            #for JS loop
            var.put('i', var.get('startIndex'))
            while (var.get('i')<var.get('endIndex')):
                try:
                    var.get('addNode')(var.get('node').callprop('child', var.get('i')), var.get('target'))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            if ((var.get('$end') and (var.get('$end').get('depth')==var.get('depth'))) and var.get('$end').get('textOffset')):
                var.get('addNode')(var.get('$end').get('nodeBefore'), var.get('target'))
        PyJsHoisted_addRange_.func_name = 'addRange'
        var.put('addRange', PyJsHoisted_addRange_)
        @Js
        def PyJsHoisted_close_(node, content, this, arguments, var=var):
            var = Scope({'node':node, 'content':content, 'this':this, 'arguments':arguments}, var)
            var.registers(['content', 'node'])
            if var.get('node').get('type').callprop('validContent', var.get('content')).neg():
                PyJsTempException = JsToPyException(var.get('ReplaceError').create((Js('Invalid content for node ')+var.get('node').get('type').get('name'))))
                raise PyJsTempException
            return var.get('node').callprop('copy', var.get('content'))
        PyJsHoisted_close_.func_name = 'close'
        var.put('close', PyJsHoisted_close_)
        @Js
        def PyJsHoisted_replaceThreeWay_(PyJsArg_2466726f6d_, PyJsArg_247374617274_, PyJsArg_24656e64_, PyJsArg_24746f_, depth, this, arguments, var=var):
            var = Scope({'$from':PyJsArg_2466726f6d_, '$start':PyJsArg_247374617274_, '$end':PyJsArg_24656e64_, '$to':PyJsArg_24746f_, 'depth':depth, 'this':this, 'arguments':arguments}, var)
            var.registers(['$to', 'openStart', 'openEnd', '$from', '$start', 'depth', '$end', 'content'])
            var.put('openStart', ((var.get('$from').get('depth')>var.get('depth')) and var.get('joinable')(var.get('$from'), var.get('$start'), (var.get('depth')+Js(1.0)))))
            var.put('openEnd', ((var.get('$to').get('depth')>var.get('depth')) and var.get('joinable')(var.get('$end'), var.get('$to'), (var.get('depth')+Js(1.0)))))
            var.put('content', Js([]))
            var.get('addRange')(var.get(u"null"), var.get('$from'), var.get('depth'), var.get('content'))
            if ((var.get('openStart') and var.get('openEnd')) and (var.get('$start').callprop('index', var.get('depth'))==var.get('$end').callprop('index', var.get('depth')))):
                var.get('checkJoin')(var.get('openStart'), var.get('openEnd'))
                var.get('addNode')(var.get('close')(var.get('openStart'), var.get('replaceThreeWay')(var.get('$from'), var.get('$start'), var.get('$end'), var.get('$to'), (var.get('depth')+Js(1.0)))), var.get('content'))
            else:
                if var.get('openStart'):
                    var.get('addNode')(var.get('close')(var.get('openStart'), var.get('replaceTwoWay')(var.get('$from'), var.get('$start'), (var.get('depth')+Js(1.0)))), var.get('content'))
                var.get('addRange')(var.get('$start'), var.get('$end'), var.get('depth'), var.get('content'))
                if var.get('openEnd'):
                    var.get('addNode')(var.get('close')(var.get('openEnd'), var.get('replaceTwoWay')(var.get('$end'), var.get('$to'), (var.get('depth')+Js(1.0)))), var.get('content'))
            var.get('addRange')(var.get('$to'), var.get(u"null"), var.get('depth'), var.get('content'))
            return var.get('Fragment').create(var.get('content'))
        PyJsHoisted_replaceThreeWay_.func_name = 'replaceThreeWay'
        var.put('replaceThreeWay', PyJsHoisted_replaceThreeWay_)
        @Js
        def PyJsHoisted_replaceTwoWay_(PyJsArg_2466726f6d_, PyJsArg_24746f_, depth, this, arguments, var=var):
            var = Scope({'$from':PyJsArg_2466726f6d_, '$to':PyJsArg_24746f_, 'depth':depth, 'this':this, 'arguments':arguments}, var)
            var.registers(['$to', '$from', 'type', 'depth', 'content'])
            var.put('content', Js([]))
            var.get('addRange')(var.get(u"null"), var.get('$from'), var.get('depth'), var.get('content'))
            if (var.get('$from').get('depth')>var.get('depth')):
                var.put('type', var.get('joinable')(var.get('$from'), var.get('$to'), (var.get('depth')+Js(1.0))))
                var.get('addNode')(var.get('close')(var.get('type'), var.get('replaceTwoWay')(var.get('$from'), var.get('$to'), (var.get('depth')+Js(1.0)))), var.get('content'))
            var.get('addRange')(var.get('$to'), var.get(u"null"), var.get('depth'), var.get('content'))
            return var.get('Fragment').create(var.get('content'))
        PyJsHoisted_replaceTwoWay_.func_name = 'replaceTwoWay'
        var.put('replaceTwoWay', PyJsHoisted_replaceTwoWay_)
        @Js
        def PyJsHoisted_prepareSliceForReplace_(slice, PyJsArg_24616c6f6e67_, this, arguments, var=var):
            var = Scope({'slice':slice, '$along':PyJsArg_24616c6f6e67_, 'this':this, 'arguments':arguments}, var)
            var.registers(['slice', 'extra', 'node', '$along', 'i', 'parent'])
            var.put('extra', (var.get('$along').get('depth')-var.get('slice').get('openStart')))
            var.put('parent', var.get('$along').callprop('node', var.get('extra')))
            var.put('node', var.get('parent').callprop('copy', var.get('slice').get('content')))
            #for JS loop
            var.put('i', (var.get('extra')-Js(1.0)))
            while (var.get('i')>=Js(0.0)):
                try:
                    var.put('node', var.get('$along').callprop('node', var.get('i')).callprop('copy', var.get('Fragment').callprop('from', var.get('node'))))
                finally:
                        (var.put('i',Js(var.get('i').to_number())-Js(1))+Js(1))
            PyJs_Object_78_ = Js({'start':var.get('node').callprop('resolveNoCache', (var.get('slice').get('openStart')+var.get('extra'))),'end':var.get('node').callprop('resolveNoCache', ((var.get('node').get('content').get('size')-var.get('slice').get('openEnd'))-var.get('extra')))})
            return PyJs_Object_78_
        PyJsHoisted_prepareSliceForReplace_.func_name = 'prepareSliceForReplace'
        var.put('prepareSliceForReplace', PyJsHoisted_prepareSliceForReplace_)
        @Js
        def PyJsHoisted_wrapMarks_(marks, str, this, arguments, var=var):
            var = Scope({'marks':marks, 'str':str, 'this':this, 'arguments':arguments}, var)
            var.registers(['i', 'marks', 'str'])
            #for JS loop
            var.put('i', (var.get('marks').get('length')-Js(1.0)))
            while (var.get('i')>=Js(0.0)):
                try:
                    var.put('str', (((var.get('marks').get(var.get('i')).get('type').get('name')+Js('('))+var.get('str'))+Js(')')))
                finally:
                        (var.put('i',Js(var.get('i').to_number())-Js(1))+Js(1))
            return var.get('str')
        PyJsHoisted_wrapMarks_.func_name = 'wrapMarks'
        var.put('wrapMarks', PyJsHoisted_wrapMarks_)
        @Js
        def PyJsHoisted_parseExpr_(stream, this, arguments, var=var):
            var = Scope({'stream':stream, 'this':this, 'arguments':arguments}, var)
            var.registers(['exprs', 'stream'])
            var.put('exprs', Js([]))
            while 1:
                var.get('exprs').callprop('push', var.get('parseExprSeq')(var.get('stream')))
                if not var.get('stream').callprop('eat', Js('|')):
                    break
            PyJs_Object_225_ = Js({'type':Js('choice'),'exprs':var.get('exprs')})
            return (var.get('exprs').get('0') if (var.get('exprs').get('length')==Js(1.0)) else PyJs_Object_225_)
        PyJsHoisted_parseExpr_.func_name = 'parseExpr'
        var.put('parseExpr', PyJsHoisted_parseExpr_)
        @Js
        def PyJsHoisted_parseExprSeq_(stream, this, arguments, var=var):
            var = Scope({'stream':stream, 'this':this, 'arguments':arguments}, var)
            var.registers(['exprs', 'stream'])
            var.put('exprs', Js([]))
            while 1:
                var.get('exprs').callprop('push', var.get('parseExprSubscript')(var.get('stream')))
                if not ((var.get('stream').get('next') and (var.get('stream').get('next')!=Js(')'))) and (var.get('stream').get('next')!=Js('|'))):
                    break
            PyJs_Object_226_ = Js({'type':Js('seq'),'exprs':var.get('exprs')})
            return (var.get('exprs').get('0') if (var.get('exprs').get('length')==Js(1.0)) else PyJs_Object_226_)
        PyJsHoisted_parseExprSeq_.func_name = 'parseExprSeq'
        var.put('parseExprSeq', PyJsHoisted_parseExprSeq_)
        @Js
        def PyJsHoisted_parseExprSubscript_(stream, this, arguments, var=var):
            var = Scope({'stream':stream, 'this':this, 'arguments':arguments}, var)
            var.registers(['stream', 'expr'])
            var.put('expr', var.get('parseExprAtom')(var.get('stream')))
            #for JS loop
            
            while 1:
                if var.get('stream').callprop('eat', Js('+')):
                    PyJs_Object_227_ = Js({'type':Js('plus'),'expr':var.get('expr')})
                    var.put('expr', PyJs_Object_227_)
                else:
                    if var.get('stream').callprop('eat', Js('*')):
                        PyJs_Object_228_ = Js({'type':Js('star'),'expr':var.get('expr')})
                        var.put('expr', PyJs_Object_228_)
                    else:
                        if var.get('stream').callprop('eat', Js('?')):
                            PyJs_Object_229_ = Js({'type':Js('opt'),'expr':var.get('expr')})
                            var.put('expr', PyJs_Object_229_)
                        else:
                            if var.get('stream').callprop('eat', Js('{')):
                                var.put('expr', var.get('parseExprRange')(var.get('stream'), var.get('expr')))
                            else:
                                break
            
            return var.get('expr')
        PyJsHoisted_parseExprSubscript_.func_name = 'parseExprSubscript'
        var.put('parseExprSubscript', PyJsHoisted_parseExprSubscript_)
        @Js
        def PyJsHoisted_parseNum_(stream, this, arguments, var=var):
            var = Scope({'stream':stream, 'this':this, 'arguments':arguments}, var)
            var.registers(['stream', 'result'])
            if JsRegExp('/\\D/').callprop('test', var.get('stream').get('next')):
                var.get('stream').callprop('err', ((Js("Expected number, got '")+var.get('stream').get('next'))+Js("'")))
            var.put('result', var.get('Number')(var.get('stream').get('next')))
            (var.get('stream').put('pos',Js(var.get('stream').get('pos').to_number())+Js(1))-Js(1))
            return var.get('result')
        PyJsHoisted_parseNum_.func_name = 'parseNum'
        var.put('parseNum', PyJsHoisted_parseNum_)
        @Js
        def PyJsHoisted_parseExprRange_(stream, expr, this, arguments, var=var):
            var = Scope({'stream':stream, 'expr':expr, 'this':this, 'arguments':arguments}, var)
            var.registers(['max', 'stream', 'min', 'expr'])
            var.put('min', var.get('parseNum')(var.get('stream')))
            var.put('max', var.get('min'))
            if var.get('stream').callprop('eat', Js(',')):
                if (var.get('stream').get('next')!=Js('}')):
                    var.put('max', var.get('parseNum')(var.get('stream')))
                else:
                    var.put('max', (-Js(1.0)))
            if var.get('stream').callprop('eat', Js('}')).neg():
                var.get('stream').callprop('err', Js('Unclosed braced range'))
            PyJs_Object_230_ = Js({'type':Js('range'),'min':var.get('min'),'max':var.get('max'),'expr':var.get('expr')})
            return PyJs_Object_230_
        PyJsHoisted_parseExprRange_.func_name = 'parseExprRange'
        var.put('parseExprRange', PyJsHoisted_parseExprRange_)
        @Js
        def PyJsHoisted_resolveName_(stream, name, this, arguments, var=var):
            var = Scope({'stream':stream, 'name':name, 'this':this, 'arguments':arguments}, var)
            var.registers(['stream', 'result', 'types', 'type', 'type$1', 'name', 'typeName'])
            var.put('types', var.get('stream').get('nodeTypes'))
            var.put('type', var.get('types').get(var.get('name')))
            if var.get('type'):
                return Js([var.get('type')])
            var.put('result', Js([]))
            for PyJsTemp in var.get('types'):
                var.put('typeName', PyJsTemp)
                var.put('type$1', var.get('types').get(var.get('typeName')))
                if (var.get('type$1').get('groups').callprop('indexOf', var.get('name'))>(-Js(1.0))):
                    var.get('result').callprop('push', var.get('type$1'))
            if (var.get('result').get('length')==Js(0.0)):
                var.get('stream').callprop('err', ((Js("No node type or group '")+var.get('name'))+Js("' found")))
            return var.get('result')
        PyJsHoisted_resolveName_.func_name = 'resolveName'
        var.put('resolveName', PyJsHoisted_resolveName_)
        @Js
        def PyJsHoisted_parseExprAtom_(stream, this, arguments, var=var):
            var = Scope({'stream':stream, 'this':this, 'arguments':arguments}, var)
            var.registers(['exprs', 'stream', 'expr'])
            if var.get('stream').callprop('eat', Js('(')):
                var.put('expr', var.get('parseExpr')(var.get('stream')))
                if var.get('stream').callprop('eat', Js(')')).neg():
                    var.get('stream').callprop('err', Js('Missing closing paren'))
                return var.get('expr')
            else:
                if JsRegExp('/\\W/').callprop('test', var.get('stream').get('next')).neg():
                    @Js
                    def PyJs_anonymous_231_(type, this, arguments, var=var):
                        var = Scope({'type':type, 'this':this, 'arguments':arguments}, var)
                        var.registers(['type'])
                        if (var.get('stream').get('inline')==var.get(u"null")):
                            var.get('stream').put('inline', var.get('type').get('isInline'))
                        else:
                            if (var.get('stream').get('inline')!=var.get('type').get('isInline')):
                                var.get('stream').callprop('err', Js('Mixing inline and block content'))
                        PyJs_Object_232_ = Js({'type':Js('name'),'value':var.get('type')})
                        return PyJs_Object_232_
                    PyJs_anonymous_231_._set_name('anonymous')
                    var.put('exprs', var.get('resolveName')(var.get('stream'), var.get('stream').get('next')).callprop('map', PyJs_anonymous_231_))
                    (var.get('stream').put('pos',Js(var.get('stream').get('pos').to_number())+Js(1))-Js(1))
                    PyJs_Object_233_ = Js({'type':Js('choice'),'exprs':var.get('exprs')})
                    return (var.get('exprs').get('0') if (var.get('exprs').get('length')==Js(1.0)) else PyJs_Object_233_)
                else:
                    var.get('stream').callprop('err', ((Js("Unexpected token '")+var.get('stream').get('next'))+Js("'")))
        PyJsHoisted_parseExprAtom_.func_name = 'parseExprAtom'
        var.put('parseExprAtom', PyJsHoisted_parseExprAtom_)
        @Js
        def PyJsHoisted_nfa_(expr, this, arguments, var=var):
            var = Scope({'expr':expr, 'this':this, 'arguments':arguments}, var)
            var.registers(['compile', 'node', 'connect', 'nfa', 'expr', 'edge'])
            @Js
            def PyJsHoisted_node_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                return (var.get('nfa').callprop('push', Js([]))-Js(1.0))
            PyJsHoisted_node_.func_name = 'node'
            var.put('node', PyJsHoisted_node_)
            @Js
            def PyJsHoisted_edge_(PyJsArg_66726f6d_, to, term, this, arguments, var=var):
                var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'term':term, 'this':this, 'arguments':arguments}, var)
                var.registers(['to', 'from', 'term', 'edge'])
                PyJs_Object_234_ = Js({'term':var.get('term'),'to':var.get('to')})
                var.put('edge', PyJs_Object_234_)
                var.get('nfa').get(var.get('from')).callprop('push', var.get('edge'))
                return var.get('edge')
            PyJsHoisted_edge_.func_name = 'edge'
            var.put('edge', PyJsHoisted_edge_)
            @Js
            def PyJsHoisted_connect_(edges, to, this, arguments, var=var):
                var = Scope({'edges':edges, 'to':to, 'this':this, 'arguments':arguments}, var)
                var.registers(['to', 'edges'])
                @Js
                def PyJs_anonymous_235_(edge, this, arguments, var=var):
                    var = Scope({'edge':edge, 'this':this, 'arguments':arguments}, var)
                    var.registers(['edge'])
                    return var.get('edge').put('to', var.get('to'))
                PyJs_anonymous_235_._set_name('anonymous')
                var.get('edges').callprop('forEach', PyJs_anonymous_235_)
            PyJsHoisted_connect_.func_name = 'connect'
            var.put('connect', PyJsHoisted_connect_)
            @Js
            def PyJsHoisted_compile_(expr, PyJsArg_66726f6d_, this, arguments, var=var):
                var = Scope({'expr':expr, 'from':PyJsArg_66726f6d_, 'this':this, 'arguments':arguments}, var)
                var.registers(['next$1', 'loop$1', 'loop', 'i$2', 'next$2', 'cur', 'next', 'i', 'expr', 'from', 'i$1'])
                if (var.get('expr').get('type')==Js('choice')):
                    @Js
                    def PyJs_anonymous_236_(out, expr, this, arguments, var=var):
                        var = Scope({'out':out, 'expr':expr, 'this':this, 'arguments':arguments}, var)
                        var.registers(['expr', 'out'])
                        return var.get('out').callprop('concat', var.get('compile')(var.get('expr'), var.get('from')))
                    PyJs_anonymous_236_._set_name('anonymous')
                    return var.get('expr').get('exprs').callprop('reduce', PyJs_anonymous_236_, Js([]))
                else:
                    if (var.get('expr').get('type')==Js('seq')):
                        #for JS loop
                        var.put('i', Js(0.0))
                        while 1:
                            try:
                                var.put('next', var.get('compile')(var.get('expr').get('exprs').get(var.get('i')), var.get('from')))
                                if (var.get('i')==(var.get('expr').get('exprs').get('length')-Js(1.0))):
                                    return var.get('next')
                                var.get('connect')(var.get('next'), var.put('from', var.get('node')()))
                            finally:
                                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                    else:
                        if (var.get('expr').get('type')==Js('star')):
                            var.put('loop', var.get('node')())
                            var.get('edge')(var.get('from'), var.get('loop'))
                            var.get('connect')(var.get('compile')(var.get('expr').get('expr'), var.get('loop')), var.get('loop'))
                            return Js([var.get('edge')(var.get('loop'))])
                        else:
                            if (var.get('expr').get('type')==Js('plus')):
                                var.put('loop$1', var.get('node')())
                                var.get('connect')(var.get('compile')(var.get('expr').get('expr'), var.get('from')), var.get('loop$1'))
                                var.get('connect')(var.get('compile')(var.get('expr').get('expr'), var.get('loop$1')), var.get('loop$1'))
                                return Js([var.get('edge')(var.get('loop$1'))])
                            else:
                                if (var.get('expr').get('type')==Js('opt')):
                                    return Js([var.get('edge')(var.get('from'))]).callprop('concat', var.get('compile')(var.get('expr').get('expr'), var.get('from')))
                                else:
                                    if (var.get('expr').get('type')==Js('range')):
                                        var.put('cur', var.get('from'))
                                        #for JS loop
                                        var.put('i$1', Js(0.0))
                                        while (var.get('i$1')<var.get('expr').get('min')):
                                            try:
                                                var.put('next$1', var.get('node')())
                                                var.get('connect')(var.get('compile')(var.get('expr').get('expr'), var.get('cur')), var.get('next$1'))
                                                var.put('cur', var.get('next$1'))
                                            finally:
                                                    (var.put('i$1',Js(var.get('i$1').to_number())+Js(1))-Js(1))
                                        if (var.get('expr').get('max')==(-Js(1.0))):
                                            var.get('connect')(var.get('compile')(var.get('expr').get('expr'), var.get('cur')), var.get('cur'))
                                        else:
                                            #for JS loop
                                            var.put('i$2', var.get('expr').get('min'))
                                            while (var.get('i$2')<var.get('expr').get('max')):
                                                try:
                                                    var.put('next$2', var.get('node')())
                                                    var.get('edge')(var.get('cur'), var.get('next$2'))
                                                    var.get('connect')(var.get('compile')(var.get('expr').get('expr'), var.get('cur')), var.get('next$2'))
                                                    var.put('cur', var.get('next$2'))
                                                finally:
                                                        (var.put('i$2',Js(var.get('i$2').to_number())+Js(1))-Js(1))
                                        return Js([var.get('edge')(var.get('cur'))])
                                    else:
                                        if (var.get('expr').get('type')==Js('name')):
                                            return Js([var.get('edge')(var.get('from'), var.get(u"null"), var.get('expr').get('value'))])
            PyJsHoisted_compile_.func_name = 'compile'
            var.put('compile', PyJsHoisted_compile_)
            var.put('nfa', Js([Js([])]))
            var.get('connect')(var.get('compile')(var.get('expr'), Js(0.0)), var.get('node')())
            return var.get('nfa')
            pass
            pass
            pass
            pass
        PyJsHoisted_nfa_.func_name = 'nfa'
        var.put('nfa', PyJsHoisted_nfa_)
        @Js
        def PyJsHoisted_cmp_(a, b, this, arguments, var=var):
            var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
            var.registers(['a', 'b'])
            return (var.get('a')-var.get('b'))
        PyJsHoisted_cmp_.func_name = 'cmp'
        var.put('cmp', PyJsHoisted_cmp_)
        @Js
        def PyJsHoisted_nullFrom_(nfa, node, this, arguments, var=var):
            var = Scope({'nfa':nfa, 'node':node, 'this':this, 'arguments':arguments}, var)
            var.registers(['nfa', 'scan', 'result', 'node'])
            @Js
            def PyJsHoisted_scan_(node, this, arguments, var=var):
                var = Scope({'node':node, 'this':this, 'arguments':arguments}, var)
                var.registers(['node', 'ref', 'i', 'term', 'edges', 'to'])
                var.put('edges', var.get('nfa').get(var.get('node')))
                if ((var.get('edges').get('length')==Js(1.0)) and var.get('edges').get('0').get('term').neg()):
                    return var.get('scan')(var.get('edges').get('0').get('to'))
                var.get('result').callprop('push', var.get('node'))
                #for JS loop
                var.put('i', Js(0.0))
                while (var.get('i')<var.get('edges').get('length')):
                    try:
                        var.put('ref', var.get('edges').get(var.get('i')))
                        var.put('term', var.get('ref').get('term'))
                        var.put('to', var.get('ref').get('to'))
                        if (var.get('term').neg() and (var.get('result').callprop('indexOf', var.get('to'))==(-Js(1.0)))):
                            var.get('scan')(var.get('to'))
                    finally:
                            (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            PyJsHoisted_scan_.func_name = 'scan'
            var.put('scan', PyJsHoisted_scan_)
            var.put('result', Js([]))
            var.get('scan')(var.get('node'))
            return var.get('result').callprop('sort', var.get('cmp'))
            pass
        PyJsHoisted_nullFrom_.func_name = 'nullFrom'
        var.put('nullFrom', PyJsHoisted_nullFrom_)
        @Js
        def PyJsHoisted_dfa_(nfa, this, arguments, var=var):
            var = Scope({'nfa':nfa, 'this':this, 'arguments':arguments}, var)
            var.registers(['labeled', 'explore', 'nfa'])
            @Js
            def PyJsHoisted_explore_(states, this, arguments, var=var):
                var = Scope({'states':states, 'this':this, 'arguments':arguments}, var)
                var.registers(['out', 'i', 'states', 'state', 'states$1'])
                var.put('out', Js([]))
                @Js
                def PyJs_anonymous_237_(node, this, arguments, var=var):
                    var = Scope({'node':node, 'this':this, 'arguments':arguments}, var)
                    var.registers(['node'])
                    @Js
                    def PyJs_anonymous_238_(ref, this, arguments, var=var):
                        var = Scope({'ref':ref, 'this':this, 'arguments':arguments}, var)
                        var.registers(['known', 'ref', 'term', 'set', 'to'])
                        var.put('term', var.get('ref').get('term'))
                        var.put('to', var.get('ref').get('to'))
                        if var.get('term').neg():
                            return var.get('undefined')
                        var.put('known', var.get('out').callprop('indexOf', var.get('term')))
                        var.put('set', ((var.get('known')>(-Js(1.0))) and var.get('out').get((var.get('known')+Js(1.0)))))
                        @Js
                        def PyJs_anonymous_239_(node, this, arguments, var=var):
                            var = Scope({'node':node, 'this':this, 'arguments':arguments}, var)
                            var.registers(['node'])
                            if var.get('set').neg():
                                var.get('out').callprop('push', var.get('term'), var.put('set', Js([])))
                            if (var.get('set').callprop('indexOf', var.get('node'))==(-Js(1.0))):
                                var.get('set').callprop('push', var.get('node'))
                        PyJs_anonymous_239_._set_name('anonymous')
                        var.get('nullFrom')(var.get('nfa'), var.get('to')).callprop('forEach', PyJs_anonymous_239_)
                    PyJs_anonymous_238_._set_name('anonymous')
                    var.get('nfa').get(var.get('node')).callprop('forEach', PyJs_anonymous_238_)
                PyJs_anonymous_237_._set_name('anonymous')
                var.get('states').callprop('forEach', PyJs_anonymous_237_)
                var.put('state', var.get('labeled').put(var.get('states').callprop('join', Js(',')), var.get('ContentMatch').create((var.get('states').callprop('indexOf', (var.get('nfa').get('length')-Js(1.0)))>(-Js(1.0))))))
                #for JS loop
                var.put('i', Js(0.0))
                while (var.get('i')<var.get('out').get('length')):
                    try:
                        var.put('states$1', var.get('out').get((var.get('i')+Js(1.0))).callprop('sort', var.get('cmp')))
                        var.get('state').get('next').callprop('push', var.get('out').get(var.get('i')), (var.get('labeled').get(var.get('states$1').callprop('join', Js(','))) or var.get('explore')(var.get('states$1'))))
                    finally:
                            var.put('i', Js(2.0), '+')
                return var.get('state')
            PyJsHoisted_explore_.func_name = 'explore'
            var.put('explore', PyJsHoisted_explore_)
            var.put('labeled', var.get('Object').callprop('create', var.get(u"null")))
            return var.get('explore')(var.get('nullFrom')(var.get('nfa'), Js(0.0)))
            pass
        PyJsHoisted_dfa_.func_name = 'dfa'
        var.put('dfa', PyJsHoisted_dfa_)
        @Js
        def PyJsHoisted_checkForDeadEnds_(match, stream, this, arguments, var=var):
            var = Scope({'match':match, 'stream':stream, 'this':this, 'arguments':arguments}, var)
            var.registers(['nodes', 'match', 'stream', 'node', 'j', 'dead', 'i', 'work', 'next', 'state'])
            #for JS loop
            var.put('i', Js(0.0))
            var.put('work', Js([var.get('match')]))
            while (var.get('i')<var.get('work').get('length')):
                try:
                    var.put('state', var.get('work').get(var.get('i')))
                    var.put('dead', var.get('state').get('validEnd').neg())
                    var.put('nodes', Js([]))
                    #for JS loop
                    var.put('j', Js(0.0))
                    while (var.get('j')<var.get('state').get('next').get('length')):
                        try:
                            var.put('node', var.get('state').get('next').get(var.get('j')))
                            var.put('next', var.get('state').get('next').get((var.get('j')+Js(1.0))))
                            var.get('nodes').callprop('push', var.get('node').get('name'))
                            if (var.get('dead') and (var.get('node').get('isText') or var.get('node').callprop('hasRequiredAttrs')).neg()):
                                var.put('dead', Js(False))
                            if (var.get('work').callprop('indexOf', var.get('next'))==(-Js(1.0))):
                                var.get('work').callprop('push', var.get('next'))
                        finally:
                                var.put('j', Js(2.0), '+')
                    if var.get('dead'):
                        var.get('stream').callprop('err', ((Js('Only non-generatable nodes (')+var.get('nodes').callprop('join', Js(', ')))+Js(') in a required position')))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        PyJsHoisted_checkForDeadEnds_.func_name = 'checkForDeadEnds'
        var.put('checkForDeadEnds', PyJsHoisted_checkForDeadEnds_)
        @Js
        def PyJsHoisted_defaultAttrs_(attrs, this, arguments, var=var):
            var = Scope({'attrs':attrs, 'this':this, 'arguments':arguments}, var)
            var.registers(['defaults', 'attrName', 'attr', 'attrs'])
            var.put('defaults', var.get('Object').callprop('create', var.get(u"null")))
            for PyJsTemp in var.get('attrs'):
                var.put('attrName', PyJsTemp)
                var.put('attr', var.get('attrs').get(var.get('attrName')))
                if var.get('attr').get('hasDefault').neg():
                    return var.get(u"null")
                var.get('defaults').put(var.get('attrName'), var.get('attr').get('default'))
            return var.get('defaults')
        PyJsHoisted_defaultAttrs_.func_name = 'defaultAttrs'
        var.put('defaultAttrs', PyJsHoisted_defaultAttrs_)
        @Js
        def PyJsHoisted_computeAttrs_(attrs, value, this, arguments, var=var):
            var = Scope({'attrs':attrs, 'value':value, 'this':this, 'arguments':arguments}, var)
            var.registers(['attr', 'attrs', 'given', 'value', 'name', 'built'])
            var.put('built', var.get('Object').callprop('create', var.get(u"null")))
            for PyJsTemp in var.get('attrs'):
                var.put('name', PyJsTemp)
                var.put('given', (var.get('value') and var.get('value').get(var.get('name'))))
                if PyJsStrictEq(var.get('given'),var.get('undefined')):
                    var.put('attr', var.get('attrs').get(var.get('name')))
                    if var.get('attr').get('hasDefault'):
                        var.put('given', var.get('attr').get('default'))
                    else:
                        PyJsTempException = JsToPyException(var.get('RangeError').create((Js('No value supplied for attribute ')+var.get('name'))))
                        raise PyJsTempException
                var.get('built').put(var.get('name'), var.get('given'))
            return var.get('built')
        PyJsHoisted_computeAttrs_.func_name = 'computeAttrs'
        var.put('computeAttrs', PyJsHoisted_computeAttrs_)
        @Js
        def PyJsHoisted_initAttrs_(attrs, this, arguments, var=var):
            var = Scope({'attrs':attrs, 'this':this, 'arguments':arguments}, var)
            var.registers(['attrs', 'name', 'result'])
            var.put('result', var.get('Object').callprop('create', var.get(u"null")))
            if var.get('attrs'):
                for PyJsTemp in var.get('attrs'):
                    var.put('name', PyJsTemp)
                    var.get('result').put(var.get('name'), var.get('Attribute').create(var.get('attrs').get(var.get('name'))))
            return var.get('result')
        PyJsHoisted_initAttrs_.func_name = 'initAttrs'
        var.put('initAttrs', PyJsHoisted_initAttrs_)
        @Js
        def PyJsHoisted_gatherMarks_(schema, marks, this, arguments, var=var):
            var = Scope({'schema':schema, 'marks':marks, 'this':this, 'arguments':arguments}, var)
            var.registers(['mark', 'schema', 'prop', 'marks', 'found', 'mark$1', 'i', 'ok', 'name'])
            var.put('found', Js([]))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('marks').get('length')):
                try:
                    var.put('name', var.get('marks').get(var.get('i')))
                    var.put('mark', var.get('schema').get('marks').get(var.get('name')))
                    var.put('ok', var.get('mark'))
                    if var.get('mark'):
                        var.get('found').callprop('push', var.get('mark'))
                    else:
                        for PyJsTemp in var.get('schema').get('marks'):
                            var.put('prop', PyJsTemp)
                            var.put('mark$1', var.get('schema').get('marks').get(var.get('prop')))
                            if ((var.get('name')==Js('_')) or (var.get('mark$1').get('spec').get('group') and (var.get('mark$1').get('spec').get('group').callprop('split', Js(' ')).callprop('indexOf', var.get('name'))>(-Js(1.0))))):
                                var.get('found').callprop('push', var.put('ok', var.get('mark$1')))
                    if var.get('ok').neg():
                        PyJsTempException = JsToPyException(var.get('SyntaxError').create(((Js("Unknown mark type: '")+var.get('marks').get(var.get('i')))+Js("'"))))
                        raise PyJsTempException
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return var.get('found')
        PyJsHoisted_gatherMarks_.func_name = 'gatherMarks'
        var.put('gatherMarks', PyJsHoisted_gatherMarks_)
        @Js
        def PyJsHoisted_wsOptionsFor_(preserveWhitespace, this, arguments, var=var):
            var = Scope({'preserveWhitespace':preserveWhitespace, 'this':this, 'arguments':arguments}, var)
            var.registers(['preserveWhitespace'])
            return ((var.get('OPT_PRESERVE_WS') if var.get('preserveWhitespace') else Js(0.0))|(var.get('OPT_PRESERVE_WS_FULL') if PyJsStrictEq(var.get('preserveWhitespace'),Js('full')) else Js(0.0)))
        PyJsHoisted_wsOptionsFor_.func_name = 'wsOptionsFor'
        var.put('wsOptionsFor', PyJsHoisted_wsOptionsFor_)
        @Js
        def PyJsHoisted_normalizeList_(dom, this, arguments, var=var):
            var = Scope({'dom':dom, 'this':this, 'arguments':arguments}, var)
            var.registers(['dom', 'child', 'name', 'prevItem'])
            #for JS loop
            var.put('child', var.get('dom').get('firstChild'))
            var.put('prevItem', var.get(u"null"))
            while var.get('child'):
                try:
                    var.put('name', (var.get('child').get('nodeName').callprop('toLowerCase') if (var.get('child').get('nodeType')==Js(1.0)) else var.get(u"null")))
                    if ((var.get('name') and var.get('listTags').callprop('hasOwnProperty', var.get('name'))) and var.get('prevItem')):
                        var.get('prevItem').callprop('appendChild', var.get('child'))
                        var.put('child', var.get('prevItem'))
                    else:
                        if (var.get('name')==Js('li')):
                            var.put('prevItem', var.get('child'))
                        else:
                            if var.get('name'):
                                var.put('prevItem', var.get(u"null"))
                finally:
                        var.put('child', var.get('child').get('nextSibling'))
        PyJsHoisted_normalizeList_.func_name = 'normalizeList'
        var.put('normalizeList', PyJsHoisted_normalizeList_)
        @Js
        def PyJsHoisted_matches_(dom, selector, this, arguments, var=var):
            var = Scope({'dom':dom, 'selector':selector, 'this':this, 'arguments':arguments}, var)
            var.registers(['dom', 'selector'])
            return (((var.get('dom').get('matches') or var.get('dom').get('msMatchesSelector')) or var.get('dom').get('webkitMatchesSelector')) or var.get('dom').get('mozMatchesSelector')).callprop('call', var.get('dom'), var.get('selector'))
        PyJsHoisted_matches_.func_name = 'matches'
        var.put('matches', PyJsHoisted_matches_)
        @Js
        def PyJsHoisted_parseStyles_(style, this, arguments, var=var):
            var = Scope({'style':style, 'this':this, 'arguments':arguments}, var)
            var.registers(['style', 'result', 'm', 're'])
            var.put('re', JsRegExp('/\\s*([\\w-]+)\\s*:\\s*([^;]+)/g'))
            var.put('result', Js([]))
            while var.put('m', var.get('re').callprop('exec', var.get('style'))):
                var.get('result').callprop('push', var.get('m').get('1'), var.get('m').get('2').callprop('trim'))
            return var.get('result')
        PyJsHoisted_parseStyles_.func_name = 'parseStyles'
        var.put('parseStyles', PyJsHoisted_parseStyles_)
        @Js
        def PyJsHoisted_copy_(obj, this, arguments, var=var):
            var = Scope({'obj':obj, 'this':this, 'arguments':arguments}, var)
            var.registers(['copy', 'prop', 'obj'])
            PyJs_Object_332_ = Js({})
            var.put('copy', PyJs_Object_332_)
            for PyJsTemp in var.get('obj'):
                var.put('prop', PyJsTemp)
                var.get('copy').put(var.get('prop'), var.get('obj').get(var.get('prop')))
            return var.get('copy')
        PyJsHoisted_copy_.func_name = 'copy'
        var.put('copy', PyJsHoisted_copy_)
        @Js
        def PyJsHoisted_gatherToDOM_(obj, this, arguments, var=var):
            var = Scope({'obj':obj, 'this':this, 'arguments':arguments}, var)
            var.registers(['name', 'toDOM', 'result', 'obj'])
            PyJs_Object_354_ = Js({})
            var.put('result', PyJs_Object_354_)
            for PyJsTemp in var.get('obj'):
                var.put('name', PyJsTemp)
                var.put('toDOM', var.get('obj').get(var.get('name')).get('spec').get('toDOM'))
                if var.get('toDOM'):
                    var.get('result').put(var.get('name'), var.get('toDOM'))
            return var.get('result')
        PyJsHoisted_gatherToDOM_.func_name = 'gatherToDOM'
        var.put('gatherToDOM', PyJsHoisted_gatherToDOM_)
        @Js
        def PyJsHoisted_doc_(options, this, arguments, var=var):
            var = Scope({'options':options, 'this':this, 'arguments':arguments}, var)
            var.registers(['options'])
            return (var.get('options').get('document') or var.get('window').get('document'))
        PyJsHoisted_doc_.func_name = 'doc'
        var.put('doc', PyJsHoisted_doc_)
        PyJs_Object_18_ = Js({'value':Js(True)})
        var.get('Object').callprop('defineProperty', var.get('exports'), Js('__esModule'), PyJs_Object_18_)
        pass
        var.put('OrderedMap', var.get('_interopDefault')(var.get('orderedmap')))
        pass
        pass
        @Js
        def PyJs_Fragment_22_(content, size, this, arguments, var=var):
            var = Scope({'content':content, 'size':size, 'this':this, 'arguments':arguments, 'Fragment':PyJs_Fragment_22_}, var)
            var.registers(['size', 'this$1', 'i', 'content'])
            var.put('this$1', var.get(u"this"))
            var.get(u"this").put('content', var.get('content'))
            var.get(u"this").put('size', (var.get('size') or Js(0.0)))
            if (var.get('size')==var.get(u"null")):
                #for JS loop
                var.put('i', Js(0.0))
                while (var.get('i')<var.get('content').get('length')):
                    try:
                        var.get('this$1').put('size', var.get('content').get(var.get('i')).get('nodeSize'), '+')
                    finally:
                            (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        PyJs_Fragment_22_._set_name('Fragment')
        var.put('Fragment', PyJs_Fragment_22_)
        PyJs_Object_24_ = Js({})
        PyJs_Object_25_ = Js({})
        PyJs_Object_26_ = Js({})
        PyJs_Object_23_ = Js({'firstChild':PyJs_Object_24_,'lastChild':PyJs_Object_25_,'childCount':PyJs_Object_26_})
        var.put('prototypeAccessors$1', PyJs_Object_23_)
        @Js
        def PyJs_nodesBetween_27_(PyJsArg_66726f6d_, to, f, nodeStart, parent, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'f':f, 'nodeStart':nodeStart, 'parent':parent, 'this':this, 'arguments':arguments, 'nodesBetween':PyJs_nodesBetween_27_}, var)
            var.registers(['child', 'nodeStart', 'this$1', 'end', 'f', 'i', 'start', 'pos', 'to', 'from', 'parent'])
            var.put('this$1', var.get(u"this"))
            if PyJsStrictEq(var.get('nodeStart'),PyJsComma(Js(0.0), Js(None))):
                var.put('nodeStart', Js(0.0))
            #for JS loop
            var.put('i', Js(0.0))
            var.put('pos', Js(0.0))
            while (var.get('pos')<var.get('to')):
                try:
                    var.put('child', var.get('this$1').get('content').get(var.get('i')))
                    var.put('end', (var.get('pos')+var.get('child').get('nodeSize')))
                    if (((var.get('end')>var.get('from')) and PyJsStrictNeq(var.get('f')(var.get('child'), (var.get('nodeStart')+var.get('pos')), var.get('parent'), var.get('i')),Js(False))) and var.get('child').get('content').get('size')):
                        var.put('start', (var.get('pos')+Js(1.0)))
                        var.get('child').callprop('nodesBetween', var.get('Math').callprop('max', Js(0.0), (var.get('from')-var.get('start'))), var.get('Math').callprop('min', var.get('child').get('content').get('size'), (var.get('to')-var.get('start'))), var.get('f'), (var.get('nodeStart')+var.get('start')))
                    var.put('pos', var.get('end'))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        PyJs_nodesBetween_27_._set_name('nodesBetween')
        var.get('Fragment').get('prototype').put('nodesBetween', PyJs_nodesBetween_27_)
        @Js
        def PyJs_descendants_28_(f, this, arguments, var=var):
            var = Scope({'f':f, 'this':this, 'arguments':arguments, 'descendants':PyJs_descendants_28_}, var)
            var.registers(['f'])
            var.get(u"this").callprop('nodesBetween', Js(0.0), var.get(u"this").get('size'), var.get('f'))
        PyJs_descendants_28_._set_name('descendants')
        var.get('Fragment').get('prototype').put('descendants', PyJs_descendants_28_)
        @Js
        def PyJs_textBetween_29_(PyJsArg_66726f6d_, to, blockSeparator, leafText, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'blockSeparator':blockSeparator, 'leafText':leafText, 'this':this, 'arguments':arguments, 'textBetween':PyJs_textBetween_29_}, var)
            var.registers(['separated', 'text', 'to', 'from', 'leafText', 'blockSeparator'])
            var.put('text', Js(''))
            var.put('separated', Js(True))
            @Js
            def PyJs_anonymous_30_(node, pos, this, arguments, var=var):
                var = Scope({'node':node, 'pos':pos, 'this':this, 'arguments':arguments}, var)
                var.registers(['pos', 'node'])
                if var.get('node').get('isText'):
                    var.put('text', var.get('node').get('text').callprop('slice', (var.get('Math').callprop('max', var.get('from'), var.get('pos'))-var.get('pos')), (var.get('to')-var.get('pos'))), '+')
                    var.put('separated', var.get('blockSeparator').neg())
                else:
                    if (var.get('node').get('isLeaf') and var.get('leafText')):
                        var.put('text', var.get('leafText'), '+')
                        var.put('separated', var.get('blockSeparator').neg())
                    else:
                        if (var.get('separated').neg() and var.get('node').get('isBlock')):
                            var.put('text', var.get('blockSeparator'), '+')
                            var.put('separated', Js(True))
            PyJs_anonymous_30_._set_name('anonymous')
            var.get(u"this").callprop('nodesBetween', var.get('from'), var.get('to'), PyJs_anonymous_30_, Js(0.0))
            return var.get('text')
        PyJs_textBetween_29_._set_name('textBetween')
        var.get('Fragment').get('prototype').put('textBetween', PyJs_textBetween_29_)
        @Js
        def PyJs_append_31_(other, this, arguments, var=var):
            var = Scope({'other':other, 'this':this, 'arguments':arguments, 'append':PyJs_append_31_}, var)
            var.registers(['last', 'other', 'content', 'i', 'first'])
            if var.get('other').get('size').neg():
                return var.get(u"this")
            if var.get(u"this").get('size').neg():
                return var.get('other')
            var.put('last', var.get(u"this").get('lastChild'))
            var.put('first', var.get('other').get('firstChild'))
            var.put('content', var.get(u"this").get('content').callprop('slice'))
            var.put('i', Js(0.0))
            if (var.get('last').get('isText') and var.get('last').callprop('sameMarkup', var.get('first'))):
                var.get('content').put((var.get('content').get('length')-Js(1.0)), var.get('last').callprop('withText', (var.get('last').get('text')+var.get('first').get('text'))))
                var.put('i', Js(1.0))
            #for JS loop
            
            while (var.get('i')<var.get('other').get('content').get('length')):
                try:
                    var.get('content').callprop('push', var.get('other').get('content').get(var.get('i')))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return var.get('Fragment').create(var.get('content'), (var.get(u"this").get('size')+var.get('other').get('size')))
        PyJs_append_31_._set_name('append')
        var.get('Fragment').get('prototype').put('append', PyJs_append_31_)
        @Js
        def PyJs_cut_32_(PyJsArg_66726f6d_, to, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'this':this, 'arguments':arguments, 'cut':PyJs_cut_32_}, var)
            var.registers(['child', 'result', 'this$1', 'end', 'i', 'pos', 'size', 'from', 'to'])
            var.put('this$1', var.get(u"this"))
            if (var.get('to')==var.get(u"null")):
                var.put('to', var.get(u"this").get('size'))
            if ((var.get('from')==Js(0.0)) and (var.get('to')==var.get(u"this").get('size'))):
                return var.get(u"this")
            var.put('result', Js([]))
            var.put('size', Js(0.0))
            if (var.get('to')>var.get('from')):
                #for JS loop
                var.put('i', Js(0.0))
                var.put('pos', Js(0.0))
                while (var.get('pos')<var.get('to')):
                    try:
                        var.put('child', var.get('this$1').get('content').get(var.get('i')))
                        var.put('end', (var.get('pos')+var.get('child').get('nodeSize')))
                        if (var.get('end')>var.get('from')):
                            if ((var.get('pos')<var.get('from')) or (var.get('end')>var.get('to'))):
                                if var.get('child').get('isText'):
                                    var.put('child', var.get('child').callprop('cut', var.get('Math').callprop('max', Js(0.0), (var.get('from')-var.get('pos'))), var.get('Math').callprop('min', var.get('child').get('text').get('length'), (var.get('to')-var.get('pos')))))
                                else:
                                    var.put('child', var.get('child').callprop('cut', var.get('Math').callprop('max', Js(0.0), ((var.get('from')-var.get('pos'))-Js(1.0))), var.get('Math').callprop('min', var.get('child').get('content').get('size'), ((var.get('to')-var.get('pos'))-Js(1.0)))))
                            var.get('result').callprop('push', var.get('child'))
                            var.put('size', var.get('child').get('nodeSize'), '+')
                        var.put('pos', var.get('end'))
                    finally:
                            (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return var.get('Fragment').create(var.get('result'), var.get('size'))
        PyJs_cut_32_._set_name('cut')
        var.get('Fragment').get('prototype').put('cut', PyJs_cut_32_)
        @Js
        def PyJs_cutByIndex_33_(PyJsArg_66726f6d_, to, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'this':this, 'arguments':arguments, 'cutByIndex':PyJs_cutByIndex_33_}, var)
            var.registers(['to', 'from'])
            if (var.get('from')==var.get('to')):
                return var.get('Fragment').get('empty')
            if ((var.get('from')==Js(0.0)) and (var.get('to')==var.get(u"this").get('content').get('length'))):
                return var.get(u"this")
            return var.get('Fragment').create(var.get(u"this").get('content').callprop('slice', var.get('from'), var.get('to')))
        PyJs_cutByIndex_33_._set_name('cutByIndex')
        var.get('Fragment').get('prototype').put('cutByIndex', PyJs_cutByIndex_33_)
        @Js
        def PyJs_replaceChild_34_(index, node, this, arguments, var=var):
            var = Scope({'index':index, 'node':node, 'this':this, 'arguments':arguments, 'replaceChild':PyJs_replaceChild_34_}, var)
            var.registers(['copy', 'node', 'index', 'current', 'size'])
            var.put('current', var.get(u"this").get('content').get(var.get('index')))
            if (var.get('current')==var.get('node')):
                return var.get(u"this")
            var.put('copy', var.get(u"this").get('content').callprop('slice'))
            var.put('size', ((var.get(u"this").get('size')+var.get('node').get('nodeSize'))-var.get('current').get('nodeSize')))
            var.get('copy').put(var.get('index'), var.get('node'))
            return var.get('Fragment').create(var.get('copy'), var.get('size'))
        PyJs_replaceChild_34_._set_name('replaceChild')
        var.get('Fragment').get('prototype').put('replaceChild', PyJs_replaceChild_34_)
        @Js
        def PyJs_addToStart_35_(node, this, arguments, var=var):
            var = Scope({'node':node, 'this':this, 'arguments':arguments, 'addToStart':PyJs_addToStart_35_}, var)
            var.registers(['node'])
            return var.get('Fragment').create(Js([var.get('node')]).callprop('concat', var.get(u"this").get('content')), (var.get(u"this").get('size')+var.get('node').get('nodeSize')))
        PyJs_addToStart_35_._set_name('addToStart')
        var.get('Fragment').get('prototype').put('addToStart', PyJs_addToStart_35_)
        @Js
        def PyJs_addToEnd_36_(node, this, arguments, var=var):
            var = Scope({'node':node, 'this':this, 'arguments':arguments, 'addToEnd':PyJs_addToEnd_36_}, var)
            var.registers(['node'])
            return var.get('Fragment').create(var.get(u"this").get('content').callprop('concat', var.get('node')), (var.get(u"this").get('size')+var.get('node').get('nodeSize')))
        PyJs_addToEnd_36_._set_name('addToEnd')
        var.get('Fragment').get('prototype').put('addToEnd', PyJs_addToEnd_36_)
        @Js
        def PyJs_eq_37_(other, this, arguments, var=var):
            var = Scope({'other':other, 'this':this, 'arguments':arguments, 'eq':PyJs_eq_37_}, var)
            var.registers(['other', 'this$1', 'i'])
            var.put('this$1', var.get(u"this"))
            if (var.get(u"this").get('content').get('length')!=var.get('other').get('content').get('length')):
                return Js(False)
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get(u"this").get('content').get('length')):
                try:
                    if var.get('this$1').get('content').get(var.get('i')).callprop('eq', var.get('other').get('content').get(var.get('i'))).neg():
                        return Js(False)
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return Js(True)
        PyJs_eq_37_._set_name('eq')
        var.get('Fragment').get('prototype').put('eq', PyJs_eq_37_)
        @Js
        def PyJs_anonymous_38_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return (var.get(u"this").get('content').get('0') if var.get(u"this").get('content').get('length') else var.get(u"null"))
        PyJs_anonymous_38_._set_name('anonymous')
        var.get('prototypeAccessors$1').get('firstChild').put('get', PyJs_anonymous_38_)
        @Js
        def PyJs_anonymous_39_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return (var.get(u"this").get('content').get((var.get(u"this").get('content').get('length')-Js(1.0))) if var.get(u"this").get('content').get('length') else var.get(u"null"))
        PyJs_anonymous_39_._set_name('anonymous')
        var.get('prototypeAccessors$1').get('lastChild').put('get', PyJs_anonymous_39_)
        @Js
        def PyJs_anonymous_40_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get('content').get('length')
        PyJs_anonymous_40_._set_name('anonymous')
        var.get('prototypeAccessors$1').get('childCount').put('get', PyJs_anonymous_40_)
        @Js
        def PyJs_child_41_(index, this, arguments, var=var):
            var = Scope({'index':index, 'this':this, 'arguments':arguments, 'child':PyJs_child_41_}, var)
            var.registers(['found', 'index'])
            var.put('found', var.get(u"this").get('content').get(var.get('index')))
            if var.get('found').neg():
                PyJsTempException = JsToPyException(var.get('RangeError').create((((Js('Index ')+var.get('index'))+Js(' out of range for '))+var.get(u"this"))))
                raise PyJsTempException
            return var.get('found')
        PyJs_child_41_._set_name('child')
        var.get('Fragment').get('prototype').put('child', PyJs_child_41_)
        @Js
        def PyJs_maybeChild_42_(index, this, arguments, var=var):
            var = Scope({'index':index, 'this':this, 'arguments':arguments, 'maybeChild':PyJs_maybeChild_42_}, var)
            var.registers(['index'])
            return var.get(u"this").get('content').get(var.get('index'))
        PyJs_maybeChild_42_._set_name('maybeChild')
        var.get('Fragment').get('prototype').put('maybeChild', PyJs_maybeChild_42_)
        @Js
        def PyJs_forEach_43_(f, this, arguments, var=var):
            var = Scope({'f':f, 'this':this, 'arguments':arguments, 'forEach':PyJs_forEach_43_}, var)
            var.registers(['child', 'this$1', 'f', 'p', 'i'])
            var.put('this$1', var.get(u"this"))
            #for JS loop
            var.put('i', Js(0.0))
            var.put('p', Js(0.0))
            while (var.get('i')<var.get(u"this").get('content').get('length')):
                try:
                    var.put('child', var.get('this$1').get('content').get(var.get('i')))
                    var.get('f')(var.get('child'), var.get('p'), var.get('i'))
                    var.put('p', var.get('child').get('nodeSize'), '+')
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        PyJs_forEach_43_._set_name('forEach')
        var.get('Fragment').get('prototype').put('forEach', PyJs_forEach_43_)
        @Js
        def PyJs_InlineNonPyName_44_(other, pos, this, arguments, var=var):
            var = Scope({'other':other, 'pos':pos, 'this':this, 'arguments':arguments, 'findDiffStart$1':PyJs_InlineNonPyName_44_}, var)
            var.registers(['other', 'pos'])
            if PyJsStrictEq(var.get('pos'),PyJsComma(Js(0.0), Js(None))):
                var.put('pos', Js(0.0))
            return var.get('findDiffStart')(var.get(u"this"), var.get('other'), var.get('pos'))
        PyJs_InlineNonPyName_44_._set_name('findDiffStart$1')
        var.get('Fragment').get('prototype').put('findDiffStart', PyJs_InlineNonPyName_44_)
        @Js
        def PyJs_InlineNonPyName_45_(other, pos, otherPos, this, arguments, var=var):
            var = Scope({'other':other, 'pos':pos, 'otherPos':otherPos, 'this':this, 'arguments':arguments, 'findDiffEnd$1':PyJs_InlineNonPyName_45_}, var)
            var.registers(['otherPos', 'other', 'pos'])
            if PyJsStrictEq(var.get('pos'),PyJsComma(Js(0.0), Js(None))):
                var.put('pos', var.get(u"this").get('size'))
            if PyJsStrictEq(var.get('otherPos'),PyJsComma(Js(0.0), Js(None))):
                var.put('otherPos', var.get('other').get('size'))
            return var.get('findDiffEnd')(var.get(u"this"), var.get('other'), var.get('pos'), var.get('otherPos'))
        PyJs_InlineNonPyName_45_._set_name('findDiffEnd$1')
        var.get('Fragment').get('prototype').put('findDiffEnd', PyJs_InlineNonPyName_45_)
        @Js
        def PyJs_findIndex_46_(pos, round, this, arguments, var=var):
            var = Scope({'pos':pos, 'round':round, 'this':this, 'arguments':arguments, 'findIndex':PyJs_findIndex_46_}, var)
            var.registers(['this$1', 'end', 'cur', 'i', 'round', 'pos', 'curPos'])
            var.put('this$1', var.get(u"this"))
            if PyJsStrictEq(var.get('round'),PyJsComma(Js(0.0), Js(None))):
                var.put('round', (-Js(1.0)))
            if (var.get('pos')==Js(0.0)):
                return var.get('retIndex')(Js(0.0), var.get('pos'))
            if (var.get('pos')==var.get(u"this").get('size')):
                return var.get('retIndex')(var.get(u"this").get('content').get('length'), var.get('pos'))
            if ((var.get('pos')>var.get(u"this").get('size')) or (var.get('pos')<Js(0.0))):
                PyJsTempException = JsToPyException(var.get('RangeError').create(((((Js('Position ')+var.get('pos'))+Js(' outside of fragment ('))+var.get(u"this"))+Js(')'))))
                raise PyJsTempException
            #for JS loop
            var.put('i', Js(0.0))
            var.put('curPos', Js(0.0))
            while 1:
                try:
                    var.put('cur', var.get('this$1').callprop('child', var.get('i')))
                    var.put('end', (var.get('curPos')+var.get('cur').get('nodeSize')))
                    if (var.get('end')>=var.get('pos')):
                        if ((var.get('end')==var.get('pos')) or (var.get('round')>Js(0.0))):
                            return var.get('retIndex')((var.get('i')+Js(1.0)), var.get('end'))
                        return var.get('retIndex')(var.get('i'), var.get('curPos'))
                    var.put('curPos', var.get('end'))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        PyJs_findIndex_46_._set_name('findIndex')
        var.get('Fragment').get('prototype').put('findIndex', PyJs_findIndex_46_)
        @Js
        def PyJs_toString_47_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'toString':PyJs_toString_47_}, var)
            var.registers([])
            return ((Js('<')+var.get(u"this").callprop('toStringInner'))+Js('>'))
        PyJs_toString_47_._set_name('toString')
        var.get('Fragment').get('prototype').put('toString', PyJs_toString_47_)
        @Js
        def PyJs_toStringInner_48_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'toStringInner':PyJs_toStringInner_48_}, var)
            var.registers([])
            return var.get(u"this").get('content').callprop('join', Js(', '))
        PyJs_toStringInner_48_._set_name('toStringInner')
        var.get('Fragment').get('prototype').put('toStringInner', PyJs_toStringInner_48_)
        @Js
        def PyJs_toJSON_49_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'toJSON':PyJs_toJSON_49_}, var)
            var.registers([])
            @Js
            def PyJs_anonymous_50_(n, this, arguments, var=var):
                var = Scope({'n':n, 'this':this, 'arguments':arguments}, var)
                var.registers(['n'])
                return var.get('n').callprop('toJSON')
            PyJs_anonymous_50_._set_name('anonymous')
            return (var.get(u"this").get('content').callprop('map', PyJs_anonymous_50_) if var.get(u"this").get('content').get('length') else var.get(u"null"))
        PyJs_toJSON_49_._set_name('toJSON')
        var.get('Fragment').get('prototype').put('toJSON', PyJs_toJSON_49_)
        @Js
        def PyJs_fromJSON_51_(schema, value, this, arguments, var=var):
            var = Scope({'schema':schema, 'value':value, 'this':this, 'arguments':arguments, 'fromJSON':PyJs_fromJSON_51_}, var)
            var.registers(['schema', 'value'])
            if var.get('value').neg():
                return var.get('Fragment').get('empty')
            if var.get('Array').callprop('isArray', var.get('value')).neg():
                PyJsTempException = JsToPyException(var.get('RangeError').create(Js('Invalid input for Fragment.fromJSON')))
                raise PyJsTempException
            return var.get('Fragment').create(var.get('value').callprop('map', var.get('schema').get('nodeFromJSON')))
        PyJs_fromJSON_51_._set_name('fromJSON')
        var.get('Fragment').put('fromJSON', PyJs_fromJSON_51_)
        @Js
        def PyJs_fromArray_52_(array, this, arguments, var=var):
            var = Scope({'array':array, 'this':this, 'arguments':arguments, 'fromArray':PyJs_fromArray_52_}, var)
            var.registers(['joined', 'node', 'i', 'size', 'array'])
            if var.get('array').get('length').neg():
                return var.get('Fragment').get('empty')
            var.put('size', Js(0.0))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('array').get('length')):
                try:
                    var.put('node', var.get('array').get(var.get('i')))
                    var.put('size', var.get('node').get('nodeSize'), '+')
                    if ((var.get('i') and var.get('node').get('isText')) and var.get('array').get((var.get('i')-Js(1.0))).callprop('sameMarkup', var.get('node'))):
                        if var.get('joined').neg():
                            var.put('joined', var.get('array').callprop('slice', Js(0.0), var.get('i')))
                        var.get('joined').put((var.get('joined').get('length')-Js(1.0)), var.get('node').callprop('withText', (var.get('joined').get((var.get('joined').get('length')-Js(1.0))).get('text')+var.get('node').get('text'))))
                    else:
                        if var.get('joined'):
                            var.get('joined').callprop('push', var.get('node'))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return var.get('Fragment').create((var.get('joined') or var.get('array')), var.get('size'))
        PyJs_fromArray_52_._set_name('fromArray')
        var.get('Fragment').put('fromArray', PyJs_fromArray_52_)
        @Js
        def PyJs_InlineNonPyName_53_(nodes, this, arguments, var=var):
            var = Scope({'nodes':nodes, 'this':this, 'arguments':arguments, 'from':PyJs_InlineNonPyName_53_}, var)
            var.registers(['nodes'])
            if var.get('nodes').neg():
                return var.get('Fragment').get('empty')
            if var.get('nodes').instanceof(var.get('Fragment')):
                return var.get('nodes')
            if var.get('Array').callprop('isArray', var.get('nodes')):
                return var.get(u"this").callprop('fromArray', var.get('nodes'))
            return var.get('Fragment').create(Js([var.get('nodes')]), var.get('nodes').get('nodeSize'))
        PyJs_InlineNonPyName_53_._set_name('from')
        var.get('Fragment').put('from', PyJs_InlineNonPyName_53_)
        var.get('Object').callprop('defineProperties', var.get('Fragment').get('prototype'), var.get('prototypeAccessors$1'))
        PyJs_Object_54_ = Js({'index':Js(0.0),'offset':Js(0.0)})
        var.put('found', PyJs_Object_54_)
        pass
        var.get('Fragment').put('empty', var.get('Fragment').create(Js([]), Js(0.0)))
        pass
        @Js
        def PyJs_Mark_55_(type, attrs, this, arguments, var=var):
            var = Scope({'type':type, 'attrs':attrs, 'this':this, 'arguments':arguments, 'Mark':PyJs_Mark_55_}, var)
            var.registers(['attrs', 'type'])
            var.get(u"this").put('type', var.get('type'))
            var.get(u"this").put('attrs', var.get('attrs'))
        PyJs_Mark_55_._set_name('Mark')
        var.put('Mark', PyJs_Mark_55_)
        @Js
        def PyJs_addToSet_56_(set, this, arguments, var=var):
            var = Scope({'set':set, 'this':this, 'arguments':arguments, 'addToSet':PyJs_addToSet_56_}, var)
            var.registers(['copy', 'this$1', 'other', 'placed', 'i', 'set'])
            var.put('this$1', var.get(u"this"))
            var.put('placed', Js(False))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('set').get('length')):
                try:
                    var.put('other', var.get('set').get(var.get('i')))
                    if var.get('this$1').callprop('eq', var.get('other')):
                        return var.get('set')
                    if var.get('this$1').get('type').callprop('excludes', var.get('other').get('type')):
                        if var.get('copy').neg():
                            var.put('copy', var.get('set').callprop('slice', Js(0.0), var.get('i')))
                    else:
                        if var.get('other').get('type').callprop('excludes', var.get('this$1').get('type')):
                            return var.get('set')
                        else:
                            if (var.get('placed').neg() and (var.get('other').get('type').get('rank')>var.get('this$1').get('type').get('rank'))):
                                if var.get('copy').neg():
                                    var.put('copy', var.get('set').callprop('slice', Js(0.0), var.get('i')))
                                var.get('copy').callprop('push', var.get('this$1'))
                                var.put('placed', Js(True))
                            if var.get('copy'):
                                var.get('copy').callprop('push', var.get('other'))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            if var.get('copy').neg():
                var.put('copy', var.get('set').callprop('slice'))
            if var.get('placed').neg():
                var.get('copy').callprop('push', var.get(u"this"))
            return var.get('copy')
        PyJs_addToSet_56_._set_name('addToSet')
        var.get('Mark').get('prototype').put('addToSet', PyJs_addToSet_56_)
        @Js
        def PyJs_removeFromSet_57_(set, this, arguments, var=var):
            var = Scope({'set':set, 'this':this, 'arguments':arguments, 'removeFromSet':PyJs_removeFromSet_57_}, var)
            var.registers(['set', 'this$1', 'i'])
            var.put('this$1', var.get(u"this"))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('set').get('length')):
                try:
                    if var.get('this$1').callprop('eq', var.get('set').get(var.get('i'))):
                        return var.get('set').callprop('slice', Js(0.0), var.get('i')).callprop('concat', var.get('set').callprop('slice', (var.get('i')+Js(1.0))))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return var.get('set')
        PyJs_removeFromSet_57_._set_name('removeFromSet')
        var.get('Mark').get('prototype').put('removeFromSet', PyJs_removeFromSet_57_)
        @Js
        def PyJs_isInSet_58_(set, this, arguments, var=var):
            var = Scope({'set':set, 'this':this, 'arguments':arguments, 'isInSet':PyJs_isInSet_58_}, var)
            var.registers(['set', 'this$1', 'i'])
            var.put('this$1', var.get(u"this"))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('set').get('length')):
                try:
                    if var.get('this$1').callprop('eq', var.get('set').get(var.get('i'))):
                        return Js(True)
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return Js(False)
        PyJs_isInSet_58_._set_name('isInSet')
        var.get('Mark').get('prototype').put('isInSet', PyJs_isInSet_58_)
        @Js
        def PyJs_eq_59_(other, this, arguments, var=var):
            var = Scope({'other':other, 'this':this, 'arguments':arguments, 'eq':PyJs_eq_59_}, var)
            var.registers(['other'])
            return ((var.get(u"this")==var.get('other')) or ((var.get(u"this").get('type')==var.get('other').get('type')) and var.get('compareDeep')(var.get(u"this").get('attrs'), var.get('other').get('attrs'))))
        PyJs_eq_59_._set_name('eq')
        var.get('Mark').get('prototype').put('eq', PyJs_eq_59_)
        @Js
        def PyJs_toJSON_60_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'toJSON':PyJs_toJSON_60_}, var)
            var.registers(['this$1', '_', 'obj'])
            var.put('this$1', var.get(u"this"))
            PyJs_Object_61_ = Js({'type':var.get(u"this").get('type').get('name')})
            var.put('obj', PyJs_Object_61_)
            for PyJsTemp in var.get('this$1').get('attrs'):
                var.put('_', PyJsTemp)
                var.get('obj').put('attrs', var.get('this$1').get('attrs'))
                break
            return var.get('obj')
        PyJs_toJSON_60_._set_name('toJSON')
        var.get('Mark').get('prototype').put('toJSON', PyJs_toJSON_60_)
        @Js
        def PyJs_fromJSON_62_(schema, json, this, arguments, var=var):
            var = Scope({'schema':schema, 'json':json, 'this':this, 'arguments':arguments, 'fromJSON':PyJs_fromJSON_62_}, var)
            var.registers(['schema', 'json', 'type'])
            if var.get('json').neg():
                PyJsTempException = JsToPyException(var.get('RangeError').create(Js('Invalid input for Mark.fromJSON')))
                raise PyJsTempException
            var.put('type', var.get('schema').get('marks').get(var.get('json').get('type')))
            if var.get('type').neg():
                PyJsTempException = JsToPyException(var.get('RangeError').create(((Js('There is no mark type ')+var.get('json').get('type'))+Js(' in this schema'))))
                raise PyJsTempException
            return var.get('type').callprop('create', var.get('json').get('attrs'))
        PyJs_fromJSON_62_._set_name('fromJSON')
        var.get('Mark').put('fromJSON', PyJs_fromJSON_62_)
        @Js
        def PyJs_sameSet_63_(a, b, this, arguments, var=var):
            var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments, 'sameSet':PyJs_sameSet_63_}, var)
            var.registers(['a', 'b', 'i'])
            if (var.get('a')==var.get('b')):
                return Js(True)
            if (var.get('a').get('length')!=var.get('b').get('length')):
                return Js(False)
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('a').get('length')):
                try:
                    if var.get('a').get(var.get('i')).callprop('eq', var.get('b').get(var.get('i'))).neg():
                        return Js(False)
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return Js(True)
        PyJs_sameSet_63_._set_name('sameSet')
        var.get('Mark').put('sameSet', PyJs_sameSet_63_)
        @Js
        def PyJs_setFrom_64_(marks, this, arguments, var=var):
            var = Scope({'marks':marks, 'this':this, 'arguments':arguments, 'setFrom':PyJs_setFrom_64_}, var)
            var.registers(['copy', 'marks'])
            if (var.get('marks').neg() or (var.get('marks').get('length')==Js(0.0))):
                return var.get('Mark').get('none')
            if var.get('marks').instanceof(var.get('Mark')):
                return Js([var.get('marks')])
            var.put('copy', var.get('marks').callprop('slice'))
            @Js
            def PyJs_anonymous_65_(a, b, this, arguments, var=var):
                var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
                var.registers(['a', 'b'])
                return (var.get('a').get('type').get('rank')-var.get('b').get('type').get('rank'))
            PyJs_anonymous_65_._set_name('anonymous')
            var.get('copy').callprop('sort', PyJs_anonymous_65_)
            return var.get('copy')
        PyJs_setFrom_64_._set_name('setFrom')
        var.get('Mark').put('setFrom', PyJs_setFrom_64_)
        var.get('Mark').put('none', Js([]))
        pass
        var.get('ReplaceError').put('prototype', var.get('Object').callprop('create', var.get('Error').get('prototype')))
        var.get('ReplaceError').get('prototype').put('constructor', var.get('ReplaceError'))
        var.get('ReplaceError').get('prototype').put('name', Js('ReplaceError'))
        @Js
        def PyJs_Slice_66_(content, openStart, openEnd, this, arguments, var=var):
            var = Scope({'content':content, 'openStart':openStart, 'openEnd':openEnd, 'this':this, 'arguments':arguments, 'Slice':PyJs_Slice_66_}, var)
            var.registers(['content', 'openStart', 'openEnd'])
            var.get(u"this").put('content', var.get('content'))
            var.get(u"this").put('openStart', var.get('openStart'))
            var.get(u"this").put('openEnd', var.get('openEnd'))
        PyJs_Slice_66_._set_name('Slice')
        var.put('Slice', PyJs_Slice_66_)
        PyJs_Object_68_ = Js({})
        PyJs_Object_67_ = Js({'size':PyJs_Object_68_})
        var.put('prototypeAccessors$2', PyJs_Object_67_)
        @Js
        def PyJs_anonymous_69_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return ((var.get(u"this").get('content').get('size')-var.get(u"this").get('openStart'))-var.get(u"this").get('openEnd'))
        PyJs_anonymous_69_._set_name('anonymous')
        var.get('prototypeAccessors$2').get('size').put('get', PyJs_anonymous_69_)
        @Js
        def PyJs_insertAt_70_(pos, fragment, this, arguments, var=var):
            var = Scope({'pos':pos, 'fragment':fragment, 'this':this, 'arguments':arguments, 'insertAt':PyJs_insertAt_70_}, var)
            var.registers(['content', 'fragment', 'pos'])
            var.put('content', var.get('insertInto')(var.get(u"this").get('content'), (var.get('pos')+var.get(u"this").get('openStart')), var.get('fragment'), var.get(u"null")))
            return (var.get('content') and var.get('Slice').create(var.get('content'), var.get(u"this").get('openStart'), var.get(u"this").get('openEnd')))
        PyJs_insertAt_70_._set_name('insertAt')
        var.get('Slice').get('prototype').put('insertAt', PyJs_insertAt_70_)
        @Js
        def PyJs_removeBetween_71_(PyJsArg_66726f6d_, to, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'this':this, 'arguments':arguments, 'removeBetween':PyJs_removeBetween_71_}, var)
            var.registers(['to', 'from'])
            return var.get('Slice').create(var.get('removeRange')(var.get(u"this").get('content'), (var.get('from')+var.get(u"this").get('openStart')), (var.get('to')+var.get(u"this").get('openStart'))), var.get(u"this").get('openStart'), var.get(u"this").get('openEnd'))
        PyJs_removeBetween_71_._set_name('removeBetween')
        var.get('Slice').get('prototype').put('removeBetween', PyJs_removeBetween_71_)
        @Js
        def PyJs_eq_72_(other, this, arguments, var=var):
            var = Scope({'other':other, 'this':this, 'arguments':arguments, 'eq':PyJs_eq_72_}, var)
            var.registers(['other'])
            return ((var.get(u"this").get('content').callprop('eq', var.get('other').get('content')) and (var.get(u"this").get('openStart')==var.get('other').get('openStart'))) and (var.get(u"this").get('openEnd')==var.get('other').get('openEnd')))
        PyJs_eq_72_._set_name('eq')
        var.get('Slice').get('prototype').put('eq', PyJs_eq_72_)
        @Js
        def PyJs_toString_73_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'toString':PyJs_toString_73_}, var)
            var.registers([])
            return (((((var.get(u"this").get('content')+Js('('))+var.get(u"this").get('openStart'))+Js(','))+var.get(u"this").get('openEnd'))+Js(')'))
        PyJs_toString_73_._set_name('toString')
        var.get('Slice').get('prototype').put('toString', PyJs_toString_73_)
        @Js
        def PyJs_toJSON_74_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'toJSON':PyJs_toJSON_74_}, var)
            var.registers(['json'])
            if var.get(u"this").get('content').get('size').neg():
                return var.get(u"null")
            PyJs_Object_75_ = Js({'content':var.get(u"this").get('content').callprop('toJSON')})
            var.put('json', PyJs_Object_75_)
            if (var.get(u"this").get('openStart')>Js(0.0)):
                var.get('json').put('openStart', var.get(u"this").get('openStart'))
            if (var.get(u"this").get('openEnd')>Js(0.0)):
                var.get('json').put('openEnd', var.get(u"this").get('openEnd'))
            return var.get('json')
        PyJs_toJSON_74_._set_name('toJSON')
        var.get('Slice').get('prototype').put('toJSON', PyJs_toJSON_74_)
        @Js
        def PyJs_fromJSON_76_(schema, json, this, arguments, var=var):
            var = Scope({'schema':schema, 'json':json, 'this':this, 'arguments':arguments, 'fromJSON':PyJs_fromJSON_76_}, var)
            var.registers(['schema', 'json', 'openStart', 'openEnd'])
            if var.get('json').neg():
                return var.get('Slice').get('empty')
            var.put('openStart', (var.get('json').get('openStart') or Js(0.0)))
            var.put('openEnd', (var.get('json').get('openEnd') or Js(0.0)))
            if ((var.get('openStart',throw=False).typeof()!=Js('number')) or (var.get('openEnd',throw=False).typeof()!=Js('number'))):
                PyJsTempException = JsToPyException(var.get('RangeError').create(Js('Invalid input for Slice.fromJSON')))
                raise PyJsTempException
            return var.get('Slice').create(var.get('Fragment').callprop('fromJSON', var.get('schema'), var.get('json').get('content')), (var.get('json').get('openStart') or Js(0.0)), (var.get('json').get('openEnd') or Js(0.0)))
        PyJs_fromJSON_76_._set_name('fromJSON')
        var.get('Slice').put('fromJSON', PyJs_fromJSON_76_)
        @Js
        def PyJs_maxOpen_77_(fragment, openIsolating, this, arguments, var=var):
            var = Scope({'fragment':fragment, 'openIsolating':openIsolating, 'this':this, 'arguments':arguments, 'maxOpen':PyJs_maxOpen_77_}, var)
            var.registers(['n$1', 'openIsolating', 'openStart', 'n', 'openEnd', 'fragment'])
            if PyJsStrictEq(var.get('openIsolating'),PyJsComma(Js(0.0), Js(None))):
                var.put('openIsolating', Js(True))
            var.put('openStart', Js(0.0))
            var.put('openEnd', Js(0.0))
            #for JS loop
            var.put('n', var.get('fragment').get('firstChild'))
            while ((var.get('n') and var.get('n').get('isLeaf').neg()) and (var.get('openIsolating') or var.get('n').get('type').get('spec').get('isolating').neg())):
                try:
                    (var.put('openStart',Js(var.get('openStart').to_number())+Js(1))-Js(1))
                finally:
                        var.put('n', var.get('n').get('firstChild'))
            #for JS loop
            var.put('n$1', var.get('fragment').get('lastChild'))
            while ((var.get('n$1') and var.get('n$1').get('isLeaf').neg()) and (var.get('openIsolating') or var.get('n$1').get('type').get('spec').get('isolating').neg())):
                try:
                    (var.put('openEnd',Js(var.get('openEnd').to_number())+Js(1))-Js(1))
                finally:
                        var.put('n$1', var.get('n$1').get('lastChild'))
            return var.get('Slice').create(var.get('fragment'), var.get('openStart'), var.get('openEnd'))
        PyJs_maxOpen_77_._set_name('maxOpen')
        var.get('Slice').put('maxOpen', PyJs_maxOpen_77_)
        var.get('Object').callprop('defineProperties', var.get('Slice').get('prototype'), var.get('prototypeAccessors$2'))
        pass
        pass
        var.get('Slice').put('empty', var.get('Slice').create(var.get('Fragment').get('empty'), Js(0.0), Js(0.0)))
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
            var = Scope({'pos':pos, 'path':path, 'parentOffset':parentOffset, 'this':this, 'arguments':arguments, 'ResolvedPos':PyJs_ResolvedPos_79_}, var)
            var.registers(['parentOffset', 'path', 'pos'])
            var.get(u"this").put('pos', var.get('pos'))
            var.get(u"this").put('path', var.get('path'))
            var.get(u"this").put('depth', ((var.get('path').get('length')/Js(3.0))-Js(1.0)))
            var.get(u"this").put('parentOffset', var.get('parentOffset'))
        PyJs_ResolvedPos_79_._set_name('ResolvedPos')
        var.put('ResolvedPos', PyJs_ResolvedPos_79_)
        PyJs_Object_81_ = Js({})
        PyJs_Object_82_ = Js({})
        PyJs_Object_83_ = Js({})
        PyJs_Object_84_ = Js({})
        PyJs_Object_85_ = Js({})
        PyJs_Object_80_ = Js({'parent':PyJs_Object_81_,'doc':PyJs_Object_82_,'textOffset':PyJs_Object_83_,'nodeAfter':PyJs_Object_84_,'nodeBefore':PyJs_Object_85_})
        var.put('prototypeAccessors$3', PyJs_Object_80_)
        @Js
        def PyJs_resolveDepth_86_(val, this, arguments, var=var):
            var = Scope({'val':val, 'this':this, 'arguments':arguments, 'resolveDepth':PyJs_resolveDepth_86_}, var)
            var.registers(['val'])
            if (var.get('val')==var.get(u"null")):
                return var.get(u"this").get('depth')
            if (var.get('val')<Js(0.0)):
                return (var.get(u"this").get('depth')+var.get('val'))
            return var.get('val')
        PyJs_resolveDepth_86_._set_name('resolveDepth')
        var.get('ResolvedPos').get('prototype').put('resolveDepth', PyJs_resolveDepth_86_)
        @Js
        def PyJs_anonymous_87_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").callprop('node', var.get(u"this").get('depth'))
        PyJs_anonymous_87_._set_name('anonymous')
        var.get('prototypeAccessors$3').get('parent').put('get', PyJs_anonymous_87_)
        @Js
        def PyJs_anonymous_88_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").callprop('node', Js(0.0))
        PyJs_anonymous_88_._set_name('anonymous')
        var.get('prototypeAccessors$3').get('doc').put('get', PyJs_anonymous_88_)
        @Js
        def PyJs_node_89_(depth, this, arguments, var=var):
            var = Scope({'depth':depth, 'this':this, 'arguments':arguments, 'node':PyJs_node_89_}, var)
            var.registers(['depth'])
            return var.get(u"this").get('path').get((var.get(u"this").callprop('resolveDepth', var.get('depth'))*Js(3.0)))
        PyJs_node_89_._set_name('node')
        var.get('ResolvedPos').get('prototype').put('node', PyJs_node_89_)
        @Js
        def PyJs_index_90_(depth, this, arguments, var=var):
            var = Scope({'depth':depth, 'this':this, 'arguments':arguments, 'index':PyJs_index_90_}, var)
            var.registers(['depth'])
            return var.get(u"this").get('path').get(((var.get(u"this").callprop('resolveDepth', var.get('depth'))*Js(3.0))+Js(1.0)))
        PyJs_index_90_._set_name('index')
        var.get('ResolvedPos').get('prototype').put('index', PyJs_index_90_)
        @Js
        def PyJs_indexAfter_91_(depth, this, arguments, var=var):
            var = Scope({'depth':depth, 'this':this, 'arguments':arguments, 'indexAfter':PyJs_indexAfter_91_}, var)
            var.registers(['depth'])
            var.put('depth', var.get(u"this").callprop('resolveDepth', var.get('depth')))
            return (var.get(u"this").callprop('index', var.get('depth'))+(Js(0.0) if ((var.get('depth')==var.get(u"this").get('depth')) and var.get(u"this").get('textOffset').neg()) else Js(1.0)))
        PyJs_indexAfter_91_._set_name('indexAfter')
        var.get('ResolvedPos').get('prototype').put('indexAfter', PyJs_indexAfter_91_)
        @Js
        def PyJs_start_92_(depth, this, arguments, var=var):
            var = Scope({'depth':depth, 'this':this, 'arguments':arguments, 'start':PyJs_start_92_}, var)
            var.registers(['depth'])
            var.put('depth', var.get(u"this").callprop('resolveDepth', var.get('depth')))
            return (Js(0.0) if (var.get('depth')==Js(0.0)) else (var.get(u"this").get('path').get(((var.get('depth')*Js(3.0))-Js(1.0)))+Js(1.0)))
        PyJs_start_92_._set_name('start')
        var.get('ResolvedPos').get('prototype').put('start', PyJs_start_92_)
        @Js
        def PyJs_end_93_(depth, this, arguments, var=var):
            var = Scope({'depth':depth, 'this':this, 'arguments':arguments, 'end':PyJs_end_93_}, var)
            var.registers(['depth'])
            var.put('depth', var.get(u"this").callprop('resolveDepth', var.get('depth')))
            return (var.get(u"this").callprop('start', var.get('depth'))+var.get(u"this").callprop('node', var.get('depth')).get('content').get('size'))
        PyJs_end_93_._set_name('end')
        var.get('ResolvedPos').get('prototype').put('end', PyJs_end_93_)
        @Js
        def PyJs_before_94_(depth, this, arguments, var=var):
            var = Scope({'depth':depth, 'this':this, 'arguments':arguments, 'before':PyJs_before_94_}, var)
            var.registers(['depth'])
            var.put('depth', var.get(u"this").callprop('resolveDepth', var.get('depth')))
            if var.get('depth').neg():
                PyJsTempException = JsToPyException(var.get('RangeError').create(Js('There is no position before the top-level node')))
                raise PyJsTempException
            return (var.get(u"this").get('pos') if (var.get('depth')==(var.get(u"this").get('depth')+Js(1.0))) else var.get(u"this").get('path').get(((var.get('depth')*Js(3.0))-Js(1.0))))
        PyJs_before_94_._set_name('before')
        var.get('ResolvedPos').get('prototype').put('before', PyJs_before_94_)
        @Js
        def PyJs_after_95_(depth, this, arguments, var=var):
            var = Scope({'depth':depth, 'this':this, 'arguments':arguments, 'after':PyJs_after_95_}, var)
            var.registers(['depth'])
            var.put('depth', var.get(u"this").callprop('resolveDepth', var.get('depth')))
            if var.get('depth').neg():
                PyJsTempException = JsToPyException(var.get('RangeError').create(Js('There is no position after the top-level node')))
                raise PyJsTempException
            return (var.get(u"this").get('pos') if (var.get('depth')==(var.get(u"this").get('depth')+Js(1.0))) else (var.get(u"this").get('path').get(((var.get('depth')*Js(3.0))-Js(1.0)))+var.get(u"this").get('path').get((var.get('depth')*Js(3.0))).get('nodeSize')))
        PyJs_after_95_._set_name('after')
        var.get('ResolvedPos').get('prototype').put('after', PyJs_after_95_)
        @Js
        def PyJs_anonymous_96_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return (var.get(u"this").get('pos')-var.get(u"this").get('path').get((var.get(u"this").get('path').get('length')-Js(1.0))))
        PyJs_anonymous_96_._set_name('anonymous')
        var.get('prototypeAccessors$3').get('textOffset').put('get', PyJs_anonymous_96_)
        @Js
        def PyJs_anonymous_97_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers(['child', 'parent', 'index', 'dOff'])
            var.put('parent', var.get(u"this").get('parent'))
            var.put('index', var.get(u"this").callprop('index', var.get(u"this").get('depth')))
            if (var.get('index')==var.get('parent').get('childCount')):
                return var.get(u"null")
            var.put('dOff', (var.get(u"this").get('pos')-var.get(u"this").get('path').get((var.get(u"this").get('path').get('length')-Js(1.0)))))
            var.put('child', var.get('parent').callprop('child', var.get('index')))
            return (var.get('parent').callprop('child', var.get('index')).callprop('cut', var.get('dOff')) if var.get('dOff') else var.get('child'))
        PyJs_anonymous_97_._set_name('anonymous')
        var.get('prototypeAccessors$3').get('nodeAfter').put('get', PyJs_anonymous_97_)
        @Js
        def PyJs_anonymous_98_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers(['index', 'dOff'])
            var.put('index', var.get(u"this").callprop('index', var.get(u"this").get('depth')))
            var.put('dOff', (var.get(u"this").get('pos')-var.get(u"this").get('path').get((var.get(u"this").get('path').get('length')-Js(1.0)))))
            if var.get('dOff'):
                return var.get(u"this").get('parent').callprop('child', var.get('index')).callprop('cut', Js(0.0), var.get('dOff'))
            return (var.get(u"null") if (var.get('index')==Js(0.0)) else var.get(u"this").get('parent').callprop('child', (var.get('index')-Js(1.0))))
        PyJs_anonymous_98_._set_name('anonymous')
        var.get('prototypeAccessors$3').get('nodeBefore').put('get', PyJs_anonymous_98_)
        @Js
        def PyJs_marks_99_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'marks':PyJs_marks_99_}, var)
            var.registers(['main', 'other', 'tmp', 'marks', 'index', 'i', 'parent'])
            var.put('parent', var.get(u"this").get('parent'))
            var.put('index', var.get(u"this").callprop('index'))
            if (var.get('parent').get('content').get('size')==Js(0.0)):
                return var.get('Mark').get('none')
            if var.get(u"this").get('textOffset'):
                return var.get('parent').callprop('child', var.get('index')).get('marks')
            var.put('main', var.get('parent').callprop('maybeChild', (var.get('index')-Js(1.0))))
            var.put('other', var.get('parent').callprop('maybeChild', var.get('index')))
            if var.get('main').neg():
                var.put('tmp', var.get('main'))
                var.put('main', var.get('other'))
                var.put('other', var.get('tmp'))
            var.put('marks', var.get('main').get('marks'))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('marks').get('length')):
                try:
                    if (PyJsStrictEq(var.get('marks').get(var.get('i')).get('type').get('spec').get('inclusive'),Js(False)) and (var.get('other').neg() or var.get('marks').get(var.get('i')).callprop('isInSet', var.get('other').get('marks')).neg())):
                        var.put('marks', var.get('marks').get((var.put('i',Js(var.get('i').to_number())-Js(1))+Js(1))).callprop('removeFromSet', var.get('marks')))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return var.get('marks')
        PyJs_marks_99_._set_name('marks')
        var.get('ResolvedPos').get('prototype').put('marks', PyJs_marks_99_)
        @Js
        def PyJs_marksAcross_100_(PyJsArg_24656e64_, this, arguments, var=var):
            var = Scope({'$end':PyJsArg_24656e64_, 'this':this, 'arguments':arguments, 'marksAcross':PyJs_marksAcross_100_}, var)
            var.registers(['marks', 'after', '$end', 'i', 'next'])
            var.put('after', var.get(u"this").get('parent').callprop('maybeChild', var.get(u"this").callprop('index')))
            if (var.get('after').neg() or var.get('after').get('isInline').neg()):
                return var.get(u"null")
            var.put('marks', var.get('after').get('marks'))
            var.put('next', var.get('$end').get('parent').callprop('maybeChild', var.get('$end').callprop('index')))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('marks').get('length')):
                try:
                    if (PyJsStrictEq(var.get('marks').get(var.get('i')).get('type').get('spec').get('inclusive'),Js(False)) and (var.get('next').neg() or var.get('marks').get(var.get('i')).callprop('isInSet', var.get('next').get('marks')).neg())):
                        var.put('marks', var.get('marks').get((var.put('i',Js(var.get('i').to_number())-Js(1))+Js(1))).callprop('removeFromSet', var.get('marks')))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return var.get('marks')
        PyJs_marksAcross_100_._set_name('marksAcross')
        var.get('ResolvedPos').get('prototype').put('marksAcross', PyJs_marksAcross_100_)
        @Js
        def PyJs_sharedDepth_101_(pos, this, arguments, var=var):
            var = Scope({'pos':pos, 'this':this, 'arguments':arguments, 'sharedDepth':PyJs_sharedDepth_101_}, var)
            var.registers(['depth', 'this$1', 'pos'])
            var.put('this$1', var.get(u"this"))
            #for JS loop
            var.put('depth', var.get(u"this").get('depth'))
            while (var.get('depth')>Js(0.0)):
                try:
                    if ((var.get('this$1').callprop('start', var.get('depth'))<=var.get('pos')) and (var.get('this$1').callprop('end', var.get('depth'))>=var.get('pos'))):
                        return var.get('depth')
                finally:
                        (var.put('depth',Js(var.get('depth').to_number())-Js(1))+Js(1))
            return Js(0.0)
        PyJs_sharedDepth_101_._set_name('sharedDepth')
        var.get('ResolvedPos').get('prototype').put('sharedDepth', PyJs_sharedDepth_101_)
        @Js
        def PyJs_blockRange_102_(other, pred, this, arguments, var=var):
            var = Scope({'other':other, 'pred':pred, 'this':this, 'arguments':arguments, 'blockRange':PyJs_blockRange_102_}, var)
            var.registers(['pred', 'd', 'this$1', 'other'])
            var.put('this$1', var.get(u"this"))
            if PyJsStrictEq(var.get('other'),PyJsComma(Js(0.0), Js(None))):
                var.put('other', var.get(u"this"))
            if (var.get('other').get('pos')<var.get(u"this").get('pos')):
                return var.get('other').callprop('blockRange', var.get(u"this"))
            #for JS loop
            var.put('d', (var.get(u"this").get('depth')-(Js(1.0) if (var.get(u"this").get('parent').get('inlineContent') or (var.get(u"this").get('pos')==var.get('other').get('pos'))) else Js(0.0))))
            while (var.get('d')>=Js(0.0)):
                try:
                    if ((var.get('other').get('pos')<=var.get('this$1').callprop('end', var.get('d'))) and (var.get('pred').neg() or var.get('pred')(var.get('this$1').callprop('node', var.get('d'))))):
                        return var.get('NodeRange').create(var.get('this$1'), var.get('other'), var.get('d'))
                finally:
                        (var.put('d',Js(var.get('d').to_number())-Js(1))+Js(1))
        PyJs_blockRange_102_._set_name('blockRange')
        var.get('ResolvedPos').get('prototype').put('blockRange', PyJs_blockRange_102_)
        @Js
        def PyJs_sameParent_103_(other, this, arguments, var=var):
            var = Scope({'other':other, 'this':this, 'arguments':arguments, 'sameParent':PyJs_sameParent_103_}, var)
            var.registers(['other'])
            return ((var.get(u"this").get('pos')-var.get(u"this").get('parentOffset'))==(var.get('other').get('pos')-var.get('other').get('parentOffset')))
        PyJs_sameParent_103_._set_name('sameParent')
        var.get('ResolvedPos').get('prototype').put('sameParent', PyJs_sameParent_103_)
        @Js
        def PyJs_max_104_(other, this, arguments, var=var):
            var = Scope({'other':other, 'this':this, 'arguments':arguments, 'max':PyJs_max_104_}, var)
            var.registers(['other'])
            return (var.get('other') if (var.get('other').get('pos')>var.get(u"this").get('pos')) else var.get(u"this"))
        PyJs_max_104_._set_name('max')
        var.get('ResolvedPos').get('prototype').put('max', PyJs_max_104_)
        @Js
        def PyJs_min_105_(other, this, arguments, var=var):
            var = Scope({'other':other, 'this':this, 'arguments':arguments, 'min':PyJs_min_105_}, var)
            var.registers(['other'])
            return (var.get('other') if (var.get('other').get('pos')<var.get(u"this").get('pos')) else var.get(u"this"))
        PyJs_min_105_._set_name('min')
        var.get('ResolvedPos').get('prototype').put('min', PyJs_min_105_)
        @Js
        def PyJs_toString_106_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'toString':PyJs_toString_106_}, var)
            var.registers(['this$1', 'i', 'str'])
            var.put('this$1', var.get(u"this"))
            var.put('str', Js(''))
            #for JS loop
            var.put('i', Js(1.0))
            while (var.get('i')<=var.get(u"this").get('depth')):
                try:
                    var.put('str', ((((Js('/') if var.get('str') else Js(''))+var.get('this$1').callprop('node', var.get('i')).get('type').get('name'))+Js('_'))+var.get('this$1').callprop('index', (var.get('i')-Js(1.0)))), '+')
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return ((var.get('str')+Js(':'))+var.get(u"this").get('parentOffset'))
        PyJs_toString_106_._set_name('toString')
        var.get('ResolvedPos').get('prototype').put('toString', PyJs_toString_106_)
        @Js
        def PyJs_resolve_107_(doc, pos, this, arguments, var=var):
            var = Scope({'doc':doc, 'pos':pos, 'this':this, 'arguments':arguments, 'resolve':PyJs_resolve_107_}, var)
            var.registers(['doc', 'node', 'rem', 'offset', 'path', 'ref', 'index', 'start', 'pos', 'parentOffset'])
            if ((var.get('pos')>=Js(0.0)) and (var.get('pos')<=var.get('doc').get('content').get('size'))).neg():
                PyJsTempException = JsToPyException(var.get('RangeError').create(((Js('Position ')+var.get('pos'))+Js(' out of range'))))
                raise PyJsTempException
            var.put('path', Js([]))
            var.put('start', Js(0.0))
            var.put('parentOffset', var.get('pos'))
            #for JS loop
            var.put('node', var.get('doc'))
            while 1:
                var.put('ref', var.get('node').get('content').callprop('findIndex', var.get('parentOffset')))
                var.put('index', var.get('ref').get('index'))
                var.put('offset', var.get('ref').get('offset'))
                var.put('rem', (var.get('parentOffset')-var.get('offset')))
                var.get('path').callprop('push', var.get('node'), var.get('index'), (var.get('start')+var.get('offset')))
                if var.get('rem').neg():
                    break
                var.put('node', var.get('node').callprop('child', var.get('index')))
                if var.get('node').get('isText'):
                    break
                var.put('parentOffset', (var.get('rem')-Js(1.0)))
                var.put('start', (var.get('offset')+Js(1.0)), '+')
            
            return var.get('ResolvedPos').create(var.get('pos'), var.get('path'), var.get('parentOffset'))
        PyJs_resolve_107_._set_name('resolve')
        var.get('ResolvedPos').put('resolve', PyJs_resolve_107_)
        @Js
        def PyJs_resolveCached_108_(doc, pos, this, arguments, var=var):
            var = Scope({'doc':doc, 'pos':pos, 'this':this, 'arguments':arguments, 'resolveCached':PyJs_resolveCached_108_}, var)
            var.registers(['doc', 'result', 'i', 'pos', 'cached'])
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('resolveCache').get('length')):
                try:
                    var.put('cached', var.get('resolveCache').get(var.get('i')))
                    if ((var.get('cached').get('pos')==var.get('pos')) and (var.get('cached').get('doc')==var.get('doc'))):
                        return var.get('cached')
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            var.put('result', var.get('resolveCache').put(var.get('resolveCachePos'), var.get('ResolvedPos').callprop('resolve', var.get('doc'), var.get('pos'))))
            var.put('resolveCachePos', ((var.get('resolveCachePos')+Js(1.0))%var.get('resolveCacheSize')))
            return var.get('result')
        PyJs_resolveCached_108_._set_name('resolveCached')
        var.get('ResolvedPos').put('resolveCached', PyJs_resolveCached_108_)
        var.get('Object').callprop('defineProperties', var.get('ResolvedPos').get('prototype'), var.get('prototypeAccessors$3'))
        var.put('resolveCache', Js([]))
        var.put('resolveCachePos', Js(0.0))
        var.put('resolveCacheSize', Js(12.0))
        @Js
        def PyJs_NodeRange_109_(PyJsArg_2466726f6d_, PyJsArg_24746f_, depth, this, arguments, var=var):
            var = Scope({'$from':PyJsArg_2466726f6d_, '$to':PyJsArg_24746f_, 'depth':depth, 'this':this, 'arguments':arguments, 'NodeRange':PyJs_NodeRange_109_}, var)
            var.registers(['depth', '$to', '$from'])
            var.get(u"this").put('$from', var.get('$from'))
            var.get(u"this").put('$to', var.get('$to'))
            var.get(u"this").put('depth', var.get('depth'))
        PyJs_NodeRange_109_._set_name('NodeRange')
        var.put('NodeRange', PyJs_NodeRange_109_)
        PyJs_Object_111_ = Js({})
        PyJs_Object_112_ = Js({})
        PyJs_Object_113_ = Js({})
        PyJs_Object_114_ = Js({})
        PyJs_Object_115_ = Js({})
        PyJs_Object_110_ = Js({'start':PyJs_Object_111_,'end':PyJs_Object_112_,'parent':PyJs_Object_113_,'startIndex':PyJs_Object_114_,'endIndex':PyJs_Object_115_})
        var.put('prototypeAccessors$1$1', PyJs_Object_110_)
        @Js
        def PyJs_anonymous_116_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get('$from').callprop('before', (var.get(u"this").get('depth')+Js(1.0)))
        PyJs_anonymous_116_._set_name('anonymous')
        var.get('prototypeAccessors$1$1').get('start').put('get', PyJs_anonymous_116_)
        @Js
        def PyJs_anonymous_117_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get('$to').callprop('after', (var.get(u"this").get('depth')+Js(1.0)))
        PyJs_anonymous_117_._set_name('anonymous')
        var.get('prototypeAccessors$1$1').get('end').put('get', PyJs_anonymous_117_)
        @Js
        def PyJs_anonymous_118_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get('$from').callprop('node', var.get(u"this").get('depth'))
        PyJs_anonymous_118_._set_name('anonymous')
        var.get('prototypeAccessors$1$1').get('parent').put('get', PyJs_anonymous_118_)
        @Js
        def PyJs_anonymous_119_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get('$from').callprop('index', var.get(u"this").get('depth'))
        PyJs_anonymous_119_._set_name('anonymous')
        var.get('prototypeAccessors$1$1').get('startIndex').put('get', PyJs_anonymous_119_)
        @Js
        def PyJs_anonymous_120_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get('$to').callprop('indexAfter', var.get(u"this").get('depth'))
        PyJs_anonymous_120_._set_name('anonymous')
        var.get('prototypeAccessors$1$1').get('endIndex').put('get', PyJs_anonymous_120_)
        var.get('Object').callprop('defineProperties', var.get('NodeRange').get('prototype'), var.get('prototypeAccessors$1$1'))
        var.put('emptyAttrs', var.get('Object').callprop('create', var.get(u"null")))
        @Js
        def PyJs_Node_121_(type, attrs, content, marks, this, arguments, var=var):
            var = Scope({'type':type, 'attrs':attrs, 'content':content, 'marks':marks, 'this':this, 'arguments':arguments, 'Node':PyJs_Node_121_}, var)
            var.registers(['marks', 'content', 'attrs', 'type'])
            var.get(u"this").put('type', var.get('type'))
            var.get(u"this").put('attrs', var.get('attrs'))
            var.get(u"this").put('content', (var.get('content') or var.get('Fragment').get('empty')))
            var.get(u"this").put('marks', (var.get('marks') or var.get('Mark').get('none')))
        PyJs_Node_121_._set_name('Node')
        var.put('Node', PyJs_Node_121_)
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
        PyJs_Object_122_ = Js({'nodeSize':PyJs_Object_123_,'childCount':PyJs_Object_124_,'textContent':PyJs_Object_125_,'firstChild':PyJs_Object_126_,'lastChild':PyJs_Object_127_,'isBlock':PyJs_Object_128_,'isTextblock':PyJs_Object_129_,'inlineContent':PyJs_Object_130_,'isInline':PyJs_Object_131_,'isText':PyJs_Object_132_,'isLeaf':PyJs_Object_133_,'isAtom':PyJs_Object_134_})
        var.put('prototypeAccessors', PyJs_Object_122_)
        @Js
        def PyJs_anonymous_135_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return (Js(1.0) if var.get(u"this").get('isLeaf') else (Js(2.0)+var.get(u"this").get('content').get('size')))
        PyJs_anonymous_135_._set_name('anonymous')
        var.get('prototypeAccessors').get('nodeSize').put('get', PyJs_anonymous_135_)
        @Js
        def PyJs_anonymous_136_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get('content').get('childCount')
        PyJs_anonymous_136_._set_name('anonymous')
        var.get('prototypeAccessors').get('childCount').put('get', PyJs_anonymous_136_)
        @Js
        def PyJs_child_137_(index, this, arguments, var=var):
            var = Scope({'index':index, 'this':this, 'arguments':arguments, 'child':PyJs_child_137_}, var)
            var.registers(['index'])
            return var.get(u"this").get('content').callprop('child', var.get('index'))
        PyJs_child_137_._set_name('child')
        var.get('Node').get('prototype').put('child', PyJs_child_137_)
        @Js
        def PyJs_maybeChild_138_(index, this, arguments, var=var):
            var = Scope({'index':index, 'this':this, 'arguments':arguments, 'maybeChild':PyJs_maybeChild_138_}, var)
            var.registers(['index'])
            return var.get(u"this").get('content').callprop('maybeChild', var.get('index'))
        PyJs_maybeChild_138_._set_name('maybeChild')
        var.get('Node').get('prototype').put('maybeChild', PyJs_maybeChild_138_)
        @Js
        def PyJs_forEach_139_(f, this, arguments, var=var):
            var = Scope({'f':f, 'this':this, 'arguments':arguments, 'forEach':PyJs_forEach_139_}, var)
            var.registers(['f'])
            var.get(u"this").get('content').callprop('forEach', var.get('f'))
        PyJs_forEach_139_._set_name('forEach')
        var.get('Node').get('prototype').put('forEach', PyJs_forEach_139_)
        @Js
        def PyJs_nodesBetween_140_(PyJsArg_66726f6d_, to, f, startPos, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'f':f, 'startPos':startPos, 'this':this, 'arguments':arguments, 'nodesBetween':PyJs_nodesBetween_140_}, var)
            var.registers(['to', 'from', 'f', 'startPos'])
            if PyJsStrictEq(var.get('startPos'),PyJsComma(Js(0.0), Js(None))):
                var.put('startPos', Js(0.0))
            var.get(u"this").get('content').callprop('nodesBetween', var.get('from'), var.get('to'), var.get('f'), var.get('startPos'), var.get(u"this"))
        PyJs_nodesBetween_140_._set_name('nodesBetween')
        var.get('Node').get('prototype').put('nodesBetween', PyJs_nodesBetween_140_)
        @Js
        def PyJs_descendants_141_(f, this, arguments, var=var):
            var = Scope({'f':f, 'this':this, 'arguments':arguments, 'descendants':PyJs_descendants_141_}, var)
            var.registers(['f'])
            var.get(u"this").callprop('nodesBetween', Js(0.0), var.get(u"this").get('content').get('size'), var.get('f'))
        PyJs_descendants_141_._set_name('descendants')
        var.get('Node').get('prototype').put('descendants', PyJs_descendants_141_)
        @Js
        def PyJs_anonymous_142_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").callprop('textBetween', Js(0.0), var.get(u"this").get('content').get('size'), Js(''))
        PyJs_anonymous_142_._set_name('anonymous')
        var.get('prototypeAccessors').get('textContent').put('get', PyJs_anonymous_142_)
        @Js
        def PyJs_textBetween_143_(PyJsArg_66726f6d_, to, blockSeparator, leafText, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'blockSeparator':blockSeparator, 'leafText':leafText, 'this':this, 'arguments':arguments, 'textBetween':PyJs_textBetween_143_}, var)
            var.registers(['to', 'from', 'leafText', 'blockSeparator'])
            return var.get(u"this").get('content').callprop('textBetween', var.get('from'), var.get('to'), var.get('blockSeparator'), var.get('leafText'))
        PyJs_textBetween_143_._set_name('textBetween')
        var.get('Node').get('prototype').put('textBetween', PyJs_textBetween_143_)
        @Js
        def PyJs_anonymous_144_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get('content').get('firstChild')
        PyJs_anonymous_144_._set_name('anonymous')
        var.get('prototypeAccessors').get('firstChild').put('get', PyJs_anonymous_144_)
        @Js
        def PyJs_anonymous_145_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get('content').get('lastChild')
        PyJs_anonymous_145_._set_name('anonymous')
        var.get('prototypeAccessors').get('lastChild').put('get', PyJs_anonymous_145_)
        @Js
        def PyJs_eq_146_(other, this, arguments, var=var):
            var = Scope({'other':other, 'this':this, 'arguments':arguments, 'eq':PyJs_eq_146_}, var)
            var.registers(['other'])
            return ((var.get(u"this")==var.get('other')) or (var.get(u"this").callprop('sameMarkup', var.get('other')) and var.get(u"this").get('content').callprop('eq', var.get('other').get('content'))))
        PyJs_eq_146_._set_name('eq')
        var.get('Node').get('prototype').put('eq', PyJs_eq_146_)
        @Js
        def PyJs_sameMarkup_147_(other, this, arguments, var=var):
            var = Scope({'other':other, 'this':this, 'arguments':arguments, 'sameMarkup':PyJs_sameMarkup_147_}, var)
            var.registers(['other'])
            return var.get(u"this").callprop('hasMarkup', var.get('other').get('type'), var.get('other').get('attrs'), var.get('other').get('marks'))
        PyJs_sameMarkup_147_._set_name('sameMarkup')
        var.get('Node').get('prototype').put('sameMarkup', PyJs_sameMarkup_147_)
        @Js
        def PyJs_hasMarkup_148_(type, attrs, marks, this, arguments, var=var):
            var = Scope({'type':type, 'attrs':attrs, 'marks':marks, 'this':this, 'arguments':arguments, 'hasMarkup':PyJs_hasMarkup_148_}, var)
            var.registers(['marks', 'attrs', 'type'])
            return (((var.get(u"this").get('type')==var.get('type')) and var.get('compareDeep')(var.get(u"this").get('attrs'), ((var.get('attrs') or var.get('type').get('defaultAttrs')) or var.get('emptyAttrs')))) and var.get('Mark').callprop('sameSet', var.get(u"this").get('marks'), (var.get('marks') or var.get('Mark').get('none'))))
        PyJs_hasMarkup_148_._set_name('hasMarkup')
        var.get('Node').get('prototype').put('hasMarkup', PyJs_hasMarkup_148_)
        @Js
        def PyJs_copy_149_(content, this, arguments, var=var):
            var = Scope({'content':content, 'this':this, 'arguments':arguments, 'copy':PyJs_copy_149_}, var)
            var.registers(['content'])
            if PyJsStrictEq(var.get('content'),PyJsComma(Js(0.0), Js(None))):
                var.put('content', var.get(u"null"))
            if (var.get('content')==var.get(u"this").get('content')):
                return var.get(u"this")
            return var.get(u"this").get('constructor').create(var.get(u"this").get('type'), var.get(u"this").get('attrs'), var.get('content'), var.get(u"this").get('marks'))
        PyJs_copy_149_._set_name('copy')
        var.get('Node').get('prototype').put('copy', PyJs_copy_149_)
        @Js
        def PyJs_mark_150_(marks, this, arguments, var=var):
            var = Scope({'marks':marks, 'this':this, 'arguments':arguments, 'mark':PyJs_mark_150_}, var)
            var.registers(['marks'])
            return (var.get(u"this") if (var.get('marks')==var.get(u"this").get('marks')) else var.get(u"this").get('constructor').create(var.get(u"this").get('type'), var.get(u"this").get('attrs'), var.get(u"this").get('content'), var.get('marks')))
        PyJs_mark_150_._set_name('mark')
        var.get('Node').get('prototype').put('mark', PyJs_mark_150_)
        @Js
        def PyJs_cut_151_(PyJsArg_66726f6d_, to, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'this':this, 'arguments':arguments, 'cut':PyJs_cut_151_}, var)
            var.registers(['to', 'from'])
            if ((var.get('from')==Js(0.0)) and (var.get('to')==var.get(u"this").get('content').get('size'))):
                return var.get(u"this")
            return var.get(u"this").callprop('copy', var.get(u"this").get('content').callprop('cut', var.get('from'), var.get('to')))
        PyJs_cut_151_._set_name('cut')
        var.get('Node').get('prototype').put('cut', PyJs_cut_151_)
        @Js
        def PyJs_slice_152_(PyJsArg_66726f6d_, to, includeParents, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'includeParents':includeParents, 'this':this, 'arguments':arguments, 'slice':PyJs_slice_152_}, var)
            var.registers(['$to', 'node', '$from', 'includeParents', 'depth', 'content', 'start', 'to', 'from'])
            if PyJsStrictEq(var.get('to'),PyJsComma(Js(0.0), Js(None))):
                var.put('to', var.get(u"this").get('content').get('size'))
            if PyJsStrictEq(var.get('includeParents'),PyJsComma(Js(0.0), Js(None))):
                var.put('includeParents', Js(False))
            if (var.get('from')==var.get('to')):
                return var.get('Slice').get('empty')
            var.put('$from', var.get(u"this").callprop('resolve', var.get('from')))
            var.put('$to', var.get(u"this").callprop('resolve', var.get('to')))
            var.put('depth', (Js(0.0) if var.get('includeParents') else var.get('$from').callprop('sharedDepth', var.get('to'))))
            var.put('start', var.get('$from').callprop('start', var.get('depth')))
            var.put('node', var.get('$from').callprop('node', var.get('depth')))
            var.put('content', var.get('node').get('content').callprop('cut', (var.get('$from').get('pos')-var.get('start')), (var.get('$to').get('pos')-var.get('start'))))
            return var.get('Slice').create(var.get('content'), (var.get('$from').get('depth')-var.get('depth')), (var.get('$to').get('depth')-var.get('depth')))
        PyJs_slice_152_._set_name('slice')
        var.get('Node').get('prototype').put('slice', PyJs_slice_152_)
        @Js
        def PyJs_InlineNonPyName_153_(PyJsArg_66726f6d_, to, slice, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'slice':slice, 'this':this, 'arguments':arguments, 'replace$1':PyJs_InlineNonPyName_153_}, var)
            var.registers(['to', 'from', 'slice'])
            return var.get('replace')(var.get(u"this").callprop('resolve', var.get('from')), var.get(u"this").callprop('resolve', var.get('to')), var.get('slice'))
        PyJs_InlineNonPyName_153_._set_name('replace$1')
        var.get('Node').get('prototype').put('replace', PyJs_InlineNonPyName_153_)
        @Js
        def PyJs_nodeAt_154_(pos, this, arguments, var=var):
            var = Scope({'pos':pos, 'this':this, 'arguments':arguments, 'nodeAt':PyJs_nodeAt_154_}, var)
            var.registers(['node', 'offset', 'ref', 'index', 'pos'])
            #for JS loop
            var.put('node', var.get(u"this"))
            while 1:
                var.put('ref', var.get('node').get('content').callprop('findIndex', var.get('pos')))
                var.put('index', var.get('ref').get('index'))
                var.put('offset', var.get('ref').get('offset'))
                var.put('node', var.get('node').callprop('maybeChild', var.get('index')))
                if var.get('node').neg():
                    return var.get(u"null")
                if ((var.get('offset')==var.get('pos')) or var.get('node').get('isText')):
                    return var.get('node')
                var.put('pos', (var.get('offset')+Js(1.0)), '-')
            
        PyJs_nodeAt_154_._set_name('nodeAt')
        var.get('Node').get('prototype').put('nodeAt', PyJs_nodeAt_154_)
        @Js
        def PyJs_childAfter_155_(pos, this, arguments, var=var):
            var = Scope({'pos':pos, 'this':this, 'arguments':arguments, 'childAfter':PyJs_childAfter_155_}, var)
            var.registers(['ref', 'offset', 'index', 'pos'])
            var.put('ref', var.get(u"this").get('content').callprop('findIndex', var.get('pos')))
            var.put('index', var.get('ref').get('index'))
            var.put('offset', var.get('ref').get('offset'))
            PyJs_Object_156_ = Js({'node':var.get(u"this").get('content').callprop('maybeChild', var.get('index')),'index':var.get('index'),'offset':var.get('offset')})
            return PyJs_Object_156_
        PyJs_childAfter_155_._set_name('childAfter')
        var.get('Node').get('prototype').put('childAfter', PyJs_childAfter_155_)
        @Js
        def PyJs_childBefore_157_(pos, this, arguments, var=var):
            var = Scope({'pos':pos, 'this':this, 'arguments':arguments, 'childBefore':PyJs_childBefore_157_}, var)
            var.registers(['node', 'offset', 'ref', 'index', 'pos'])
            if (var.get('pos')==Js(0.0)):
                PyJs_Object_158_ = Js({'node':var.get(u"null"),'index':Js(0.0),'offset':Js(0.0)})
                return PyJs_Object_158_
            var.put('ref', var.get(u"this").get('content').callprop('findIndex', var.get('pos')))
            var.put('index', var.get('ref').get('index'))
            var.put('offset', var.get('ref').get('offset'))
            if (var.get('offset')<var.get('pos')):
                PyJs_Object_159_ = Js({'node':var.get(u"this").get('content').callprop('child', var.get('index')),'index':var.get('index'),'offset':var.get('offset')})
                return PyJs_Object_159_
            var.put('node', var.get(u"this").get('content').callprop('child', (var.get('index')-Js(1.0))))
            PyJs_Object_160_ = Js({'node':var.get('node'),'index':(var.get('index')-Js(1.0)),'offset':(var.get('offset')-var.get('node').get('nodeSize'))})
            return PyJs_Object_160_
        PyJs_childBefore_157_._set_name('childBefore')
        var.get('Node').get('prototype').put('childBefore', PyJs_childBefore_157_)
        @Js
        def PyJs_resolve_161_(pos, this, arguments, var=var):
            var = Scope({'pos':pos, 'this':this, 'arguments':arguments, 'resolve':PyJs_resolve_161_}, var)
            var.registers(['pos'])
            return var.get('ResolvedPos').callprop('resolveCached', var.get(u"this"), var.get('pos'))
        PyJs_resolve_161_._set_name('resolve')
        var.get('Node').get('prototype').put('resolve', PyJs_resolve_161_)
        @Js
        def PyJs_resolveNoCache_162_(pos, this, arguments, var=var):
            var = Scope({'pos':pos, 'this':this, 'arguments':arguments, 'resolveNoCache':PyJs_resolveNoCache_162_}, var)
            var.registers(['pos'])
            return var.get('ResolvedPos').callprop('resolve', var.get(u"this"), var.get('pos'))
        PyJs_resolveNoCache_162_._set_name('resolveNoCache')
        var.get('Node').get('prototype').put('resolveNoCache', PyJs_resolveNoCache_162_)
        @Js
        def PyJs_rangeHasMark_163_(PyJsArg_66726f6d_, to, type, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'type':type, 'this':this, 'arguments':arguments, 'rangeHasMark':PyJs_rangeHasMark_163_}, var)
            var.registers(['to', 'from', 'found', 'type'])
            var.put('found', Js(False))
            if (var.get('to')>var.get('from')):
                @Js
                def PyJs_anonymous_164_(node, this, arguments, var=var):
                    var = Scope({'node':node, 'this':this, 'arguments':arguments}, var)
                    var.registers(['node'])
                    if var.get('type').callprop('isInSet', var.get('node').get('marks')):
                        var.put('found', Js(True))
                    return var.get('found').neg()
                PyJs_anonymous_164_._set_name('anonymous')
                var.get(u"this").callprop('nodesBetween', var.get('from'), var.get('to'), PyJs_anonymous_164_)
            return var.get('found')
        PyJs_rangeHasMark_163_._set_name('rangeHasMark')
        var.get('Node').get('prototype').put('rangeHasMark', PyJs_rangeHasMark_163_)
        @Js
        def PyJs_anonymous_165_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get('type').get('isBlock')
        PyJs_anonymous_165_._set_name('anonymous')
        var.get('prototypeAccessors').get('isBlock').put('get', PyJs_anonymous_165_)
        @Js
        def PyJs_anonymous_166_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get('type').get('isTextblock')
        PyJs_anonymous_166_._set_name('anonymous')
        var.get('prototypeAccessors').get('isTextblock').put('get', PyJs_anonymous_166_)
        @Js
        def PyJs_anonymous_167_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get('type').get('inlineContent')
        PyJs_anonymous_167_._set_name('anonymous')
        var.get('prototypeAccessors').get('inlineContent').put('get', PyJs_anonymous_167_)
        @Js
        def PyJs_anonymous_168_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get('type').get('isInline')
        PyJs_anonymous_168_._set_name('anonymous')
        var.get('prototypeAccessors').get('isInline').put('get', PyJs_anonymous_168_)
        @Js
        def PyJs_anonymous_169_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get('type').get('isText')
        PyJs_anonymous_169_._set_name('anonymous')
        var.get('prototypeAccessors').get('isText').put('get', PyJs_anonymous_169_)
        @Js
        def PyJs_anonymous_170_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get('type').get('isLeaf')
        PyJs_anonymous_170_._set_name('anonymous')
        var.get('prototypeAccessors').get('isLeaf').put('get', PyJs_anonymous_170_)
        @Js
        def PyJs_anonymous_171_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get('type').get('isAtom')
        PyJs_anonymous_171_._set_name('anonymous')
        var.get('prototypeAccessors').get('isAtom').put('get', PyJs_anonymous_171_)
        @Js
        def PyJs_toString_172_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'toString':PyJs_toString_172_}, var)
            var.registers(['name'])
            if var.get(u"this").get('type').get('spec').get('toDebugString'):
                return var.get(u"this").get('type').get('spec').callprop('toDebugString', var.get(u"this"))
            var.put('name', var.get(u"this").get('type').get('name'))
            if var.get(u"this").get('content').get('size'):
                var.put('name', ((Js('(')+var.get(u"this").get('content').callprop('toStringInner'))+Js(')')), '+')
            return var.get('wrapMarks')(var.get(u"this").get('marks'), var.get('name'))
        PyJs_toString_172_._set_name('toString')
        var.get('Node').get('prototype').put('toString', PyJs_toString_172_)
        @Js
        def PyJs_contentMatchAt_173_(index, this, arguments, var=var):
            var = Scope({'index':index, 'this':this, 'arguments':arguments, 'contentMatchAt':PyJs_contentMatchAt_173_}, var)
            var.registers(['match', 'index'])
            var.put('match', var.get(u"this").get('type').get('contentMatch').callprop('matchFragment', var.get(u"this").get('content'), Js(0.0), var.get('index')))
            if var.get('match').neg():
                PyJsTempException = JsToPyException(var.get('Error').create(Js('Called contentMatchAt on a node with invalid content')))
                raise PyJsTempException
            return var.get('match')
        PyJs_contentMatchAt_173_._set_name('contentMatchAt')
        var.get('Node').get('prototype').put('contentMatchAt', PyJs_contentMatchAt_173_)
        @Js
        def PyJs_canReplace_174_(PyJsArg_66726f6d_, to, replacement, start, end, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'replacement':replacement, 'start':start, 'end':end, 'this':this, 'arguments':arguments, 'canReplace':PyJs_canReplace_174_}, var)
            var.registers(['this$1', 'one', 'end', 'replacement', 'two', 'i', 'start', 'to', 'from'])
            var.put('this$1', var.get(u"this"))
            if PyJsStrictEq(var.get('replacement'),PyJsComma(Js(0.0), Js(None))):
                var.put('replacement', var.get('Fragment').get('empty'))
            if PyJsStrictEq(var.get('start'),PyJsComma(Js(0.0), Js(None))):
                var.put('start', Js(0.0))
            if PyJsStrictEq(var.get('end'),PyJsComma(Js(0.0), Js(None))):
                var.put('end', var.get('replacement').get('childCount'))
            var.put('one', var.get(u"this").callprop('contentMatchAt', var.get('from')).callprop('matchFragment', var.get('replacement'), var.get('start'), var.get('end')))
            var.put('two', (var.get('one') and var.get('one').callprop('matchFragment', var.get(u"this").get('content'), var.get('to'))))
            if (var.get('two').neg() or var.get('two').get('validEnd').neg()):
                return Js(False)
            #for JS loop
            var.put('i', var.get('start'))
            while (var.get('i')<var.get('end')):
                try:
                    if var.get('this$1').get('type').callprop('allowsMarks', var.get('replacement').callprop('child', var.get('i')).get('marks')).neg():
                        return Js(False)
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return Js(True)
        PyJs_canReplace_174_._set_name('canReplace')
        var.get('Node').get('prototype').put('canReplace', PyJs_canReplace_174_)
        @Js
        def PyJs_canReplaceWith_175_(PyJsArg_66726f6d_, to, type, marks, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'type':type, 'marks':marks, 'this':this, 'arguments':arguments, 'canReplaceWith':PyJs_canReplaceWith_175_}, var)
            var.registers(['end', 'marks', 'type', 'start', 'to', 'from'])
            if (var.get('marks') and var.get(u"this").get('type').callprop('allowsMarks', var.get('marks')).neg()):
                return Js(False)
            var.put('start', var.get(u"this").callprop('contentMatchAt', var.get('from')).callprop('matchType', var.get('type')))
            var.put('end', (var.get('start') and var.get('start').callprop('matchFragment', var.get(u"this").get('content'), var.get('to'))))
            return (var.get('end').get('validEnd') if var.get('end') else Js(False))
        PyJs_canReplaceWith_175_._set_name('canReplaceWith')
        var.get('Node').get('prototype').put('canReplaceWith', PyJs_canReplaceWith_175_)
        @Js
        def PyJs_canAppend_176_(other, this, arguments, var=var):
            var = Scope({'other':other, 'this':this, 'arguments':arguments, 'canAppend':PyJs_canAppend_176_}, var)
            var.registers(['other'])
            if var.get('other').get('content').get('size'):
                return var.get(u"this").callprop('canReplace', var.get(u"this").get('childCount'), var.get(u"this").get('childCount'), var.get('other').get('content'))
            else:
                return var.get(u"this").get('type').callprop('compatibleContent', var.get('other').get('type'))
        PyJs_canAppend_176_._set_name('canAppend')
        var.get('Node').get('prototype').put('canAppend', PyJs_canAppend_176_)
        @Js
        def PyJs_defaultContentType_177_(at, this, arguments, var=var):
            var = Scope({'at':at, 'this':this, 'arguments':arguments, 'defaultContentType':PyJs_defaultContentType_177_}, var)
            var.registers(['at'])
            return var.get(u"this").callprop('contentMatchAt', var.get('at')).get('defaultType')
        PyJs_defaultContentType_177_._set_name('defaultContentType')
        var.get('Node').get('prototype').put('defaultContentType', PyJs_defaultContentType_177_)
        @Js
        def PyJs_check_178_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'check':PyJs_check_178_}, var)
            var.registers([])
            if var.get(u"this").get('type').callprop('validContent', var.get(u"this").get('content')).neg():
                PyJsTempException = JsToPyException(var.get('RangeError').create((((Js('Invalid content for node ')+var.get(u"this").get('type').get('name'))+Js(': '))+var.get(u"this").get('content').callprop('toString').callprop('slice', Js(0.0), Js(50.0)))))
                raise PyJsTempException
            @Js
            def PyJs_anonymous_179_(node, this, arguments, var=var):
                var = Scope({'node':node, 'this':this, 'arguments':arguments}, var)
                var.registers(['node'])
                return var.get('node').callprop('check')
            PyJs_anonymous_179_._set_name('anonymous')
            var.get(u"this").get('content').callprop('forEach', PyJs_anonymous_179_)
        PyJs_check_178_._set_name('check')
        var.get('Node').get('prototype').put('check', PyJs_check_178_)
        @Js
        def PyJs_toJSON_180_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'toJSON':PyJs_toJSON_180_}, var)
            var.registers(['this$1', '_', 'obj'])
            var.put('this$1', var.get(u"this"))
            PyJs_Object_181_ = Js({'type':var.get(u"this").get('type').get('name')})
            var.put('obj', PyJs_Object_181_)
            for PyJsTemp in var.get('this$1').get('attrs'):
                var.put('_', PyJsTemp)
                var.get('obj').put('attrs', var.get('this$1').get('attrs'))
                break
            if var.get(u"this").get('content').get('size'):
                var.get('obj').put('content', var.get(u"this").get('content').callprop('toJSON'))
            if var.get(u"this").get('marks').get('length'):
                @Js
                def PyJs_anonymous_182_(n, this, arguments, var=var):
                    var = Scope({'n':n, 'this':this, 'arguments':arguments}, var)
                    var.registers(['n'])
                    return var.get('n').callprop('toJSON')
                PyJs_anonymous_182_._set_name('anonymous')
                var.get('obj').put('marks', var.get(u"this").get('marks').callprop('map', PyJs_anonymous_182_))
            return var.get('obj')
        PyJs_toJSON_180_._set_name('toJSON')
        var.get('Node').get('prototype').put('toJSON', PyJs_toJSON_180_)
        @Js
        def PyJs_fromJSON_183_(schema, json, this, arguments, var=var):
            var = Scope({'schema':schema, 'json':json, 'this':this, 'arguments':arguments, 'fromJSON':PyJs_fromJSON_183_}, var)
            var.registers(['schema', 'content', 'json', 'marks'])
            if var.get('json').neg():
                PyJsTempException = JsToPyException(var.get('RangeError').create(Js('Invalid input for Node.fromJSON')))
                raise PyJsTempException
            var.put('marks', var.get(u"null"))
            if var.get('json').get('marks'):
                if var.get('Array').callprop('isArray', var.get('json').get('marks')).neg():
                    PyJsTempException = JsToPyException(var.get('RangeError').create(Js('Invalid mark data for Node.fromJSON')))
                    raise PyJsTempException
                var.put('marks', var.get('json').get('marks').callprop('map', var.get('schema').get('markFromJSON')))
            if (var.get('json').get('type')==Js('text')):
                if (var.get('json').get('text').typeof()!=Js('string')):
                    PyJsTempException = JsToPyException(var.get('RangeError').create(Js('Invalid text node in JSON')))
                    raise PyJsTempException
                return var.get('schema').callprop('text', var.get('json').get('text'), var.get('marks'))
            var.put('content', var.get('Fragment').callprop('fromJSON', var.get('schema'), var.get('json').get('content')))
            return var.get('schema').callprop('nodeType', var.get('json').get('type')).callprop('create', var.get('json').get('attrs'), var.get('content'), var.get('marks'))
        PyJs_fromJSON_183_._set_name('fromJSON')
        var.get('Node').put('fromJSON', PyJs_fromJSON_183_)
        var.get('Object').callprop('defineProperties', var.get('Node').get('prototype'), var.get('prototypeAccessors'))
        @Js
        def PyJs_anonymous_184_(Node, this, arguments, var=var):
            var = Scope({'Node':Node, 'this':this, 'arguments':arguments}, var)
            var.registers(['prototypeAccessors$1', 'Node', 'TextNode'])
            @Js
            def PyJsHoisted_TextNode_(type, attrs, content, marks, this, arguments, var=var):
                var = Scope({'type':type, 'attrs':attrs, 'content':content, 'marks':marks, 'this':this, 'arguments':arguments}, var)
                var.registers(['marks', 'content', 'attrs', 'type'])
                var.get('Node').callprop('call', var.get(u"this"), var.get('type'), var.get('attrs'), var.get(u"null"), var.get('marks'))
                if var.get('content').neg():
                    PyJsTempException = JsToPyException(var.get('RangeError').create(Js('Empty text nodes are not allowed')))
                    raise PyJsTempException
                var.get(u"this").put('text', var.get('content'))
            PyJsHoisted_TextNode_.func_name = 'TextNode'
            var.put('TextNode', PyJsHoisted_TextNode_)
            pass
            if var.get('Node'):
                var.get('TextNode').put('__proto__', var.get('Node'))
            var.get('TextNode').put('prototype', var.get('Object').callprop('create', (var.get('Node') and var.get('Node').get('prototype'))))
            var.get('TextNode').get('prototype').put('constructor', var.get('TextNode'))
            PyJs_Object_186_ = Js({})
            PyJs_Object_187_ = Js({})
            PyJs_Object_185_ = Js({'textContent':PyJs_Object_186_,'nodeSize':PyJs_Object_187_})
            var.put('prototypeAccessors$1', PyJs_Object_185_)
            @Js
            def PyJs_toString_188_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments, 'toString':PyJs_toString_188_}, var)
                var.registers([])
                if var.get(u"this").get('type').get('spec').get('toDebugString'):
                    return var.get(u"this").get('type').get('spec').callprop('toDebugString', var.get(u"this"))
                return var.get('wrapMarks')(var.get(u"this").get('marks'), var.get('JSON').callprop('stringify', var.get(u"this").get('text')))
            PyJs_toString_188_._set_name('toString')
            var.get('TextNode').get('prototype').put('toString', PyJs_toString_188_)
            @Js
            def PyJs_anonymous_189_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                return var.get(u"this").get('text')
            PyJs_anonymous_189_._set_name('anonymous')
            var.get('prototypeAccessors$1').get('textContent').put('get', PyJs_anonymous_189_)
            @Js
            def PyJs_textBetween_190_(PyJsArg_66726f6d_, to, this, arguments, var=var):
                var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'this':this, 'arguments':arguments, 'textBetween':PyJs_textBetween_190_}, var)
                var.registers(['to', 'from'])
                return var.get(u"this").get('text').callprop('slice', var.get('from'), var.get('to'))
            PyJs_textBetween_190_._set_name('textBetween')
            var.get('TextNode').get('prototype').put('textBetween', PyJs_textBetween_190_)
            @Js
            def PyJs_anonymous_191_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments}, var)
                var.registers([])
                return var.get(u"this").get('text').get('length')
            PyJs_anonymous_191_._set_name('anonymous')
            var.get('prototypeAccessors$1').get('nodeSize').put('get', PyJs_anonymous_191_)
            @Js
            def PyJs_mark_192_(marks, this, arguments, var=var):
                var = Scope({'marks':marks, 'this':this, 'arguments':arguments, 'mark':PyJs_mark_192_}, var)
                var.registers(['marks'])
                return (var.get(u"this") if (var.get('marks')==var.get(u"this").get('marks')) else var.get('TextNode').create(var.get(u"this").get('type'), var.get(u"this").get('attrs'), var.get(u"this").get('text'), var.get('marks')))
            PyJs_mark_192_._set_name('mark')
            var.get('TextNode').get('prototype').put('mark', PyJs_mark_192_)
            @Js
            def PyJs_withText_193_(text, this, arguments, var=var):
                var = Scope({'text':text, 'this':this, 'arguments':arguments, 'withText':PyJs_withText_193_}, var)
                var.registers(['text'])
                if (var.get('text')==var.get(u"this").get('text')):
                    return var.get(u"this")
                return var.get('TextNode').create(var.get(u"this").get('type'), var.get(u"this").get('attrs'), var.get('text'), var.get(u"this").get('marks'))
            PyJs_withText_193_._set_name('withText')
            var.get('TextNode').get('prototype').put('withText', PyJs_withText_193_)
            @Js
            def PyJs_cut_194_(PyJsArg_66726f6d_, to, this, arguments, var=var):
                var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'this':this, 'arguments':arguments, 'cut':PyJs_cut_194_}, var)
                var.registers(['to', 'from'])
                if PyJsStrictEq(var.get('from'),PyJsComma(Js(0.0), Js(None))):
                    var.put('from', Js(0.0))
                if PyJsStrictEq(var.get('to'),PyJsComma(Js(0.0), Js(None))):
                    var.put('to', var.get(u"this").get('text').get('length'))
                if ((var.get('from')==Js(0.0)) and (var.get('to')==var.get(u"this").get('text').get('length'))):
                    return var.get(u"this")
                return var.get(u"this").callprop('withText', var.get(u"this").get('text').callprop('slice', var.get('from'), var.get('to')))
            PyJs_cut_194_._set_name('cut')
            var.get('TextNode').get('prototype').put('cut', PyJs_cut_194_)
            @Js
            def PyJs_eq_195_(other, this, arguments, var=var):
                var = Scope({'other':other, 'this':this, 'arguments':arguments, 'eq':PyJs_eq_195_}, var)
                var.registers(['other'])
                return (var.get(u"this").callprop('sameMarkup', var.get('other')) and (var.get(u"this").get('text')==var.get('other').get('text')))
            PyJs_eq_195_._set_name('eq')
            var.get('TextNode').get('prototype').put('eq', PyJs_eq_195_)
            @Js
            def PyJs_toJSON_196_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments, 'toJSON':PyJs_toJSON_196_}, var)
                var.registers(['base'])
                var.put('base', var.get('Node').get('prototype').get('toJSON').callprop('call', var.get(u"this")))
                var.get('base').put('text', var.get(u"this").get('text'))
                return var.get('base')
            PyJs_toJSON_196_._set_name('toJSON')
            var.get('TextNode').get('prototype').put('toJSON', PyJs_toJSON_196_)
            var.get('Object').callprop('defineProperties', var.get('TextNode').get('prototype'), var.get('prototypeAccessors$1'))
            return var.get('TextNode')
        PyJs_anonymous_184_._set_name('anonymous')
        var.put('TextNode', PyJs_anonymous_184_(var.get('Node')))
        pass
        @Js
        def PyJs_ContentMatch_197_(validEnd, this, arguments, var=var):
            var = Scope({'validEnd':validEnd, 'this':this, 'arguments':arguments, 'ContentMatch':PyJs_ContentMatch_197_}, var)
            var.registers(['validEnd'])
            var.get(u"this").put('validEnd', var.get('validEnd'))
            var.get(u"this").put('next', Js([]))
            var.get(u"this").put('wrapCache', Js([]))
        PyJs_ContentMatch_197_._set_name('ContentMatch')
        var.put('ContentMatch', PyJs_ContentMatch_197_)
        PyJs_Object_199_ = Js({})
        PyJs_Object_200_ = Js({})
        PyJs_Object_201_ = Js({})
        PyJs_Object_198_ = Js({'inlineContent':PyJs_Object_199_,'defaultType':PyJs_Object_200_,'edgeCount':PyJs_Object_201_})
        var.put('prototypeAccessors$5', PyJs_Object_198_)
        @Js
        def PyJs_parse_202_(string, nodeTypes, this, arguments, var=var):
            var = Scope({'string':string, 'nodeTypes':nodeTypes, 'this':this, 'arguments':arguments, 'parse':PyJs_parse_202_}, var)
            var.registers(['match', 'stream', 'nodeTypes', 'string', 'expr'])
            var.put('stream', var.get('TokenStream').create(var.get('string'), var.get('nodeTypes')))
            if (var.get('stream').get('next')==var.get(u"null")):
                return var.get('ContentMatch').get('empty')
            var.put('expr', var.get('parseExpr')(var.get('stream')))
            if var.get('stream').get('next'):
                var.get('stream').callprop('err', Js('Unexpected trailing text'))
            var.put('match', var.get('dfa')(var.get('nfa')(var.get('expr'))))
            var.get('checkForDeadEnds')(var.get('match'), var.get('stream'))
            return var.get('match')
        PyJs_parse_202_._set_name('parse')
        var.get('ContentMatch').put('parse', PyJs_parse_202_)
        @Js
        def PyJs_matchType_203_(type, this, arguments, var=var):
            var = Scope({'type':type, 'this':this, 'arguments':arguments, 'matchType':PyJs_matchType_203_}, var)
            var.registers(['this$1', 'i', 'type'])
            var.put('this$1', var.get(u"this"))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get(u"this").get('next').get('length')):
                try:
                    if (var.get('this$1').get('next').get(var.get('i'))==var.get('type')):
                        return var.get('this$1').get('next').get((var.get('i')+Js(1.0)))
                finally:
                        var.put('i', Js(2.0), '+')
            return var.get(u"null")
        PyJs_matchType_203_._set_name('matchType')
        var.get('ContentMatch').get('prototype').put('matchType', PyJs_matchType_203_)
        @Js
        def PyJs_matchFragment_204_(frag, start, end, this, arguments, var=var):
            var = Scope({'frag':frag, 'start':start, 'end':end, 'this':this, 'arguments':arguments, 'matchFragment':PyJs_matchFragment_204_}, var)
            var.registers(['frag', 'end', 'cur', 'i', 'start'])
            if PyJsStrictEq(var.get('start'),PyJsComma(Js(0.0), Js(None))):
                var.put('start', Js(0.0))
            if PyJsStrictEq(var.get('end'),PyJsComma(Js(0.0), Js(None))):
                var.put('end', var.get('frag').get('childCount'))
            var.put('cur', var.get(u"this"))
            #for JS loop
            var.put('i', var.get('start'))
            while (var.get('cur') and (var.get('i')<var.get('end'))):
                try:
                    var.put('cur', var.get('cur').callprop('matchType', var.get('frag').callprop('child', var.get('i')).get('type')))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return var.get('cur')
        PyJs_matchFragment_204_._set_name('matchFragment')
        var.get('ContentMatch').get('prototype').put('matchFragment', PyJs_matchFragment_204_)
        @Js
        def PyJs_anonymous_205_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers(['first'])
            var.put('first', var.get(u"this").get('next').get('0'))
            return (var.get('first').get('isInline') if var.get('first') else Js(False))
        PyJs_anonymous_205_._set_name('anonymous')
        var.get('prototypeAccessors$5').get('inlineContent').put('get', PyJs_anonymous_205_)
        @Js
        def PyJs_anonymous_206_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers(['this$1', 'i', 'type'])
            var.put('this$1', var.get(u"this"))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get(u"this").get('next').get('length')):
                try:
                    var.put('type', var.get('this$1').get('next').get(var.get('i')))
                    if (var.get('type').get('isText') or var.get('type').callprop('hasRequiredAttrs')).neg():
                        return var.get('type')
                finally:
                        var.put('i', Js(2.0), '+')
        PyJs_anonymous_206_._set_name('anonymous')
        var.get('prototypeAccessors$5').get('defaultType').put('get', PyJs_anonymous_206_)
        @Js
        def PyJs_compatible_207_(other, this, arguments, var=var):
            var = Scope({'other':other, 'this':this, 'arguments':arguments, 'compatible':PyJs_compatible_207_}, var)
            var.registers(['other', 'this$1', 'i', 'j'])
            var.put('this$1', var.get(u"this"))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get(u"this").get('next').get('length')):
                try:
                    #for JS loop
                    var.put('j', Js(0.0))
                    while (var.get('j')<var.get('other').get('next').get('length')):
                        try:
                            if (var.get('this$1').get('next').get(var.get('i'))==var.get('other').get('next').get(var.get('j'))):
                                return Js(True)
                        finally:
                                var.put('j', Js(2.0), '+')
                finally:
                        var.put('i', Js(2.0), '+')
            return Js(False)
        PyJs_compatible_207_._set_name('compatible')
        var.get('ContentMatch').get('prototype').put('compatible', PyJs_compatible_207_)
        @Js
        def PyJs_fillBefore_208_(after, toEnd, startIndex, this, arguments, var=var):
            var = Scope({'after':after, 'toEnd':toEnd, 'startIndex':startIndex, 'this':this, 'arguments':arguments, 'fillBefore':PyJs_fillBefore_208_}, var)
            var.registers(['startIndex', 'search', 'after', 'toEnd', 'seen'])
            @Js
            def PyJsHoisted_search_(match, types, this, arguments, var=var):
                var = Scope({'match':match, 'types':types, 'this':this, 'arguments':arguments}, var)
                var.registers(['match', 'types', 'type', 'finished', 'found', 'i', 'next'])
                var.put('finished', var.get('match').callprop('matchFragment', var.get('after'), var.get('startIndex')))
                if (var.get('finished') and (var.get('toEnd').neg() or var.get('finished').get('validEnd'))):
                    @Js
                    def PyJs_anonymous_209_(tp, this, arguments, var=var):
                        var = Scope({'tp':tp, 'this':this, 'arguments':arguments}, var)
                        var.registers(['tp'])
                        return var.get('tp').callprop('createAndFill')
                    PyJs_anonymous_209_._set_name('anonymous')
                    return var.get('Fragment').callprop('from', var.get('types').callprop('map', PyJs_anonymous_209_))
                #for JS loop
                var.put('i', Js(0.0))
                while (var.get('i')<var.get('match').get('next').get('length')):
                    try:
                        var.put('type', var.get('match').get('next').get(var.get('i')))
                        var.put('next', var.get('match').get('next').get((var.get('i')+Js(1.0))))
                        if ((var.get('type').get('isText') or var.get('type').callprop('hasRequiredAttrs')).neg() and (var.get('seen').callprop('indexOf', var.get('next'))==(-Js(1.0)))):
                            var.get('seen').callprop('push', var.get('next'))
                            var.put('found', var.get('search')(var.get('next'), var.get('types').callprop('concat', var.get('type'))))
                            if var.get('found'):
                                return var.get('found')
                    finally:
                            var.put('i', Js(2.0), '+')
            PyJsHoisted_search_.func_name = 'search'
            var.put('search', PyJsHoisted_search_)
            if PyJsStrictEq(var.get('toEnd'),PyJsComma(Js(0.0), Js(None))):
                var.put('toEnd', Js(False))
            if PyJsStrictEq(var.get('startIndex'),PyJsComma(Js(0.0), Js(None))):
                var.put('startIndex', Js(0.0))
            var.put('seen', Js([var.get(u"this")]))
            pass
            return var.get('search')(var.get(u"this"), Js([]))
        PyJs_fillBefore_208_._set_name('fillBefore')
        var.get('ContentMatch').get('prototype').put('fillBefore', PyJs_fillBefore_208_)
        @Js
        def PyJs_findWrapping_210_(target, this, arguments, var=var):
            var = Scope({'target':target, 'this':this, 'arguments':arguments, 'findWrapping':PyJs_findWrapping_210_}, var)
            var.registers(['computed', 'target', 'this$1', 'i'])
            var.put('this$1', var.get(u"this"))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get(u"this").get('wrapCache').get('length')):
                try:
                    if (var.get('this$1').get('wrapCache').get(var.get('i'))==var.get('target')):
                        return var.get('this$1').get('wrapCache').get((var.get('i')+Js(1.0)))
                finally:
                        var.put('i', Js(2.0), '+')
            var.put('computed', var.get(u"this").callprop('computeWrapping', var.get('target')))
            var.get(u"this").get('wrapCache').callprop('push', var.get('target'), var.get('computed'))
            return var.get('computed')
        PyJs_findWrapping_210_._set_name('findWrapping')
        var.get('ContentMatch').get('prototype').put('findWrapping', PyJs_findWrapping_210_)
        @Js
        def PyJs_computeWrapping_211_(target, this, arguments, var=var):
            var = Scope({'target':target, 'this':this, 'arguments':arguments, 'computeWrapping':PyJs_computeWrapping_211_}, var)
            var.registers(['match', 'active', 'result', 'obj', 'type', 'target', 'current', 'i', 'seen'])
            var.put('seen', var.get('Object').callprop('create', var.get(u"null")))
            PyJs_Object_212_ = Js({'match':var.get(u"this"),'type':var.get(u"null"),'via':var.get(u"null")})
            var.put('active', Js([PyJs_Object_212_]))
            while var.get('active').get('length'):
                var.put('current', var.get('active').callprop('shift'))
                var.put('match', var.get('current').get('match'))
                if var.get('match').callprop('matchType', var.get('target')):
                    var.put('result', Js([]))
                    #for JS loop
                    var.put('obj', var.get('current'))
                    while var.get('obj').get('type'):
                        try:
                            var.get('result').callprop('push', var.get('obj').get('type'))
                        finally:
                                var.put('obj', var.get('obj').get('via'))
                    return var.get('result').callprop('reverse')
                #for JS loop
                var.put('i', Js(0.0))
                while (var.get('i')<var.get('match').get('next').get('length')):
                    try:
                        var.put('type', var.get('match').get('next').get(var.get('i')))
                        if (((var.get('type').get('isLeaf').neg() and var.get('type').callprop('hasRequiredAttrs').neg()) and var.get('seen').contains(var.get('type').get('name')).neg()) and (var.get('current').get('type').neg() or var.get('match').get('next').get((var.get('i')+Js(1.0))).get('validEnd'))):
                            PyJs_Object_213_ = Js({'match':var.get('type').get('contentMatch'),'type':var.get('type'),'via':var.get('current')})
                            var.get('active').callprop('push', PyJs_Object_213_)
                            var.get('seen').put(var.get('type').get('name'), Js(True))
                    finally:
                            var.put('i', Js(2.0), '+')
        PyJs_computeWrapping_211_._set_name('computeWrapping')
        var.get('ContentMatch').get('prototype').put('computeWrapping', PyJs_computeWrapping_211_)
        @Js
        def PyJs_anonymous_214_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return (var.get(u"this").get('next').get('length')>>Js(1.0))
        PyJs_anonymous_214_._set_name('anonymous')
        var.get('prototypeAccessors$5').get('edgeCount').put('get', PyJs_anonymous_214_)
        @Js
        def PyJs_edge_215_(n, this, arguments, var=var):
            var = Scope({'n':n, 'this':this, 'arguments':arguments, 'edge':PyJs_edge_215_}, var)
            var.registers(['i', 'n'])
            var.put('i', (var.get('n')<<Js(1.0)))
            if (var.get('i')>var.get(u"this").get('next').get('length')):
                PyJsTempException = JsToPyException(var.get('RangeError').create(((Js("There's no ")+var.get('n'))+Js('th edge in this content match'))))
                raise PyJsTempException
            PyJs_Object_216_ = Js({'type':var.get(u"this").get('next').get(var.get('i')),'next':var.get(u"this").get('next').get((var.get('i')+Js(1.0)))})
            return PyJs_Object_216_
        PyJs_edge_215_._set_name('edge')
        var.get('ContentMatch').get('prototype').put('edge', PyJs_edge_215_)
        @Js
        def PyJs_toString_217_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'toString':PyJs_toString_217_}, var)
            var.registers(['seen', 'scan'])
            @Js
            def PyJsHoisted_scan_(m, this, arguments, var=var):
                var = Scope({'m':m, 'this':this, 'arguments':arguments}, var)
                var.registers(['i', 'm'])
                var.get('seen').callprop('push', var.get('m'))
                #for JS loop
                var.put('i', Js(1.0))
                while (var.get('i')<var.get('m').get('next').get('length')):
                    try:
                        if (var.get('seen').callprop('indexOf', var.get('m').get('next').get(var.get('i')))==(-Js(1.0))):
                            var.get('scan')(var.get('m').get('next').get(var.get('i')))
                    finally:
                            var.put('i', Js(2.0), '+')
            PyJsHoisted_scan_.func_name = 'scan'
            var.put('scan', PyJsHoisted_scan_)
            var.put('seen', Js([]))
            pass
            var.get('scan')(var.get(u"this"))
            @Js
            def PyJs_anonymous_218_(m, i, this, arguments, var=var):
                var = Scope({'m':m, 'i':i, 'this':this, 'arguments':arguments}, var)
                var.registers(['i$1', 'i', 'm', 'out'])
                var.put('out', ((var.get('i')+(Js('*') if var.get('m').get('validEnd') else Js(' ')))+Js(' ')))
                #for JS loop
                var.put('i$1', Js(0.0))
                while (var.get('i$1')<var.get('m').get('next').get('length')):
                    try:
                        var.put('out', ((((Js(', ') if var.get('i$1') else Js(''))+var.get('m').get('next').get(var.get('i$1')).get('name'))+Js('->'))+var.get('seen').callprop('indexOf', var.get('m').get('next').get((var.get('i$1')+Js(1.0))))), '+')
                    finally:
                            var.put('i$1', Js(2.0), '+')
                return var.get('out')
            PyJs_anonymous_218_._set_name('anonymous')
            return var.get('seen').callprop('map', PyJs_anonymous_218_).callprop('join', Js('\n'))
        PyJs_toString_217_._set_name('toString')
        var.get('ContentMatch').get('prototype').put('toString', PyJs_toString_217_)
        var.get('Object').callprop('defineProperties', var.get('ContentMatch').get('prototype'), var.get('prototypeAccessors$5'))
        var.get('ContentMatch').put('empty', var.get('ContentMatch').create(Js(True)))
        @Js
        def PyJs_TokenStream_219_(string, nodeTypes, this, arguments, var=var):
            var = Scope({'string':string, 'nodeTypes':nodeTypes, 'this':this, 'arguments':arguments, 'TokenStream':PyJs_TokenStream_219_}, var)
            var.registers(['string', 'nodeTypes'])
            var.get(u"this").put('string', var.get('string'))
            var.get(u"this").put('nodeTypes', var.get('nodeTypes'))
            var.get(u"this").put('inline', var.get(u"null"))
            var.get(u"this").put('pos', Js(0.0))
            var.get(u"this").put('tokens', var.get('string').callprop('split', JsRegExp('/\\s*(?=\\b|\\W|$)/')))
            if (var.get(u"this").get('tokens').get((var.get(u"this").get('tokens').get('length')-Js(1.0)))==Js('')):
                var.get(u"this").get('tokens').callprop('pop')
            if (var.get(u"this").get('tokens').get('0')==Js('')):
                var.get(u"this").get('tokens').callprop('unshift')
        PyJs_TokenStream_219_._set_name('TokenStream')
        var.put('TokenStream', PyJs_TokenStream_219_)
        PyJs_Object_221_ = Js({})
        PyJs_Object_220_ = Js({'next':PyJs_Object_221_})
        var.put('prototypeAccessors$1$3', PyJs_Object_220_)
        @Js
        def PyJs_anonymous_222_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get('tokens').get(var.get(u"this").get('pos'))
        PyJs_anonymous_222_._set_name('anonymous')
        var.get('prototypeAccessors$1$3').get('next').put('get', PyJs_anonymous_222_)
        @Js
        def PyJs_eat_223_(tok, this, arguments, var=var):
            var = Scope({'tok':tok, 'this':this, 'arguments':arguments, 'eat':PyJs_eat_223_}, var)
            var.registers(['tok'])
            return ((var.get(u"this").get('next')==var.get('tok')) and ((var.get(u"this").put('pos',Js(var.get(u"this").get('pos').to_number())+Js(1))-Js(1)) or Js(True)))
        PyJs_eat_223_._set_name('eat')
        var.get('TokenStream').get('prototype').put('eat', PyJs_eat_223_)
        @Js
        def PyJs_err_224_(str, this, arguments, var=var):
            var = Scope({'str':str, 'this':this, 'arguments':arguments, 'err':PyJs_err_224_}, var)
            var.registers(['str'])
            PyJsTempException = JsToPyException(var.get('SyntaxError').create((((var.get('str')+Js(" (in content expression '"))+var.get(u"this").get('string'))+Js("')"))))
            raise PyJsTempException
        PyJs_err_224_._set_name('err')
        var.get('TokenStream').get('prototype').put('err', PyJs_err_224_)
        var.get('Object').callprop('defineProperties', var.get('TokenStream').get('prototype'), var.get('prototypeAccessors$1$3'))
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
            var = Scope({'name':name, 'schema':schema, 'spec':spec, 'this':this, 'arguments':arguments, 'NodeType':PyJs_NodeType_240_}, var)
            var.registers(['schema', 'name', 'spec'])
            var.get(u"this").put('name', var.get('name'))
            var.get(u"this").put('schema', var.get('schema'))
            var.get(u"this").put('spec', var.get('spec'))
            var.get(u"this").put('groups', (var.get('spec').get('group').callprop('split', Js(' ')) if var.get('spec').get('group') else Js([])))
            var.get(u"this").put('attrs', var.get('initAttrs')(var.get('spec').get('attrs')))
            var.get(u"this").put('defaultAttrs', var.get('defaultAttrs')(var.get(u"this").get('attrs')))
            var.get(u"this").put('contentMatch', var.get(u"null"))
            var.get(u"this").put('markSet', var.get(u"null"))
            var.get(u"this").put('inlineContent', var.get(u"null"))
            var.get(u"this").put('isBlock', (var.get('spec').get('inline') or (var.get('name')==Js('text'))).neg())
            var.get(u"this").put('isText', (var.get('name')==Js('text')))
        PyJs_NodeType_240_._set_name('NodeType')
        var.put('NodeType', PyJs_NodeType_240_)
        PyJs_Object_242_ = Js({})
        PyJs_Object_243_ = Js({})
        PyJs_Object_244_ = Js({})
        PyJs_Object_245_ = Js({})
        PyJs_Object_241_ = Js({'isInline':PyJs_Object_242_,'isTextblock':PyJs_Object_243_,'isLeaf':PyJs_Object_244_,'isAtom':PyJs_Object_245_})
        var.put('prototypeAccessors$4', PyJs_Object_241_)
        @Js
        def PyJs_anonymous_246_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get('isBlock').neg()
        PyJs_anonymous_246_._set_name('anonymous')
        var.get('prototypeAccessors$4').get('isInline').put('get', PyJs_anonymous_246_)
        @Js
        def PyJs_anonymous_247_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return (var.get(u"this").get('isBlock') and var.get(u"this").get('inlineContent'))
        PyJs_anonymous_247_._set_name('anonymous')
        var.get('prototypeAccessors$4').get('isTextblock').put('get', PyJs_anonymous_247_)
        @Js
        def PyJs_anonymous_248_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return (var.get(u"this").get('contentMatch')==var.get('ContentMatch').get('empty'))
        PyJs_anonymous_248_._set_name('anonymous')
        var.get('prototypeAccessors$4').get('isLeaf').put('get', PyJs_anonymous_248_)
        @Js
        def PyJs_anonymous_249_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return (var.get(u"this").get('isLeaf') or var.get(u"this").get('spec').get('atom'))
        PyJs_anonymous_249_._set_name('anonymous')
        var.get('prototypeAccessors$4').get('isAtom').put('get', PyJs_anonymous_249_)
        @Js
        def PyJs_hasRequiredAttrs_250_(ignore, this, arguments, var=var):
            var = Scope({'ignore':ignore, 'this':this, 'arguments':arguments, 'hasRequiredAttrs':PyJs_hasRequiredAttrs_250_}, var)
            var.registers(['this$1', 'ignore', 'n'])
            var.put('this$1', var.get(u"this"))
            for PyJsTemp in var.get('this$1').get('attrs'):
                var.put('n', PyJsTemp)
                if (var.get('this$1').get('attrs').get(var.get('n')).get('isRequired') and (var.get('ignore').neg() or var.get('ignore').contains(var.get('n')).neg())):
                    return Js(True)
            return Js(False)
        PyJs_hasRequiredAttrs_250_._set_name('hasRequiredAttrs')
        var.get('NodeType').get('prototype').put('hasRequiredAttrs', PyJs_hasRequiredAttrs_250_)
        @Js
        def PyJs_compatibleContent_251_(other, this, arguments, var=var):
            var = Scope({'other':other, 'this':this, 'arguments':arguments, 'compatibleContent':PyJs_compatibleContent_251_}, var)
            var.registers(['other'])
            return ((var.get(u"this")==var.get('other')) or var.get(u"this").get('contentMatch').callprop('compatible', var.get('other').get('contentMatch')))
        PyJs_compatibleContent_251_._set_name('compatibleContent')
        var.get('NodeType').get('prototype').put('compatibleContent', PyJs_compatibleContent_251_)
        @Js
        def PyJs_InlineNonPyName_252_(attrs, this, arguments, var=var):
            var = Scope({'attrs':attrs, 'this':this, 'arguments':arguments, 'computeAttrs$1':PyJs_InlineNonPyName_252_}, var)
            var.registers(['attrs'])
            if (var.get('attrs').neg() and var.get(u"this").get('defaultAttrs')):
                return var.get(u"this").get('defaultAttrs')
            else:
                return var.get('computeAttrs')(var.get(u"this").get('attrs'), var.get('attrs'))
        PyJs_InlineNonPyName_252_._set_name('computeAttrs$1')
        var.get('NodeType').get('prototype').put('computeAttrs', PyJs_InlineNonPyName_252_)
        @Js
        def PyJs_create_253_(attrs, content, marks, this, arguments, var=var):
            var = Scope({'attrs':attrs, 'content':content, 'marks':marks, 'this':this, 'arguments':arguments, 'create':PyJs_create_253_}, var)
            var.registers(['marks', 'content', 'attrs'])
            if var.get(u"this").get('isText'):
                PyJsTempException = JsToPyException(var.get('Error').create(Js("NodeType.create can't construct text nodes")))
                raise PyJsTempException
            return var.get('Node').create(var.get(u"this"), var.get(u"this").callprop('computeAttrs', var.get('attrs')), var.get('Fragment').callprop('from', var.get('content')), var.get('Mark').callprop('setFrom', var.get('marks')))
        PyJs_create_253_._set_name('create')
        var.get('NodeType').get('prototype').put('create', PyJs_create_253_)
        @Js
        def PyJs_createChecked_254_(attrs, content, marks, this, arguments, var=var):
            var = Scope({'attrs':attrs, 'content':content, 'marks':marks, 'this':this, 'arguments':arguments, 'createChecked':PyJs_createChecked_254_}, var)
            var.registers(['marks', 'content', 'attrs'])
            var.put('content', var.get('Fragment').callprop('from', var.get('content')))
            if var.get(u"this").callprop('validContent', var.get('content')).neg():
                PyJsTempException = JsToPyException(var.get('RangeError').create((Js('Invalid content for node ')+var.get(u"this").get('name'))))
                raise PyJsTempException
            return var.get('Node').create(var.get(u"this"), var.get(u"this").callprop('computeAttrs', var.get('attrs')), var.get('content'), var.get('Mark').callprop('setFrom', var.get('marks')))
        PyJs_createChecked_254_._set_name('createChecked')
        var.get('NodeType').get('prototype').put('createChecked', PyJs_createChecked_254_)
        @Js
        def PyJs_createAndFill_255_(attrs, content, marks, this, arguments, var=var):
            var = Scope({'attrs':attrs, 'content':content, 'marks':marks, 'this':this, 'arguments':arguments, 'createAndFill':PyJs_createAndFill_255_}, var)
            var.registers(['before', 'marks', 'attrs', 'after', 'content'])
            var.put('attrs', var.get(u"this").callprop('computeAttrs', var.get('attrs')))
            var.put('content', var.get('Fragment').callprop('from', var.get('content')))
            if var.get('content').get('size'):
                var.put('before', var.get(u"this").get('contentMatch').callprop('fillBefore', var.get('content')))
                if var.get('before').neg():
                    return var.get(u"null")
                var.put('content', var.get('before').callprop('append', var.get('content')))
            var.put('after', var.get(u"this").get('contentMatch').callprop('matchFragment', var.get('content')).callprop('fillBefore', var.get('Fragment').get('empty'), Js(True)))
            if var.get('after').neg():
                return var.get(u"null")
            return var.get('Node').create(var.get(u"this"), var.get('attrs'), var.get('content').callprop('append', var.get('after')), var.get('Mark').callprop('setFrom', var.get('marks')))
        PyJs_createAndFill_255_._set_name('createAndFill')
        var.get('NodeType').get('prototype').put('createAndFill', PyJs_createAndFill_255_)
        @Js
        def PyJs_validContent_256_(content, this, arguments, var=var):
            var = Scope({'content':content, 'this':this, 'arguments':arguments, 'validContent':PyJs_validContent_256_}, var)
            var.registers(['this$1', 'i', 'result', 'content'])
            var.put('this$1', var.get(u"this"))
            var.put('result', var.get(u"this").get('contentMatch').callprop('matchFragment', var.get('content')))
            if (var.get('result').neg() or var.get('result').get('validEnd').neg()):
                return Js(False)
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('content').get('childCount')):
                try:
                    if var.get('this$1').callprop('allowsMarks', var.get('content').callprop('child', var.get('i')).get('marks')).neg():
                        return Js(False)
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return Js(True)
        PyJs_validContent_256_._set_name('validContent')
        var.get('NodeType').get('prototype').put('validContent', PyJs_validContent_256_)
        @Js
        def PyJs_allowsMarkType_257_(markType, this, arguments, var=var):
            var = Scope({'markType':markType, 'this':this, 'arguments':arguments, 'allowsMarkType':PyJs_allowsMarkType_257_}, var)
            var.registers(['markType'])
            return ((var.get(u"this").get('markSet')==var.get(u"null")) or (var.get(u"this").get('markSet').callprop('indexOf', var.get('markType'))>(-Js(1.0))))
        PyJs_allowsMarkType_257_._set_name('allowsMarkType')
        var.get('NodeType').get('prototype').put('allowsMarkType', PyJs_allowsMarkType_257_)
        @Js
        def PyJs_allowsMarks_258_(marks, this, arguments, var=var):
            var = Scope({'marks':marks, 'this':this, 'arguments':arguments, 'allowsMarks':PyJs_allowsMarks_258_}, var)
            var.registers(['this$1', 'i', 'marks'])
            var.put('this$1', var.get(u"this"))
            if (var.get(u"this").get('markSet')==var.get(u"null")):
                return Js(True)
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('marks').get('length')):
                try:
                    if var.get('this$1').callprop('allowsMarkType', var.get('marks').get(var.get('i')).get('type')).neg():
                        return Js(False)
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return Js(True)
        PyJs_allowsMarks_258_._set_name('allowsMarks')
        var.get('NodeType').get('prototype').put('allowsMarks', PyJs_allowsMarks_258_)
        @Js
        def PyJs_allowedMarks_259_(marks, this, arguments, var=var):
            var = Scope({'marks':marks, 'this':this, 'arguments':arguments, 'allowedMarks':PyJs_allowedMarks_259_}, var)
            var.registers(['copy', 'this$1', 'i', 'marks'])
            var.put('this$1', var.get(u"this"))
            if (var.get(u"this").get('markSet')==var.get(u"null")):
                return var.get('marks')
            pass
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('marks').get('length')):
                try:
                    if var.get('this$1').callprop('allowsMarkType', var.get('marks').get(var.get('i')).get('type')).neg():
                        if var.get('copy').neg():
                            var.put('copy', var.get('marks').callprop('slice', Js(0.0), var.get('i')))
                    else:
                        if var.get('copy'):
                            var.get('copy').callprop('push', var.get('marks').get(var.get('i')))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return (var.get('marks') if var.get('copy').neg() else (var.get('copy') if var.get('copy').get('length') else var.get('Mark').get('empty')))
        PyJs_allowedMarks_259_._set_name('allowedMarks')
        var.get('NodeType').get('prototype').put('allowedMarks', PyJs_allowedMarks_259_)
        @Js
        def PyJs_compile_260_(nodes, schema, this, arguments, var=var):
            var = Scope({'nodes':nodes, 'schema':schema, 'this':this, 'arguments':arguments, 'compile':PyJs_compile_260_}, var)
            var.registers(['nodes', 'topType', 'result', 'schema', '_'])
            var.put('result', var.get('Object').callprop('create', var.get(u"null")))
            @Js
            def PyJs_anonymous_261_(name, spec, this, arguments, var=var):
                var = Scope({'name':name, 'spec':spec, 'this':this, 'arguments':arguments}, var)
                var.registers(['name', 'spec'])
                return var.get('result').put(var.get('name'), var.get('NodeType').create(var.get('name'), var.get('schema'), var.get('spec')))
            PyJs_anonymous_261_._set_name('anonymous')
            var.get('nodes').callprop('forEach', PyJs_anonymous_261_)
            var.put('topType', (var.get('schema').get('spec').get('topNode') or Js('doc')))
            if var.get('result').get(var.get('topType')).neg():
                PyJsTempException = JsToPyException(var.get('RangeError').create(((Js("Schema is missing its top node type ('")+var.get('topType'))+Js("')"))))
                raise PyJsTempException
            if var.get('result').get('text').neg():
                PyJsTempException = JsToPyException(var.get('RangeError').create(Js("Every schema needs a 'text' type")))
                raise PyJsTempException
            for PyJsTemp in var.get('result').get('text').get('attrs'):
                var.put('_', PyJsTemp)
                PyJsTempException = JsToPyException(var.get('RangeError').create(Js('The text node type should not have attributes')))
                raise PyJsTempException
            return var.get('result')
        PyJs_compile_260_._set_name('compile')
        var.get('NodeType').put('compile', PyJs_compile_260_)
        var.get('Object').callprop('defineProperties', var.get('NodeType').get('prototype'), var.get('prototypeAccessors$4'))
        @Js
        def PyJs_Attribute_262_(options, this, arguments, var=var):
            var = Scope({'options':options, 'this':this, 'arguments':arguments, 'Attribute':PyJs_Attribute_262_}, var)
            var.registers(['options'])
            var.get(u"this").put('hasDefault', var.get('Object').get('prototype').get('hasOwnProperty').callprop('call', var.get('options'), Js('default')))
            var.get(u"this").put('default', var.get('options').get('default'))
        PyJs_Attribute_262_._set_name('Attribute')
        var.put('Attribute', PyJs_Attribute_262_)
        PyJs_Object_264_ = Js({})
        PyJs_Object_263_ = Js({'isRequired':PyJs_Object_264_})
        var.put('prototypeAccessors$1$2', PyJs_Object_263_)
        @Js
        def PyJs_anonymous_265_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get('hasDefault').neg()
        PyJs_anonymous_265_._set_name('anonymous')
        var.get('prototypeAccessors$1$2').get('isRequired').put('get', PyJs_anonymous_265_)
        var.get('Object').callprop('defineProperties', var.get('Attribute').get('prototype'), var.get('prototypeAccessors$1$2'))
        @Js
        def PyJs_MarkType_266_(name, rank, schema, spec, this, arguments, var=var):
            var = Scope({'name':name, 'rank':rank, 'schema':schema, 'spec':spec, 'this':this, 'arguments':arguments, 'MarkType':PyJs_MarkType_266_}, var)
            var.registers(['defaults', 'rank', 'schema', 'spec', 'name'])
            var.get(u"this").put('name', var.get('name'))
            var.get(u"this").put('schema', var.get('schema'))
            var.get(u"this").put('spec', var.get('spec'))
            var.get(u"this").put('attrs', var.get('initAttrs')(var.get('spec').get('attrs')))
            var.get(u"this").put('rank', var.get('rank'))
            var.get(u"this").put('excluded', var.get(u"null"))
            var.put('defaults', var.get('defaultAttrs')(var.get(u"this").get('attrs')))
            var.get(u"this").put('instance', (var.get('defaults') and var.get('Mark').create(var.get(u"this"), var.get('defaults'))))
        PyJs_MarkType_266_._set_name('MarkType')
        var.put('MarkType', PyJs_MarkType_266_)
        @Js
        def PyJs_create_267_(attrs, this, arguments, var=var):
            var = Scope({'attrs':attrs, 'this':this, 'arguments':arguments, 'create':PyJs_create_267_}, var)
            var.registers(['attrs'])
            if (var.get('attrs').neg() and var.get(u"this").get('instance')):
                return var.get(u"this").get('instance')
            return var.get('Mark').create(var.get(u"this"), var.get('computeAttrs')(var.get(u"this").get('attrs'), var.get('attrs')))
        PyJs_create_267_._set_name('create')
        var.get('MarkType').get('prototype').put('create', PyJs_create_267_)
        @Js
        def PyJs_compile_268_(marks, schema, this, arguments, var=var):
            var = Scope({'marks':marks, 'schema':schema, 'this':this, 'arguments':arguments, 'compile':PyJs_compile_268_}, var)
            var.registers(['marks', 'schema', 'result', 'rank'])
            var.put('result', var.get('Object').callprop('create', var.get(u"null")))
            var.put('rank', Js(0.0))
            @Js
            def PyJs_anonymous_269_(name, spec, this, arguments, var=var):
                var = Scope({'name':name, 'spec':spec, 'this':this, 'arguments':arguments}, var)
                var.registers(['name', 'spec'])
                return var.get('result').put(var.get('name'), var.get('MarkType').create(var.get('name'), (var.put('rank',Js(var.get('rank').to_number())+Js(1))-Js(1)), var.get('schema'), var.get('spec')))
            PyJs_anonymous_269_._set_name('anonymous')
            var.get('marks').callprop('forEach', PyJs_anonymous_269_)
            return var.get('result')
        PyJs_compile_268_._set_name('compile')
        var.get('MarkType').put('compile', PyJs_compile_268_)
        @Js
        def PyJs_removeFromSet_270_(set, this, arguments, var=var):
            var = Scope({'set':set, 'this':this, 'arguments':arguments, 'removeFromSet':PyJs_removeFromSet_270_}, var)
            var.registers(['set', 'this$1', 'i'])
            var.put('this$1', var.get(u"this"))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('set').get('length')):
                try:
                    if (var.get('set').get(var.get('i')).get('type')==var.get('this$1')):
                        return var.get('set').callprop('slice', Js(0.0), var.get('i')).callprop('concat', var.get('set').callprop('slice', (var.get('i')+Js(1.0))))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return var.get('set')
        PyJs_removeFromSet_270_._set_name('removeFromSet')
        var.get('MarkType').get('prototype').put('removeFromSet', PyJs_removeFromSet_270_)
        @Js
        def PyJs_isInSet_271_(set, this, arguments, var=var):
            var = Scope({'set':set, 'this':this, 'arguments':arguments, 'isInSet':PyJs_isInSet_271_}, var)
            var.registers(['set', 'this$1', 'i'])
            var.put('this$1', var.get(u"this"))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('set').get('length')):
                try:
                    if (var.get('set').get(var.get('i')).get('type')==var.get('this$1')):
                        return var.get('set').get(var.get('i'))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        PyJs_isInSet_271_._set_name('isInSet')
        var.get('MarkType').get('prototype').put('isInSet', PyJs_isInSet_271_)
        @Js
        def PyJs_excludes_272_(other, this, arguments, var=var):
            var = Scope({'other':other, 'this':this, 'arguments':arguments, 'excludes':PyJs_excludes_272_}, var)
            var.registers(['other'])
            return (var.get(u"this").get('excluded').callprop('indexOf', var.get('other'))>(-Js(1.0)))
        PyJs_excludes_272_._set_name('excludes')
        var.get('MarkType').get('prototype').put('excludes', PyJs_excludes_272_)
        @Js
        def PyJs_Schema_273_(spec, this, arguments, var=var):
            var = Scope({'spec':spec, 'this':this, 'arguments':arguments, 'Schema':PyJs_Schema_273_}, var)
            var.registers(['prop$2', 'spec', 'prop$1', 'contentExprCache', 'this$1', 'prop', 'excl', 'type', 'markExpr', 'type$1', 'contentExpr'])
            var.put('this$1', var.get(u"this"))
            PyJs_Object_274_ = Js({})
            var.get(u"this").put('spec', PyJs_Object_274_)
            for PyJsTemp in var.get('spec'):
                var.put('prop', PyJsTemp)
                var.get('this$1').get('spec').put(var.get('prop'), var.get('spec').get(var.get('prop')))
            var.get(u"this").get('spec').put('nodes', var.get('OrderedMap').callprop('from', var.get('spec').get('nodes')))
            var.get(u"this").get('spec').put('marks', var.get('OrderedMap').callprop('from', var.get('spec').get('marks')))
            var.get(u"this").put('nodes', var.get('NodeType').callprop('compile', var.get(u"this").get('spec').get('nodes'), var.get(u"this")))
            var.get(u"this").put('marks', var.get('MarkType').callprop('compile', var.get(u"this").get('spec').get('marks'), var.get(u"this")))
            var.put('contentExprCache', var.get('Object').callprop('create', var.get(u"null")))
            for PyJsTemp in var.get('this$1').get('nodes'):
                var.put('prop$1', PyJsTemp)
                if var.get('this$1').get('marks').contains(var.get('prop$1')):
                    PyJsTempException = JsToPyException(var.get('RangeError').create((var.get('prop$1')+Js(' can not be both a node and a mark'))))
                    raise PyJsTempException
                var.put('type', var.get('this$1').get('nodes').get(var.get('prop$1')))
                var.put('contentExpr', (var.get('type').get('spec').get('content') or Js('')))
                var.put('markExpr', var.get('type').get('spec').get('marks'))
                var.get('type').put('contentMatch', (var.get('contentExprCache').get(var.get('contentExpr')) or var.get('contentExprCache').put(var.get('contentExpr'), var.get('ContentMatch').callprop('parse', var.get('contentExpr'), var.get('this$1').get('nodes')))))
                var.get('type').put('inlineContent', var.get('type').get('contentMatch').get('inlineContent'))
                var.get('type').put('markSet', (var.get(u"null") if (var.get('markExpr')==Js('_')) else (var.get('gatherMarks')(var.get('this$1'), var.get('markExpr').callprop('split', Js(' '))) if var.get('markExpr') else (Js([]) if ((var.get('markExpr')==Js('')) or var.get('type').get('inlineContent').neg()) else var.get(u"null")))))
            for PyJsTemp in var.get('this$1').get('marks'):
                var.put('prop$2', PyJsTemp)
                var.put('type$1', var.get('this$1').get('marks').get(var.get('prop$2')))
                var.put('excl', var.get('type$1').get('spec').get('excludes'))
                var.get('type$1').put('excluded', (Js([var.get('type$1')]) if (var.get('excl')==var.get(u"null")) else (Js([]) if (var.get('excl')==Js('')) else var.get('gatherMarks')(var.get('this$1'), var.get('excl').callprop('split', Js(' '))))))
            var.get(u"this").put('nodeFromJSON', var.get(u"this").get('nodeFromJSON').callprop('bind', var.get(u"this")))
            var.get(u"this").put('markFromJSON', var.get(u"this").get('markFromJSON').callprop('bind', var.get(u"this")))
            var.get(u"this").put('topNodeType', var.get(u"this").get('nodes').get((var.get(u"this").get('spec').get('topNode') or Js('doc'))))
            var.get(u"this").put('cached', var.get('Object').callprop('create', var.get(u"null")))
            var.get(u"this").get('cached').put('wrappings', var.get('Object').callprop('create', var.get(u"null")))
        PyJs_Schema_273_._set_name('Schema')
        var.put('Schema', PyJs_Schema_273_)
        @Js
        def PyJs_node_275_(type, attrs, content, marks, this, arguments, var=var):
            var = Scope({'type':type, 'attrs':attrs, 'content':content, 'marks':marks, 'this':this, 'arguments':arguments, 'node':PyJs_node_275_}, var)
            var.registers(['marks', 'content', 'attrs', 'type'])
            if (var.get('type',throw=False).typeof()==Js('string')):
                var.put('type', var.get(u"this").callprop('nodeType', var.get('type')))
            else:
                if var.get('type').instanceof(var.get('NodeType')).neg():
                    PyJsTempException = JsToPyException(var.get('RangeError').create((Js('Invalid node type: ')+var.get('type'))))
                    raise PyJsTempException
                else:
                    if (var.get('type').get('schema')!=var.get(u"this")):
                        PyJsTempException = JsToPyException(var.get('RangeError').create(((Js('Node type from different schema used (')+var.get('type').get('name'))+Js(')'))))
                        raise PyJsTempException
            return var.get('type').callprop('createChecked', var.get('attrs'), var.get('content'), var.get('marks'))
        PyJs_node_275_._set_name('node')
        var.get('Schema').get('prototype').put('node', PyJs_node_275_)
        @Js
        def PyJs_text_276_(PyJsArg_746578742431_, marks, this, arguments, var=var):
            var = Scope({'text$1':PyJsArg_746578742431_, 'marks':marks, 'this':this, 'arguments':arguments, 'text':PyJs_text_276_}, var)
            var.registers(['text$1', 'marks', 'type'])
            var.put('type', var.get(u"this").get('nodes').get('text'))
            return var.get('TextNode').create(var.get('type'), var.get('type').get('defaultAttrs'), var.get('text$1'), var.get('Mark').callprop('setFrom', var.get('marks')))
        PyJs_text_276_._set_name('text')
        var.get('Schema').get('prototype').put('text', PyJs_text_276_)
        @Js
        def PyJs_mark_277_(type, attrs, this, arguments, var=var):
            var = Scope({'type':type, 'attrs':attrs, 'this':this, 'arguments':arguments, 'mark':PyJs_mark_277_}, var)
            var.registers(['attrs', 'type'])
            if (var.get('type',throw=False).typeof()==Js('string')):
                var.put('type', var.get(u"this").get('marks').get(var.get('type')))
            return var.get('type').callprop('create', var.get('attrs'))
        PyJs_mark_277_._set_name('mark')
        var.get('Schema').get('prototype').put('mark', PyJs_mark_277_)
        @Js
        def PyJs_nodeFromJSON_278_(json, this, arguments, var=var):
            var = Scope({'json':json, 'this':this, 'arguments':arguments, 'nodeFromJSON':PyJs_nodeFromJSON_278_}, var)
            var.registers(['json'])
            return var.get('Node').callprop('fromJSON', var.get(u"this"), var.get('json'))
        PyJs_nodeFromJSON_278_._set_name('nodeFromJSON')
        var.get('Schema').get('prototype').put('nodeFromJSON', PyJs_nodeFromJSON_278_)
        @Js
        def PyJs_markFromJSON_279_(json, this, arguments, var=var):
            var = Scope({'json':json, 'this':this, 'arguments':arguments, 'markFromJSON':PyJs_markFromJSON_279_}, var)
            var.registers(['json'])
            return var.get('Mark').callprop('fromJSON', var.get(u"this"), var.get('json'))
        PyJs_markFromJSON_279_._set_name('markFromJSON')
        var.get('Schema').get('prototype').put('markFromJSON', PyJs_markFromJSON_279_)
        @Js
        def PyJs_nodeType_280_(name, this, arguments, var=var):
            var = Scope({'name':name, 'this':this, 'arguments':arguments, 'nodeType':PyJs_nodeType_280_}, var)
            var.registers(['name', 'found'])
            var.put('found', var.get(u"this").get('nodes').get(var.get('name')))
            if var.get('found').neg():
                PyJsTempException = JsToPyException(var.get('RangeError').create((Js('Unknown node type: ')+var.get('name'))))
                raise PyJsTempException
            return var.get('found')
        PyJs_nodeType_280_._set_name('nodeType')
        var.get('Schema').get('prototype').put('nodeType', PyJs_nodeType_280_)
        pass
        @Js
        def PyJs_DOMParser_281_(schema, rules, this, arguments, var=var):
            var = Scope({'schema':schema, 'rules':rules, 'this':this, 'arguments':arguments, 'DOMParser':PyJs_DOMParser_281_}, var)
            var.registers(['schema', 'this$1', 'rules'])
            var.put('this$1', var.get(u"this"))
            var.get(u"this").put('schema', var.get('schema'))
            var.get(u"this").put('rules', var.get('rules'))
            var.get(u"this").put('tags', Js([]))
            var.get(u"this").put('styles', Js([]))
            @Js
            def PyJs_anonymous_282_(rule, this, arguments, var=var):
                var = Scope({'rule':rule, 'this':this, 'arguments':arguments}, var)
                var.registers(['rule'])
                if var.get('rule').get('tag'):
                    var.get('this$1').get('tags').callprop('push', var.get('rule'))
                else:
                    if var.get('rule').get('style'):
                        var.get('this$1').get('styles').callprop('push', var.get('rule'))
            PyJs_anonymous_282_._set_name('anonymous')
            var.get('rules').callprop('forEach', PyJs_anonymous_282_)
        PyJs_DOMParser_281_._set_name('DOMParser')
        var.put('DOMParser', PyJs_DOMParser_281_)
        @Js
        def PyJs_parse_283_(dom, options, this, arguments, var=var):
            var = Scope({'dom':dom, 'options':options, 'this':this, 'arguments':arguments, 'parse':PyJs_parse_283_}, var)
            var.registers(['dom', 'options', 'context'])
            if PyJsStrictEq(var.get('options'),PyJsComma(Js(0.0), Js(None))):
                PyJs_Object_284_ = Js({})
                var.put('options', PyJs_Object_284_)
            var.put('context', var.get('ParseContext').create(var.get(u"this"), var.get('options'), Js(False)))
            var.get('context').callprop('addAll', var.get('dom'), var.get(u"null"), var.get('options').get('from'), var.get('options').get('to'))
            return var.get('context').callprop('finish')
        PyJs_parse_283_._set_name('parse')
        var.get('DOMParser').get('prototype').put('parse', PyJs_parse_283_)
        @Js
        def PyJs_parseSlice_285_(dom, options, this, arguments, var=var):
            var = Scope({'dom':dom, 'options':options, 'this':this, 'arguments':arguments, 'parseSlice':PyJs_parseSlice_285_}, var)
            var.registers(['dom', 'options', 'context'])
            if PyJsStrictEq(var.get('options'),PyJsComma(Js(0.0), Js(None))):
                PyJs_Object_286_ = Js({})
                var.put('options', PyJs_Object_286_)
            var.put('context', var.get('ParseContext').create(var.get(u"this"), var.get('options'), Js(True)))
            var.get('context').callprop('addAll', var.get('dom'), var.get(u"null"), var.get('options').get('from'), var.get('options').get('to'))
            return var.get('Slice').callprop('maxOpen', var.get('context').callprop('finish'))
        PyJs_parseSlice_285_._set_name('parseSlice')
        var.get('DOMParser').get('prototype').put('parseSlice', PyJs_parseSlice_285_)
        @Js
        def PyJs_matchTag_287_(dom, context, this, arguments, var=var):
            var = Scope({'dom':dom, 'context':context, 'this':this, 'arguments':arguments, 'matchTag':PyJs_matchTag_287_}, var)
            var.registers(['context', 'result', 'this$1', 'rule', 'i', 'dom'])
            var.put('this$1', var.get(u"this"))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get(u"this").get('tags').get('length')):
                try:
                    var.put('rule', var.get('this$1').get('tags').get(var.get('i')))
                    if ((var.get('matches')(var.get('dom'), var.get('rule').get('tag')) and (PyJsStrictEq(var.get('rule').get('namespace'),var.get('undefined')) or (var.get('dom').get('namespaceURI')==var.get('rule').get('namespace')))) and (var.get('rule').get('context').neg() or var.get('context').callprop('matchesContext', var.get('rule').get('context')))):
                        if var.get('rule').get('getAttrs'):
                            var.put('result', var.get('rule').callprop('getAttrs', var.get('dom')))
                            if PyJsStrictEq(var.get('result'),Js(False)):
                                continue
                            var.get('rule').put('attrs', var.get('result'))
                        return var.get('rule')
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        PyJs_matchTag_287_._set_name('matchTag')
        var.get('DOMParser').get('prototype').put('matchTag', PyJs_matchTag_287_)
        @Js
        def PyJs_matchStyle_288_(prop, value, context, this, arguments, var=var):
            var = Scope({'prop':prop, 'value':value, 'context':context, 'this':this, 'arguments':arguments, 'matchStyle':PyJs_matchStyle_288_}, var)
            var.registers(['context', 'result', 'this$1', 'prop', 'rule', 'value', 'i'])
            var.put('this$1', var.get(u"this"))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get(u"this").get('styles').get('length')):
                try:
                    var.put('rule', var.get('this$1').get('styles').get(var.get('i')))
                    def PyJs_LONG_289_(var=var):
                        return (((var.get('rule').get('style').callprop('indexOf', var.get('prop'))!=Js(0.0)) or (var.get('rule').get('context') and var.get('context').callprop('matchesContext', var.get('rule').get('context')).neg())) or ((var.get('rule').get('style').get('length')>var.get('prop').get('length')) and ((var.get('rule').get('style').callprop('charCodeAt', var.get('prop').get('length'))!=Js(61.0)) or (var.get('rule').get('style').callprop('slice', (var.get('prop').get('length')+Js(1.0)))!=var.get('value')))))
                    if PyJs_LONG_289_():
                        continue
                    if var.get('rule').get('getAttrs'):
                        var.put('result', var.get('rule').callprop('getAttrs', var.get('value')))
                        if PyJsStrictEq(var.get('result'),Js(False)):
                            continue
                        var.get('rule').put('attrs', var.get('result'))
                    return var.get('rule')
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        PyJs_matchStyle_288_._set_name('matchStyle')
        var.get('DOMParser').get('prototype').put('matchStyle', PyJs_matchStyle_288_)
        @Js
        def PyJs_schemaRules_290_(schema, this, arguments, var=var):
            var = Scope({'schema':schema, 'this':this, 'arguments':arguments, 'schemaRules':PyJs_schemaRules_290_}, var)
            var.registers(['result', 'insert', 'loop$1', 'schema', 'loop', 'name$1', 'name'])
            @Js
            def PyJsHoisted_insert_(rule, this, arguments, var=var):
                var = Scope({'rule':rule, 'this':this, 'arguments':arguments}, var)
                var.registers(['priority', 'rule', 'next', 'i', 'nextPriority'])
                var.put('priority', (Js(50.0) if (var.get('rule').get('priority')==var.get(u"null")) else var.get('rule').get('priority')))
                var.put('i', Js(0.0))
                #for JS loop
                
                while (var.get('i')<var.get('result').get('length')):
                    try:
                        var.put('next', var.get('result').get(var.get('i')))
                        var.put('nextPriority', (Js(50.0) if (var.get('next').get('priority')==var.get(u"null")) else var.get('next').get('priority')))
                        if (var.get('nextPriority')<var.get('priority')):
                            break
                    finally:
                            (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                var.get('result').callprop('splice', var.get('i'), Js(0.0), var.get('rule'))
            PyJsHoisted_insert_.func_name = 'insert'
            var.put('insert', PyJsHoisted_insert_)
            var.put('result', Js([]))
            pass
            @Js
            def PyJs_anonymous_291_(name, this, arguments, var=var):
                var = Scope({'name':name, 'this':this, 'arguments':arguments}, var)
                var.registers(['name', 'rules'])
                var.put('rules', var.get('schema').get('marks').get(var.get('name')).get('spec').get('parseDOM'))
                if var.get('rules'):
                    @Js
                    def PyJs_anonymous_292_(rule, this, arguments, var=var):
                        var = Scope({'rule':rule, 'this':this, 'arguments':arguments}, var)
                        var.registers(['rule'])
                        var.get('insert')(var.put('rule', var.get('copy')(var.get('rule'))))
                        var.get('rule').put('mark', var.get('name'))
                    PyJs_anonymous_292_._set_name('anonymous')
                    var.get('rules').callprop('forEach', PyJs_anonymous_292_)
            PyJs_anonymous_291_._set_name('anonymous')
            var.put('loop', PyJs_anonymous_291_)
            for PyJsTemp in var.get('schema').get('marks'):
                var.put('name', PyJsTemp)
                var.get('loop')(var.get('name'))
            @Js
            def PyJs_anonymous_293_(name, this, arguments, var=var):
                var = Scope({'name':name, 'this':this, 'arguments':arguments}, var)
                var.registers(['name', 'rules$1'])
                var.put('rules$1', var.get('schema').get('nodes').get(var.get('name$1')).get('spec').get('parseDOM'))
                if var.get('rules$1'):
                    @Js
                    def PyJs_anonymous_294_(rule, this, arguments, var=var):
                        var = Scope({'rule':rule, 'this':this, 'arguments':arguments}, var)
                        var.registers(['rule'])
                        var.get('insert')(var.put('rule', var.get('copy')(var.get('rule'))))
                        var.get('rule').put('node', var.get('name$1'))
                    PyJs_anonymous_294_._set_name('anonymous')
                    var.get('rules$1').callprop('forEach', PyJs_anonymous_294_)
            PyJs_anonymous_293_._set_name('anonymous')
            var.put('loop$1', PyJs_anonymous_293_)
            for PyJsTemp in var.get('schema').get('nodes'):
                var.put('name$1', PyJsTemp)
                var.get('loop$1')(var.get('name'))
            return var.get('result')
        PyJs_schemaRules_290_._set_name('schemaRules')
        var.get('DOMParser').put('schemaRules', PyJs_schemaRules_290_)
        @Js
        def PyJs_fromSchema_295_(schema, this, arguments, var=var):
            var = Scope({'schema':schema, 'this':this, 'arguments':arguments, 'fromSchema':PyJs_fromSchema_295_}, var)
            var.registers(['schema'])
            return (var.get('schema').get('cached').get('domParser') or var.get('schema').get('cached').put('domParser', var.get('DOMParser').create(var.get('schema'), var.get('DOMParser').callprop('schemaRules', var.get('schema')))))
        PyJs_fromSchema_295_._set_name('fromSchema')
        var.get('DOMParser').put('fromSchema', PyJs_fromSchema_295_)
        PyJs_Object_296_ = Js({'address':Js(True),'article':Js(True),'aside':Js(True),'blockquote':Js(True),'canvas':Js(True),'dd':Js(True),'div':Js(True),'dl':Js(True),'fieldset':Js(True),'figcaption':Js(True),'figure':Js(True),'footer':Js(True),'form':Js(True),'h1':Js(True),'h2':Js(True),'h3':Js(True),'h4':Js(True),'h5':Js(True),'h6':Js(True),'header':Js(True),'hgroup':Js(True),'hr':Js(True),'li':Js(True),'noscript':Js(True),'ol':Js(True),'output':Js(True),'p':Js(True),'pre':Js(True),'section':Js(True),'table':Js(True),'tfoot':Js(True),'ul':Js(True)})
        var.put('blockTags', PyJs_Object_296_)
        PyJs_Object_297_ = Js({'head':Js(True),'noscript':Js(True),'object':Js(True),'script':Js(True),'style':Js(True),'title':Js(True)})
        var.put('ignoreTags', PyJs_Object_297_)
        PyJs_Object_298_ = Js({'ol':Js(True),'ul':Js(True)})
        var.put('listTags', PyJs_Object_298_)
        var.put('OPT_PRESERVE_WS', Js(1.0))
        var.put('OPT_PRESERVE_WS_FULL', Js(2.0))
        var.put('OPT_OPEN_LEFT', Js(4.0))
        pass
        @Js
        def PyJs_NodeContext_299_(type, attrs, marks, solid, match, options, this, arguments, var=var):
            var = Scope({'type':type, 'attrs':attrs, 'marks':marks, 'solid':solid, 'match':match, 'options':options, 'this':this, 'arguments':arguments, 'NodeContext':PyJs_NodeContext_299_}, var)
            var.registers(['match', 'marks', 'attrs', 'type', 'solid', 'options'])
            var.get(u"this").put('type', var.get('type'))
            var.get(u"this").put('attrs', var.get('attrs'))
            var.get(u"this").put('solid', var.get('solid'))
            var.get(u"this").put('match', (var.get('match') or (var.get(u"null") if (var.get('options')&var.get('OPT_OPEN_LEFT')) else var.get('type').get('contentMatch'))))
            var.get(u"this").put('options', var.get('options'))
            var.get(u"this").put('content', Js([]))
            var.get(u"this").put('marks', var.get('marks'))
            var.get(u"this").put('activeMarks', var.get('Mark').get('none'))
        PyJs_NodeContext_299_._set_name('NodeContext')
        var.put('NodeContext', PyJs_NodeContext_299_)
        @Js
        def PyJs_findWrapping_300_(node, this, arguments, var=var):
            var = Scope({'node':node, 'this':this, 'arguments':arguments, 'findWrapping':PyJs_findWrapping_300_}, var)
            var.registers(['node', 'fill', 'start', 'wrap'])
            if var.get(u"this").get('match').neg():
                if var.get(u"this").get('type').neg():
                    return Js([])
                var.put('fill', var.get(u"this").get('type').get('contentMatch').callprop('fillBefore', var.get('Fragment').callprop('from', var.get('node'))))
                if var.get('fill'):
                    var.get(u"this").put('match', var.get(u"this").get('type').get('contentMatch').callprop('matchFragment', var.get('fill')))
                else:
                    var.put('start', var.get(u"this").get('type').get('contentMatch'))
                    if var.put('wrap', var.get('start').callprop('findWrapping', var.get('node').get('type'))):
                        var.get(u"this").put('match', var.get('start'))
                        return var.get('wrap')
                    else:
                        return var.get(u"null")
            return var.get(u"this").get('match').callprop('findWrapping', var.get('node').get('type'))
        PyJs_findWrapping_300_._set_name('findWrapping')
        var.get('NodeContext').get('prototype').put('findWrapping', PyJs_findWrapping_300_)
        @Js
        def PyJs_finish_301_(openEnd, this, arguments, var=var):
            var = Scope({'openEnd':openEnd, 'this':this, 'arguments':arguments, 'finish':PyJs_finish_301_}, var)
            var.registers(['last', 'content', 'm', 'openEnd'])
            if (var.get(u"this").get('options')&var.get('OPT_PRESERVE_WS')).neg():
                var.put('last', var.get(u"this").get('content').get((var.get(u"this").get('content').get('length')-Js(1.0))))
                if ((var.get('last') and var.get('last').get('isText')) and var.put('m', JsRegExp('/\\s+$/').callprop('exec', var.get('last').get('text')))):
                    if (var.get('last').get('text').get('length')==var.get('m').get('0').get('length')):
                        var.get(u"this").get('content').callprop('pop')
                    else:
                        var.get(u"this").get('content').put((var.get(u"this").get('content').get('length')-Js(1.0)), var.get('last').callprop('withText', var.get('last').get('text').callprop('slice', Js(0.0), (var.get('last').get('text').get('length')-var.get('m').get('0').get('length')))))
            var.put('content', var.get('Fragment').callprop('from', var.get(u"this").get('content')))
            if (var.get('openEnd').neg() and var.get(u"this").get('match')):
                var.put('content', var.get('content').callprop('append', var.get(u"this").get('match').callprop('fillBefore', var.get('Fragment').get('empty'), Js(True))))
            return (var.get(u"this").get('type').callprop('create', var.get(u"this").get('attrs'), var.get('content'), var.get(u"this").get('marks')) if var.get(u"this").get('type') else var.get('content'))
        PyJs_finish_301_._set_name('finish')
        var.get('NodeContext').get('prototype').put('finish', PyJs_finish_301_)
        @Js
        def PyJs_ParseContext_302_(parser, options, open, this, arguments, var=var):
            var = Scope({'parser':parser, 'options':options, 'open':open, 'this':this, 'arguments':arguments, 'ParseContext':PyJs_ParseContext_302_}, var)
            var.registers(['topContext', 'open', 'parser', 'topNode', 'topOptions', 'options'])
            var.get(u"this").put('parser', var.get('parser'))
            var.get(u"this").put('options', var.get('options'))
            var.get(u"this").put('isOpen', var.get('open'))
            var.get(u"this").put('pendingMarks', Js([]))
            var.put('topNode', var.get('options').get('topNode'))
            var.put('topOptions', (var.get('wsOptionsFor')(var.get('options').get('preserveWhitespace'))|(var.get('OPT_OPEN_LEFT') if var.get('open') else Js(0.0))))
            if var.get('topNode'):
                var.put('topContext', var.get('NodeContext').create(var.get('topNode').get('type'), var.get('topNode').get('attrs'), var.get('Mark').get('none'), Js(True), (var.get('options').get('topMatch') or var.get('topNode').get('type').get('contentMatch')), var.get('topOptions')))
            else:
                if var.get('open'):
                    var.put('topContext', var.get('NodeContext').create(var.get(u"null"), var.get(u"null"), var.get('Mark').get('none'), Js(True), var.get(u"null"), var.get('topOptions')))
                else:
                    var.put('topContext', var.get('NodeContext').create(var.get('parser').get('schema').get('topNodeType'), var.get(u"null"), var.get('Mark').get('none'), Js(True), var.get(u"null"), var.get('topOptions')))
            var.get(u"this").put('nodes', Js([var.get('topContext')]))
            var.get(u"this").put('open', Js(0.0))
            var.get(u"this").put('find', var.get('options').get('findPositions'))
            var.get(u"this").put('needsBlock', Js(False))
        PyJs_ParseContext_302_._set_name('ParseContext')
        var.put('ParseContext', PyJs_ParseContext_302_)
        PyJs_Object_304_ = Js({})
        PyJs_Object_305_ = Js({})
        PyJs_Object_303_ = Js({'top':PyJs_Object_304_,'currentPos':PyJs_Object_305_})
        var.put('prototypeAccessors$6', PyJs_Object_303_)
        @Js
        def PyJs_anonymous_306_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return var.get(u"this").get('nodes').get(var.get(u"this").get('open'))
        PyJs_anonymous_306_._set_name('anonymous')
        var.get('prototypeAccessors$6').get('top').put('get', PyJs_anonymous_306_)
        @Js
        def PyJs_addDOM_307_(dom, this, arguments, var=var):
            var = Scope({'dom':dom, 'this':this, 'arguments':arguments, 'addDOM':PyJs_addDOM_307_}, var)
            var.registers(['this$1', 'marks', 'i', 'dom', 'style', 'i$1'])
            var.put('this$1', var.get(u"this"))
            if (var.get('dom').get('nodeType')==Js(3.0)):
                var.get(u"this").callprop('addTextNode', var.get('dom'))
            else:
                if (var.get('dom').get('nodeType')==Js(1.0)):
                    var.put('style', var.get('dom').callprop('getAttribute', Js('style')))
                    var.put('marks', (var.get(u"this").callprop('readStyles', var.get('parseStyles')(var.get('style'))) if var.get('style') else var.get(u"null")))
                    if (var.get('marks')!=var.get(u"null")):
                        #for JS loop
                        var.put('i', Js(0.0))
                        while (var.get('i')<var.get('marks').get('length')):
                            try:
                                var.get('this$1').callprop('addPendingMark', var.get('marks').get(var.get('i')))
                            finally:
                                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                    var.get(u"this").callprop('addElement', var.get('dom'))
                    if (var.get('marks')!=var.get(u"null")):
                        #for JS loop
                        var.put('i$1', Js(0.0))
                        while (var.get('i$1')<var.get('marks').get('length')):
                            try:
                                var.get('this$1').callprop('removePendingMark', var.get('marks').get(var.get('i$1')))
                            finally:
                                    (var.put('i$1',Js(var.get('i$1').to_number())+Js(1))-Js(1))
        PyJs_addDOM_307_._set_name('addDOM')
        var.get('ParseContext').get('prototype').put('addDOM', PyJs_addDOM_307_)
        @Js
        def PyJs_addTextNode_308_(dom, this, arguments, var=var):
            var = Scope({'dom':dom, 'this':this, 'arguments':arguments, 'addTextNode':PyJs_addTextNode_308_}, var)
            var.registers(['top', 'value', 'domNodeBefore', 'dom', 'nodeBefore'])
            var.put('value', var.get('dom').get('nodeValue'))
            var.put('top', var.get(u"this").get('top'))
            if ((var.get('top').get('type').get('inlineContent') if var.get('top').get('type') else (var.get('top').get('content').get('length') and var.get('top').get('content').get('0').get('isInline'))) or JsRegExp('/\\S/').callprop('test', var.get('value'))):
                if (var.get('top').get('options')&var.get('OPT_PRESERVE_WS')).neg():
                    var.put('value', var.get('value').callprop('replace', JsRegExp('/\\s+/g'), Js(' ')))
                    if (JsRegExp('/^\\s/').callprop('test', var.get('value')) and (var.get(u"this").get('open')==(var.get(u"this").get('nodes').get('length')-Js(1.0)))):
                        var.put('nodeBefore', var.get('top').get('content').get((var.get('top').get('content').get('length')-Js(1.0))))
                        var.put('domNodeBefore', var.get('dom').get('previousSibling'))
                        if ((var.get('nodeBefore').neg() or (var.get('domNodeBefore') and (var.get('domNodeBefore').get('nodeName')==Js('BR')))) or (var.get('nodeBefore').get('isText') and JsRegExp('/\\s$/').callprop('test', var.get('nodeBefore').get('text')))):
                            var.put('value', var.get('value').callprop('slice', Js(1.0)))
                else:
                    if (var.get('top').get('options')&var.get('OPT_PRESERVE_WS_FULL')).neg():
                        var.put('value', var.get('value').callprop('replace', JsRegExp('/\\r?\\n|\\r/g'), Js(' ')))
                if var.get('value'):
                    var.get(u"this").callprop('insertNode', var.get(u"this").get('parser').get('schema').callprop('text', var.get('value')))
                var.get(u"this").callprop('findInText', var.get('dom'))
            else:
                var.get(u"this").callprop('findInside', var.get('dom'))
        PyJs_addTextNode_308_._set_name('addTextNode')
        var.get('ParseContext').get('prototype').put('addTextNode', PyJs_addTextNode_308_)
        @Js
        def PyJs_addElement_309_(dom, this, arguments, var=var):
            var = Scope({'dom':dom, 'this':this, 'arguments':arguments, 'addElement':PyJs_addElement_309_}, var)
            var.registers(['oldNeedsBlock', 'top', 'sync', 'rule', 'dom', 'name'])
            var.put('name', var.get('dom').get('nodeName').callprop('toLowerCase'))
            if var.get('listTags').callprop('hasOwnProperty', var.get('name')):
                var.get('normalizeList')(var.get('dom'))
            var.put('rule', ((var.get(u"this").get('options').get('ruleFromNode') and var.get(u"this").get('options').callprop('ruleFromNode', var.get('dom'))) or var.get(u"this").get('parser').callprop('matchTag', var.get('dom'), var.get(u"this"))))
            if (var.get('rule').get('ignore') if var.get('rule') else var.get('ignoreTags').callprop('hasOwnProperty', var.get('name'))):
                var.get(u"this").callprop('findInside', var.get('dom'))
            else:
                if (var.get('rule').neg() or var.get('rule').get('skip')):
                    if (var.get('rule') and var.get('rule').get('skip').get('nodeType')):
                        var.put('dom', var.get('rule').get('skip'))
                    var.put('top', var.get(u"this").get('top'))
                    var.put('oldNeedsBlock', var.get(u"this").get('needsBlock'))
                    if var.get('blockTags').callprop('hasOwnProperty', var.get('name')):
                        var.put('sync', Js(True))
                        if var.get('top').get('type').neg():
                            var.get(u"this").put('needsBlock', Js(True))
                    var.get(u"this").callprop('addAll', var.get('dom'))
                    if var.get('sync'):
                        var.get(u"this").callprop('sync', var.get('top'))
                    var.get(u"this").put('needsBlock', var.get('oldNeedsBlock'))
                else:
                    var.get(u"this").callprop('addElementByRule', var.get('dom'), var.get('rule'))
        PyJs_addElement_309_._set_name('addElement')
        var.get('ParseContext').get('prototype').put('addElement', PyJs_addElement_309_)
        @Js
        def PyJs_readStyles_310_(styles, this, arguments, var=var):
            var = Scope({'styles':styles, 'this':this, 'arguments':arguments, 'readStyles':PyJs_readStyles_310_}, var)
            var.registers(['styles', 'this$1', 'rule', 'marks', 'i'])
            var.put('this$1', var.get(u"this"))
            var.put('marks', var.get('Mark').get('none'))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('styles').get('length')):
                try:
                    var.put('rule', var.get('this$1').get('parser').callprop('matchStyle', var.get('styles').get(var.get('i')), var.get('styles').get((var.get('i')+Js(1.0))), var.get('this$1')))
                    if var.get('rule').neg():
                        continue
                    if var.get('rule').get('ignore'):
                        return var.get(u"null")
                    var.put('marks', var.get('this$1').get('parser').get('schema').get('marks').get(var.get('rule').get('mark')).callprop('create', var.get('rule').get('attrs')).callprop('addToSet', var.get('marks')))
                finally:
                        var.put('i', Js(2.0), '+')
            return var.get('marks')
        PyJs_readStyles_310_._set_name('readStyles')
        var.get('ParseContext').get('prototype').put('readStyles', PyJs_readStyles_310_)
        @Js
        def PyJs_addElementByRule_311_(dom, rule, this, arguments, var=var):
            var = Scope({'dom':dom, 'rule':rule, 'this':this, 'arguments':arguments, 'addElementByRule':PyJs_addElementByRule_311_}, var)
            var.registers(['mark', 'nodeType', 'sync', 'this$1', 'markType', 'rule', 'startIn', 'contentDOM', 'dom'])
            var.put('this$1', var.get(u"this"))
            pass
            if var.get('rule').get('node'):
                var.put('nodeType', var.get(u"this").get('parser').get('schema').get('nodes').get(var.get('rule').get('node')))
                if var.get('nodeType').get('isLeaf'):
                    var.get(u"this").callprop('insertNode', var.get('nodeType').callprop('create', var.get('rule').get('attrs')))
                else:
                    var.put('sync', var.get(u"this").callprop('enter', var.get('nodeType'), var.get('rule').get('attrs'), var.get('rule').get('preserveWhitespace')))
            else:
                var.put('markType', var.get(u"this").get('parser').get('schema').get('marks').get(var.get('rule').get('mark')))
                var.put('mark', var.get('markType').callprop('create', var.get('rule').get('attrs')))
                var.get(u"this").callprop('addPendingMark', var.get('mark'))
            var.put('startIn', var.get(u"this").get('top'))
            if (var.get('nodeType') and var.get('nodeType').get('isLeaf')):
                var.get(u"this").callprop('findInside', var.get('dom'))
            else:
                if var.get('rule').get('getContent'):
                    var.get(u"this").callprop('findInside', var.get('dom'))
                    @Js
                    def PyJs_anonymous_312_(node, this, arguments, var=var):
                        var = Scope({'node':node, 'this':this, 'arguments':arguments}, var)
                        var.registers(['node'])
                        return var.get('this$1').callprop('insertNode', var.get('node'))
                    PyJs_anonymous_312_._set_name('anonymous')
                    var.get('rule').callprop('getContent', var.get('dom'), var.get(u"this").get('parser').get('schema')).callprop('forEach', PyJs_anonymous_312_)
                else:
                    var.put('contentDOM', var.get('rule').get('contentElement'))
                    if (var.get('contentDOM',throw=False).typeof()==Js('string')):
                        var.put('contentDOM', var.get('dom').callprop('querySelector', var.get('contentDOM')))
                    else:
                        if (var.get('contentDOM',throw=False).typeof()==Js('function')):
                            var.put('contentDOM', var.get('contentDOM')(var.get('dom')))
                    if var.get('contentDOM').neg():
                        var.put('contentDOM', var.get('dom'))
                    var.get(u"this").callprop('findAround', var.get('dom'), var.get('contentDOM'), Js(True))
                    var.get(u"this").callprop('addAll', var.get('contentDOM'), var.get('sync'))
            if var.get('sync'):
                var.get(u"this").callprop('sync', var.get('startIn'))
                (var.get(u"this").put('open',Js(var.get(u"this").get('open').to_number())-Js(1))+Js(1))
            if var.get('mark'):
                var.get(u"this").callprop('removePendingMark', var.get('mark'))
            return Js(True)
        PyJs_addElementByRule_311_._set_name('addElementByRule')
        var.get('ParseContext').get('prototype').put('addElementByRule', PyJs_addElementByRule_311_)
        @Js
        def PyJs_addAll_313_(parent, sync, startIndex, endIndex, this, arguments, var=var):
            var = Scope({'parent':parent, 'sync':sync, 'startIndex':startIndex, 'endIndex':endIndex, 'this':this, 'arguments':arguments, 'addAll':PyJs_addAll_313_}, var)
            var.registers(['startIndex', 'sync', 'this$1', 'end', 'endIndex', 'index', 'dom', 'parent'])
            var.put('this$1', var.get(u"this"))
            var.put('index', (var.get('startIndex') or Js(0.0)))
            #for JS loop
            var.put('dom', (var.get('parent').get('childNodes').get(var.get('startIndex')) if var.get('startIndex') else var.get('parent').get('firstChild')))
            var.put('end', (var.get(u"null") if (var.get('endIndex')==var.get(u"null")) else var.get('parent').get('childNodes').get(var.get('endIndex'))))
            while (var.get('dom')!=var.get('end')):
                try:
                    var.get('this$1').callprop('findAtPoint', var.get('parent'), var.get('index'))
                    var.get('this$1').callprop('addDOM', var.get('dom'))
                    if (var.get('sync') and var.get('blockTags').callprop('hasOwnProperty', var.get('dom').get('nodeName').callprop('toLowerCase'))):
                        var.get('this$1').callprop('sync', var.get('sync'))
                finally:
                        PyJsComma(var.put('dom', var.get('dom').get('nextSibling')),var.put('index',Js(var.get('index').to_number())+Js(1)))
            var.get(u"this").callprop('findAtPoint', var.get('parent'), var.get('index'))
        PyJs_addAll_313_._set_name('addAll')
        var.get('ParseContext').get('prototype').put('addAll', PyJs_addAll_313_)
        @Js
        def PyJs_findPlace_314_(node, this, arguments, var=var):
            var = Scope({'node':node, 'this':this, 'arguments':arguments, 'findPlace':PyJs_findPlace_314_}, var)
            var.registers(['route', 'node', 'sync', 'this$1', 'depth', 'found', 'i', 'cx'])
            var.put('this$1', var.get(u"this"))
            pass
            #for JS loop
            var.put('depth', var.get(u"this").get('open'))
            while (var.get('depth')>=Js(0.0)):
                try:
                    var.put('cx', var.get('this$1').get('nodes').get(var.get('depth')))
                    var.put('found', var.get('cx').callprop('findWrapping', var.get('node')))
                    if (var.get('found') and (var.get('route').neg() or (var.get('route').get('length')>var.get('found').get('length')))):
                        var.put('route', var.get('found'))
                        var.put('sync', var.get('cx'))
                        if var.get('found').get('length').neg():
                            break
                    if var.get('cx').get('solid'):
                        break
                finally:
                        (var.put('depth',Js(var.get('depth').to_number())-Js(1))+Js(1))
            if var.get('route').neg():
                return Js(False)
            var.get(u"this").callprop('sync', var.get('sync'))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('route').get('length')):
                try:
                    var.get('this$1').callprop('enterInner', var.get('route').get(var.get('i')), var.get(u"null"), Js(False))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return Js(True)
        PyJs_findPlace_314_._set_name('findPlace')
        var.get('ParseContext').get('prototype').put('findPlace', PyJs_findPlace_314_)
        @Js
        def PyJs_insertNode_315_(node, this, arguments, var=var):
            var = Scope({'node':node, 'this':this, 'arguments':arguments, 'insertNode':PyJs_insertNode_315_}, var)
            var.registers(['node', 'top', 'marks', 'block', 'i'])
            if ((var.get('node').get('isInline') and var.get(u"this").get('needsBlock')) and var.get(u"this").get('top').get('type').neg()):
                var.put('block', var.get(u"this").callprop('textblockFromContext'))
                if var.get('block'):
                    var.get(u"this").callprop('enterInner', var.get('block'))
            if var.get(u"this").callprop('findPlace', var.get('node')):
                var.get(u"this").callprop('closeExtra')
                var.put('top', var.get(u"this").get('top'))
                var.get(u"this").callprop('applyPendingMarks', var.get('top'))
                if var.get('top').get('match'):
                    var.get('top').put('match', var.get('top').get('match').callprop('matchType', var.get('node').get('type')))
                var.put('marks', var.get('top').get('activeMarks'))
                #for JS loop
                var.put('i', Js(0.0))
                while (var.get('i')<var.get('node').get('marks').get('length')):
                    try:
                        if (var.get('top').get('type').neg() or var.get('top').get('type').callprop('allowsMarkType', var.get('node').get('marks').get(var.get('i')).get('type'))):
                            var.put('marks', var.get('node').get('marks').get(var.get('i')).callprop('addToSet', var.get('marks')))
                    finally:
                            (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                var.get('top').get('content').callprop('push', var.get('node').callprop('mark', var.get('marks')))
        PyJs_insertNode_315_._set_name('insertNode')
        var.get('ParseContext').get('prototype').put('insertNode', PyJs_insertNode_315_)
        @Js
        def PyJs_applyPendingMarks_316_(top, this, arguments, var=var):
            var = Scope({'top':top, 'this':this, 'arguments':arguments, 'applyPendingMarks':PyJs_applyPendingMarks_316_}, var)
            var.registers(['this$1', 'i', 'top', 'mark'])
            var.put('this$1', var.get(u"this"))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get(u"this").get('pendingMarks').get('length')):
                try:
                    var.put('mark', var.get('this$1').get('pendingMarks').get(var.get('i')))
                    if ((var.get('top').get('type').neg() or var.get('top').get('type').callprop('allowsMarkType', var.get('mark').get('type'))) and var.get('mark').get('type').callprop('isInSet', var.get('top').get('activeMarks')).neg()):
                        var.get('top').put('activeMarks', var.get('mark').callprop('addToSet', var.get('top').get('activeMarks')))
                        var.get('this$1').get('pendingMarks').callprop('splice', (var.put('i',Js(var.get('i').to_number())-Js(1))+Js(1)), Js(1.0))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        PyJs_applyPendingMarks_316_._set_name('applyPendingMarks')
        var.get('ParseContext').get('prototype').put('applyPendingMarks', PyJs_applyPendingMarks_316_)
        @Js
        def PyJs_enter_317_(type, attrs, preserveWS, this, arguments, var=var):
            var = Scope({'type':type, 'attrs':attrs, 'preserveWS':preserveWS, 'this':this, 'arguments':arguments, 'enter':PyJs_enter_317_}, var)
            var.registers(['ok', 'preserveWS', 'attrs', 'type'])
            var.put('ok', var.get(u"this").callprop('findPlace', var.get('type').callprop('create', var.get('attrs'))))
            if var.get('ok'):
                var.get(u"this").callprop('applyPendingMarks', var.get(u"this").get('top'))
                var.get(u"this").callprop('enterInner', var.get('type'), var.get('attrs'), Js(True), var.get('preserveWS'))
            return var.get('ok')
        PyJs_enter_317_._set_name('enter')
        var.get('ParseContext').get('prototype').put('enter', PyJs_enter_317_)
        @Js
        def PyJs_enterInner_318_(type, attrs, solid, preserveWS, this, arguments, var=var):
            var = Scope({'type':type, 'attrs':attrs, 'solid':solid, 'preserveWS':preserveWS, 'this':this, 'arguments':arguments, 'enterInner':PyJs_enterInner_318_}, var)
            var.registers(['top', 'preserveWS', 'attrs', 'type', 'solid', 'options'])
            var.get(u"this").callprop('closeExtra')
            var.put('top', var.get(u"this").get('top'))
            var.get('top').put('match', (var.get('top').get('match') and var.get('top').get('match').callprop('matchType', var.get('type'), var.get('attrs'))))
            var.put('options', ((var.get('top').get('options')&(~var.get('OPT_OPEN_LEFT'))) if (var.get('preserveWS')==var.get(u"null")) else var.get('wsOptionsFor')(var.get('preserveWS'))))
            if ((var.get('top').get('options')&var.get('OPT_OPEN_LEFT')) and (var.get('top').get('content').get('length')==Js(0.0))):
                var.put('options', var.get('OPT_OPEN_LEFT'), '|')
            var.get(u"this").get('nodes').callprop('push', var.get('NodeContext').create(var.get('type'), var.get('attrs'), var.get('top').get('activeMarks'), var.get('solid'), var.get(u"null"), var.get('options')))
            (var.get(u"this").put('open',Js(var.get(u"this").get('open').to_number())+Js(1))-Js(1))
        PyJs_enterInner_318_._set_name('enterInner')
        var.get('ParseContext').get('prototype').put('enterInner', PyJs_enterInner_318_)
        @Js
        def PyJs_closeExtra_319_(openEnd, this, arguments, var=var):
            var = Scope({'openEnd':openEnd, 'this':this, 'arguments':arguments, 'closeExtra':PyJs_closeExtra_319_}, var)
            var.registers(['this$1', 'i', 'openEnd'])
            var.put('this$1', var.get(u"this"))
            var.put('i', (var.get(u"this").get('nodes').get('length')-Js(1.0)))
            if (var.get('i')>var.get(u"this").get('open')):
                #for JS loop
                
                while (var.get('i')>var.get(u"this").get('open')):
                    try:
                        var.get('this$1').get('nodes').get((var.get('i')-Js(1.0))).get('content').callprop('push', var.get('this$1').get('nodes').get(var.get('i')).callprop('finish', var.get('openEnd')))
                    finally:
                            (var.put('i',Js(var.get('i').to_number())-Js(1))+Js(1))
                var.get(u"this").get('nodes').put('length', (var.get(u"this").get('open')+Js(1.0)))
        PyJs_closeExtra_319_._set_name('closeExtra')
        var.get('ParseContext').get('prototype').put('closeExtra', PyJs_closeExtra_319_)
        @Js
        def PyJs_finish_320_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'finish':PyJs_finish_320_}, var)
            var.registers([])
            var.get(u"this").put('open', Js(0.0))
            var.get(u"this").callprop('closeExtra', var.get(u"this").get('isOpen'))
            return var.get(u"this").get('nodes').get('0').callprop('finish', (var.get(u"this").get('isOpen') or var.get(u"this").get('options').get('topOpen')))
        PyJs_finish_320_._set_name('finish')
        var.get('ParseContext').get('prototype').put('finish', PyJs_finish_320_)
        @Js
        def PyJs_sync_321_(to, this, arguments, var=var):
            var = Scope({'to':to, 'this':this, 'arguments':arguments, 'sync':PyJs_sync_321_}, var)
            var.registers(['to', 'this$1', 'i'])
            var.put('this$1', var.get(u"this"))
            #for JS loop
            var.put('i', var.get(u"this").get('open'))
            while (var.get('i')>=Js(0.0)):
                try:
                    if (var.get('this$1').get('nodes').get(var.get('i'))==var.get('to')):
                        var.get('this$1').put('open', var.get('i'))
                        return var.get('undefined')
                finally:
                        (var.put('i',Js(var.get('i').to_number())-Js(1))+Js(1))
        PyJs_sync_321_._set_name('sync')
        var.get('ParseContext').get('prototype').put('sync', PyJs_sync_321_)
        @Js
        def PyJs_addPendingMark_322_(mark, this, arguments, var=var):
            var = Scope({'mark':mark, 'this':this, 'arguments':arguments, 'addPendingMark':PyJs_addPendingMark_322_}, var)
            var.registers(['mark'])
            var.get(u"this").get('pendingMarks').callprop('push', var.get('mark'))
        PyJs_addPendingMark_322_._set_name('addPendingMark')
        var.get('ParseContext').get('prototype').put('addPendingMark', PyJs_addPendingMark_322_)
        @Js
        def PyJs_removePendingMark_323_(mark, this, arguments, var=var):
            var = Scope({'mark':mark, 'this':this, 'arguments':arguments, 'removePendingMark':PyJs_removePendingMark_323_}, var)
            var.registers(['found', 'mark', 'top'])
            var.put('found', var.get(u"this").get('pendingMarks').callprop('lastIndexOf', var.get('mark')))
            if (var.get('found')>(-Js(1.0))):
                var.get(u"this").get('pendingMarks').callprop('splice', var.get('found'), Js(1.0))
            else:
                var.put('top', var.get(u"this").get('top'))
                var.get('top').put('activeMarks', var.get('mark').callprop('removeFromSet', var.get('top').get('activeMarks')))
        PyJs_removePendingMark_323_._set_name('removePendingMark')
        var.get('ParseContext').get('prototype').put('removePendingMark', PyJs_removePendingMark_323_)
        @Js
        def PyJs_anonymous_324_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers(['this$1', 'j', 'content', 'i', 'pos'])
            var.put('this$1', var.get(u"this"))
            var.get(u"this").callprop('closeExtra')
            var.put('pos', Js(0.0))
            #for JS loop
            var.put('i', var.get(u"this").get('open'))
            while (var.get('i')>=Js(0.0)):
                try:
                    var.put('content', var.get('this$1').get('nodes').get(var.get('i')).get('content'))
                    #for JS loop
                    var.put('j', (var.get('content').get('length')-Js(1.0)))
                    while (var.get('j')>=Js(0.0)):
                        try:
                            var.put('pos', var.get('content').get(var.get('j')).get('nodeSize'), '+')
                        finally:
                                (var.put('j',Js(var.get('j').to_number())-Js(1))+Js(1))
                    if var.get('i'):
                        (var.put('pos',Js(var.get('pos').to_number())+Js(1))-Js(1))
                finally:
                        (var.put('i',Js(var.get('i').to_number())-Js(1))+Js(1))
            return var.get('pos')
        PyJs_anonymous_324_._set_name('anonymous')
        var.get('prototypeAccessors$6').get('currentPos').put('get', PyJs_anonymous_324_)
        @Js
        def PyJs_findAtPoint_325_(parent, offset, this, arguments, var=var):
            var = Scope({'parent':parent, 'offset':offset, 'this':this, 'arguments':arguments, 'findAtPoint':PyJs_findAtPoint_325_}, var)
            var.registers(['parent', 'this$1', 'offset', 'i'])
            var.put('this$1', var.get(u"this"))
            if var.get(u"this").get('find'):
                #for JS loop
                var.put('i', Js(0.0))
                while (var.get('i')<var.get(u"this").get('find').get('length')):
                    try:
                        if ((var.get('this$1').get('find').get(var.get('i')).get('node')==var.get('parent')) and (var.get('this$1').get('find').get(var.get('i')).get('offset')==var.get('offset'))):
                            var.get('this$1').get('find').get(var.get('i')).put('pos', var.get('this$1').get('currentPos'))
                    finally:
                            (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        PyJs_findAtPoint_325_._set_name('findAtPoint')
        var.get('ParseContext').get('prototype').put('findAtPoint', PyJs_findAtPoint_325_)
        @Js
        def PyJs_findInside_326_(parent, this, arguments, var=var):
            var = Scope({'parent':parent, 'this':this, 'arguments':arguments, 'findInside':PyJs_findInside_326_}, var)
            var.registers(['parent', 'this$1', 'i'])
            var.put('this$1', var.get(u"this"))
            if var.get(u"this").get('find'):
                #for JS loop
                var.put('i', Js(0.0))
                while (var.get('i')<var.get(u"this").get('find').get('length')):
                    try:
                        if (((var.get('this$1').get('find').get(var.get('i')).get('pos')==var.get(u"null")) and (var.get('parent').get('nodeType')==Js(1.0))) and var.get('parent').callprop('contains', var.get('this$1').get('find').get(var.get('i')).get('node'))):
                            var.get('this$1').get('find').get(var.get('i')).put('pos', var.get('this$1').get('currentPos'))
                    finally:
                            (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        PyJs_findInside_326_._set_name('findInside')
        var.get('ParseContext').get('prototype').put('findInside', PyJs_findInside_326_)
        @Js
        def PyJs_findAround_327_(parent, content, before, this, arguments, var=var):
            var = Scope({'parent':parent, 'content':content, 'before':before, 'this':this, 'arguments':arguments, 'findAround':PyJs_findAround_327_}, var)
            var.registers(['before', 'this$1', 'content', 'i', 'pos', 'parent'])
            var.put('this$1', var.get(u"this"))
            if ((var.get('parent')!=var.get('content')) and var.get(u"this").get('find')):
                #for JS loop
                var.put('i', Js(0.0))
                while (var.get('i')<var.get(u"this").get('find').get('length')):
                    try:
                        if (((var.get('this$1').get('find').get(var.get('i')).get('pos')==var.get(u"null")) and (var.get('parent').get('nodeType')==Js(1.0))) and var.get('parent').callprop('contains', var.get('this$1').get('find').get(var.get('i')).get('node'))):
                            var.put('pos', var.get('content').callprop('compareDocumentPosition', var.get('this$1').get('find').get(var.get('i')).get('node')))
                            if (var.get('pos')&(Js(2.0) if var.get('before') else Js(4.0))):
                                var.get('this$1').get('find').get(var.get('i')).put('pos', var.get('this$1').get('currentPos'))
                    finally:
                            (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        PyJs_findAround_327_._set_name('findAround')
        var.get('ParseContext').get('prototype').put('findAround', PyJs_findAround_327_)
        @Js
        def PyJs_findInText_328_(textNode, this, arguments, var=var):
            var = Scope({'textNode':textNode, 'this':this, 'arguments':arguments, 'findInText':PyJs_findInText_328_}, var)
            var.registers(['textNode', 'this$1', 'i'])
            var.put('this$1', var.get(u"this"))
            if var.get(u"this").get('find'):
                #for JS loop
                var.put('i', Js(0.0))
                while (var.get('i')<var.get(u"this").get('find').get('length')):
                    try:
                        if (var.get('this$1').get('find').get(var.get('i')).get('node')==var.get('textNode')):
                            var.get('this$1').get('find').get(var.get('i')).put('pos', (var.get('this$1').get('currentPos')-(var.get('textNode').get('nodeValue').get('length')-var.get('this$1').get('find').get(var.get('i')).get('offset'))))
                    finally:
                            (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        PyJs_findInText_328_._set_name('findInText')
        var.get('ParseContext').get('prototype').put('findInText', PyJs_findInText_328_)
        @Js
        def PyJs_matchesContext_329_(context, this, arguments, var=var):
            var = Scope({'context':context, 'this':this, 'arguments':arguments, 'matchesContext':PyJs_matchesContext_329_}, var)
            var.registers(['minDepth', 'match', 'context', 'useRoot', 'parts', 'this$1', 'option'])
            var.put('this$1', var.get(u"this"))
            if (var.get('context').callprop('indexOf', Js('|'))>(-Js(1.0))):
                return var.get('context').callprop('split', JsRegExp('/\\s*\\|\\s*/')).callprop('some', var.get(u"this").get('matchesContext'), var.get(u"this"))
            var.put('parts', var.get('context').callprop('split', Js('/')))
            var.put('option', var.get(u"this").get('options').get('context'))
            var.put('useRoot', (var.get(u"this").get('isOpen').neg() and (var.get('option').neg() or (var.get('option').get('parent').get('type')==var.get(u"this").get('nodes').get('0').get('type')))))
            var.put('minDepth', ((-((var.get('option').get('depth')+Js(1.0)) if var.get('option') else Js(0.0)))+(Js(0.0) if var.get('useRoot') else Js(1.0))))
            @Js
            def PyJs_anonymous_330_(i, depth, this, arguments, var=var):
                var = Scope({'i':i, 'depth':depth, 'this':this, 'arguments':arguments}, var)
                var.registers(['next', 'depth', 'part', 'i'])
                #for JS loop
                
                while (var.get('i')>=Js(0.0)):
                    try:
                        var.put('part', var.get('parts').get(var.get('i')))
                        if (var.get('part')==Js('')):
                            if ((var.get('i')==(var.get('parts').get('length')-Js(1.0))) or (var.get('i')==Js(0.0))):
                                continue
                            #for JS loop
                            
                            while (var.get('depth')>=var.get('minDepth')):
                                try:
                                    if var.get('match')((var.get('i')-Js(1.0)), var.get('depth')):
                                        return Js(True)
                                finally:
                                        (var.put('depth',Js(var.get('depth').to_number())-Js(1))+Js(1))
                            return Js(False)
                        else:
                            var.put('next', (var.get('this$1').get('nodes').get(var.get('depth')).get('type') if ((var.get('depth')>Js(0.0)) or ((var.get('depth')==Js(0.0)) and var.get('useRoot'))) else (var.get('option').callprop('node', (var.get('depth')-var.get('minDepth'))).get('type') if (var.get('option') and (var.get('depth')>=var.get('minDepth'))) else var.get(u"null"))))
                            if (var.get('next').neg() or ((var.get('next').get('name')!=var.get('part')) and (var.get('next').get('groups').callprop('indexOf', var.get('part'))==(-Js(1.0))))):
                                return Js(False)
                            (var.put('depth',Js(var.get('depth').to_number())-Js(1))+Js(1))
                    finally:
                            (var.put('i',Js(var.get('i').to_number())-Js(1))+Js(1))
                return Js(True)
            PyJs_anonymous_330_._set_name('anonymous')
            var.put('match', PyJs_anonymous_330_)
            return var.get('match')((var.get('parts').get('length')-Js(1.0)), var.get(u"this").get('open'))
        PyJs_matchesContext_329_._set_name('matchesContext')
        var.get('ParseContext').get('prototype').put('matchesContext', PyJs_matchesContext_329_)
        @Js
        def PyJs_textblockFromContext_331_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'textblockFromContext':PyJs_textblockFromContext_331_}, var)
            var.registers(['deflt', '$context', 'this$1', 'type', 'd', 'name'])
            var.put('this$1', var.get(u"this"))
            var.put('$context', var.get(u"this").get('options').get('context'))
            if var.get('$context'):
                #for JS loop
                var.put('d', var.get('$context').get('depth'))
                while (var.get('d')>=Js(0.0)):
                    try:
                        var.put('deflt', var.get('$context').callprop('node', var.get('d')).callprop('contentMatchAt', var.get('$context').callprop('indexAfter', var.get('d'))).get('defaultType'))
                        if ((var.get('deflt') and var.get('deflt').get('isTextblock')) and var.get('deflt').get('defaultAttrs')):
                            return var.get('deflt')
                    finally:
                            (var.put('d',Js(var.get('d').to_number())-Js(1))+Js(1))
            for PyJsTemp in var.get('this$1').get('parser').get('schema').get('nodes'):
                var.put('name', PyJsTemp)
                var.put('type', var.get('this$1').get('parser').get('schema').get('nodes').get(var.get('name')))
                if (var.get('type').get('isTextblock') and var.get('type').get('defaultAttrs')):
                    return var.get('type')
        PyJs_textblockFromContext_331_._set_name('textblockFromContext')
        var.get('ParseContext').get('prototype').put('textblockFromContext', PyJs_textblockFromContext_331_)
        var.get('Object').callprop('defineProperties', var.get('ParseContext').get('prototype'), var.get('prototypeAccessors$6'))
        pass
        pass
        pass
        pass
        @Js
        def PyJs_DOMSerializer_333_(nodes, marks, this, arguments, var=var):
            var = Scope({'nodes':nodes, 'marks':marks, 'this':this, 'arguments':arguments, 'DOMSerializer':PyJs_DOMSerializer_333_}, var)
            var.registers(['nodes', 'marks'])
            PyJs_Object_334_ = Js({})
            var.get(u"this").put('nodes', (var.get('nodes') or PyJs_Object_334_))
            PyJs_Object_335_ = Js({})
            var.get(u"this").put('marks', (var.get('marks') or PyJs_Object_335_))
        PyJs_DOMSerializer_333_._set_name('DOMSerializer')
        var.put('DOMSerializer', PyJs_DOMSerializer_333_)
        @Js
        def PyJs_serializeFragment_336_(fragment, options, target, this, arguments, var=var):
            var = Scope({'fragment':fragment, 'options':options, 'target':target, 'this':this, 'arguments':arguments, 'serializeFragment':PyJs_serializeFragment_336_}, var)
            var.registers(['active', 'top', 'this$1', 'target', 'fragment', 'options'])
            var.put('this$1', var.get(u"this"))
            if PyJsStrictEq(var.get('options'),PyJsComma(Js(0.0), Js(None))):
                PyJs_Object_337_ = Js({})
                var.put('options', PyJs_Object_337_)
            if var.get('target').neg():
                var.put('target', var.get('doc')(var.get('options')).callprop('createDocumentFragment'))
            var.put('top', var.get('target'))
            var.put('active', var.get(u"null"))
            @Js
            def PyJs_anonymous_338_(node, this, arguments, var=var):
                var = Scope({'node':node, 'this':this, 'arguments':arguments}, var)
                var.registers(['rendered', 'node', 'markDOM', 'keep', 'add', 'next'])
                if (var.get('active') or var.get('node').get('marks').get('length')):
                    if var.get('active').neg():
                        var.put('active', Js([]))
                    var.put('keep', Js(0.0))
                    var.put('rendered', Js(0.0))
                    while ((var.get('keep')<var.get('active').get('length')) and (var.get('rendered')<var.get('node').get('marks').get('length'))):
                        var.put('next', var.get('node').get('marks').get(var.get('rendered')))
                        if var.get('this$1').get('marks').get(var.get('next').get('type').get('name')).neg():
                            (var.put('rendered',Js(var.get('rendered').to_number())+Js(1))-Js(1))
                            continue
                        if var.get('next').callprop('eq', var.get('active').get(var.get('keep'))).neg():
                            break
                        var.put('keep', Js(2.0), '+')
                        (var.put('rendered',Js(var.get('rendered').to_number())+Js(1))-Js(1))
                    while (var.get('keep')<var.get('active').get('length')):
                        var.put('top', var.get('active').callprop('pop'))
                        var.get('active').callprop('pop')
                    while (var.get('rendered')<var.get('node').get('marks').get('length')):
                        var.put('add', var.get('node').get('marks').get((var.put('rendered',Js(var.get('rendered').to_number())+Js(1))-Js(1))))
                        var.put('markDOM', var.get('this$1').callprop('serializeMark', var.get('add'), var.get('node').get('isInline'), var.get('options')))
                        if var.get('markDOM'):
                            var.get('active').callprop('push', var.get('add'), var.get('top'))
                            var.get('top').callprop('appendChild', var.get('markDOM').get('dom'))
                            var.put('top', (var.get('markDOM').get('contentDOM') or var.get('markDOM').get('dom')))
                var.get('top').callprop('appendChild', var.get('this$1').callprop('serializeNode', var.get('node'), var.get('options')))
            PyJs_anonymous_338_._set_name('anonymous')
            var.get('fragment').callprop('forEach', PyJs_anonymous_338_)
            return var.get('target')
        PyJs_serializeFragment_336_._set_name('serializeFragment')
        var.get('DOMSerializer').get('prototype').put('serializeFragment', PyJs_serializeFragment_336_)
        @Js
        def PyJs_serializeNode_339_(node, options, this, arguments, var=var):
            var = Scope({'node':node, 'options':options, 'this':this, 'arguments':arguments, 'serializeNode':PyJs_serializeNode_339_}, var)
            var.registers(['node', 'contentDOM', 'ref', 'dom', 'options'])
            if PyJsStrictEq(var.get('options'),PyJsComma(Js(0.0), Js(None))):
                PyJs_Object_340_ = Js({})
                var.put('options', PyJs_Object_340_)
            var.put('ref', var.get('DOMSerializer').callprop('renderSpec', var.get('doc')(var.get('options')), var.get(u"this").get('nodes').callprop(var.get('node').get('type').get('name'), var.get('node'))))
            var.put('dom', var.get('ref').get('dom'))
            var.put('contentDOM', var.get('ref').get('contentDOM'))
            if var.get('contentDOM'):
                if var.get('node').get('isLeaf'):
                    PyJsTempException = JsToPyException(var.get('RangeError').create(Js('Content hole not allowed in a leaf node spec')))
                    raise PyJsTempException
                if var.get('options').get('onContent'):
                    var.get('options').callprop('onContent', var.get('node'), var.get('contentDOM'), var.get('options'))
                else:
                    var.get(u"this").callprop('serializeFragment', var.get('node').get('content'), var.get('options'), var.get('contentDOM'))
            return var.get('dom')
        PyJs_serializeNode_339_._set_name('serializeNode')
        var.get('DOMSerializer').get('prototype').put('serializeNode', PyJs_serializeNode_339_)
        @Js
        def PyJs_serializeNodeAndMarks_341_(node, options, this, arguments, var=var):
            var = Scope({'node':node, 'options':options, 'this':this, 'arguments':arguments, 'serializeNodeAndMarks':PyJs_serializeNodeAndMarks_341_}, var)
            var.registers(['node', 'this$1', 'i', 'dom', 'options', 'wrap'])
            var.put('this$1', var.get(u"this"))
            if PyJsStrictEq(var.get('options'),PyJsComma(Js(0.0), Js(None))):
                PyJs_Object_342_ = Js({})
                var.put('options', PyJs_Object_342_)
            var.put('dom', var.get(u"this").callprop('serializeNode', var.get('node'), var.get('options')))
            #for JS loop
            var.put('i', (var.get('node').get('marks').get('length')-Js(1.0)))
            while (var.get('i')>=Js(0.0)):
                try:
                    var.put('wrap', var.get('this$1').callprop('serializeMark', var.get('node').get('marks').get(var.get('i')), var.get('node').get('isInline'), var.get('options')))
                    if var.get('wrap'):
                        (var.get('wrap').get('contentDOM') or var.get('wrap').get('dom')).callprop('appendChild', var.get('dom'))
                        var.put('dom', var.get('wrap').get('dom'))
                finally:
                        (var.put('i',Js(var.get('i').to_number())-Js(1))+Js(1))
            return var.get('dom')
        PyJs_serializeNodeAndMarks_341_._set_name('serializeNodeAndMarks')
        var.get('DOMSerializer').get('prototype').put('serializeNodeAndMarks', PyJs_serializeNodeAndMarks_341_)
        @Js
        def PyJs_serializeMark_343_(mark, inline, options, this, arguments, var=var):
            var = Scope({'mark':mark, 'inline':inline, 'options':options, 'this':this, 'arguments':arguments, 'serializeMark':PyJs_serializeMark_343_}, var)
            var.registers(['inline', 'toDOM', 'options', 'mark'])
            if PyJsStrictEq(var.get('options'),PyJsComma(Js(0.0), Js(None))):
                PyJs_Object_344_ = Js({})
                var.put('options', PyJs_Object_344_)
            var.put('toDOM', var.get(u"this").get('marks').get(var.get('mark').get('type').get('name')))
            return (var.get('toDOM') and var.get('DOMSerializer').callprop('renderSpec', var.get('doc')(var.get('options')), var.get('toDOM')(var.get('mark'), var.get('inline'))))
        PyJs_serializeMark_343_._set_name('serializeMark')
        var.get('DOMSerializer').get('prototype').put('serializeMark', PyJs_serializeMark_343_)
        @Js
        def PyJs_renderSpec_345_(doc, structure, this, arguments, var=var):
            var = Scope({'doc':doc, 'structure':structure, 'this':this, 'arguments':arguments, 'renderSpec':PyJs_renderSpec_345_}, var)
            var.registers(['child', 'doc', 'inner', 'attrs', 'contentDOM', 'ref', 'i', 'start', 'structure', 'dom', 'name', 'innerContent'])
            if (var.get('structure',throw=False).typeof()==Js('string')):
                PyJs_Object_346_ = Js({'dom':var.get('doc').callprop('createTextNode', var.get('structure'))})
                return PyJs_Object_346_
            if (var.get('structure').get('nodeType')!=var.get(u"null")):
                PyJs_Object_347_ = Js({'dom':var.get('structure')})
                return PyJs_Object_347_
            var.put('dom', var.get('doc').callprop('createElement', var.get('structure').get('0')))
            var.put('contentDOM', var.get(u"null"))
            var.put('attrs', var.get('structure').get('1'))
            var.put('start', Js(1.0))
            if (((var.get('attrs') and (var.get('attrs',throw=False).typeof()==Js('object'))) and (var.get('attrs').get('nodeType')==var.get(u"null"))) and var.get('Array').callprop('isArray', var.get('attrs')).neg()):
                var.put('start', Js(2.0))
                for PyJsTemp in var.get('attrs'):
                    var.put('name', PyJsTemp)
                    if (var.get('name')==Js('style')):
                        var.get('dom').get('style').put('cssText', var.get('attrs').get(var.get('name')))
                    else:
                        if (var.get('attrs').get(var.get('name'))!=var.get(u"null")):
                            var.get('dom').callprop('setAttribute', var.get('name'), var.get('attrs').get(var.get('name')))
            #for JS loop
            var.put('i', var.get('start'))
            while (var.get('i')<var.get('structure').get('length')):
                try:
                    var.put('child', var.get('structure').get(var.get('i')))
                    if PyJsStrictEq(var.get('child'),Js(0.0)):
                        if ((var.get('i')<(var.get('structure').get('length')-Js(1.0))) or (var.get('i')>var.get('start'))):
                            PyJsTempException = JsToPyException(var.get('RangeError').create(Js('Content hole must be the only child of its parent node')))
                            raise PyJsTempException
                        PyJs_Object_348_ = Js({'dom':var.get('dom'),'contentDOM':var.get('dom')})
                        return PyJs_Object_348_
                    else:
                        var.put('ref', var.get('DOMSerializer').callprop('renderSpec', var.get('doc'), var.get('child')))
                        var.put('inner', var.get('ref').get('dom'))
                        var.put('innerContent', var.get('ref').get('contentDOM'))
                        var.get('dom').callprop('appendChild', var.get('inner'))
                        if var.get('innerContent'):
                            if var.get('contentDOM'):
                                PyJsTempException = JsToPyException(var.get('RangeError').create(Js('Multiple content holes')))
                                raise PyJsTempException
                            var.put('contentDOM', var.get('innerContent'))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            PyJs_Object_349_ = Js({'dom':var.get('dom'),'contentDOM':var.get('contentDOM')})
            return PyJs_Object_349_
        PyJs_renderSpec_345_._set_name('renderSpec')
        var.get('DOMSerializer').put('renderSpec', PyJs_renderSpec_345_)
        @Js
        def PyJs_fromSchema_350_(schema, this, arguments, var=var):
            var = Scope({'schema':schema, 'this':this, 'arguments':arguments, 'fromSchema':PyJs_fromSchema_350_}, var)
            var.registers(['schema'])
            return (var.get('schema').get('cached').get('domSerializer') or var.get('schema').get('cached').put('domSerializer', var.get('DOMSerializer').create(var.get(u"this").callprop('nodesFromSchema', var.get('schema')), var.get(u"this").callprop('marksFromSchema', var.get('schema')))))
        PyJs_fromSchema_350_._set_name('fromSchema')
        var.get('DOMSerializer').put('fromSchema', PyJs_fromSchema_350_)
        @Js
        def PyJs_nodesFromSchema_351_(schema, this, arguments, var=var):
            var = Scope({'schema':schema, 'this':this, 'arguments':arguments, 'nodesFromSchema':PyJs_nodesFromSchema_351_}, var)
            var.registers(['schema', 'result'])
            var.put('result', var.get('gatherToDOM')(var.get('schema').get('nodes')))
            if var.get('result').get('text').neg():
                @Js
                def PyJs_anonymous_352_(node, this, arguments, var=var):
                    var = Scope({'node':node, 'this':this, 'arguments':arguments}, var)
                    var.registers(['node'])
                    return var.get('node').get('text')
                PyJs_anonymous_352_._set_name('anonymous')
                var.get('result').put('text', PyJs_anonymous_352_)
            return var.get('result')
        PyJs_nodesFromSchema_351_._set_name('nodesFromSchema')
        var.get('DOMSerializer').put('nodesFromSchema', PyJs_nodesFromSchema_351_)
        @Js
        def PyJs_marksFromSchema_353_(schema, this, arguments, var=var):
            var = Scope({'schema':schema, 'this':this, 'arguments':arguments, 'marksFromSchema':PyJs_marksFromSchema_353_}, var)
            var.registers(['schema'])
            return var.get('gatherToDOM')(var.get('schema').get('marks'))
        PyJs_marksFromSchema_353_._set_name('marksFromSchema')
        var.get('DOMSerializer').put('marksFromSchema', PyJs_marksFromSchema_353_)
        pass
        pass
        var.get('exports').put('Node', var.get('Node'))
        var.get('exports').put('ResolvedPos', var.get('ResolvedPos'))
        var.get('exports').put('NodeRange', var.get('NodeRange'))
        var.get('exports').put('Fragment', var.get('Fragment'))
        var.get('exports').put('Slice', var.get('Slice'))
        var.get('exports').put('ReplaceError', var.get('ReplaceError'))
        var.get('exports').put('Mark', var.get('Mark'))
        var.get('exports').put('Schema', var.get('Schema'))
        var.get('exports').put('NodeType', var.get('NodeType'))
        var.get('exports').put('MarkType', var.get('MarkType'))
        var.get('exports').put('ContentMatch', var.get('ContentMatch'))
        var.get('exports').put('DOMParser', var.get('DOMParser'))
        var.get('exports').put('DOMSerializer', var.get('DOMSerializer'))
    PyJs_anonymous_17_._set_name('anonymous')
    var.put('dist', var.get('createCommonjsModule')(PyJs_anonymous_17_))
    var.get('unwrapExports')(var.get('dist'))
    var.put('dist_1', var.get('dist').get('Node'))
    var.put('dist_2', var.get('dist').get('ResolvedPos'))
    var.put('dist_3', var.get('dist').get('NodeRange'))
    var.put('dist_4', var.get('dist').get('Fragment'))
    var.put('dist_5', var.get('dist').get('Slice'))
    var.put('dist_6', var.get('dist').get('ReplaceError'))
    var.put('dist_7', var.get('dist').get('Mark'))
    var.put('dist_8', var.get('dist').get('Schema'))
    var.put('dist_9', var.get('dist').get('NodeType'))
    var.put('dist_10', var.get('dist').get('MarkType'))
    var.put('dist_11', var.get('dist').get('ContentMatch'))
    var.put('dist_12', var.get('dist').get('DOMParser'))
    var.put('dist_13', var.get('dist').get('DOMSerializer'))
    @Js
    def PyJs_anonymous_355_(module, exports, this, arguments, var=var):
        var = Scope({'module':module, 'exports':exports, 'this':this, 'arguments':arguments}, var)
        var.registers(['ReplaceAroundStep', 'factor16', 'canChangeType', 'fitRightSeparate', 'closeNodeEnd', 'joinPoint', 'exports', 'closeNodeStart', 'Frontier', 'StepResult', 'StepMap', 'canJoin', 'closeFragmentEnd', 'replaceStep', 'normalizeSlice', 'canMoveText', 'prototypeAccessors', 'insertPoint', 'dropPoint', 'nodeRight', 'findWrappingInside', 'lower16', 'withAttrs', 'mapFragment', 'recoverOffset', 'module', 'findWrappingOutside', 'fitRight', 'closeFragment', 'mustOverride', 'RemoveMarkStep', 'canCut', 'recoverIndex', 'joinable', 'fitLeftInner', 'fitLeft', 'makeRecover', 'Mapping', 'contentBetween', 'findWrapping', 'fitsTrivially', 'liftTarget', 'placeSlice', 'TransformError', 'Transform', 'canSplit', 'fitRightJoin', 'coveredDepths', 'AddMarkStep', 'ReplaceStep', 'MapResult', 'fitRightClosed', 'stepsByID', 'Step'])
        @Js
        def PyJsHoisted_makeRecover_(index, offset, this, arguments, var=var):
            var = Scope({'index':index, 'offset':offset, 'this':this, 'arguments':arguments}, var)
            var.registers(['offset', 'index'])
            return (var.get('index')+(var.get('offset')*var.get('factor16')))
        PyJsHoisted_makeRecover_.func_name = 'makeRecover'
        var.put('makeRecover', PyJsHoisted_makeRecover_)
        @Js
        def PyJsHoisted_recoverIndex_(value, this, arguments, var=var):
            var = Scope({'value':value, 'this':this, 'arguments':arguments}, var)
            var.registers(['value'])
            return (var.get('value')&var.get('lower16'))
        PyJsHoisted_recoverIndex_.func_name = 'recoverIndex'
        var.put('recoverIndex', PyJsHoisted_recoverIndex_)
        @Js
        def PyJsHoisted_recoverOffset_(value, this, arguments, var=var):
            var = Scope({'value':value, 'this':this, 'arguments':arguments}, var)
            var.registers(['value'])
            return ((var.get('value')-(var.get('value')&var.get('lower16')))/var.get('factor16'))
        PyJsHoisted_recoverOffset_.func_name = 'recoverOffset'
        var.put('recoverOffset', PyJsHoisted_recoverOffset_)
        @Js
        def PyJsHoisted_TransformError_(message, this, arguments, var=var):
            var = Scope({'message':message, 'this':this, 'arguments':arguments}, var)
            var.registers(['err', 'message'])
            var.put('err', var.get('Error').callprop('call', var.get(u"this"), var.get('message')))
            var.get('err').put('__proto__', var.get('TransformError').get('prototype'))
            return var.get('err')
        PyJsHoisted_TransformError_.func_name = 'TransformError'
        var.put('TransformError', PyJsHoisted_TransformError_)
        @Js
        def PyJsHoisted_mustOverride_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            PyJsTempException = JsToPyException(var.get('Error').create(Js('Override me')))
            raise PyJsTempException
        PyJsHoisted_mustOverride_.func_name = 'mustOverride'
        var.put('mustOverride', PyJsHoisted_mustOverride_)
        @Js
        def PyJsHoisted_contentBetween_(doc, PyJsArg_66726f6d_, to, this, arguments, var=var):
            var = Scope({'doc':doc, 'from':PyJsArg_66726f6d_, 'to':to, 'this':this, 'arguments':arguments}, var)
            var.registers(['doc', '$from', 'depth', 'dist$$1', 'next', 'to', 'from'])
            var.put('$from', var.get('doc').callprop('resolve', var.get('from')))
            var.put('dist$$1', (var.get('to')-var.get('from')))
            var.put('depth', var.get('$from').get('depth'))
            while (((var.get('dist$$1')>Js(0.0)) and (var.get('depth')>Js(0.0))) and (var.get('$from').callprop('indexAfter', var.get('depth'))==var.get('$from').callprop('node', var.get('depth')).get('childCount'))):
                (var.put('depth',Js(var.get('depth').to_number())-Js(1))+Js(1))
                (var.put('dist$$1',Js(var.get('dist$$1').to_number())-Js(1))+Js(1))
            if (var.get('dist$$1')>Js(0.0)):
                var.put('next', var.get('$from').callprop('node', var.get('depth')).callprop('maybeChild', var.get('$from').callprop('indexAfter', var.get('depth'))))
                while (var.get('dist$$1')>Js(0.0)):
                    if (var.get('next').neg() or var.get('next').get('isLeaf')):
                        return Js(True)
                    var.put('next', var.get('next').get('firstChild'))
                    (var.put('dist$$1',Js(var.get('dist$$1').to_number())-Js(1))+Js(1))
            return Js(False)
        PyJsHoisted_contentBetween_.func_name = 'contentBetween'
        var.put('contentBetween', PyJsHoisted_contentBetween_)
        @Js
        def PyJsHoisted_canCut_(node, start, end, this, arguments, var=var):
            var = Scope({'node':node, 'start':start, 'end':end, 'this':this, 'arguments':arguments}, var)
            var.registers(['end', 'start', 'node'])
            return (((var.get('start')==Js(0.0)) or var.get('node').callprop('canReplace', var.get('start'), var.get('node').get('childCount'))) and ((var.get('end')==var.get('node').get('childCount')) or var.get('node').callprop('canReplace', Js(0.0), var.get('end'))))
        PyJsHoisted_canCut_.func_name = 'canCut'
        var.put('canCut', PyJsHoisted_canCut_)
        @Js
        def PyJsHoisted_liftTarget_(range, this, arguments, var=var):
            var = Scope({'range':range, 'this':this, 'arguments':arguments}, var)
            var.registers(['node', 'endIndex', 'range', 'depth', 'content', 'index', 'parent'])
            var.put('parent', var.get('range').get('parent'))
            var.put('content', var.get('parent').get('content').callprop('cutByIndex', var.get('range').get('startIndex'), var.get('range').get('endIndex')))
            #for JS loop
            var.put('depth', var.get('range').get('depth'))
            while 1:
                try:
                    var.put('node', var.get('range').get('$from').callprop('node', var.get('depth')))
                    var.put('index', var.get('range').get('$from').callprop('index', var.get('depth')))
                    var.put('endIndex', var.get('range').get('$to').callprop('indexAfter', var.get('depth')))
                    if ((var.get('depth')<var.get('range').get('depth')) and var.get('node').callprop('canReplace', var.get('index'), var.get('endIndex'), var.get('content'))):
                        return var.get('depth')
                    if (((var.get('depth')==Js(0.0)) or var.get('node').get('type').get('spec').get('isolating')) or var.get('canCut')(var.get('node'), var.get('index'), var.get('endIndex')).neg()):
                        break
                finally:
                        var.put('depth',Js(var.get('depth').to_number())-Js(1))
        PyJsHoisted_liftTarget_.func_name = 'liftTarget'
        var.put('liftTarget', PyJsHoisted_liftTarget_)
        @Js
        def PyJsHoisted_findWrapping_(range, nodeType, attrs, innerRange, this, arguments, var=var):
            var = Scope({'range':range, 'nodeType':nodeType, 'attrs':attrs, 'innerRange':innerRange, 'this':this, 'arguments':arguments}, var)
            var.registers(['nodeType', 'range', 'attrs', 'innerRange', 'inner', 'around'])
            if PyJsStrictEq(var.get('innerRange'),PyJsComma(Js(0.0), Js(None))):
                var.put('innerRange', var.get('range'))
            var.put('around', var.get('findWrappingOutside')(var.get('range'), var.get('nodeType')))
            var.put('inner', (var.get('around') and var.get('findWrappingInside')(var.get('innerRange'), var.get('nodeType'))))
            if var.get('inner').neg():
                return var.get(u"null")
            PyJs_Object_421_ = Js({'type':var.get('nodeType'),'attrs':var.get('attrs')})
            return var.get('around').callprop('map', var.get('withAttrs')).callprop('concat', PyJs_Object_421_).callprop('concat', var.get('inner').callprop('map', var.get('withAttrs')))
        PyJsHoisted_findWrapping_.func_name = 'findWrapping'
        var.put('findWrapping', PyJsHoisted_findWrapping_)
        @Js
        def PyJsHoisted_withAttrs_(type, this, arguments, var=var):
            var = Scope({'type':type, 'this':this, 'arguments':arguments}, var)
            var.registers(['type'])
            PyJs_Object_422_ = Js({'type':var.get('type'),'attrs':var.get(u"null")})
            return PyJs_Object_422_
        PyJsHoisted_withAttrs_.func_name = 'withAttrs'
        var.put('withAttrs', PyJsHoisted_withAttrs_)
        @Js
        def PyJsHoisted_findWrappingOutside_(range, type, this, arguments, var=var):
            var = Scope({'range':range, 'type':type, 'this':this, 'arguments':arguments}, var)
            var.registers(['startIndex', 'outer', 'endIndex', 'range', 'type', 'parent', 'around'])
            var.put('parent', var.get('range').get('parent'))
            var.put('startIndex', var.get('range').get('startIndex'))
            var.put('endIndex', var.get('range').get('endIndex'))
            var.put('around', var.get('parent').callprop('contentMatchAt', var.get('startIndex')).callprop('findWrapping', var.get('type')))
            if var.get('around').neg():
                return var.get(u"null")
            var.put('outer', (var.get('around').get('0') if var.get('around').get('length') else var.get('type')))
            return (var.get('around') if var.get('parent').callprop('canReplaceWith', var.get('startIndex'), var.get('endIndex'), var.get('outer')) else var.get(u"null"))
        PyJsHoisted_findWrappingOutside_.func_name = 'findWrappingOutside'
        var.put('findWrappingOutside', PyJsHoisted_findWrappingOutside_)
        @Js
        def PyJsHoisted_findWrappingInside_(range, type, this, arguments, var=var):
            var = Scope({'range':range, 'type':type, 'this':this, 'arguments':arguments}, var)
            var.registers(['startIndex', 'lastType', 'innerMatch', 'inside', 'endIndex', 'range', 'type', 'i', 'inner', 'parent'])
            var.put('parent', var.get('range').get('parent'))
            var.put('startIndex', var.get('range').get('startIndex'))
            var.put('endIndex', var.get('range').get('endIndex'))
            var.put('inner', var.get('parent').callprop('child', var.get('startIndex')))
            var.put('inside', var.get('type').get('contentMatch').callprop('findWrapping', var.get('inner').get('type')))
            if var.get('inside').neg():
                return var.get(u"null")
            var.put('lastType', (var.get('inside').get((var.get('inside').get('length')-Js(1.0))) if var.get('inside').get('length') else var.get('type')))
            var.put('innerMatch', var.get('lastType').get('contentMatch'))
            #for JS loop
            var.put('i', var.get('startIndex'))
            while (var.get('innerMatch') and (var.get('i')<var.get('endIndex'))):
                try:
                    var.put('innerMatch', var.get('innerMatch').callprop('matchType', var.get('parent').callprop('child', var.get('i')).get('type')))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            if (var.get('innerMatch').neg() or var.get('innerMatch').get('validEnd').neg()):
                return var.get(u"null")
            return var.get('inside')
        PyJsHoisted_findWrappingInside_.func_name = 'findWrappingInside'
        var.put('findWrappingInside', PyJsHoisted_findWrappingInside_)
        @Js
        def PyJsHoisted_canChangeType_(doc, pos, type, this, arguments, var=var):
            var = Scope({'doc':doc, 'pos':pos, 'type':type, 'this':this, 'arguments':arguments}, var)
            var.registers(['doc', 'type', 'index', 'pos', '$pos'])
            var.put('$pos', var.get('doc').callprop('resolve', var.get('pos')))
            var.put('index', var.get('$pos').callprop('index'))
            return var.get('$pos').get('parent').callprop('canReplaceWith', var.get('index'), (var.get('index')+Js(1.0)), var.get('type'))
        PyJsHoisted_canChangeType_.func_name = 'canChangeType'
        var.put('canChangeType', PyJsHoisted_canChangeType_)
        @Js
        def PyJsHoisted_canSplit_(doc, pos, depth, typesAfter, this, arguments, var=var):
            var = Scope({'doc':doc, 'pos':pos, 'depth':depth, 'typesAfter':typesAfter, 'this':this, 'arguments':arguments}, var)
            var.registers(['baseType', 'doc', 'innerType', 'pos', 'node', 'typesAfter', 'index$1', 'base', 'after', 'depth', 'i', 'rest', 'index', 'd', '$pos'])
            if PyJsStrictEq(var.get('depth'),PyJsComma(Js(0.0), Js(None))):
                var.put('depth', Js(1.0))
            var.put('$pos', var.get('doc').callprop('resolve', var.get('pos')))
            var.put('base', (var.get('$pos').get('depth')-var.get('depth')))
            var.put('innerType', ((var.get('typesAfter') and var.get('typesAfter').get((var.get('typesAfter').get('length')-Js(1.0)))) or var.get('$pos').get('parent')))
            def PyJs_LONG_427_(var=var):
                return ((((var.get('base')<Js(0.0)) or var.get('$pos').get('parent').get('type').get('spec').get('isolating')) or var.get('$pos').get('parent').callprop('canReplace', var.get('$pos').callprop('index'), var.get('$pos').get('parent').get('childCount')).neg()) or var.get('innerType').get('type').callprop('validContent', var.get('$pos').get('parent').get('content').callprop('cutByIndex', var.get('$pos').callprop('index'), var.get('$pos').get('parent').get('childCount'))).neg())
            if PyJs_LONG_427_():
                return Js(False)
            #for JS loop
            var.put('d', (var.get('$pos').get('depth')-Js(1.0)))
            var.put('i', (var.get('depth')-Js(2.0)))
            while (var.get('d')>var.get('base')):
                try:
                    var.put('node', var.get('$pos').callprop('node', var.get('d')))
                    var.put('index$1', var.get('$pos').callprop('index', var.get('d')))
                    if var.get('node').get('type').get('spec').get('isolating'):
                        return Js(False)
                    var.put('rest', var.get('node').get('content').callprop('cutByIndex', var.get('index$1'), var.get('node').get('childCount')))
                    var.put('after', ((var.get('typesAfter') and var.get('typesAfter').get(var.get('i'))) or var.get('node')))
                    if (var.get('after')!=var.get('node')):
                        var.put('rest', var.get('rest').callprop('replaceChild', Js(0.0), var.get('after').get('type').callprop('create', var.get('after').get('attrs'))))
                    if (var.get('node').callprop('canReplace', (var.get('index$1')+Js(1.0)), var.get('node').get('childCount')).neg() or var.get('after').get('type').callprop('validContent', var.get('rest')).neg()):
                        return Js(False)
                finally:
                        PyJsComma((var.put('d',Js(var.get('d').to_number())-Js(1))+Js(1)),(var.put('i',Js(var.get('i').to_number())-Js(1))+Js(1)))
            var.put('index', var.get('$pos').callprop('indexAfter', var.get('base')))
            var.put('baseType', (var.get('typesAfter') and var.get('typesAfter').get('0')))
            return var.get('$pos').callprop('node', var.get('base')).callprop('canReplaceWith', var.get('index'), var.get('index'), (var.get('baseType').get('type') if var.get('baseType') else var.get('$pos').callprop('node', (var.get('base')+Js(1.0))).get('type')))
        PyJsHoisted_canSplit_.func_name = 'canSplit'
        var.put('canSplit', PyJsHoisted_canSplit_)
        @Js
        def PyJsHoisted_canJoin_(doc, pos, this, arguments, var=var):
            var = Scope({'doc':doc, 'pos':pos, 'this':this, 'arguments':arguments}, var)
            var.registers(['doc', 'index', 'pos', '$pos'])
            var.put('$pos', var.get('doc').callprop('resolve', var.get('pos')))
            var.put('index', var.get('$pos').callprop('index'))
            return (var.get('joinable')(var.get('$pos').get('nodeBefore'), var.get('$pos').get('nodeAfter')) and var.get('$pos').get('parent').callprop('canReplace', var.get('index'), (var.get('index')+Js(1.0))))
        PyJsHoisted_canJoin_.func_name = 'canJoin'
        var.put('canJoin', PyJsHoisted_canJoin_)
        @Js
        def PyJsHoisted_joinable_(a, b, this, arguments, var=var):
            var = Scope({'a':a, 'b':b, 'this':this, 'arguments':arguments}, var)
            var.registers(['a', 'b'])
            return (((var.get('a') and var.get('b')) and var.get('a').get('isLeaf').neg()) and var.get('a').callprop('canAppend', var.get('b')))
        PyJsHoisted_joinable_.func_name = 'joinable'
        var.put('joinable', PyJsHoisted_joinable_)
        @Js
        def PyJsHoisted_joinPoint_(doc, pos, dir, this, arguments, var=var):
            var = Scope({'doc':doc, 'pos':pos, 'dir':dir, 'this':this, 'arguments':arguments}, var)
            var.registers(['doc', 'before', 'after', 'pos', 'dir', 'd', '$pos'])
            if PyJsStrictEq(var.get('dir'),PyJsComma(Js(0.0), Js(None))):
                var.put('dir', (-Js(1.0)))
            var.put('$pos', var.get('doc').callprop('resolve', var.get('pos')))
            #for JS loop
            var.put('d', var.get('$pos').get('depth'))
            while 1:
                try:
                    var.put('before', PyJsComma(Js(0.0), Js(None)))
                    var.put('after', PyJsComma(Js(0.0), Js(None)))
                    if (var.get('d')==var.get('$pos').get('depth')):
                        var.put('before', var.get('$pos').get('nodeBefore'))
                        var.put('after', var.get('$pos').get('nodeAfter'))
                    else:
                        if (var.get('dir')>Js(0.0)):
                            var.put('before', var.get('$pos').callprop('node', (var.get('d')+Js(1.0))))
                            var.put('after', var.get('$pos').callprop('node', var.get('d')).callprop('maybeChild', (var.get('$pos').callprop('index', var.get('d'))+Js(1.0))))
                        else:
                            var.put('before', var.get('$pos').callprop('node', var.get('d')).callprop('maybeChild', (var.get('$pos').callprop('index', var.get('d'))-Js(1.0))))
                            var.put('after', var.get('$pos').callprop('node', (var.get('d')+Js(1.0))))
                    if ((var.get('before') and var.get('before').get('isTextblock').neg()) and var.get('joinable')(var.get('before'), var.get('after'))):
                        return var.get('pos')
                    if (var.get('d')==Js(0.0)):
                        break
                    var.put('pos', (var.get('$pos').callprop('before', var.get('d')) if (var.get('dir')<Js(0.0)) else var.get('$pos').callprop('after', var.get('d'))))
                finally:
                        (var.put('d',Js(var.get('d').to_number())-Js(1))+Js(1))
        PyJsHoisted_joinPoint_.func_name = 'joinPoint'
        var.put('joinPoint', PyJsHoisted_joinPoint_)
        @Js
        def PyJsHoisted_insertPoint_(doc, pos, nodeType, this, arguments, var=var):
            var = Scope({'doc':doc, 'pos':pos, 'nodeType':nodeType, 'this':this, 'arguments':arguments}, var)
            var.registers(['doc', 'd$1', 'index$1', 'nodeType', 'index', 'pos', 'd', '$pos'])
            var.put('$pos', var.get('doc').callprop('resolve', var.get('pos')))
            if var.get('$pos').get('parent').callprop('canReplaceWith', var.get('$pos').callprop('index'), var.get('$pos').callprop('index'), var.get('nodeType')):
                return var.get('pos')
            if (var.get('$pos').get('parentOffset')==Js(0.0)):
                #for JS loop
                var.put('d', (var.get('$pos').get('depth')-Js(1.0)))
                while (var.get('d')>=Js(0.0)):
                    try:
                        var.put('index', var.get('$pos').callprop('index', var.get('d')))
                        if var.get('$pos').callprop('node', var.get('d')).callprop('canReplaceWith', var.get('index'), var.get('index'), var.get('nodeType')):
                            return var.get('$pos').callprop('before', (var.get('d')+Js(1.0)))
                        if (var.get('index')>Js(0.0)):
                            return var.get(u"null")
                    finally:
                            (var.put('d',Js(var.get('d').to_number())-Js(1))+Js(1))
            if (var.get('$pos').get('parentOffset')==var.get('$pos').get('parent').get('content').get('size')):
                #for JS loop
                var.put('d$1', (var.get('$pos').get('depth')-Js(1.0)))
                while (var.get('d$1')>=Js(0.0)):
                    try:
                        var.put('index$1', var.get('$pos').callprop('indexAfter', var.get('d$1')))
                        if var.get('$pos').callprop('node', var.get('d$1')).callprop('canReplaceWith', var.get('index$1'), var.get('index$1'), var.get('nodeType')):
                            return var.get('$pos').callprop('after', (var.get('d$1')+Js(1.0)))
                        if (var.get('index$1')<var.get('$pos').callprop('node', var.get('d$1')).get('childCount')):
                            return var.get(u"null")
                    finally:
                            (var.put('d$1',Js(var.get('d$1').to_number())-Js(1))+Js(1))
        PyJsHoisted_insertPoint_.func_name = 'insertPoint'
        var.put('insertPoint', PyJsHoisted_insertPoint_)
        @Js
        def PyJsHoisted_dropPoint_(doc, pos, slice, this, arguments, var=var):
            var = Scope({'doc':doc, 'pos':pos, 'slice':slice, 'this':this, 'arguments':arguments}, var)
            var.registers(['insertPos', 'slice', 'doc', '$pos', 'content', 'i', 'pos', 'd', 'bias', 'pass'])
            var.put('$pos', var.get('doc').callprop('resolve', var.get('pos')))
            if var.get('slice').get('content').get('size').neg():
                return var.get('pos')
            var.put('content', var.get('slice').get('content'))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('slice').get('openStart')):
                try:
                    var.put('content', var.get('content').get('firstChild').get('content'))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            #for JS loop
            var.put('pass', Js(1.0))
            while (var.get('pass')<=(Js(2.0) if ((var.get('slice').get('openStart')==Js(0.0)) and var.get('slice').get('size')) else Js(1.0))):
                try:
                    #for JS loop
                    var.put('d', var.get('$pos').get('depth'))
                    while (var.get('d')>=Js(0.0)):
                        try:
                            var.put('bias', (Js(0.0) if (var.get('d')==var.get('$pos').get('depth')) else ((-Js(1.0)) if (var.get('$pos').get('pos')<=((var.get('$pos').callprop('start', (var.get('d')+Js(1.0)))+var.get('$pos').callprop('end', (var.get('d')+Js(1.0))))/Js(2.0))) else Js(1.0))))
                            var.put('insertPos', (var.get('$pos').callprop('index', var.get('d'))+(Js(1.0) if (var.get('bias')>Js(0.0)) else Js(0.0))))
                            if (var.get('$pos').callprop('node', var.get('d')).callprop('canReplace', var.get('insertPos'), var.get('insertPos'), var.get('content')) if (var.get('pass')==Js(1.0)) else var.get('$pos').callprop('node', var.get('d')).callprop('contentMatchAt', var.get('insertPos')).callprop('findWrapping', var.get('content').get('firstChild').get('type'))):
                                return (var.get('$pos').get('pos') if (var.get('bias')==Js(0.0)) else (var.get('$pos').callprop('before', (var.get('d')+Js(1.0))) if (var.get('bias')<Js(0.0)) else var.get('$pos').callprop('after', (var.get('d')+Js(1.0)))))
                        finally:
                                (var.put('d',Js(var.get('d').to_number())-Js(1))+Js(1))
                finally:
                        (var.put('pass',Js(var.get('pass').to_number())+Js(1))-Js(1))
            return var.get(u"null")
        PyJsHoisted_dropPoint_.func_name = 'dropPoint'
        var.put('dropPoint', PyJsHoisted_dropPoint_)
        @Js
        def PyJsHoisted_mapFragment_(fragment, f, parent, this, arguments, var=var):
            var = Scope({'fragment':fragment, 'f':f, 'parent':parent, 'this':this, 'arguments':arguments}, var)
            var.registers(['child', 'mapped', 'f', 'i', 'fragment', 'parent'])
            var.put('mapped', Js([]))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('fragment').get('childCount')):
                try:
                    var.put('child', var.get('fragment').callprop('child', var.get('i')))
                    if var.get('child').get('content').get('size'):
                        var.put('child', var.get('child').callprop('copy', var.get('mapFragment')(var.get('child').get('content'), var.get('f'), var.get('child'))))
                    if var.get('child').get('isInline'):
                        var.put('child', var.get('f')(var.get('child'), var.get('parent'), var.get('i')))
                    var.get('mapped').callprop('push', var.get('child'))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return var.get('dist').get('Fragment').callprop('fromArray', var.get('mapped'))
        PyJsHoisted_mapFragment_.func_name = 'mapFragment'
        var.put('mapFragment', PyJsHoisted_mapFragment_)
        @Js
        def PyJsHoisted_replaceStep_(doc, PyJsArg_66726f6d_, to, slice, this, arguments, var=var):
            var = Scope({'doc':doc, 'from':PyJsArg_66726f6d_, 'to':to, 'slice':slice, 'this':this, 'arguments':arguments}, var)
            var.registers(['$to', 'slice', 'doc', 'fittedAfter', '$from', 'from', 'placed', 'after', 'fitted', 'fittedLeft', 'to', 'd'])
            if PyJsStrictEq(var.get('to'),PyJsComma(Js(0.0), Js(None))):
                var.put('to', var.get('from'))
            if PyJsStrictEq(var.get('slice'),PyJsComma(Js(0.0), Js(None))):
                var.put('slice', var.get('dist').get('Slice').get('empty'))
            if ((var.get('from')==var.get('to')) and var.get('slice').get('size').neg()):
                return var.get(u"null")
            var.put('$from', var.get('doc').callprop('resolve', var.get('from')))
            var.put('$to', var.get('doc').callprop('resolve', var.get('to')))
            if var.get('fitsTrivially')(var.get('$from'), var.get('$to'), var.get('slice')):
                return var.get('ReplaceStep').create(var.get('from'), var.get('to'), var.get('slice'))
            var.put('placed', var.get('placeSlice')(var.get('$from'), var.get('slice')))
            var.put('fittedLeft', var.get('fitLeft')(var.get('$from'), var.get('placed')))
            var.put('fitted', var.get('fitRight')(var.get('$from'), var.get('$to'), var.get('fittedLeft')))
            if var.get('fitted').neg():
                return var.get(u"null")
            if ((var.get('fittedLeft').get('size')!=var.get('fitted').get('size')) and var.get('canMoveText')(var.get('$from'), var.get('$to'), var.get('fittedLeft'))):
                var.put('d', var.get('$to').get('depth'))
                var.put('after', var.get('$to').callprop('after', var.get('d')))
                while ((var.get('d')>Js(1.0)) and (var.get('after')==var.get('$to').callprop('end', var.put('d',Js(var.get('d').to_number())-Js(1))))):
                    var.put('after',Js(var.get('after').to_number())+Js(1))
                var.put('fittedAfter', var.get('fitRight')(var.get('$from'), var.get('doc').callprop('resolve', var.get('after')), var.get('fittedLeft')))
                if var.get('fittedAfter'):
                    return var.get('ReplaceAroundStep').create(var.get('from'), var.get('after'), var.get('to'), var.get('$to').callprop('end'), var.get('fittedAfter'), var.get('fittedLeft').get('size'))
            return (var.get('ReplaceStep').create(var.get('from'), var.get('to'), var.get('fitted')) if (var.get('fitted').get('size') or (var.get('from')!=var.get('to'))) else var.get(u"null"))
        PyJsHoisted_replaceStep_.func_name = 'replaceStep'
        var.put('replaceStep', PyJsHoisted_replaceStep_)
        @Js
        def PyJsHoisted_fitLeftInner_(PyJsArg_2466726f6d_, depth, placed, placedBelow, this, arguments, var=var):
            var = Scope({'$from':PyJsArg_2466726f6d_, 'depth':depth, 'placed':placed, 'placedBelow':placedBelow, 'this':this, 'arguments':arguments}, var)
            var.registers(['placedBelow', 'openEnd', '$from', 'placed', 'depth', 'content', 'placedHere', 'inner'])
            var.put('content', var.get('dist').get('Fragment').get('empty'))
            var.put('openEnd', Js(0.0))
            var.put('placedHere', var.get('placed').get(var.get('depth')))
            if (var.get('$from').get('depth')>var.get('depth')):
                var.put('inner', var.get('fitLeftInner')(var.get('$from'), (var.get('depth')+Js(1.0)), var.get('placed'), (var.get('placedBelow') or var.get('placedHere'))))
                var.put('openEnd', (var.get('inner').get('openEnd')+Js(1.0)))
                var.put('content', var.get('dist').get('Fragment').callprop('from', var.get('$from').callprop('node', (var.get('depth')+Js(1.0))).callprop('copy', var.get('inner').get('content'))))
            if var.get('placedHere'):
                var.put('content', var.get('content').callprop('append', var.get('placedHere').get('content')))
                var.put('openEnd', var.get('placedHere').get('openEnd'))
            if var.get('placedBelow'):
                var.put('content', var.get('content').callprop('append', var.get('$from').callprop('node', var.get('depth')).callprop('contentMatchAt', var.get('$from').callprop('indexAfter', var.get('depth'))).callprop('fillBefore', var.get('dist').get('Fragment').get('empty'), Js(True))))
                var.put('openEnd', Js(0.0))
            PyJs_Object_461_ = Js({'content':var.get('content'),'openEnd':var.get('openEnd')})
            return PyJs_Object_461_
        PyJsHoisted_fitLeftInner_.func_name = 'fitLeftInner'
        var.put('fitLeftInner', PyJsHoisted_fitLeftInner_)
        @Js
        def PyJsHoisted_fitLeft_(PyJsArg_2466726f6d_, placed, this, arguments, var=var):
            var = Scope({'$from':PyJsArg_2466726f6d_, 'placed':placed, 'this':this, 'arguments':arguments}, var)
            var.registers(['openEnd', '$from', 'placed', 'ref', 'content'])
            var.put('ref', var.get('fitLeftInner')(var.get('$from'), Js(0.0), var.get('placed'), Js(False)))
            var.put('content', var.get('ref').get('content'))
            var.put('openEnd', var.get('ref').get('openEnd'))
            return var.get('dist').get('Slice').create(var.get('content'), var.get('$from').get('depth'), (var.get('openEnd') or Js(0.0)))
        PyJsHoisted_fitLeft_.func_name = 'fitLeft'
        var.put('fitLeft', PyJsHoisted_fitLeft_)
        @Js
        def PyJsHoisted_fitRightJoin_(content, parent, PyJsArg_2466726f6d_, PyJsArg_24746f_, depth, openStart, openEnd, this, arguments, var=var):
            var = Scope({'content':content, 'parent':parent, '$from':PyJsArg_2466726f6d_, '$to':PyJsArg_24746f_, 'depth':depth, 'openStart':openStart, 'openEnd':openEnd, 'this':this, 'arguments':arguments}, var)
            var.registers(['$to', 'joinable$1', 'match', 'openStart', 'openEnd', 'toIndex', 'last', '$from', 'count', 'after', 'depth', 'content', 'matchCount', 'i', 'parentNode', 'closed', 'inner', 'parent', 'toNode', 'joinable'])
            var.put('count', var.get('content').get('childCount'))
            var.put('matchCount', (var.get('count')-(Js(1.0) if (var.get('openEnd')>Js(0.0)) else Js(0.0))))
            var.put('parentNode', (var.get('parent') if (var.get('openStart')<Js(0.0)) else var.get('$from').callprop('node', var.get('depth'))))
            if (var.get('openStart')<Js(0.0)):
                var.put('match', var.get('parentNode').callprop('contentMatchAt', var.get('matchCount')))
            else:
                if ((var.get('count')==Js(1.0)) and (var.get('openEnd')>Js(0.0))):
                    var.put('match', var.get('parentNode').callprop('contentMatchAt', (var.get('$from').callprop('index', var.get('depth')) if var.get('openStart') else var.get('$from').callprop('indexAfter', var.get('depth')))))
                else:
                    var.put('match', var.get('parentNode').callprop('contentMatchAt', var.get('$from').callprop('indexAfter', var.get('depth'))).callprop('matchFragment', var.get('content'), (Js(1.0) if ((var.get('count')>Js(0.0)) and var.get('openStart')) else Js(0.0)), var.get('matchCount')))
            var.put('toNode', var.get('$to').callprop('node', var.get('depth')))
            if ((var.get('openEnd')>Js(0.0)) and (var.get('depth')<var.get('$to').get('depth'))):
                var.put('after', var.get('toNode').get('content').callprop('cutByIndex', var.get('$to').callprop('indexAfter', var.get('depth'))).callprop('addToStart', var.get('content').get('lastChild')))
                var.put('joinable$1', var.get('match').callprop('fillBefore', var.get('after'), Js(True)))
                if (((var.get('joinable$1') and var.get('joinable$1').get('size')) and (var.get('openStart')>Js(0.0))) and (var.get('count')==Js(1.0))):
                    var.put('joinable$1', var.get(u"null"))
                if var.get('joinable$1'):
                    var.put('inner', var.get('fitRightJoin')(var.get('content').get('lastChild').get('content'), var.get('content').get('lastChild'), var.get('$from'), var.get('$to'), (var.get('depth')+Js(1.0)), ((var.get('openStart')-Js(1.0)) if (var.get('count')==Js(1.0)) else (-Js(1.0))), (var.get('openEnd')-Js(1.0))))
                    if var.get('inner'):
                        var.put('last', var.get('content').get('lastChild').callprop('copy', var.get('inner')))
                        if var.get('joinable$1').get('size'):
                            return var.get('content').callprop('cutByIndex', Js(0.0), (var.get('count')-Js(1.0))).callprop('append', var.get('joinable$1')).callprop('addToEnd', var.get('last'))
                        else:
                            return var.get('content').callprop('replaceChild', (var.get('count')-Js(1.0)), var.get('last'))
            if (var.get('openEnd')>Js(0.0)):
                var.put('match', var.get('match').callprop('matchType', (var.get('$from').callprop('node', (var.get('depth')+Js(1.0))) if ((var.get('count')==Js(1.0)) and (var.get('openStart')>Js(0.0))) else var.get('content').get('lastChild')).get('type')))
            var.put('toIndex', var.get('$to').callprop('index', var.get('depth')))
            if ((var.get('toIndex')==var.get('toNode').get('childCount')) and var.get('toNode').get('type').callprop('compatibleContent', var.get('parent').get('type')).neg()):
                return var.get(u"null")
            var.put('joinable', var.get('match').callprop('fillBefore', var.get('toNode').get('content'), Js(True), var.get('toIndex')))
            #for JS loop
            var.put('i', var.get('toIndex'))
            while (var.get('joinable') and (var.get('i')<var.get('toNode').get('content').get('childCount'))):
                try:
                    if var.get('parentNode').get('type').callprop('allowsMarks', var.get('toNode').get('content').callprop('child', var.get('i')).get('marks')).neg():
                        var.put('joinable', var.get(u"null"))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            if var.get('joinable').neg():
                return var.get(u"null")
            if (var.get('openEnd')>Js(0.0)):
                var.put('closed', var.get('fitRightClosed')(var.get('content').get('lastChild'), (var.get('openEnd')-Js(1.0)), var.get('$from'), (var.get('depth')+Js(1.0)), ((var.get('openStart')-Js(1.0)) if (var.get('count')==Js(1.0)) else (-Js(1.0)))))
                var.put('content', var.get('content').callprop('replaceChild', (var.get('count')-Js(1.0)), var.get('closed')))
            var.put('content', var.get('content').callprop('append', var.get('joinable')))
            if (var.get('$to').get('depth')>var.get('depth')):
                var.put('content', var.get('content').callprop('addToEnd', var.get('fitRightSeparate')(var.get('$to'), (var.get('depth')+Js(1.0)))))
            return var.get('content')
        PyJsHoisted_fitRightJoin_.func_name = 'fitRightJoin'
        var.put('fitRightJoin', PyJsHoisted_fitRightJoin_)
        @Js
        def PyJsHoisted_fitRightClosed_(node, openEnd, PyJsArg_2466726f6d_, depth, openStart, this, arguments, var=var):
            var = Scope({'node':node, 'openEnd':openEnd, '$from':PyJsArg_2466726f6d_, 'depth':depth, 'openStart':openStart, 'this':this, 'arguments':arguments}, var)
            var.registers(['match', 'openStart', 'node', 'openEnd', '$from', 'depth', 'content', 'closed', 'count'])
            var.put('content', var.get('node').get('content'))
            var.put('count', var.get('content').get('childCount'))
            if (var.get('openStart')>=Js(0.0)):
                var.put('match', var.get('$from').callprop('node', var.get('depth')).callprop('contentMatchAt', var.get('$from').callprop('indexAfter', var.get('depth'))).callprop('matchFragment', var.get('content'), (Js(1.0) if (var.get('openStart')>Js(0.0)) else Js(0.0)), var.get('count')))
            else:
                var.put('match', var.get('node').callprop('contentMatchAt', var.get('count')))
            if (var.get('openEnd')>Js(0.0)):
                var.put('closed', var.get('fitRightClosed')(var.get('content').get('lastChild'), (var.get('openEnd')-Js(1.0)), var.get('$from'), (var.get('depth')+Js(1.0)), ((var.get('openStart')-Js(1.0)) if (var.get('count')==Js(1.0)) else (-Js(1.0)))))
                var.put('content', var.get('content').callprop('replaceChild', (var.get('count')-Js(1.0)), var.get('closed')))
            return var.get('node').callprop('copy', var.get('content').callprop('append', var.get('match').callprop('fillBefore', var.get('dist').get('Fragment').get('empty'), Js(True))))
        PyJsHoisted_fitRightClosed_.func_name = 'fitRightClosed'
        var.put('fitRightClosed', PyJsHoisted_fitRightClosed_)
        @Js
        def PyJsHoisted_fitRightSeparate_(PyJsArg_24746f_, depth, this, arguments, var=var):
            var = Scope({'$to':PyJsArg_24746f_, 'depth':depth, 'this':this, 'arguments':arguments}, var)
            var.registers(['depth', '$to', 'fill', 'node'])
            var.put('node', var.get('$to').callprop('node', var.get('depth')))
            var.put('fill', var.get('node').callprop('contentMatchAt', Js(0.0)).callprop('fillBefore', var.get('node').get('content'), Js(True), var.get('$to').callprop('index', var.get('depth'))))
            if (var.get('$to').get('depth')>var.get('depth')):
                var.put('fill', var.get('fill').callprop('addToEnd', var.get('fitRightSeparate')(var.get('$to'), (var.get('depth')+Js(1.0)))))
            return var.get('node').callprop('copy', var.get('fill'))
        PyJsHoisted_fitRightSeparate_.func_name = 'fitRightSeparate'
        var.put('fitRightSeparate', PyJsHoisted_fitRightSeparate_)
        @Js
        def PyJsHoisted_normalizeSlice_(content, openStart, openEnd, this, arguments, var=var):
            var = Scope({'content':content, 'openStart':openStart, 'openEnd':openEnd, 'this':this, 'arguments':arguments}, var)
            var.registers(['content', 'openStart', 'openEnd'])
            while (((var.get('openStart')>Js(0.0)) and (var.get('openEnd')>Js(0.0))) and (var.get('content').get('childCount')==Js(1.0))):
                var.put('content', var.get('content').get('firstChild').get('content'))
                (var.put('openStart',Js(var.get('openStart').to_number())-Js(1))+Js(1))
                (var.put('openEnd',Js(var.get('openEnd').to_number())-Js(1))+Js(1))
            return var.get('dist').get('Slice').create(var.get('content'), var.get('openStart'), var.get('openEnd'))
        PyJsHoisted_normalizeSlice_.func_name = 'normalizeSlice'
        var.put('normalizeSlice', PyJsHoisted_normalizeSlice_)
        @Js
        def PyJsHoisted_fitRight_(PyJsArg_2466726f6d_, PyJsArg_24746f_, slice, this, arguments, var=var):
            var = Scope({'$from':PyJsArg_2466726f6d_, '$to':PyJsArg_24746f_, 'slice':slice, 'this':this, 'arguments':arguments}, var)
            var.registers(['$to', '$from', 'fitted', 'slice'])
            var.put('fitted', var.get('fitRightJoin')(var.get('slice').get('content'), var.get('$from').callprop('node', Js(0.0)), var.get('$from'), var.get('$to'), Js(0.0), var.get('slice').get('openStart'), var.get('slice').get('openEnd')))
            if var.get('fitted').neg():
                return var.get(u"null")
            return var.get('normalizeSlice')(var.get('fitted'), var.get('slice').get('openStart'), var.get('$to').get('depth'))
        PyJsHoisted_fitRight_.func_name = 'fitRight'
        var.put('fitRight', PyJsHoisted_fitRight_)
        @Js
        def PyJsHoisted_fitsTrivially_(PyJsArg_2466726f6d_, PyJsArg_24746f_, slice, this, arguments, var=var):
            var = Scope({'$from':PyJsArg_2466726f6d_, '$to':PyJsArg_24746f_, 'slice':slice, 'this':this, 'arguments':arguments}, var)
            var.registers(['$to', '$from', 'slice'])
            return (((var.get('slice').get('openStart').neg() and var.get('slice').get('openEnd').neg()) and (var.get('$from').callprop('start')==var.get('$to').callprop('start'))) and var.get('$from').get('parent').callprop('canReplace', var.get('$from').callprop('index'), var.get('$to').callprop('index'), var.get('slice').get('content')))
        PyJsHoisted_fitsTrivially_.func_name = 'fitsTrivially'
        var.put('fitsTrivially', PyJsHoisted_fitsTrivially_)
        @Js
        def PyJsHoisted_canMoveText_(PyJsArg_2466726f6d_, PyJsArg_24746f_, slice, this, arguments, var=var):
            var = Scope({'$from':PyJsArg_2466726f6d_, '$to':PyJsArg_24746f_, 'slice':slice, 'this':this, 'arguments':arguments}, var)
            var.registers(['$to', 'slice', 'match', '$from', 'i', 'parent'])
            if var.get('$to').get('parent').get('isTextblock').neg():
                return Js(False)
            var.put('parent', (var.get('nodeRight')(var.get('slice').get('content'), var.get('slice').get('openEnd')) if var.get('slice').get('openEnd') else var.get('$from').callprop('node', (var.get('$from').get('depth')-(var.get('slice').get('openStart')-var.get('slice').get('openEnd'))))))
            if var.get('parent').get('isTextblock').neg():
                return Js(False)
            #for JS loop
            var.put('i', var.get('$to').callprop('index'))
            while (var.get('i')<var.get('$to').get('parent').get('childCount')):
                try:
                    if var.get('parent').get('type').callprop('allowsMarks', var.get('$to').get('parent').callprop('child', var.get('i')).get('marks')).neg():
                        return Js(False)
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            pass
            if var.get('slice').get('openEnd'):
                var.put('match', var.get('parent').callprop('contentMatchAt', var.get('parent').get('childCount')))
            else:
                var.put('match', var.get('parent').callprop('contentMatchAt', var.get('parent').get('childCount')))
                if var.get('slice').get('size'):
                    var.put('match', var.get('match').callprop('matchFragment', var.get('slice').get('content'), (Js(1.0) if var.get('slice').get('openStart') else Js(0.0))))
            var.put('match', var.get('match').callprop('matchFragment', var.get('$to').get('parent').get('content'), var.get('$to').callprop('index')))
            return (var.get('match') and var.get('match').get('validEnd'))
        PyJsHoisted_canMoveText_.func_name = 'canMoveText'
        var.put('canMoveText', PyJsHoisted_canMoveText_)
        @Js
        def PyJsHoisted_nodeRight_(content, depth, this, arguments, var=var):
            var = Scope({'content':content, 'depth':depth, 'this':this, 'arguments':arguments}, var)
            var.registers(['depth', 'content', 'i'])
            #for JS loop
            var.put('i', Js(1.0))
            while (var.get('i')<var.get('depth')):
                try:
                    var.put('content', var.get('content').get('lastChild').get('content'))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return var.get('content').get('lastChild')
        PyJsHoisted_nodeRight_.func_name = 'nodeRight'
        var.put('nodeRight', PyJsHoisted_nodeRight_)
        @Js
        def PyJsHoisted_placeSlice_(PyJsArg_2466726f6d_, slice, this, arguments, var=var):
            var = Scope({'$from':PyJsArg_2466726f6d_, 'slice':slice, 'this':this, 'arguments':arguments}, var)
            var.registers(['frontier', '$from', 'slice', 'pass'])
            var.put('frontier', var.get('Frontier').create(var.get('$from')))
            #for JS loop
            var.put('pass', Js(1.0))
            while (var.get('slice').get('size') and (var.get('pass')<=Js(3.0))):
                try:
                    var.put('slice', var.get('frontier').callprop('placeSlice', var.get('slice').get('content'), var.get('slice').get('openStart'), var.get('slice').get('openEnd'), var.get('pass')))
                finally:
                        (var.put('pass',Js(var.get('pass').to_number())+Js(1))-Js(1))
            while var.get('frontier').get('open').get('length'):
                var.get('frontier').callprop('closeNode')
            return var.get('frontier').get('placed')
        PyJsHoisted_placeSlice_.func_name = 'placeSlice'
        var.put('placeSlice', PyJsHoisted_placeSlice_)
        @Js
        def PyJsHoisted_closeNodeStart_(node, openStart, openEnd, this, arguments, var=var):
            var = Scope({'node':node, 'openStart':openStart, 'openEnd':openEnd, 'this':this, 'arguments':arguments}, var)
            var.registers(['openStart', 'node', 'openEnd', 'content', 'first', 'fill'])
            var.put('content', var.get('node').get('content'))
            if (var.get('openStart')>Js(1.0)):
                var.put('first', var.get('closeNodeStart')(var.get('node').get('firstChild'), (var.get('openStart')-Js(1.0)), ((var.get('openEnd')-Js(1.0)) if (var.get('node').get('childCount')==Js(1.0)) else Js(0.0))))
                var.put('content', var.get('node').get('content').callprop('replaceChild', Js(0.0), var.get('first')))
            var.put('fill', var.get('node').get('type').get('contentMatch').callprop('fillBefore', var.get('content'), (var.get('openEnd')==Js(0.0))))
            return var.get('node').callprop('copy', var.get('fill').callprop('append', var.get('content')))
        PyJsHoisted_closeNodeStart_.func_name = 'closeNodeStart'
        var.put('closeNodeStart', PyJsHoisted_closeNodeStart_)
        @Js
        def PyJsHoisted_closeNodeEnd_(node, depth, this, arguments, var=var):
            var = Scope({'node':node, 'depth':depth, 'this':this, 'arguments':arguments}, var)
            var.registers(['node', 'last', 'depth', 'content', 'fill'])
            var.put('content', var.get('node').get('content'))
            if (var.get('depth')>Js(1.0)):
                var.put('last', var.get('closeNodeEnd')(var.get('node').get('lastChild'), (var.get('depth')-Js(1.0))))
                var.put('content', var.get('node').get('content').callprop('replaceChild', (var.get('node').get('childCount')-Js(1.0)), var.get('last')))
            var.put('fill', var.get('node').callprop('contentMatchAt', var.get('node').get('childCount')).callprop('fillBefore', var.get('dist').get('Fragment').get('empty'), Js(True)))
            return var.get('node').callprop('copy', var.get('content').callprop('append', var.get('fill')))
        PyJsHoisted_closeNodeEnd_.func_name = 'closeNodeEnd'
        var.put('closeNodeEnd', PyJsHoisted_closeNodeEnd_)
        @Js
        def PyJsHoisted_closeFragmentEnd_(fragment, depth, this, arguments, var=var):
            var = Scope({'fragment':fragment, 'depth':depth, 'this':this, 'arguments':arguments}, var)
            var.registers(['depth', 'fragment'])
            return (var.get('fragment').callprop('replaceChild', (var.get('fragment').get('childCount')-Js(1.0)), var.get('closeNodeEnd')(var.get('fragment').get('lastChild'), var.get('depth'))) if var.get('depth') else var.get('fragment'))
        PyJsHoisted_closeFragmentEnd_.func_name = 'closeFragmentEnd'
        var.put('closeFragmentEnd', PyJsHoisted_closeFragmentEnd_)
        @Js
        def PyJsHoisted_closeFragment_(fragment, depth, oldOpen, newOpen, parent, this, arguments, var=var):
            var = Scope({'fragment':fragment, 'depth':depth, 'oldOpen':oldOpen, 'newOpen':newOpen, 'parent':parent, 'this':this, 'arguments':arguments}, var)
            var.registers(['depth', 'fragment', 'first', 'parent', 'oldOpen', 'newOpen'])
            if (var.get('depth')<var.get('oldOpen')):
                var.put('first', var.get('fragment').get('firstChild'))
                var.put('fragment', var.get('fragment').callprop('replaceChild', Js(0.0), var.get('first').callprop('copy', var.get('closeFragment')(var.get('first').get('content'), (var.get('depth')+Js(1.0)), var.get('oldOpen'), var.get('newOpen'), var.get('first')))))
            if (var.get('depth')>var.get('newOpen')):
                var.put('fragment', var.get('parent').callprop('contentMatchAt', Js(0.0)).callprop('fillBefore', var.get('fragment'), Js(True)).callprop('append', var.get('fragment')))
            return var.get('fragment')
        PyJsHoisted_closeFragment_.func_name = 'closeFragment'
        var.put('closeFragment', PyJsHoisted_closeFragment_)
        @Js
        def PyJsHoisted_coveredDepths_(PyJsArg_2466726f6d_, PyJsArg_24746f_, this, arguments, var=var):
            var = Scope({'$from':PyJsArg_2466726f6d_, '$to':PyJsArg_24746f_, 'this':this, 'arguments':arguments}, var)
            var.registers(['minDepth', '$to', 'result', '$from', 'start', 'd'])
            var.put('result', Js([]))
            var.put('minDepth', var.get('Math').callprop('min', var.get('$from').get('depth'), var.get('$to').get('depth')))
            #for JS loop
            var.put('d', var.get('minDepth'))
            while (var.get('d')>=Js(0.0)):
                try:
                    var.put('start', var.get('$from').callprop('start', var.get('d')))
                    def PyJs_LONG_474_(var=var):
                        return ((((var.get('start')<(var.get('$from').get('pos')-(var.get('$from').get('depth')-var.get('d')))) or (var.get('$to').callprop('end', var.get('d'))>(var.get('$to').get('pos')+(var.get('$to').get('depth')-var.get('d'))))) or var.get('$from').callprop('node', var.get('d')).get('type').get('spec').get('isolating')) or var.get('$to').callprop('node', var.get('d')).get('type').get('spec').get('isolating'))
                    if PyJs_LONG_474_():
                        break
                    if (var.get('start')==var.get('$to').callprop('start', var.get('d'))):
                        var.get('result').callprop('push', var.get('d'))
                finally:
                        (var.put('d',Js(var.get('d').to_number())-Js(1))+Js(1))
            return var.get('result')
        PyJsHoisted_coveredDepths_.func_name = 'coveredDepths'
        var.put('coveredDepths', PyJsHoisted_coveredDepths_)
        PyJs_Object_356_ = Js({'value':Js(True)})
        var.get('Object').callprop('defineProperty', var.get('exports'), Js('__esModule'), PyJs_Object_356_)
        var.put('lower16', Js(65535))
        var.put('factor16', var.get('Math').callprop('pow', Js(2.0), Js(16.0)))
        pass
        pass
        pass
        @Js
        def PyJs_MapResult_357_(pos, deleted, recover, this, arguments, var=var):
            var = Scope({'pos':pos, 'deleted':deleted, 'recover':recover, 'this':this, 'arguments':arguments, 'MapResult':PyJs_MapResult_357_}, var)
            var.registers(['recover', 'deleted', 'pos'])
            if PyJsStrictEq(var.get('deleted'),PyJsComma(Js(0.0), Js(None))):
                var.put('deleted', Js(False))
            if PyJsStrictEq(var.get('recover'),PyJsComma(Js(0.0), Js(None))):
                var.put('recover', var.get(u"null"))
            var.get(u"this").put('pos', var.get('pos'))
            var.get(u"this").put('deleted', var.get('deleted'))
            var.get(u"this").put('recover', var.get('recover'))
        PyJs_MapResult_357_._set_name('MapResult')
        var.put('MapResult', PyJs_MapResult_357_)
        @Js
        def PyJs_StepMap_358_(ranges, inverted, this, arguments, var=var):
            var = Scope({'ranges':ranges, 'inverted':inverted, 'this':this, 'arguments':arguments, 'StepMap':PyJs_StepMap_358_}, var)
            var.registers(['inverted', 'ranges'])
            if PyJsStrictEq(var.get('inverted'),PyJsComma(Js(0.0), Js(None))):
                var.put('inverted', Js(False))
            var.get(u"this").put('ranges', var.get('ranges'))
            var.get(u"this").put('inverted', var.get('inverted'))
        PyJs_StepMap_358_._set_name('StepMap')
        var.put('StepMap', PyJs_StepMap_358_)
        @Js
        def PyJs_recover_359_(value, this, arguments, var=var):
            var = Scope({'value':value, 'this':this, 'arguments':arguments, 'recover':PyJs_recover_359_}, var)
            var.registers(['this$1', 'value', 'index', 'i', 'diff'])
            var.put('this$1', var.get(u"this"))
            var.put('diff', Js(0.0))
            var.put('index', var.get('recoverIndex')(var.get('value')))
            if var.get(u"this").get('inverted').neg():
                #for JS loop
                var.put('i', Js(0.0))
                while (var.get('i')<var.get('index')):
                    try:
                        var.put('diff', (var.get('this$1').get('ranges').get(((var.get('i')*Js(3.0))+Js(2.0)))-var.get('this$1').get('ranges').get(((var.get('i')*Js(3.0))+Js(1.0)))), '+')
                    finally:
                            (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return ((var.get(u"this").get('ranges').get((var.get('index')*Js(3.0)))+var.get('diff'))+var.get('recoverOffset')(var.get('value')))
        PyJs_recover_359_._set_name('recover')
        var.get('StepMap').get('prototype').put('recover', PyJs_recover_359_)
        @Js
        def PyJs_mapResult_360_(pos, assoc, this, arguments, var=var):
            var = Scope({'pos':pos, 'assoc':assoc, 'this':this, 'arguments':arguments, 'mapResult':PyJs_mapResult_360_}, var)
            var.registers(['assoc', 'pos'])
            if PyJsStrictEq(var.get('assoc'),PyJsComma(Js(0.0), Js(None))):
                var.put('assoc', Js(1.0))
            return var.get(u"this").callprop('_map', var.get('pos'), var.get('assoc'), Js(False))
        PyJs_mapResult_360_._set_name('mapResult')
        var.get('StepMap').get('prototype').put('mapResult', PyJs_mapResult_360_)
        @Js
        def PyJs_map_361_(pos, assoc, this, arguments, var=var):
            var = Scope({'pos':pos, 'assoc':assoc, 'this':this, 'arguments':arguments, 'map':PyJs_map_361_}, var)
            var.registers(['assoc', 'pos'])
            if PyJsStrictEq(var.get('assoc'),PyJsComma(Js(0.0), Js(None))):
                var.put('assoc', Js(1.0))
            return var.get(u"this").callprop('_map', var.get('pos'), var.get('assoc'), Js(True))
        PyJs_map_361_._set_name('map')
        var.get('StepMap').get('prototype').put('map', PyJs_map_361_)
        @Js
        def PyJs__map_362_(pos, assoc, simple, this, arguments, var=var):
            var = Scope({'pos':pos, 'assoc':assoc, 'simple':simple, 'this':this, 'arguments':arguments, '_map':PyJs__map_362_}, var)
            var.registers(['oldSize', 'newIndex', 'newSize', 'result', 'simple', 'recover', 'this$1', 'side', 'end', 'i', 'start', 'pos', 'oldIndex', 'diff', 'assoc'])
            var.put('this$1', var.get(u"this"))
            var.put('diff', Js(0.0))
            var.put('oldIndex', (Js(2.0) if var.get(u"this").get('inverted') else Js(1.0)))
            var.put('newIndex', (Js(1.0) if var.get(u"this").get('inverted') else Js(2.0)))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get(u"this").get('ranges').get('length')):
                try:
                    var.put('start', (var.get('this$1').get('ranges').get(var.get('i'))-(var.get('diff') if var.get('this$1').get('inverted') else Js(0.0))))
                    if (var.get('start')>var.get('pos')):
                        break
                    var.put('oldSize', var.get('this$1').get('ranges').get((var.get('i')+var.get('oldIndex'))))
                    var.put('newSize', var.get('this$1').get('ranges').get((var.get('i')+var.get('newIndex'))))
                    var.put('end', (var.get('start')+var.get('oldSize')))
                    if (var.get('pos')<=var.get('end')):
                        var.put('side', (var.get('assoc') if var.get('oldSize').neg() else ((-Js(1.0)) if (var.get('pos')==var.get('start')) else (Js(1.0) if (var.get('pos')==var.get('end')) else var.get('assoc')))))
                        var.put('result', ((var.get('start')+var.get('diff'))+(Js(0.0) if (var.get('side')<Js(0.0)) else var.get('newSize'))))
                        if var.get('simple'):
                            return var.get('result')
                        var.put('recover', var.get('makeRecover')((var.get('i')/Js(3.0)), (var.get('pos')-var.get('start'))))
                        return var.get('MapResult').create(var.get('result'), ((var.get('pos')!=var.get('start')) if (var.get('assoc')<Js(0.0)) else (var.get('pos')!=var.get('end'))), var.get('recover'))
                    var.put('diff', (var.get('newSize')-var.get('oldSize')), '+')
                finally:
                        var.put('i', Js(3.0), '+')
            return ((var.get('pos')+var.get('diff')) if var.get('simple') else var.get('MapResult').create((var.get('pos')+var.get('diff'))))
        PyJs__map_362_._set_name('_map')
        var.get('StepMap').get('prototype').put('_map', PyJs__map_362_)
        @Js
        def PyJs_touches_363_(pos, recover, this, arguments, var=var):
            var = Scope({'pos':pos, 'recover':recover, 'this':this, 'arguments':arguments, 'touches':PyJs_touches_363_}, var)
            var.registers(['oldSize', 'newIndex', 'pos', 'recover', 'this$1', 'end', 'index', 'i', 'start', 'oldIndex', 'diff'])
            var.put('this$1', var.get(u"this"))
            var.put('diff', Js(0.0))
            var.put('index', var.get('recoverIndex')(var.get('recover')))
            var.put('oldIndex', (Js(2.0) if var.get(u"this").get('inverted') else Js(1.0)))
            var.put('newIndex', (Js(1.0) if var.get(u"this").get('inverted') else Js(2.0)))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get(u"this").get('ranges').get('length')):
                try:
                    var.put('start', (var.get('this$1').get('ranges').get(var.get('i'))-(var.get('diff') if var.get('this$1').get('inverted') else Js(0.0))))
                    if (var.get('start')>var.get('pos')):
                        break
                    var.put('oldSize', var.get('this$1').get('ranges').get((var.get('i')+var.get('oldIndex'))))
                    var.put('end', (var.get('start')+var.get('oldSize')))
                    if ((var.get('pos')<=var.get('end')) and (var.get('i')==(var.get('index')*Js(3.0)))):
                        return Js(True)
                    var.put('diff', (var.get('this$1').get('ranges').get((var.get('i')+var.get('newIndex')))-var.get('oldSize')), '+')
                finally:
                        var.put('i', Js(3.0), '+')
            return Js(False)
        PyJs_touches_363_._set_name('touches')
        var.get('StepMap').get('prototype').put('touches', PyJs_touches_363_)
        @Js
        def PyJs_forEach_364_(f, this, arguments, var=var):
            var = Scope({'f':f, 'this':this, 'arguments':arguments, 'forEach':PyJs_forEach_364_}, var)
            var.registers(['newStart', 'oldSize', 'newIndex', 'newSize', 'this$1', 'oldStart', 'f', 'i', 'start', 'oldIndex', 'diff'])
            var.put('this$1', var.get(u"this"))
            var.put('oldIndex', (Js(2.0) if var.get(u"this").get('inverted') else Js(1.0)))
            var.put('newIndex', (Js(1.0) if var.get(u"this").get('inverted') else Js(2.0)))
            #for JS loop
            var.put('i', Js(0.0))
            var.put('diff', Js(0.0))
            while (var.get('i')<var.get(u"this").get('ranges').get('length')):
                try:
                    var.put('start', var.get('this$1').get('ranges').get(var.get('i')))
                    var.put('oldStart', (var.get('start')-(var.get('diff') if var.get('this$1').get('inverted') else Js(0.0))))
                    var.put('newStart', (var.get('start')+(Js(0.0) if var.get('this$1').get('inverted') else var.get('diff'))))
                    var.put('oldSize', var.get('this$1').get('ranges').get((var.get('i')+var.get('oldIndex'))))
                    var.put('newSize', var.get('this$1').get('ranges').get((var.get('i')+var.get('newIndex'))))
                    var.get('f')(var.get('oldStart'), (var.get('oldStart')+var.get('oldSize')), var.get('newStart'), (var.get('newStart')+var.get('newSize')))
                    var.put('diff', (var.get('newSize')-var.get('oldSize')), '+')
                finally:
                        var.put('i', Js(3.0), '+')
        PyJs_forEach_364_._set_name('forEach')
        var.get('StepMap').get('prototype').put('forEach', PyJs_forEach_364_)
        @Js
        def PyJs_invert_365_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'invert':PyJs_invert_365_}, var)
            var.registers([])
            return var.get('StepMap').create(var.get(u"this").get('ranges'), var.get(u"this").get('inverted').neg())
        PyJs_invert_365_._set_name('invert')
        var.get('StepMap').get('prototype').put('invert', PyJs_invert_365_)
        @Js
        def PyJs_toString_366_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'toString':PyJs_toString_366_}, var)
            var.registers([])
            return ((Js('-') if var.get(u"this").get('inverted') else Js(''))+var.get('JSON').callprop('stringify', var.get(u"this").get('ranges')))
        PyJs_toString_366_._set_name('toString')
        var.get('StepMap').get('prototype').put('toString', PyJs_toString_366_)
        @Js
        def PyJs_offset_367_(n, this, arguments, var=var):
            var = Scope({'n':n, 'this':this, 'arguments':arguments, 'offset':PyJs_offset_367_}, var)
            var.registers(['n'])
            return (var.get('StepMap').get('empty') if (var.get('n')==Js(0.0)) else var.get('StepMap').create((Js([Js(0.0), (-var.get('n')), Js(0.0)]) if (var.get('n')<Js(0.0)) else Js([Js(0.0), Js(0.0), var.get('n')]))))
        PyJs_offset_367_._set_name('offset')
        var.get('StepMap').put('offset', PyJs_offset_367_)
        var.get('StepMap').put('empty', var.get('StepMap').create(Js([])))
        @Js
        def PyJs_Mapping_368_(maps, mirror, PyJsArg_66726f6d_, to, this, arguments, var=var):
            var = Scope({'maps':maps, 'mirror':mirror, 'from':PyJsArg_66726f6d_, 'to':to, 'this':this, 'arguments':arguments, 'Mapping':PyJs_Mapping_368_}, var)
            var.registers(['to', 'from', 'mirror', 'maps'])
            var.get(u"this").put('maps', (var.get('maps') or Js([])))
            var.get(u"this").put('from', (var.get('from') or Js(0.0)))
            var.get(u"this").put('to', (var.get(u"this").get('maps').get('length') if (var.get('to')==var.get(u"null")) else var.get('to')))
            var.get(u"this").put('mirror', var.get('mirror'))
        PyJs_Mapping_368_._set_name('Mapping')
        var.put('Mapping', PyJs_Mapping_368_)
        @Js
        def PyJs_slice_369_(PyJsArg_66726f6d_, to, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'this':this, 'arguments':arguments, 'slice':PyJs_slice_369_}, var)
            var.registers(['to', 'from'])
            if PyJsStrictEq(var.get('from'),PyJsComma(Js(0.0), Js(None))):
                var.put('from', Js(0.0))
            if PyJsStrictEq(var.get('to'),PyJsComma(Js(0.0), Js(None))):
                var.put('to', var.get(u"this").get('maps').get('length'))
            return var.get('Mapping').create(var.get(u"this").get('maps'), var.get(u"this").get('mirror'), var.get('from'), var.get('to'))
        PyJs_slice_369_._set_name('slice')
        var.get('Mapping').get('prototype').put('slice', PyJs_slice_369_)
        @Js
        def PyJs_copy_370_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'copy':PyJs_copy_370_}, var)
            var.registers([])
            return var.get('Mapping').create(var.get(u"this").get('maps').callprop('slice'), (var.get(u"this").get('mirror') and var.get(u"this").get('mirror').callprop('slice')), var.get(u"this").get('from'), var.get(u"this").get('to'))
        PyJs_copy_370_._set_name('copy')
        var.get('Mapping').get('prototype').put('copy', PyJs_copy_370_)
        @Js
        def PyJs_appendMap_371_(map, mirrors, this, arguments, var=var):
            var = Scope({'map':map, 'mirrors':mirrors, 'this':this, 'arguments':arguments, 'appendMap':PyJs_appendMap_371_}, var)
            var.registers(['map', 'mirrors'])
            var.get(u"this").put('to', var.get(u"this").get('maps').callprop('push', var.get('map')))
            if (var.get('mirrors')!=var.get(u"null")):
                var.get(u"this").callprop('setMirror', (var.get(u"this").get('maps').get('length')-Js(1.0)), var.get('mirrors'))
        PyJs_appendMap_371_._set_name('appendMap')
        var.get('Mapping').get('prototype').put('appendMap', PyJs_appendMap_371_)
        @Js
        def PyJs_appendMapping_372_(mapping, this, arguments, var=var):
            var = Scope({'mapping':mapping, 'this':this, 'arguments':arguments, 'appendMapping':PyJs_appendMapping_372_}, var)
            var.registers(['startSize', 'mapping', 'this$1', 'i', 'mirr'])
            var.put('this$1', var.get(u"this"))
            #for JS loop
            var.put('i', Js(0.0))
            var.put('startSize', var.get(u"this").get('maps').get('length'))
            while (var.get('i')<var.get('mapping').get('maps').get('length')):
                try:
                    var.put('mirr', var.get('mapping').callprop('getMirror', var.get('i')))
                    var.get('this$1').callprop('appendMap', var.get('mapping').get('maps').get(var.get('i')), ((var.get('startSize')+var.get('mirr')) if ((var.get('mirr')!=var.get(u"null")) and (var.get('mirr')<var.get('i'))) else var.get(u"null")))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        PyJs_appendMapping_372_._set_name('appendMapping')
        var.get('Mapping').get('prototype').put('appendMapping', PyJs_appendMapping_372_)
        @Js
        def PyJs_getMirror_373_(n, this, arguments, var=var):
            var = Scope({'n':n, 'this':this, 'arguments':arguments, 'getMirror':PyJs_getMirror_373_}, var)
            var.registers(['this$1', 'i', 'n'])
            var.put('this$1', var.get(u"this"))
            if var.get(u"this").get('mirror'):
                #for JS loop
                var.put('i', Js(0.0))
                while (var.get('i')<var.get(u"this").get('mirror').get('length')):
                    try:
                        if (var.get('this$1').get('mirror').get(var.get('i'))==var.get('n')):
                            return var.get('this$1').get('mirror').get((var.get('i')+((-Js(1.0)) if (var.get('i')%Js(2.0)) else Js(1.0))))
                    finally:
                            (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        PyJs_getMirror_373_._set_name('getMirror')
        var.get('Mapping').get('prototype').put('getMirror', PyJs_getMirror_373_)
        @Js
        def PyJs_setMirror_374_(n, m, this, arguments, var=var):
            var = Scope({'n':n, 'm':m, 'this':this, 'arguments':arguments, 'setMirror':PyJs_setMirror_374_}, var)
            var.registers(['m', 'n'])
            if var.get(u"this").get('mirror').neg():
                var.get(u"this").put('mirror', Js([]))
            var.get(u"this").get('mirror').callprop('push', var.get('n'), var.get('m'))
        PyJs_setMirror_374_._set_name('setMirror')
        var.get('Mapping').get('prototype').put('setMirror', PyJs_setMirror_374_)
        @Js
        def PyJs_appendMappingInverted_375_(mapping, this, arguments, var=var):
            var = Scope({'mapping':mapping, 'this':this, 'arguments':arguments, 'appendMappingInverted':PyJs_appendMappingInverted_375_}, var)
            var.registers(['mapping', 'totalSize', 'this$1', 'i', 'mirr'])
            var.put('this$1', var.get(u"this"))
            #for JS loop
            var.put('i', (var.get('mapping').get('maps').get('length')-Js(1.0)))
            var.put('totalSize', (var.get(u"this").get('maps').get('length')+var.get('mapping').get('maps').get('length')))
            while (var.get('i')>=Js(0.0)):
                try:
                    var.put('mirr', var.get('mapping').callprop('getMirror', var.get('i')))
                    var.get('this$1').callprop('appendMap', var.get('mapping').get('maps').get(var.get('i')).callprop('invert'), (((var.get('totalSize')-var.get('mirr'))-Js(1.0)) if ((var.get('mirr')!=var.get(u"null")) and (var.get('mirr')>var.get('i'))) else var.get(u"null")))
                finally:
                        (var.put('i',Js(var.get('i').to_number())-Js(1))+Js(1))
        PyJs_appendMappingInverted_375_._set_name('appendMappingInverted')
        var.get('Mapping').get('prototype').put('appendMappingInverted', PyJs_appendMappingInverted_375_)
        @Js
        def PyJs_invert_376_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'invert':PyJs_invert_376_}, var)
            var.registers(['inverse'])
            var.put('inverse', var.get('Mapping').create())
            var.get('inverse').callprop('appendMappingInverted', var.get(u"this"))
            return var.get('inverse')
        PyJs_invert_376_._set_name('invert')
        var.get('Mapping').get('prototype').put('invert', PyJs_invert_376_)
        @Js
        def PyJs_map_377_(pos, assoc, this, arguments, var=var):
            var = Scope({'pos':pos, 'assoc':assoc, 'this':this, 'arguments':arguments, 'map':PyJs_map_377_}, var)
            var.registers(['this$1', 'assoc', 'i', 'pos'])
            var.put('this$1', var.get(u"this"))
            if PyJsStrictEq(var.get('assoc'),PyJsComma(Js(0.0), Js(None))):
                var.put('assoc', Js(1.0))
            if var.get(u"this").get('mirror'):
                return var.get(u"this").callprop('_map', var.get('pos'), var.get('assoc'), Js(True))
            #for JS loop
            var.put('i', var.get(u"this").get('from'))
            while (var.get('i')<var.get(u"this").get('to')):
                try:
                    var.put('pos', var.get('this$1').get('maps').get(var.get('i')).callprop('map', var.get('pos'), var.get('assoc')))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return var.get('pos')
        PyJs_map_377_._set_name('map')
        var.get('Mapping').get('prototype').put('map', PyJs_map_377_)
        @Js
        def PyJs_mapResult_378_(pos, assoc, this, arguments, var=var):
            var = Scope({'pos':pos, 'assoc':assoc, 'this':this, 'arguments':arguments, 'mapResult':PyJs_mapResult_378_}, var)
            var.registers(['assoc', 'pos'])
            if PyJsStrictEq(var.get('assoc'),PyJsComma(Js(0.0), Js(None))):
                var.put('assoc', Js(1.0))
            return var.get(u"this").callprop('_map', var.get('pos'), var.get('assoc'), Js(False))
        PyJs_mapResult_378_._set_name('mapResult')
        var.get('Mapping').get('prototype').put('mapResult', PyJs_mapResult_378_)
        @Js
        def PyJs__map_379_(pos, assoc, simple, this, arguments, var=var):
            var = Scope({'pos':pos, 'assoc':assoc, 'simple':simple, 'this':this, 'arguments':arguments, '_map':PyJs__map_379_}, var)
            var.registers(['simple', 'result', 'map', 'this$1', 'recoverables', 'rec', 'i', 'deleted', 'pos', 'corr', 'assoc'])
            var.put('this$1', var.get(u"this"))
            var.put('deleted', Js(False))
            var.put('recoverables', var.get(u"null"))
            #for JS loop
            var.put('i', var.get(u"this").get('from'))
            while (var.get('i')<var.get(u"this").get('to')):
                try:
                    var.put('map', var.get('this$1').get('maps').get(var.get('i')))
                    var.put('rec', (var.get('recoverables') and var.get('recoverables').get(var.get('i'))))
                    if ((var.get('rec')!=var.get(u"null")) and var.get('map').callprop('touches', var.get('pos'), var.get('rec'))):
                        var.put('pos', var.get('map').callprop('recover', var.get('rec')))
                        continue
                    var.put('result', var.get('map').callprop('mapResult', var.get('pos'), var.get('assoc')))
                    if (var.get('result').get('recover')!=var.get(u"null")):
                        var.put('corr', var.get('this$1').callprop('getMirror', var.get('i')))
                        if (((var.get('corr')!=var.get(u"null")) and (var.get('corr')>var.get('i'))) and (var.get('corr')<var.get('this$1').get('to'))):
                            if var.get('result').get('deleted'):
                                var.put('i', var.get('corr'))
                                var.put('pos', var.get('this$1').get('maps').get(var.get('corr')).callprop('recover', var.get('result').get('recover')))
                                continue
                            else:
                                (var.get('recoverables') or var.put('recoverables', var.get('Object').callprop('create', var.get(u"null")))).put(var.get('corr'), var.get('result').get('recover'))
                    if var.get('result').get('deleted'):
                        var.put('deleted', Js(True))
                    var.put('pos', var.get('result').get('pos'))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return (var.get('pos') if var.get('simple') else var.get('MapResult').create(var.get('pos'), var.get('deleted')))
        PyJs__map_379_._set_name('_map')
        var.get('Mapping').get('prototype').put('_map', PyJs__map_379_)
        pass
        var.get('TransformError').put('prototype', var.get('Object').callprop('create', var.get('Error').get('prototype')))
        var.get('TransformError').get('prototype').put('constructor', var.get('TransformError'))
        var.get('TransformError').get('prototype').put('name', Js('TransformError'))
        @Js
        def PyJs_Transform_380_(doc, this, arguments, var=var):
            var = Scope({'doc':doc, 'this':this, 'arguments':arguments, 'Transform':PyJs_Transform_380_}, var)
            var.registers(['doc'])
            var.get(u"this").put('doc', var.get('doc'))
            var.get(u"this").put('steps', Js([]))
            var.get(u"this").put('docs', Js([]))
            var.get(u"this").put('mapping', var.get('Mapping').create())
        PyJs_Transform_380_._set_name('Transform')
        var.put('Transform', PyJs_Transform_380_)
        PyJs_Object_382_ = Js({})
        PyJs_Object_383_ = Js({})
        PyJs_Object_381_ = Js({'before':PyJs_Object_382_,'docChanged':PyJs_Object_383_})
        var.put('prototypeAccessors', PyJs_Object_381_)
        @Js
        def PyJs_anonymous_384_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return (var.get(u"this").get('docs').get('0') if var.get(u"this").get('docs').get('length') else var.get(u"this").get('doc'))
        PyJs_anonymous_384_._set_name('anonymous')
        var.get('prototypeAccessors').get('before').put('get', PyJs_anonymous_384_)
        @Js
        def PyJs_step_385_(object, this, arguments, var=var):
            var = Scope({'object':object, 'this':this, 'arguments':arguments, 'step':PyJs_step_385_}, var)
            var.registers(['object', 'result'])
            var.put('result', var.get(u"this").callprop('maybeStep', var.get('object')))
            if var.get('result').get('failed'):
                PyJsTempException = JsToPyException(var.get('TransformError').create(var.get('result').get('failed')))
                raise PyJsTempException
            return var.get(u"this")
        PyJs_step_385_._set_name('step')
        var.get('Transform').get('prototype').put('step', PyJs_step_385_)
        @Js
        def PyJs_maybeStep_386_(step, this, arguments, var=var):
            var = Scope({'step':step, 'this':this, 'arguments':arguments, 'maybeStep':PyJs_maybeStep_386_}, var)
            var.registers(['step', 'result'])
            var.put('result', var.get('step').callprop('apply', var.get(u"this").get('doc')))
            if var.get('result').get('failed').neg():
                var.get(u"this").callprop('addStep', var.get('step'), var.get('result').get('doc'))
            return var.get('result')
        PyJs_maybeStep_386_._set_name('maybeStep')
        var.get('Transform').get('prototype').put('maybeStep', PyJs_maybeStep_386_)
        @Js
        def PyJs_anonymous_387_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            return (var.get(u"this").get('steps').get('length')>Js(0.0))
        PyJs_anonymous_387_._set_name('anonymous')
        var.get('prototypeAccessors').get('docChanged').put('get', PyJs_anonymous_387_)
        @Js
        def PyJs_addStep_388_(step, doc, this, arguments, var=var):
            var = Scope({'step':step, 'doc':doc, 'this':this, 'arguments':arguments, 'addStep':PyJs_addStep_388_}, var)
            var.registers(['step', 'doc'])
            var.get(u"this").get('docs').callprop('push', var.get(u"this").get('doc'))
            var.get(u"this").get('steps').callprop('push', var.get('step'))
            var.get(u"this").get('mapping').callprop('appendMap', var.get('step').callprop('getMap'))
            var.get(u"this").put('doc', var.get('doc'))
        PyJs_addStep_388_._set_name('addStep')
        var.get('Transform').get('prototype').put('addStep', PyJs_addStep_388_)
        var.get('Object').callprop('defineProperties', var.get('Transform').get('prototype'), var.get('prototypeAccessors'))
        pass
        var.put('stepsByID', var.get('Object').callprop('create', var.get(u"null")))
        @Js
        def PyJs_Step_389_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'Step':PyJs_Step_389_}, var)
            var.registers([])
            pass
        PyJs_Step_389_._set_name('Step')
        var.put('Step', PyJs_Step_389_)
        @Js
        def PyJs_apply_390_(_doc, this, arguments, var=var):
            var = Scope({'_doc':_doc, 'this':this, 'arguments':arguments, 'apply':PyJs_apply_390_}, var)
            var.registers(['_doc'])
            return var.get('mustOverride')()
        PyJs_apply_390_._set_name('apply')
        var.get('Step').get('prototype').put('apply', PyJs_apply_390_)
        @Js
        def PyJs_getMap_391_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'getMap':PyJs_getMap_391_}, var)
            var.registers([])
            return var.get('StepMap').get('empty')
        PyJs_getMap_391_._set_name('getMap')
        var.get('Step').get('prototype').put('getMap', PyJs_getMap_391_)
        @Js
        def PyJs_invert_392_(_doc, this, arguments, var=var):
            var = Scope({'_doc':_doc, 'this':this, 'arguments':arguments, 'invert':PyJs_invert_392_}, var)
            var.registers(['_doc'])
            return var.get('mustOverride')()
        PyJs_invert_392_._set_name('invert')
        var.get('Step').get('prototype').put('invert', PyJs_invert_392_)
        @Js
        def PyJs_map_393_(_mapping, this, arguments, var=var):
            var = Scope({'_mapping':_mapping, 'this':this, 'arguments':arguments, 'map':PyJs_map_393_}, var)
            var.registers(['_mapping'])
            return var.get('mustOverride')()
        PyJs_map_393_._set_name('map')
        var.get('Step').get('prototype').put('map', PyJs_map_393_)
        @Js
        def PyJs_merge_394_(_other, this, arguments, var=var):
            var = Scope({'_other':_other, 'this':this, 'arguments':arguments, 'merge':PyJs_merge_394_}, var)
            var.registers(['_other'])
            return var.get(u"null")
        PyJs_merge_394_._set_name('merge')
        var.get('Step').get('prototype').put('merge', PyJs_merge_394_)
        @Js
        def PyJs_toJSON_395_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'toJSON':PyJs_toJSON_395_}, var)
            var.registers([])
            return var.get('mustOverride')()
        PyJs_toJSON_395_._set_name('toJSON')
        var.get('Step').get('prototype').put('toJSON', PyJs_toJSON_395_)
        @Js
        def PyJs_fromJSON_396_(schema, json, this, arguments, var=var):
            var = Scope({'schema':schema, 'json':json, 'this':this, 'arguments':arguments, 'fromJSON':PyJs_fromJSON_396_}, var)
            var.registers(['schema', 'json', 'type'])
            if (var.get('json').neg() or var.get('json').get('stepType').neg()):
                PyJsTempException = JsToPyException(var.get('RangeError').create(Js('Invalid input for Step.fromJSON')))
                raise PyJsTempException
            var.put('type', var.get('stepsByID').get(var.get('json').get('stepType')))
            if var.get('type').neg():
                PyJsTempException = JsToPyException(var.get('RangeError').create(((Js('No step type ')+var.get('json').get('stepType'))+Js(' defined'))))
                raise PyJsTempException
            return var.get('type').callprop('fromJSON', var.get('schema'), var.get('json'))
        PyJs_fromJSON_396_._set_name('fromJSON')
        var.get('Step').put('fromJSON', PyJs_fromJSON_396_)
        @Js
        def PyJs_jsonID_397_(id, stepClass, this, arguments, var=var):
            var = Scope({'id':id, 'stepClass':stepClass, 'this':this, 'arguments':arguments, 'jsonID':PyJs_jsonID_397_}, var)
            var.registers(['id', 'stepClass'])
            if var.get('stepsByID').contains(var.get('id')):
                PyJsTempException = JsToPyException(var.get('RangeError').create((Js('Duplicate use of step JSON ID ')+var.get('id'))))
                raise PyJsTempException
            var.get('stepsByID').put(var.get('id'), var.get('stepClass'))
            var.get('stepClass').get('prototype').put('jsonID', var.get('id'))
            return var.get('stepClass')
        PyJs_jsonID_397_._set_name('jsonID')
        var.get('Step').put('jsonID', PyJs_jsonID_397_)
        @Js
        def PyJs_StepResult_398_(doc, failed, this, arguments, var=var):
            var = Scope({'doc':doc, 'failed':failed, 'this':this, 'arguments':arguments, 'StepResult':PyJs_StepResult_398_}, var)
            var.registers(['failed', 'doc'])
            var.get(u"this").put('doc', var.get('doc'))
            var.get(u"this").put('failed', var.get('failed'))
        PyJs_StepResult_398_._set_name('StepResult')
        var.put('StepResult', PyJs_StepResult_398_)
        @Js
        def PyJs_ok_399_(doc, this, arguments, var=var):
            var = Scope({'doc':doc, 'this':this, 'arguments':arguments, 'ok':PyJs_ok_399_}, var)
            var.registers(['doc'])
            return var.get('StepResult').create(var.get('doc'), var.get(u"null"))
        PyJs_ok_399_._set_name('ok')
        var.get('StepResult').put('ok', PyJs_ok_399_)
        @Js
        def PyJs_fail_400_(message, this, arguments, var=var):
            var = Scope({'message':message, 'this':this, 'arguments':arguments, 'fail':PyJs_fail_400_}, var)
            var.registers(['message'])
            return var.get('StepResult').create(var.get(u"null"), var.get('message'))
        PyJs_fail_400_._set_name('fail')
        var.get('StepResult').put('fail', PyJs_fail_400_)
        @Js
        def PyJs_fromReplace_401_(doc, PyJsArg_66726f6d_, to, slice, this, arguments, var=var):
            var = Scope({'doc':doc, 'from':PyJsArg_66726f6d_, 'to':to, 'slice':slice, 'this':this, 'arguments':arguments, 'fromReplace':PyJs_fromReplace_401_}, var)
            var.registers(['to', 'from', 'doc', 'slice'])
            try:
                return var.get('StepResult').callprop('ok', var.get('doc').callprop('replace', var.get('from'), var.get('to'), var.get('slice')))
            except PyJsException as PyJsTempException:
                PyJsHolder_65_13395772 = var.own.get('e')
                var.force_own_put('e', PyExceptionToJs(PyJsTempException))
                try:
                    if var.get('e').instanceof(var.get('dist').get('ReplaceError')):
                        return var.get('StepResult').callprop('fail', var.get('e').get('message'))
                    PyJsTempException = JsToPyException(var.get('e'))
                    raise PyJsTempException
                finally:
                    if PyJsHolder_65_13395772 is not None:
                        var.own['e'] = PyJsHolder_65_13395772
                    else:
                        del var.own['e']
                    del PyJsHolder_65_13395772
        PyJs_fromReplace_401_._set_name('fromReplace')
        var.get('StepResult').put('fromReplace', PyJs_fromReplace_401_)
        @Js
        def PyJs_anonymous_402_(PyJsArg_53746570242431_, this, arguments, var=var):
            var = Scope({'Step$$1':PyJsArg_53746570242431_, 'this':this, 'arguments':arguments}, var)
            var.registers(['ReplaceStep', 'Step$$1'])
            @Js
            def PyJsHoisted_ReplaceStep_(PyJsArg_66726f6d_, to, slice, structure, this, arguments, var=var):
                var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'slice':slice, 'structure':structure, 'this':this, 'arguments':arguments}, var)
                var.registers(['to', 'from', 'structure', 'slice'])
                var.get('Step$$1').callprop('call', var.get(u"this"))
                var.get(u"this").put('from', var.get('from'))
                var.get(u"this").put('to', var.get('to'))
                var.get(u"this").put('slice', var.get('slice'))
                var.get(u"this").put('structure', var.get('structure').neg().neg())
            PyJsHoisted_ReplaceStep_.func_name = 'ReplaceStep'
            var.put('ReplaceStep', PyJsHoisted_ReplaceStep_)
            pass
            if var.get('Step$$1'):
                var.get('ReplaceStep').put('__proto__', var.get('Step$$1'))
            var.get('ReplaceStep').put('prototype', var.get('Object').callprop('create', (var.get('Step$$1') and var.get('Step$$1').get('prototype'))))
            var.get('ReplaceStep').get('prototype').put('constructor', var.get('ReplaceStep'))
            @Js
            def PyJs_apply_403_(doc, this, arguments, var=var):
                var = Scope({'doc':doc, 'this':this, 'arguments':arguments, 'apply':PyJs_apply_403_}, var)
                var.registers(['doc'])
                if (var.get(u"this").get('structure') and var.get('contentBetween')(var.get('doc'), var.get(u"this").get('from'), var.get(u"this").get('to'))):
                    return var.get('StepResult').callprop('fail', Js('Structure replace would overwrite content'))
                return var.get('StepResult').callprop('fromReplace', var.get('doc'), var.get(u"this").get('from'), var.get(u"this").get('to'), var.get(u"this").get('slice'))
            PyJs_apply_403_._set_name('apply')
            var.get('ReplaceStep').get('prototype').put('apply', PyJs_apply_403_)
            @Js
            def PyJs_getMap_404_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments, 'getMap':PyJs_getMap_404_}, var)
                var.registers([])
                return var.get('StepMap').create(Js([var.get(u"this").get('from'), (var.get(u"this").get('to')-var.get(u"this").get('from')), var.get(u"this").get('slice').get('size')]))
            PyJs_getMap_404_._set_name('getMap')
            var.get('ReplaceStep').get('prototype').put('getMap', PyJs_getMap_404_)
            @Js
            def PyJs_invert_405_(doc, this, arguments, var=var):
                var = Scope({'doc':doc, 'this':this, 'arguments':arguments, 'invert':PyJs_invert_405_}, var)
                var.registers(['doc'])
                return var.get('ReplaceStep').create(var.get(u"this").get('from'), (var.get(u"this").get('from')+var.get(u"this").get('slice').get('size')), var.get('doc').callprop('slice', var.get(u"this").get('from'), var.get(u"this").get('to')))
            PyJs_invert_405_._set_name('invert')
            var.get('ReplaceStep').get('prototype').put('invert', PyJs_invert_405_)
            @Js
            def PyJs_map_406_(mapping, this, arguments, var=var):
                var = Scope({'mapping':mapping, 'this':this, 'arguments':arguments, 'map':PyJs_map_406_}, var)
                var.registers(['to', 'from', 'mapping'])
                var.put('from', var.get('mapping').callprop('mapResult', var.get(u"this").get('from'), Js(1.0)))
                var.put('to', var.get('mapping').callprop('mapResult', var.get(u"this").get('to'), (-Js(1.0))))
                if (var.get('from').get('deleted') and var.get('to').get('deleted')):
                    return var.get(u"null")
                return var.get('ReplaceStep').create(var.get('from').get('pos'), var.get('Math').callprop('max', var.get('from').get('pos'), var.get('to').get('pos')), var.get(u"this").get('slice'))
            PyJs_map_406_._set_name('map')
            var.get('ReplaceStep').get('prototype').put('map', PyJs_map_406_)
            @Js
            def PyJs_merge_407_(other, this, arguments, var=var):
                var = Scope({'other':other, 'this':this, 'arguments':arguments, 'merge':PyJs_merge_407_}, var)
                var.registers(['slice$1', 'slice', 'other'])
                if (var.get('other').instanceof(var.get('ReplaceStep')).neg() or (var.get('other').get('structure')!=var.get(u"this").get('structure'))):
                    return var.get(u"null")
                if ((((var.get(u"this").get('from')+var.get(u"this").get('slice').get('size'))==var.get('other').get('from')) and var.get(u"this").get('slice').get('openEnd').neg()) and var.get('other').get('slice').get('openStart').neg()):
                    var.put('slice', (var.get('dist').get('Slice').get('empty') if ((var.get(u"this").get('slice').get('size')+var.get('other').get('slice').get('size'))==Js(0.0)) else var.get('dist').get('Slice').create(var.get(u"this").get('slice').get('content').callprop('append', var.get('other').get('slice').get('content')), var.get(u"this").get('slice').get('openStart'), var.get('other').get('slice').get('openEnd'))))
                    return var.get('ReplaceStep').create(var.get(u"this").get('from'), (var.get(u"this").get('to')+(var.get('other').get('to')-var.get('other').get('from'))), var.get('slice'), var.get(u"this").get('structure'))
                else:
                    if (((var.get('other').get('to')==var.get(u"this").get('from')) and var.get(u"this").get('slice').get('openStart').neg()) and var.get('other').get('slice').get('openEnd').neg()):
                        var.put('slice$1', (var.get('dist').get('Slice').get('empty') if ((var.get(u"this").get('slice').get('size')+var.get('other').get('slice').get('size'))==Js(0.0)) else var.get('dist').get('Slice').create(var.get('other').get('slice').get('content').callprop('append', var.get(u"this").get('slice').get('content')), var.get('other').get('slice').get('openStart'), var.get(u"this").get('slice').get('openEnd'))))
                        return var.get('ReplaceStep').create(var.get('other').get('from'), var.get(u"this").get('to'), var.get('slice$1'), var.get(u"this").get('structure'))
                    else:
                        return var.get(u"null")
            PyJs_merge_407_._set_name('merge')
            var.get('ReplaceStep').get('prototype').put('merge', PyJs_merge_407_)
            @Js
            def PyJs_toJSON_408_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments, 'toJSON':PyJs_toJSON_408_}, var)
                var.registers(['json'])
                PyJs_Object_409_ = Js({'stepType':Js('replace'),'from':var.get(u"this").get('from'),'to':var.get(u"this").get('to')})
                var.put('json', PyJs_Object_409_)
                if var.get(u"this").get('slice').get('size'):
                    var.get('json').put('slice', var.get(u"this").get('slice').callprop('toJSON'))
                if var.get(u"this").get('structure'):
                    var.get('json').put('structure', Js(True))
                return var.get('json')
            PyJs_toJSON_408_._set_name('toJSON')
            var.get('ReplaceStep').get('prototype').put('toJSON', PyJs_toJSON_408_)
            @Js
            def PyJs_fromJSON_410_(schema, json, this, arguments, var=var):
                var = Scope({'schema':schema, 'json':json, 'this':this, 'arguments':arguments, 'fromJSON':PyJs_fromJSON_410_}, var)
                var.registers(['schema', 'json'])
                if ((var.get('json').get('from').typeof()!=Js('number')) or (var.get('json').get('to').typeof()!=Js('number'))):
                    PyJsTempException = JsToPyException(var.get('RangeError').create(Js('Invalid input for ReplaceStep.fromJSON')))
                    raise PyJsTempException
                return var.get('ReplaceStep').create(var.get('json').get('from'), var.get('json').get('to'), var.get('dist').get('Slice').callprop('fromJSON', var.get('schema'), var.get('json').get('slice')), var.get('json').get('structure').neg().neg())
            PyJs_fromJSON_410_._set_name('fromJSON')
            var.get('ReplaceStep').put('fromJSON', PyJs_fromJSON_410_)
            return var.get('ReplaceStep')
        PyJs_anonymous_402_._set_name('anonymous')
        var.put('ReplaceStep', PyJs_anonymous_402_(var.get('Step')))
        var.get('Step').callprop('jsonID', Js('replace'), var.get('ReplaceStep'))
        @Js
        def PyJs_anonymous_411_(PyJsArg_53746570242431_, this, arguments, var=var):
            var = Scope({'Step$$1':PyJsArg_53746570242431_, 'this':this, 'arguments':arguments}, var)
            var.registers(['ReplaceAroundStep', 'Step$$1'])
            @Js
            def PyJsHoisted_ReplaceAroundStep_(PyJsArg_66726f6d_, to, gapFrom, gapTo, slice, insert, structure, this, arguments, var=var):
                var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'gapFrom':gapFrom, 'gapTo':gapTo, 'slice':slice, 'insert':insert, 'structure':structure, 'this':this, 'arguments':arguments}, var)
                var.registers(['slice', 'gapFrom', 'insert', 'gapTo', 'structure', 'to', 'from'])
                var.get('Step$$1').callprop('call', var.get(u"this"))
                var.get(u"this").put('from', var.get('from'))
                var.get(u"this").put('to', var.get('to'))
                var.get(u"this").put('gapFrom', var.get('gapFrom'))
                var.get(u"this").put('gapTo', var.get('gapTo'))
                var.get(u"this").put('slice', var.get('slice'))
                var.get(u"this").put('insert', var.get('insert'))
                var.get(u"this").put('structure', var.get('structure').neg().neg())
            PyJsHoisted_ReplaceAroundStep_.func_name = 'ReplaceAroundStep'
            var.put('ReplaceAroundStep', PyJsHoisted_ReplaceAroundStep_)
            pass
            if var.get('Step$$1'):
                var.get('ReplaceAroundStep').put('__proto__', var.get('Step$$1'))
            var.get('ReplaceAroundStep').put('prototype', var.get('Object').callprop('create', (var.get('Step$$1') and var.get('Step$$1').get('prototype'))))
            var.get('ReplaceAroundStep').get('prototype').put('constructor', var.get('ReplaceAroundStep'))
            @Js
            def PyJs_apply_412_(doc, this, arguments, var=var):
                var = Scope({'doc':doc, 'this':this, 'arguments':arguments, 'apply':PyJs_apply_412_}, var)
                var.registers(['gap', 'doc', 'inserted'])
                if (var.get(u"this").get('structure') and (var.get('contentBetween')(var.get('doc'), var.get(u"this").get('from'), var.get(u"this").get('gapFrom')) or var.get('contentBetween')(var.get('doc'), var.get(u"this").get('gapTo'), var.get(u"this").get('to')))):
                    return var.get('StepResult').callprop('fail', Js('Structure gap-replace would overwrite content'))
                var.put('gap', var.get('doc').callprop('slice', var.get(u"this").get('gapFrom'), var.get(u"this").get('gapTo')))
                if (var.get('gap').get('openStart') or var.get('gap').get('openEnd')):
                    return var.get('StepResult').callprop('fail', Js('Gap is not a flat range'))
                var.put('inserted', var.get(u"this").get('slice').callprop('insertAt', var.get(u"this").get('insert'), var.get('gap').get('content')))
                if var.get('inserted').neg():
                    return var.get('StepResult').callprop('fail', Js('Content does not fit in gap'))
                return var.get('StepResult').callprop('fromReplace', var.get('doc'), var.get(u"this").get('from'), var.get(u"this").get('to'), var.get('inserted'))
            PyJs_apply_412_._set_name('apply')
            var.get('ReplaceAroundStep').get('prototype').put('apply', PyJs_apply_412_)
            @Js
            def PyJs_getMap_413_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments, 'getMap':PyJs_getMap_413_}, var)
                var.registers([])
                return var.get('StepMap').create(Js([var.get(u"this").get('from'), (var.get(u"this").get('gapFrom')-var.get(u"this").get('from')), var.get(u"this").get('insert'), var.get(u"this").get('gapTo'), (var.get(u"this").get('to')-var.get(u"this").get('gapTo')), (var.get(u"this").get('slice').get('size')-var.get(u"this").get('insert'))]))
            PyJs_getMap_413_._set_name('getMap')
            var.get('ReplaceAroundStep').get('prototype').put('getMap', PyJs_getMap_413_)
            @Js
            def PyJs_invert_414_(doc, this, arguments, var=var):
                var = Scope({'doc':doc, 'this':this, 'arguments':arguments, 'invert':PyJs_invert_414_}, var)
                var.registers(['gap', 'doc'])
                var.put('gap', (var.get(u"this").get('gapTo')-var.get(u"this").get('gapFrom')))
                def PyJs_LONG_415_(var=var):
                    return var.get('ReplaceAroundStep').create(var.get(u"this").get('from'), ((var.get(u"this").get('from')+var.get(u"this").get('slice').get('size'))+var.get('gap')), (var.get(u"this").get('from')+var.get(u"this").get('insert')), ((var.get(u"this").get('from')+var.get(u"this").get('insert'))+var.get('gap')), var.get('doc').callprop('slice', var.get(u"this").get('from'), var.get(u"this").get('to')).callprop('removeBetween', (var.get(u"this").get('gapFrom')-var.get(u"this").get('from')), (var.get(u"this").get('gapTo')-var.get(u"this").get('from'))), (var.get(u"this").get('gapFrom')-var.get(u"this").get('from')), var.get(u"this").get('structure'))
                return PyJs_LONG_415_()
            PyJs_invert_414_._set_name('invert')
            var.get('ReplaceAroundStep').get('prototype').put('invert', PyJs_invert_414_)
            @Js
            def PyJs_map_416_(mapping, this, arguments, var=var):
                var = Scope({'mapping':mapping, 'this':this, 'arguments':arguments, 'map':PyJs_map_416_}, var)
                var.registers(['mapping', 'gapFrom', 'gapTo', 'to', 'from'])
                var.put('from', var.get('mapping').callprop('mapResult', var.get(u"this").get('from'), Js(1.0)))
                var.put('to', var.get('mapping').callprop('mapResult', var.get(u"this").get('to'), (-Js(1.0))))
                var.put('gapFrom', var.get('mapping').callprop('map', var.get(u"this").get('gapFrom'), (-Js(1.0))))
                var.put('gapTo', var.get('mapping').callprop('map', var.get(u"this").get('gapTo'), Js(1.0)))
                if (((var.get('from').get('deleted') and var.get('to').get('deleted')) or (var.get('gapFrom')<var.get('from').get('pos'))) or (var.get('gapTo')>var.get('to').get('pos'))):
                    return var.get(u"null")
                return var.get('ReplaceAroundStep').create(var.get('from').get('pos'), var.get('to').get('pos'), var.get('gapFrom'), var.get('gapTo'), var.get(u"this").get('slice'), var.get(u"this").get('insert'), var.get(u"this").get('structure'))
            PyJs_map_416_._set_name('map')
            var.get('ReplaceAroundStep').get('prototype').put('map', PyJs_map_416_)
            @Js
            def PyJs_toJSON_417_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments, 'toJSON':PyJs_toJSON_417_}, var)
                var.registers(['json'])
                PyJs_Object_418_ = Js({'stepType':Js('replaceAround'),'from':var.get(u"this").get('from'),'to':var.get(u"this").get('to'),'gapFrom':var.get(u"this").get('gapFrom'),'gapTo':var.get(u"this").get('gapTo'),'insert':var.get(u"this").get('insert')})
                var.put('json', PyJs_Object_418_)
                if var.get(u"this").get('slice').get('size'):
                    var.get('json').put('slice', var.get(u"this").get('slice').callprop('toJSON'))
                if var.get(u"this").get('structure'):
                    var.get('json').put('structure', Js(True))
                return var.get('json')
            PyJs_toJSON_417_._set_name('toJSON')
            var.get('ReplaceAroundStep').get('prototype').put('toJSON', PyJs_toJSON_417_)
            @Js
            def PyJs_fromJSON_419_(schema, json, this, arguments, var=var):
                var = Scope({'schema':schema, 'json':json, 'this':this, 'arguments':arguments, 'fromJSON':PyJs_fromJSON_419_}, var)
                var.registers(['schema', 'json'])
                if (((((var.get('json').get('from').typeof()!=Js('number')) or (var.get('json').get('to').typeof()!=Js('number'))) or (var.get('json').get('gapFrom').typeof()!=Js('number'))) or (var.get('json').get('gapTo').typeof()!=Js('number'))) or (var.get('json').get('insert').typeof()!=Js('number'))):
                    PyJsTempException = JsToPyException(var.get('RangeError').create(Js('Invalid input for ReplaceAroundStep.fromJSON')))
                    raise PyJsTempException
                return var.get('ReplaceAroundStep').create(var.get('json').get('from'), var.get('json').get('to'), var.get('json').get('gapFrom'), var.get('json').get('gapTo'), var.get('dist').get('Slice').callprop('fromJSON', var.get('schema'), var.get('json').get('slice')), var.get('json').get('insert'), var.get('json').get('structure').neg().neg())
            PyJs_fromJSON_419_._set_name('fromJSON')
            var.get('ReplaceAroundStep').put('fromJSON', PyJs_fromJSON_419_)
            return var.get('ReplaceAroundStep')
        PyJs_anonymous_411_._set_name('anonymous')
        var.put('ReplaceAroundStep', PyJs_anonymous_411_(var.get('Step')))
        var.get('Step').callprop('jsonID', Js('replaceAround'), var.get('ReplaceAroundStep'))
        pass
        pass
        pass
        @Js
        def PyJs_anonymous_420_(range, target, this, arguments, var=var):
            var = Scope({'range':range, 'target':target, 'this':this, 'arguments':arguments}, var)
            var.registers(['$to', 'gapEnd', 'before', 'openStart', 'openEnd', '$from', 'd$1', 'splitting$1', 'end', 'range', 'depth', 'after', 'target', 'splitting', 'start', 'd', 'gapStart'])
            var.put('$from', var.get('range').get('$from'))
            var.put('$to', var.get('range').get('$to'))
            var.put('depth', var.get('range').get('depth'))
            var.put('gapStart', var.get('$from').callprop('before', (var.get('depth')+Js(1.0))))
            var.put('gapEnd', var.get('$to').callprop('after', (var.get('depth')+Js(1.0))))
            var.put('start', var.get('gapStart'))
            var.put('end', var.get('gapEnd'))
            var.put('before', var.get('dist').get('Fragment').get('empty'))
            var.put('openStart', Js(0.0))
            #for JS loop
            var.put('d', var.get('depth'))
            var.put('splitting', Js(False))
            while (var.get('d')>var.get('target')):
                try:
                    if (var.get('splitting') or (var.get('$from').callprop('index', var.get('d'))>Js(0.0))):
                        var.put('splitting', Js(True))
                        var.put('before', var.get('dist').get('Fragment').callprop('from', var.get('$from').callprop('node', var.get('d')).callprop('copy', var.get('before'))))
                        (var.put('openStart',Js(var.get('openStart').to_number())+Js(1))-Js(1))
                    else:
                        (var.put('start',Js(var.get('start').to_number())-Js(1))+Js(1))
                finally:
                        (var.put('d',Js(var.get('d').to_number())-Js(1))+Js(1))
            var.put('after', var.get('dist').get('Fragment').get('empty'))
            var.put('openEnd', Js(0.0))
            #for JS loop
            var.put('d$1', var.get('depth'))
            var.put('splitting$1', Js(False))
            while (var.get('d$1')>var.get('target')):
                try:
                    if (var.get('splitting$1') or (var.get('$to').callprop('after', (var.get('d$1')+Js(1.0)))<var.get('$to').callprop('end', var.get('d$1')))):
                        var.put('splitting$1', Js(True))
                        var.put('after', var.get('dist').get('Fragment').callprop('from', var.get('$to').callprop('node', var.get('d$1')).callprop('copy', var.get('after'))))
                        (var.put('openEnd',Js(var.get('openEnd').to_number())+Js(1))-Js(1))
                    else:
                        (var.put('end',Js(var.get('end').to_number())+Js(1))-Js(1))
                finally:
                        (var.put('d$1',Js(var.get('d$1').to_number())-Js(1))+Js(1))
            return var.get(u"this").callprop('step', var.get('ReplaceAroundStep').create(var.get('start'), var.get('end'), var.get('gapStart'), var.get('gapEnd'), var.get('dist').get('Slice').create(var.get('before').callprop('append', var.get('after')), var.get('openStart'), var.get('openEnd')), (var.get('before').get('size')-var.get('openStart')), Js(True)))
        PyJs_anonymous_420_._set_name('anonymous')
        var.get('Transform').get('prototype').put('lift', PyJs_anonymous_420_)
        pass
        pass
        pass
        pass
        @Js
        def PyJs_anonymous_423_(range, wrappers, this, arguments, var=var):
            var = Scope({'range':range, 'wrappers':wrappers, 'this':this, 'arguments':arguments}, var)
            var.registers(['wrappers', 'end', 'range', 'content', 'i', 'start'])
            var.put('content', var.get('dist').get('Fragment').get('empty'))
            #for JS loop
            var.put('i', (var.get('wrappers').get('length')-Js(1.0)))
            while (var.get('i')>=Js(0.0)):
                try:
                    var.put('content', var.get('dist').get('Fragment').callprop('from', var.get('wrappers').get(var.get('i')).get('type').callprop('create', var.get('wrappers').get(var.get('i')).get('attrs'), var.get('content'))))
                finally:
                        (var.put('i',Js(var.get('i').to_number())-Js(1))+Js(1))
            var.put('start', var.get('range').get('start'))
            var.put('end', var.get('range').get('end'))
            return var.get(u"this").callprop('step', var.get('ReplaceAroundStep').create(var.get('start'), var.get('end'), var.get('start'), var.get('end'), var.get('dist').get('Slice').create(var.get('content'), Js(0.0), Js(0.0)), var.get('wrappers').get('length'), Js(True)))
        PyJs_anonymous_423_._set_name('anonymous')
        var.get('Transform').get('prototype').put('wrap', PyJs_anonymous_423_)
        @Js
        def PyJs_anonymous_424_(PyJsArg_66726f6d_, to, type, attrs, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'type':type, 'attrs':attrs, 'this':this, 'arguments':arguments}, var)
            var.registers(['this$1', 'attrs', 'type', 'to', 'from', 'mapFrom'])
            var.put('this$1', var.get(u"this"))
            if PyJsStrictEq(var.get('to'),PyJsComma(Js(0.0), Js(None))):
                var.put('to', var.get('from'))
            if var.get('type').get('isTextblock').neg():
                PyJsTempException = JsToPyException(var.get('RangeError').create(Js('Type given to setBlockType should be a textblock')))
                raise PyJsTempException
            var.put('mapFrom', var.get(u"this").get('steps').get('length'))
            @Js
            def PyJs_anonymous_425_(node, pos, this, arguments, var=var):
                var = Scope({'node':node, 'pos':pos, 'this':this, 'arguments':arguments}, var)
                var.registers(['mapping', 'startM', 'node', 'pos', 'endM'])
                if ((var.get('node').get('isTextblock') and var.get('node').callprop('hasMarkup', var.get('type'), var.get('attrs')).neg()) and var.get('canChangeType')(var.get('this$1').get('doc'), var.get('this$1').get('mapping').callprop('slice', var.get('mapFrom')).callprop('map', var.get('pos')), var.get('type'))):
                    var.get('this$1').callprop('clearIncompatible', var.get('this$1').get('mapping').callprop('slice', var.get('mapFrom')).callprop('map', var.get('pos'), Js(1.0)), var.get('type'))
                    var.put('mapping', var.get('this$1').get('mapping').callprop('slice', var.get('mapFrom')))
                    var.put('startM', var.get('mapping').callprop('map', var.get('pos'), Js(1.0)))
                    var.put('endM', var.get('mapping').callprop('map', (var.get('pos')+var.get('node').get('nodeSize')), Js(1.0)))
                    var.get('this$1').callprop('step', var.get('ReplaceAroundStep').create(var.get('startM'), var.get('endM'), (var.get('startM')+Js(1.0)), (var.get('endM')-Js(1.0)), var.get('dist').get('Slice').create(var.get('dist').get('Fragment').callprop('from', var.get('type').callprop('create', var.get('attrs'), var.get(u"null"), var.get('node').get('marks'))), Js(0.0), Js(0.0)), Js(1.0), Js(True)))
                    return Js(False)
            PyJs_anonymous_425_._set_name('anonymous')
            var.get(u"this").get('doc').callprop('nodesBetween', var.get('from'), var.get('to'), PyJs_anonymous_425_)
            return var.get(u"this")
        PyJs_anonymous_424_._set_name('anonymous')
        var.get('Transform').get('prototype').put('setBlockType', PyJs_anonymous_424_)
        pass
        @Js
        def PyJs_anonymous_426_(pos, type, attrs, marks, this, arguments, var=var):
            var = Scope({'pos':pos, 'type':type, 'attrs':attrs, 'marks':marks, 'this':this, 'arguments':arguments}, var)
            var.registers(['node', 'attrs', 'type', 'marks', 'newNode', 'pos'])
            var.put('node', var.get(u"this").get('doc').callprop('nodeAt', var.get('pos')))
            if var.get('node').neg():
                PyJsTempException = JsToPyException(var.get('RangeError').create(Js('No node at given position')))
                raise PyJsTempException
            if var.get('type').neg():
                var.put('type', var.get('node').get('type'))
            var.put('newNode', var.get('type').callprop('create', var.get('attrs'), var.get(u"null"), (var.get('marks') or var.get('node').get('marks'))))
            if var.get('node').get('isLeaf'):
                return var.get(u"this").callprop('replaceWith', var.get('pos'), (var.get('pos')+var.get('node').get('nodeSize')), var.get('newNode'))
            if var.get('type').callprop('validContent', var.get('node').get('content')).neg():
                PyJsTempException = JsToPyException(var.get('RangeError').create((Js('Invalid content for node type ')+var.get('type').get('name'))))
                raise PyJsTempException
            return var.get(u"this").callprop('step', var.get('ReplaceAroundStep').create(var.get('pos'), (var.get('pos')+var.get('node').get('nodeSize')), (var.get('pos')+Js(1.0)), ((var.get('pos')+var.get('node').get('nodeSize'))-Js(1.0)), var.get('dist').get('Slice').create(var.get('dist').get('Fragment').callprop('from', var.get('newNode')), Js(0.0), Js(0.0)), Js(1.0), Js(True)))
        PyJs_anonymous_426_._set_name('anonymous')
        var.get('Transform').get('prototype').put('setNodeMarkup', PyJs_anonymous_426_)
        pass
        @Js
        def PyJs_anonymous_428_(pos, depth, typesAfter, this, arguments, var=var):
            var = Scope({'pos':pos, 'depth':depth, 'typesAfter':typesAfter, 'this':this, 'arguments':arguments}, var)
            var.registers(['e', 'before', 'typesAfter', 'after', 'depth', 'i', 'pos', 'd', 'typeAfter', '$pos'])
            if PyJsStrictEq(var.get('depth'),PyJsComma(Js(0.0), Js(None))):
                var.put('depth', Js(1.0))
            var.put('$pos', var.get(u"this").get('doc').callprop('resolve', var.get('pos')))
            var.put('before', var.get('dist').get('Fragment').get('empty'))
            var.put('after', var.get('dist').get('Fragment').get('empty'))
            #for JS loop
            var.put('d', var.get('$pos').get('depth'))
            var.put('e', (var.get('$pos').get('depth')-var.get('depth')))
            var.put('i', (var.get('depth')-Js(1.0)))
            while (var.get('d')>var.get('e')):
                try:
                    var.put('before', var.get('dist').get('Fragment').callprop('from', var.get('$pos').callprop('node', var.get('d')).callprop('copy', var.get('before'))))
                    var.put('typeAfter', (var.get('typesAfter') and var.get('typesAfter').get(var.get('i'))))
                    var.put('after', var.get('dist').get('Fragment').callprop('from', (var.get('typeAfter').get('type').callprop('create', var.get('typeAfter').get('attrs'), var.get('after')) if var.get('typeAfter') else var.get('$pos').callprop('node', var.get('d')).callprop('copy', var.get('after')))))
                finally:
                        PyJsComma((var.put('d',Js(var.get('d').to_number())-Js(1))+Js(1)),(var.put('i',Js(var.get('i').to_number())-Js(1))+Js(1)))
            return var.get(u"this").callprop('step', var.get('ReplaceStep').create(var.get('pos'), var.get('pos'), var.get('dist').get('Slice').create(var.get('before').callprop('append', var.get('after')), var.get('depth'), var.get('depth'), Js(True))))
        PyJs_anonymous_428_._set_name('anonymous')
        var.get('Transform').get('prototype').put('split', PyJs_anonymous_428_)
        pass
        pass
        pass
        @Js
        def PyJs_anonymous_429_(pos, depth, this, arguments, var=var):
            var = Scope({'pos':pos, 'depth':depth, 'this':this, 'arguments':arguments}, var)
            var.registers(['step', 'depth', 'pos'])
            if PyJsStrictEq(var.get('depth'),PyJsComma(Js(0.0), Js(None))):
                var.put('depth', Js(1.0))
            var.put('step', var.get('ReplaceStep').create((var.get('pos')-var.get('depth')), (var.get('pos')+var.get('depth')), var.get('dist').get('Slice').get('empty'), Js(True)))
            return var.get(u"this").callprop('step', var.get('step'))
        PyJs_anonymous_429_._set_name('anonymous')
        var.get('Transform').get('prototype').put('join', PyJs_anonymous_429_)
        pass
        pass
        pass
        @Js
        def PyJs_anonymous_430_(PyJsArg_53746570242431_, this, arguments, var=var):
            var = Scope({'Step$$1':PyJsArg_53746570242431_, 'this':this, 'arguments':arguments}, var)
            var.registers(['AddMarkStep', 'Step$$1'])
            @Js
            def PyJsHoisted_AddMarkStep_(PyJsArg_66726f6d_, to, mark, this, arguments, var=var):
                var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'mark':mark, 'this':this, 'arguments':arguments}, var)
                var.registers(['to', 'from', 'mark'])
                var.get('Step$$1').callprop('call', var.get(u"this"))
                var.get(u"this").put('from', var.get('from'))
                var.get(u"this").put('to', var.get('to'))
                var.get(u"this").put('mark', var.get('mark'))
            PyJsHoisted_AddMarkStep_.func_name = 'AddMarkStep'
            var.put('AddMarkStep', PyJsHoisted_AddMarkStep_)
            pass
            if var.get('Step$$1'):
                var.get('AddMarkStep').put('__proto__', var.get('Step$$1'))
            var.get('AddMarkStep').put('prototype', var.get('Object').callprop('create', (var.get('Step$$1') and var.get('Step$$1').get('prototype'))))
            var.get('AddMarkStep').get('prototype').put('constructor', var.get('AddMarkStep'))
            @Js
            def PyJs_apply_431_(doc, this, arguments, var=var):
                var = Scope({'doc':doc, 'this':this, 'arguments':arguments, 'apply':PyJs_apply_431_}, var)
                var.registers(['slice', 'doc', '$from', 'this$1', 'oldSlice', 'parent'])
                var.put('this$1', var.get(u"this"))
                var.put('oldSlice', var.get('doc').callprop('slice', var.get(u"this").get('from'), var.get(u"this").get('to')))
                var.put('$from', var.get('doc').callprop('resolve', var.get(u"this").get('from')))
                var.put('parent', var.get('$from').callprop('node', var.get('$from').callprop('sharedDepth', var.get(u"this").get('to'))))
                @Js
                def PyJs_anonymous_432_(node, parent, this, arguments, var=var):
                    var = Scope({'node':node, 'parent':parent, 'this':this, 'arguments':arguments}, var)
                    var.registers(['parent', 'node'])
                    if var.get('parent').get('type').callprop('allowsMarkType', var.get('this$1').get('mark').get('type')).neg():
                        return var.get('node')
                    return var.get('node').callprop('mark', var.get('this$1').get('mark').callprop('addToSet', var.get('node').get('marks')))
                PyJs_anonymous_432_._set_name('anonymous')
                var.put('slice', var.get('dist').get('Slice').create(var.get('mapFragment')(var.get('oldSlice').get('content'), PyJs_anonymous_432_, var.get('parent')), var.get('oldSlice').get('openStart'), var.get('oldSlice').get('openEnd')))
                return var.get('StepResult').callprop('fromReplace', var.get('doc'), var.get(u"this").get('from'), var.get(u"this").get('to'), var.get('slice'))
            PyJs_apply_431_._set_name('apply')
            var.get('AddMarkStep').get('prototype').put('apply', PyJs_apply_431_)
            @Js
            def PyJs_invert_433_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments, 'invert':PyJs_invert_433_}, var)
                var.registers([])
                return var.get('RemoveMarkStep').create(var.get(u"this").get('from'), var.get(u"this").get('to'), var.get(u"this").get('mark'))
            PyJs_invert_433_._set_name('invert')
            var.get('AddMarkStep').get('prototype').put('invert', PyJs_invert_433_)
            @Js
            def PyJs_map_434_(mapping, this, arguments, var=var):
                var = Scope({'mapping':mapping, 'this':this, 'arguments':arguments, 'map':PyJs_map_434_}, var)
                var.registers(['to', 'from', 'mapping'])
                var.put('from', var.get('mapping').callprop('mapResult', var.get(u"this").get('from'), Js(1.0)))
                var.put('to', var.get('mapping').callprop('mapResult', var.get(u"this").get('to'), (-Js(1.0))))
                if ((var.get('from').get('deleted') and var.get('to').get('deleted')) or (var.get('from').get('pos')>=var.get('to').get('pos'))):
                    return var.get(u"null")
                return var.get('AddMarkStep').create(var.get('from').get('pos'), var.get('to').get('pos'), var.get(u"this").get('mark'))
            PyJs_map_434_._set_name('map')
            var.get('AddMarkStep').get('prototype').put('map', PyJs_map_434_)
            @Js
            def PyJs_merge_435_(other, this, arguments, var=var):
                var = Scope({'other':other, 'this':this, 'arguments':arguments, 'merge':PyJs_merge_435_}, var)
                var.registers(['other'])
                if (((var.get('other').instanceof(var.get('AddMarkStep')) and var.get('other').get('mark').callprop('eq', var.get(u"this").get('mark'))) and (var.get(u"this").get('from')<=var.get('other').get('to'))) and (var.get(u"this").get('to')>=var.get('other').get('from'))):
                    return var.get('AddMarkStep').create(var.get('Math').callprop('min', var.get(u"this").get('from'), var.get('other').get('from')), var.get('Math').callprop('max', var.get(u"this").get('to'), var.get('other').get('to')), var.get(u"this").get('mark'))
            PyJs_merge_435_._set_name('merge')
            var.get('AddMarkStep').get('prototype').put('merge', PyJs_merge_435_)
            @Js
            def PyJs_toJSON_436_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments, 'toJSON':PyJs_toJSON_436_}, var)
                var.registers([])
                PyJs_Object_437_ = Js({'stepType':Js('addMark'),'mark':var.get(u"this").get('mark').callprop('toJSON'),'from':var.get(u"this").get('from'),'to':var.get(u"this").get('to')})
                return PyJs_Object_437_
            PyJs_toJSON_436_._set_name('toJSON')
            var.get('AddMarkStep').get('prototype').put('toJSON', PyJs_toJSON_436_)
            @Js
            def PyJs_fromJSON_438_(schema, json, this, arguments, var=var):
                var = Scope({'schema':schema, 'json':json, 'this':this, 'arguments':arguments, 'fromJSON':PyJs_fromJSON_438_}, var)
                var.registers(['schema', 'json'])
                if ((var.get('json').get('from').typeof()!=Js('number')) or (var.get('json').get('to').typeof()!=Js('number'))):
                    PyJsTempException = JsToPyException(var.get('RangeError').create(Js('Invalid input for AddMarkStep.fromJSON')))
                    raise PyJsTempException
                return var.get('AddMarkStep').create(var.get('json').get('from'), var.get('json').get('to'), var.get('schema').callprop('markFromJSON', var.get('json').get('mark')))
            PyJs_fromJSON_438_._set_name('fromJSON')
            var.get('AddMarkStep').put('fromJSON', PyJs_fromJSON_438_)
            return var.get('AddMarkStep')
        PyJs_anonymous_430_._set_name('anonymous')
        var.put('AddMarkStep', PyJs_anonymous_430_(var.get('Step')))
        var.get('Step').callprop('jsonID', Js('addMark'), var.get('AddMarkStep'))
        @Js
        def PyJs_anonymous_439_(PyJsArg_53746570242431_, this, arguments, var=var):
            var = Scope({'Step$$1':PyJsArg_53746570242431_, 'this':this, 'arguments':arguments}, var)
            var.registers(['RemoveMarkStep', 'Step$$1'])
            @Js
            def PyJsHoisted_RemoveMarkStep_(PyJsArg_66726f6d_, to, mark, this, arguments, var=var):
                var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'mark':mark, 'this':this, 'arguments':arguments}, var)
                var.registers(['to', 'from', 'mark'])
                var.get('Step$$1').callprop('call', var.get(u"this"))
                var.get(u"this").put('from', var.get('from'))
                var.get(u"this").put('to', var.get('to'))
                var.get(u"this").put('mark', var.get('mark'))
            PyJsHoisted_RemoveMarkStep_.func_name = 'RemoveMarkStep'
            var.put('RemoveMarkStep', PyJsHoisted_RemoveMarkStep_)
            pass
            if var.get('Step$$1'):
                var.get('RemoveMarkStep').put('__proto__', var.get('Step$$1'))
            var.get('RemoveMarkStep').put('prototype', var.get('Object').callprop('create', (var.get('Step$$1') and var.get('Step$$1').get('prototype'))))
            var.get('RemoveMarkStep').get('prototype').put('constructor', var.get('RemoveMarkStep'))
            @Js
            def PyJs_apply_440_(doc, this, arguments, var=var):
                var = Scope({'doc':doc, 'this':this, 'arguments':arguments, 'apply':PyJs_apply_440_}, var)
                var.registers(['oldSlice', 'this$1', 'doc', 'slice'])
                var.put('this$1', var.get(u"this"))
                var.put('oldSlice', var.get('doc').callprop('slice', var.get(u"this").get('from'), var.get(u"this").get('to')))
                @Js
                def PyJs_anonymous_441_(node, this, arguments, var=var):
                    var = Scope({'node':node, 'this':this, 'arguments':arguments}, var)
                    var.registers(['node'])
                    return var.get('node').callprop('mark', var.get('this$1').get('mark').callprop('removeFromSet', var.get('node').get('marks')))
                PyJs_anonymous_441_._set_name('anonymous')
                var.put('slice', var.get('dist').get('Slice').create(var.get('mapFragment')(var.get('oldSlice').get('content'), PyJs_anonymous_441_), var.get('oldSlice').get('openStart'), var.get('oldSlice').get('openEnd')))
                return var.get('StepResult').callprop('fromReplace', var.get('doc'), var.get(u"this").get('from'), var.get(u"this").get('to'), var.get('slice'))
            PyJs_apply_440_._set_name('apply')
            var.get('RemoveMarkStep').get('prototype').put('apply', PyJs_apply_440_)
            @Js
            def PyJs_invert_442_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments, 'invert':PyJs_invert_442_}, var)
                var.registers([])
                return var.get('AddMarkStep').create(var.get(u"this").get('from'), var.get(u"this").get('to'), var.get(u"this").get('mark'))
            PyJs_invert_442_._set_name('invert')
            var.get('RemoveMarkStep').get('prototype').put('invert', PyJs_invert_442_)
            @Js
            def PyJs_map_443_(mapping, this, arguments, var=var):
                var = Scope({'mapping':mapping, 'this':this, 'arguments':arguments, 'map':PyJs_map_443_}, var)
                var.registers(['to', 'from', 'mapping'])
                var.put('from', var.get('mapping').callprop('mapResult', var.get(u"this").get('from'), Js(1.0)))
                var.put('to', var.get('mapping').callprop('mapResult', var.get(u"this").get('to'), (-Js(1.0))))
                if ((var.get('from').get('deleted') and var.get('to').get('deleted')) or (var.get('from').get('pos')>=var.get('to').get('pos'))):
                    return var.get(u"null")
                return var.get('RemoveMarkStep').create(var.get('from').get('pos'), var.get('to').get('pos'), var.get(u"this").get('mark'))
            PyJs_map_443_._set_name('map')
            var.get('RemoveMarkStep').get('prototype').put('map', PyJs_map_443_)
            @Js
            def PyJs_merge_444_(other, this, arguments, var=var):
                var = Scope({'other':other, 'this':this, 'arguments':arguments, 'merge':PyJs_merge_444_}, var)
                var.registers(['other'])
                if (((var.get('other').instanceof(var.get('RemoveMarkStep')) and var.get('other').get('mark').callprop('eq', var.get(u"this").get('mark'))) and (var.get(u"this").get('from')<=var.get('other').get('to'))) and (var.get(u"this").get('to')>=var.get('other').get('from'))):
                    return var.get('RemoveMarkStep').create(var.get('Math').callprop('min', var.get(u"this").get('from'), var.get('other').get('from')), var.get('Math').callprop('max', var.get(u"this").get('to'), var.get('other').get('to')), var.get(u"this").get('mark'))
            PyJs_merge_444_._set_name('merge')
            var.get('RemoveMarkStep').get('prototype').put('merge', PyJs_merge_444_)
            @Js
            def PyJs_toJSON_445_(this, arguments, var=var):
                var = Scope({'this':this, 'arguments':arguments, 'toJSON':PyJs_toJSON_445_}, var)
                var.registers([])
                PyJs_Object_446_ = Js({'stepType':Js('removeMark'),'mark':var.get(u"this").get('mark').callprop('toJSON'),'from':var.get(u"this").get('from'),'to':var.get(u"this").get('to')})
                return PyJs_Object_446_
            PyJs_toJSON_445_._set_name('toJSON')
            var.get('RemoveMarkStep').get('prototype').put('toJSON', PyJs_toJSON_445_)
            @Js
            def PyJs_fromJSON_447_(schema, json, this, arguments, var=var):
                var = Scope({'schema':schema, 'json':json, 'this':this, 'arguments':arguments, 'fromJSON':PyJs_fromJSON_447_}, var)
                var.registers(['schema', 'json'])
                if ((var.get('json').get('from').typeof()!=Js('number')) or (var.get('json').get('to').typeof()!=Js('number'))):
                    PyJsTempException = JsToPyException(var.get('RangeError').create(Js('Invalid input for RemoveMarkStep.fromJSON')))
                    raise PyJsTempException
                return var.get('RemoveMarkStep').create(var.get('json').get('from'), var.get('json').get('to'), var.get('schema').callprop('markFromJSON', var.get('json').get('mark')))
            PyJs_fromJSON_447_._set_name('fromJSON')
            var.get('RemoveMarkStep').put('fromJSON', PyJs_fromJSON_447_)
            return var.get('RemoveMarkStep')
        PyJs_anonymous_439_._set_name('anonymous')
        var.put('RemoveMarkStep', PyJs_anonymous_439_(var.get('Step')))
        var.get('Step').callprop('jsonID', Js('removeMark'), var.get('RemoveMarkStep'))
        @Js
        def PyJs_anonymous_448_(PyJsArg_66726f6d_, to, mark, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'mark':mark, 'this':this, 'arguments':arguments}, var)
            var.registers(['adding', 'removed', 'mark', 'this$1', 'added', 'to', 'from', 'removing'])
            var.put('this$1', var.get(u"this"))
            var.put('removed', Js([]))
            var.put('added', Js([]))
            var.put('removing', var.get(u"null"))
            var.put('adding', var.get(u"null"))
            @Js
            def PyJs_anonymous_449_(node, pos, parent, this, arguments, var=var):
                var = Scope({'node':node, 'pos':pos, 'parent':parent, 'this':this, 'arguments':arguments}, var)
                var.registers(['node', 'newSet', 'end', 'marks', 'i', 'start', 'pos', 'parent'])
                if var.get('node').get('isInline').neg():
                    return var.get('undefined')
                var.put('marks', var.get('node').get('marks'))
                if (var.get('mark').callprop('isInSet', var.get('marks')).neg() and var.get('parent').get('type').callprop('allowsMarkType', var.get('mark').get('type'))):
                    var.put('start', var.get('Math').callprop('max', var.get('pos'), var.get('from')))
                    var.put('end', var.get('Math').callprop('min', (var.get('pos')+var.get('node').get('nodeSize')), var.get('to')))
                    var.put('newSet', var.get('mark').callprop('addToSet', var.get('marks')))
                    #for JS loop
                    var.put('i', Js(0.0))
                    while (var.get('i')<var.get('marks').get('length')):
                        try:
                            if var.get('marks').get(var.get('i')).callprop('isInSet', var.get('newSet')).neg():
                                if ((var.get('removing') and (var.get('removing').get('to')==var.get('start'))) and var.get('removing').get('mark').callprop('eq', var.get('marks').get(var.get('i')))):
                                    var.get('removing').put('to', var.get('end'))
                                else:
                                    var.get('removed').callprop('push', var.put('removing', var.get('RemoveMarkStep').create(var.get('start'), var.get('end'), var.get('marks').get(var.get('i')))))
                        finally:
                                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                    if (var.get('adding') and (var.get('adding').get('to')==var.get('start'))):
                        var.get('adding').put('to', var.get('end'))
                    else:
                        var.get('added').callprop('push', var.put('adding', var.get('AddMarkStep').create(var.get('start'), var.get('end'), var.get('mark'))))
            PyJs_anonymous_449_._set_name('anonymous')
            var.get(u"this").get('doc').callprop('nodesBetween', var.get('from'), var.get('to'), PyJs_anonymous_449_)
            @Js
            def PyJs_anonymous_450_(s, this, arguments, var=var):
                var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
                var.registers(['s'])
                return var.get('this$1').callprop('step', var.get('s'))
            PyJs_anonymous_450_._set_name('anonymous')
            var.get('removed').callprop('forEach', PyJs_anonymous_450_)
            @Js
            def PyJs_anonymous_451_(s, this, arguments, var=var):
                var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
                var.registers(['s'])
                return var.get('this$1').callprop('step', var.get('s'))
            PyJs_anonymous_451_._set_name('anonymous')
            var.get('added').callprop('forEach', PyJs_anonymous_451_)
            return var.get(u"this")
        PyJs_anonymous_448_._set_name('anonymous')
        var.get('Transform').get('prototype').put('addMark', PyJs_anonymous_448_)
        @Js
        def PyJs_anonymous_452_(PyJsArg_66726f6d_, to, mark, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'mark':mark, 'this':this, 'arguments':arguments}, var)
            var.registers(['step', 'mark', 'this$1', 'matched', 'to', 'from'])
            var.put('this$1', var.get(u"this"))
            if PyJsStrictEq(var.get('mark'),PyJsComma(Js(0.0), Js(None))):
                var.put('mark', var.get(u"null"))
            var.put('matched', Js([]))
            var.put('step', Js(0.0))
            @Js
            def PyJs_anonymous_453_(node, pos, this, arguments, var=var):
                var = Scope({'node':node, 'pos':pos, 'this':this, 'arguments':arguments}, var)
                var.registers(['toRemove', 'found$1', 'node', 'end', 'j', 'm', 'found', 'i', 'pos', 'style'])
                if var.get('node').get('isInline').neg():
                    return var.get('undefined')
                (var.put('step',Js(var.get('step').to_number())+Js(1))-Js(1))
                var.put('toRemove', var.get(u"null"))
                if var.get('mark').instanceof(var.get('dist').get('MarkType')):
                    var.put('found', var.get('mark').callprop('isInSet', var.get('node').get('marks')))
                    if var.get('found'):
                        var.put('toRemove', Js([var.get('found')]))
                else:
                    if var.get('mark'):
                        if var.get('mark').callprop('isInSet', var.get('node').get('marks')):
                            var.put('toRemove', Js([var.get('mark')]))
                    else:
                        var.put('toRemove', var.get('node').get('marks'))
                if (var.get('toRemove') and var.get('toRemove').get('length')):
                    var.put('end', var.get('Math').callprop('min', (var.get('pos')+var.get('node').get('nodeSize')), var.get('to')))
                    #for JS loop
                    var.put('i', Js(0.0))
                    while (var.get('i')<var.get('toRemove').get('length')):
                        try:
                            var.put('style', var.get('toRemove').get(var.get('i')))
                            var.put('found$1', PyJsComma(Js(0.0), Js(None)))
                            #for JS loop
                            var.put('j', Js(0.0))
                            while (var.get('j')<var.get('matched').get('length')):
                                try:
                                    var.put('m', var.get('matched').get(var.get('j')))
                                    if ((var.get('m').get('step')==(var.get('step')-Js(1.0))) and var.get('style').callprop('eq', var.get('matched').get(var.get('j')).get('style'))):
                                        var.put('found$1', var.get('m'))
                                finally:
                                        (var.put('j',Js(var.get('j').to_number())+Js(1))-Js(1))
                            if var.get('found$1'):
                                var.get('found$1').put('to', var.get('end'))
                                var.get('found$1').put('step', var.get('step'))
                            else:
                                PyJs_Object_454_ = Js({'style':var.get('style'),'from':var.get('Math').callprop('max', var.get('pos'), var.get('from')),'to':var.get('end'),'step':var.get('step')})
                                var.get('matched').callprop('push', PyJs_Object_454_)
                        finally:
                                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            PyJs_anonymous_453_._set_name('anonymous')
            var.get(u"this").get('doc').callprop('nodesBetween', var.get('from'), var.get('to'), PyJs_anonymous_453_)
            @Js
            def PyJs_anonymous_455_(m, this, arguments, var=var):
                var = Scope({'m':m, 'this':this, 'arguments':arguments}, var)
                var.registers(['m'])
                return var.get('this$1').callprop('step', var.get('RemoveMarkStep').create(var.get('m').get('from'), var.get('m').get('to'), var.get('m').get('style')))
            PyJs_anonymous_455_._set_name('anonymous')
            var.get('matched').callprop('forEach', PyJs_anonymous_455_)
            return var.get(u"this")
        PyJs_anonymous_452_._set_name('anonymous')
        var.get('Transform').get('prototype').put('removeMark', PyJs_anonymous_452_)
        @Js
        def PyJs_anonymous_456_(pos, parentType, match, this, arguments, var=var):
            var = Scope({'pos':pos, 'parentType':parentType, 'match':match, 'this':this, 'arguments':arguments}, var)
            var.registers(['child', 'match', 'node', 'this$1', 'end', 'delSteps', 'j', 'parentType', 'cur', 'i', 'pos', 'allowed', 'i$1', 'fill'])
            var.put('this$1', var.get(u"this"))
            if PyJsStrictEq(var.get('match'),PyJsComma(Js(0.0), Js(None))):
                var.put('match', var.get('parentType').get('contentMatch'))
            var.put('node', var.get(u"this").get('doc').callprop('nodeAt', var.get('pos')))
            var.put('delSteps', Js([]))
            var.put('cur', (var.get('pos')+Js(1.0)))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('node').get('childCount')):
                try:
                    var.put('child', var.get('node').callprop('child', var.get('i')))
                    var.put('end', (var.get('cur')+var.get('child').get('nodeSize')))
                    var.put('allowed', var.get('match').callprop('matchType', var.get('child').get('type'), var.get('child').get('attrs')))
                    if var.get('allowed').neg():
                        var.get('delSteps').callprop('push', var.get('ReplaceStep').create(var.get('cur'), var.get('end'), var.get('dist').get('Slice').get('empty')))
                    else:
                        var.put('match', var.get('allowed'))
                        #for JS loop
                        var.put('j', Js(0.0))
                        while (var.get('j')<var.get('child').get('marks').get('length')):
                            try:
                                if var.get('parentType').callprop('allowsMarkType', var.get('child').get('marks').get(var.get('j')).get('type')).neg():
                                    var.get('this$1').callprop('step', var.get('RemoveMarkStep').create(var.get('cur'), var.get('end'), var.get('child').get('marks').get(var.get('j'))))
                            finally:
                                    (var.put('j',Js(var.get('j').to_number())+Js(1))-Js(1))
                    var.put('cur', var.get('end'))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            if var.get('match').get('validEnd').neg():
                var.put('fill', var.get('match').callprop('fillBefore', var.get('dist').get('Fragment').get('empty'), Js(True)))
                var.get(u"this").callprop('replace', var.get('cur'), var.get('cur'), var.get('dist').get('Slice').create(var.get('fill'), Js(0.0), Js(0.0)))
            #for JS loop
            var.put('i$1', (var.get('delSteps').get('length')-Js(1.0)))
            while (var.get('i$1')>=Js(0.0)):
                try:
                    var.get('this$1').callprop('step', var.get('delSteps').get(var.get('i$1')))
                finally:
                        (var.put('i$1',Js(var.get('i$1').to_number())-Js(1))+Js(1))
            return var.get(u"this")
        PyJs_anonymous_456_._set_name('anonymous')
        var.get('Transform').get('prototype').put('clearIncompatible', PyJs_anonymous_456_)
        pass
        @Js
        def PyJs_anonymous_457_(PyJsArg_66726f6d_, to, slice, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'slice':slice, 'this':this, 'arguments':arguments}, var)
            var.registers(['step', 'from', 'slice', 'to'])
            if PyJsStrictEq(var.get('to'),PyJsComma(Js(0.0), Js(None))):
                var.put('to', var.get('from'))
            if PyJsStrictEq(var.get('slice'),PyJsComma(Js(0.0), Js(None))):
                var.put('slice', var.get('dist').get('Slice').get('empty'))
            var.put('step', var.get('replaceStep')(var.get(u"this").get('doc'), var.get('from'), var.get('to'), var.get('slice')))
            if var.get('step'):
                var.get(u"this").callprop('step', var.get('step'))
            return var.get(u"this")
        PyJs_anonymous_457_._set_name('anonymous')
        var.get('Transform').get('prototype').put('replace', PyJs_anonymous_457_)
        @Js
        def PyJs_anonymous_458_(PyJsArg_66726f6d_, to, content, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'content':content, 'this':this, 'arguments':arguments}, var)
            var.registers(['to', 'from', 'content'])
            return var.get(u"this").callprop('replace', var.get('from'), var.get('to'), var.get('dist').get('Slice').create(var.get('dist').get('Fragment').callprop('from', var.get('content')), Js(0.0), Js(0.0)))
        PyJs_anonymous_458_._set_name('anonymous')
        var.get('Transform').get('prototype').put('replaceWith', PyJs_anonymous_458_)
        @Js
        def PyJs_anonymous_459_(PyJsArg_66726f6d_, to, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'this':this, 'arguments':arguments}, var)
            var.registers(['to', 'from'])
            return var.get(u"this").callprop('replace', var.get('from'), var.get('to'), var.get('dist').get('Slice').get('empty'))
        PyJs_anonymous_459_._set_name('anonymous')
        var.get('Transform').get('prototype').put('delete', PyJs_anonymous_459_)
        @Js
        def PyJs_anonymous_460_(pos, content, this, arguments, var=var):
            var = Scope({'pos':pos, 'content':content, 'this':this, 'arguments':arguments}, var)
            var.registers(['content', 'pos'])
            return var.get(u"this").callprop('replaceWith', var.get('pos'), var.get('pos'), var.get('content'))
        PyJs_anonymous_460_._set_name('anonymous')
        var.get('Transform').get('prototype').put('insert', PyJs_anonymous_460_)
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
        def PyJs_Frontier_462_(PyJsArg_24706f73_, this, arguments, var=var):
            var = Scope({'$pos':PyJsArg_24706f73_, 'this':this, 'arguments':arguments, 'Frontier':PyJs_Frontier_462_}, var)
            var.registers(['match', 'this$1', 'd', 'parent', '$pos'])
            var.put('this$1', var.get(u"this"))
            var.get(u"this").put('open', Js([]))
            #for JS loop
            var.put('d', Js(0.0))
            while (var.get('d')<=var.get('$pos').get('depth')):
                try:
                    var.put('parent', var.get('$pos').callprop('node', var.get('d')))
                    var.put('match', var.get('parent').callprop('contentMatchAt', var.get('$pos').callprop('indexAfter', var.get('d'))))
                    PyJs_Object_463_ = Js({'parent':var.get('parent'),'match':var.get('match'),'content':var.get('dist').get('Fragment').get('empty'),'wrapper':Js(False),'openEnd':Js(0.0),'depth':var.get('d')})
                    var.get('this$1').get('open').callprop('push', PyJs_Object_463_)
                finally:
                        (var.put('d',Js(var.get('d').to_number())+Js(1))-Js(1))
            var.get(u"this").put('placed', Js([]))
        PyJs_Frontier_462_._set_name('Frontier')
        var.put('Frontier', PyJs_Frontier_462_)
        @Js
        def PyJs_placeSlice_464_(fragment, openStart, openEnd, PyJsArg_70617373_, parent, this, arguments, var=var):
            var = Scope({'fragment':fragment, 'openStart':openStart, 'openEnd':openEnd, 'pass':PyJsArg_70617373_, 'parent':parent, 'this':this, 'arguments':arguments, 'placeSlice':PyJs_placeSlice_464_}, var)
            var.registers(['child', 'result', 'openStart', 'openEnd', 'this$1', 'fragment', 'i', 'first', 'inner', 'parent', 'pass'])
            var.put('this$1', var.get(u"this"))
            if (var.get('openStart')>Js(0.0)):
                var.put('first', var.get('fragment').get('firstChild'))
                var.put('inner', var.get(u"this").callprop('placeSlice', var.get('first').get('content'), var.get('Math').callprop('max', Js(0.0), (var.get('openStart')-Js(1.0))), ((var.get('openEnd')-Js(1.0)) if (var.get('openEnd') and (var.get('fragment').get('childCount')==Js(1.0))) else Js(0.0)), var.get('pass'), var.get('first')))
                if (var.get('inner').get('content')!=var.get('first').get('content')):
                    if var.get('inner').get('content').get('size'):
                        var.put('fragment', var.get('fragment').callprop('replaceChild', Js(0.0), var.get('first').callprop('copy', var.get('inner').get('content'))))
                        var.put('openStart', (var.get('inner').get('openStart')+Js(1.0)))
                    else:
                        if (var.get('fragment').get('childCount')==Js(1.0)):
                            var.put('openEnd', Js(0.0))
                        var.put('fragment', var.get('fragment').callprop('cutByIndex', Js(1.0)))
                        var.put('openStart', Js(0.0))
            var.put('result', var.get(u"this").callprop('placeContent', var.get('fragment'), var.get('openStart'), var.get('openEnd'), var.get('pass'), var.get('parent')))
            if (((var.get('pass')>Js(2.0)) and var.get('result').get('size')) and (var.get('openStart')==Js(0.0))):
                #for JS loop
                var.put('i', Js(0.0))
                while (var.get('i')<var.get('result').get('content').get('childCount')):
                    try:
                        var.put('child', var.get('result').get('content').callprop('child', var.get('i')))
                        var.get('this$1').callprop('placeContent', var.get('child').get('content'), Js(0.0), ((var.get('openEnd')-Js(1.0)) if (var.get('openEnd') and (var.get('i')==(var.get('result').get('content').get('childCount').get('length')-Js(1.0)))) else Js(0.0)), var.get('pass'), var.get('child'))
                    finally:
                            (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                var.put('result', var.get('dist').get('Fragment').get('empty'))
            return var.get('result')
        PyJs_placeSlice_464_._set_name('placeSlice')
        var.get('Frontier').get('prototype').put('placeSlice', PyJs_placeSlice_464_)
        @Js
        def PyJs_placeContent_465_(fragment, openStart, openEnd, PyJsArg_70617373_, parent, this, arguments, var=var):
            var = Scope({'fragment':fragment, 'openStart':openStart, 'openEnd':openEnd, 'pass':PyJsArg_70617373_, 'parent':parent, 'this':this, 'arguments':arguments, 'placeContent':PyJs_placeContent_465_}, var)
            var.registers(['child', 'match', 'open', 'openStart', 'openEnd', 'last', 'this$1', 'placed', 'j', 'ch', 'pass', 'fragment', 'i', 'w', 'd', 'parent', 'fill', 'wrap'])
            var.put('this$1', var.get(u"this"))
            var.put('i', Js(0.0))
            #for JS loop
            
            while (var.get('i')<var.get('fragment').get('childCount')):
                try:
                    var.put('child', var.get('fragment').callprop('child', var.get('i')))
                    var.put('placed', Js(False))
                    var.put('last', (var.get('i')==(var.get('fragment').get('childCount')-Js(1.0))))
                    #for JS loop
                    var.put('d', (var.get(u"this").get('open').get('length')-Js(1.0)))
                    while (var.get('d')>=Js(0.0)):
                        try:
                            var.put('open', var.get('this$1').get('open').get(var.get('d')))
                            var.put('wrap', PyJsComma(Js(0.0), Js(None)))
                            if (((var.get('pass')>Js(1.0)) and var.put('wrap', var.get('open').get('match').callprop('findWrapping', var.get('child').get('type')))) and ((var.get('parent') and var.get('wrap').get('length')) and (var.get('wrap').get((var.get('wrap').get('length')-Js(1.0)))==var.get('parent').get('type'))).neg()):
                                while ((var.get(u"this").get('open').get('length')-Js(1.0))>var.get('d')):
                                    var.get('this$1').callprop('closeNode')
                                #for JS loop
                                var.put('w', Js(0.0))
                                while (var.get('w')<var.get('wrap').get('length')):
                                    try:
                                        var.get('open').put('match', var.get('open').get('match').callprop('matchType', var.get('wrap').get(var.get('w'))))
                                        (var.put('d',Js(var.get('d').to_number())+Js(1))-Js(1))
                                        PyJs_Object_466_ = Js({'parent':var.get('wrap').get(var.get('w')).callprop('create'),'match':var.get('wrap').get(var.get('w')).get('contentMatch'),'content':var.get('dist').get('Fragment').get('empty'),'wrapper':Js(True),'openEnd':Js(0.0),'depth':(var.get('d')+var.get('w'))})
                                        var.put('open', PyJs_Object_466_)
                                        var.get('this$1').get('open').callprop('push', var.get('open'))
                                    finally:
                                            (var.put('w',Js(var.get('w').to_number())+Js(1))-Js(1))
                            var.put('match', var.get('open').get('match').callprop('matchType', var.get('child').get('type')))
                            if var.get('match').neg():
                                var.put('fill', var.get('open').get('match').callprop('fillBefore', var.get('dist').get('Fragment').callprop('from', var.get('child'))))
                                if var.get('fill'):
                                    #for JS loop
                                    var.put('j', Js(0.0))
                                    while (var.get('j')<var.get('fill').get('childCount')):
                                        try:
                                            var.put('ch', var.get('fill').callprop('child', var.get('j')))
                                            var.get('this$1').callprop('addNode', var.get('open'), var.get('ch'), Js(0.0))
                                            var.put('match', var.get('open').get('match').callprop('matchFragment', var.get('ch')))
                                        finally:
                                                (var.put('j',Js(var.get('j').to_number())+Js(1))-Js(1))
                                else:
                                    if (var.get('parent') and var.get('open').get('match').callprop('matchType', var.get('parent').get('type'))):
                                        break
                                    else:
                                        continue
                            while ((var.get(u"this").get('open').get('length')-Js(1.0))>var.get('d')):
                                var.get('this$1').callprop('closeNode')
                            var.put('child', var.get('child').callprop('mark', var.get('open').get('parent').get('type').callprop('allowedMarks', var.get('child').get('marks'))))
                            if var.get('openStart'):
                                var.put('child', var.get('closeNodeStart')(var.get('child'), var.get('openStart'), (var.get('openEnd') if var.get('last') else Js(0.0))))
                                var.put('openStart', Js(0.0))
                            var.get('this$1').callprop('addNode', var.get('open'), var.get('child'), (var.get('openEnd') if var.get('last') else Js(0.0)))
                            var.get('open').put('match', var.get('match'))
                            if var.get('last'):
                                var.put('openEnd', Js(0.0))
                            var.put('placed', Js(True))
                            break
                        finally:
                                (var.put('d',Js(var.get('d').to_number())-Js(1))+Js(1))
                    if var.get('placed').neg():
                        break
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            if ((var.get(u"this").get('open').get('length')>Js(1.0)) and (((var.get('i')>Js(0.0)) and (var.get('i')==var.get('fragment').get('childCount'))) or (var.get('parent') and (var.get(u"this").get('open').get((var.get(u"this").get('open').get('length')-Js(1.0))).get('parent').get('type')==var.get('parent').get('type'))))):
                var.get(u"this").callprop('closeNode')
            return var.get('dist').get('Slice').create(var.get('fragment').callprop('cutByIndex', var.get('i')), var.get('openStart'), var.get('openEnd'))
        PyJs_placeContent_465_._set_name('placeContent')
        var.get('Frontier').get('prototype').put('placeContent', PyJs_placeContent_465_)
        @Js
        def PyJs_addNode_467_(open, node, openEnd, this, arguments, var=var):
            var = Scope({'open':open, 'node':node, 'openEnd':openEnd, 'this':this, 'arguments':arguments, 'addNode':PyJs_addNode_467_}, var)
            var.registers(['openEnd', 'open', 'node'])
            var.get('open').put('content', var.get('closeFragmentEnd')(var.get('open').get('content'), var.get('open').get('openEnd')).callprop('addToEnd', var.get('node')))
            var.get('open').put('openEnd', var.get('openEnd'))
        PyJs_addNode_467_._set_name('addNode')
        var.get('Frontier').get('prototype').put('addNode', PyJs_addNode_467_)
        @Js
        def PyJs_closeNode_468_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments, 'closeNode':PyJs_closeNode_468_}, var)
            var.registers(['open'])
            var.put('open', var.get(u"this").get('open').callprop('pop'))
            if (var.get('open').get('content').get('size')==Js(0.0)):
                pass
            else:
                if var.get('open').get('wrapper'):
                    var.get(u"this").callprop('addNode', var.get(u"this").get('open').get((var.get(u"this").get('open').get('length')-Js(1.0))), var.get('open').get('parent').callprop('copy', var.get('open').get('content')), (var.get('open').get('openEnd')+Js(1.0)))
                else:
                    PyJs_Object_469_ = Js({'depth':var.get('open').get('depth'),'content':var.get('open').get('content'),'openEnd':var.get('open').get('openEnd')})
                    var.get(u"this").get('placed').put(var.get('open').get('depth'), PyJs_Object_469_)
        PyJs_closeNode_468_._set_name('closeNode')
        var.get('Frontier').get('prototype').put('closeNode', PyJs_closeNode_468_)
        pass
        pass
        pass
        @Js
        def PyJs_anonymous_470_(PyJsArg_66726f6d_, to, slice, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'slice':slice, 'this':this, 'arguments':arguments}, var)
            var.registers(['slice', 'preferredDepth', 'insert', 'j', 'openDepth', 'preferredTarget', 'this$1', 'preferredTargetIndex', 'leftNodes', 'to', 'from', 'i', 'index', 'spec', 'pos', 'parent', 'i$1', 'targetDepths', '$to', 'expand', 'node', '$from', 'content', 'd', 'targetDepth'])
            var.put('this$1', var.get(u"this"))
            if var.get('slice').get('size').neg():
                return var.get(u"this").callprop('deleteRange', var.get('from'), var.get('to'))
            var.put('$from', var.get(u"this").get('doc').callprop('resolve', var.get('from')))
            var.put('$to', var.get(u"this").get('doc').callprop('resolve', var.get('to')))
            if var.get('fitsTrivially')(var.get('$from'), var.get('$to'), var.get('slice')):
                return var.get(u"this").callprop('step', var.get('ReplaceStep').create(var.get('from'), var.get('to'), var.get('slice')))
            var.put('targetDepths', var.get('coveredDepths')(var.get('$from'), var.get(u"this").get('doc').callprop('resolve', var.get('to'))))
            if (var.get('targetDepths').get((var.get('targetDepths').get('length')-Js(1.0)))==Js(0.0)):
                var.get('targetDepths').callprop('pop')
            var.put('preferredTarget', (-(var.get('$from').get('depth')+Js(1.0))))
            var.get('targetDepths').callprop('unshift', var.get('preferredTarget'))
            #for JS loop
            var.put('d', var.get('$from').get('depth'))
            var.put('pos', (var.get('$from').get('pos')-Js(1.0)))
            while (var.get('d')>Js(0.0)):
                try:
                    var.put('spec', var.get('$from').callprop('node', var.get('d')).get('type').get('spec'))
                    if (var.get('spec').get('defining') or var.get('spec').get('isolating')):
                        break
                    if (var.get('targetDepths').callprop('indexOf', var.get('d'))>(-Js(1.0))):
                        var.put('preferredTarget', var.get('d'))
                    else:
                        if (var.get('$from').callprop('before', var.get('d'))==var.get('pos')):
                            var.get('targetDepths').callprop('splice', Js(1.0), Js(0.0), (-var.get('d')))
                finally:
                        PyJsComma((var.put('d',Js(var.get('d').to_number())-Js(1))+Js(1)),(var.put('pos',Js(var.get('pos').to_number())-Js(1))+Js(1)))
            var.put('preferredTargetIndex', var.get('targetDepths').callprop('indexOf', var.get('preferredTarget')))
            var.put('leftNodes', Js([]))
            var.put('preferredDepth', var.get('slice').get('openStart'))
            #for JS loop
            var.put('content', var.get('slice').get('content'))
            var.put('i', Js(0.0))
            while 1:
                try:
                    var.put('node', var.get('content').get('firstChild'))
                    var.get('leftNodes').callprop('push', var.get('node'))
                    if (var.get('i')==var.get('slice').get('openStart')):
                        break
                    var.put('content', var.get('node').get('content'))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            if (((var.get('preferredDepth')>Js(0.0)) and var.get('leftNodes').get((var.get('preferredDepth')-Js(1.0))).get('type').get('spec').get('defining')) and (var.get('$from').callprop('node', var.get('preferredTargetIndex')).get('type')!=var.get('leftNodes').get((var.get('preferredDepth')-Js(1.0))).get('type'))):
                var.put('preferredDepth', Js(1.0), '-')
            else:
                if ((((var.get('preferredDepth')>=Js(2.0)) and var.get('leftNodes').get((var.get('preferredDepth')-Js(1.0))).get('isTextblock')) and var.get('leftNodes').get((var.get('preferredDepth')-Js(2.0))).get('type').get('spec').get('defining')) and (var.get('$from').callprop('node', var.get('preferredTargetIndex')).get('type')!=var.get('leftNodes').get((var.get('preferredDepth')-Js(2.0))).get('type'))):
                    var.put('preferredDepth', Js(2.0), '-')
            #for JS loop
            var.put('j', var.get('slice').get('openStart'))
            while (var.get('j')>=Js(0.0)):
                try:
                    var.put('openDepth', (((var.get('j')+var.get('preferredDepth'))+Js(1.0))%(var.get('slice').get('openStart')+Js(1.0))))
                    var.put('insert', var.get('leftNodes').get(var.get('openDepth')))
                    if var.get('insert').neg():
                        continue
                    #for JS loop
                    var.put('i$1', Js(0.0))
                    while (var.get('i$1')<var.get('targetDepths').get('length')):
                        try:
                            var.put('targetDepth', var.get('targetDepths').get(((var.get('i$1')+var.get('preferredTargetIndex'))%var.get('targetDepths').get('length'))))
                            var.put('expand', Js(True))
                            if (var.get('targetDepth')<Js(0.0)):
                                var.put('expand', Js(False))
                                var.put('targetDepth', (-var.get('targetDepth')))
                            var.put('parent', var.get('$from').callprop('node', (var.get('targetDepth')-Js(1.0))))
                            var.put('index', var.get('$from').callprop('index', (var.get('targetDepth')-Js(1.0))))
                            if var.get('parent').callprop('canReplaceWith', var.get('index'), var.get('index'), var.get('insert').get('type'), var.get('insert').get('marks')):
                                def PyJs_LONG_471_(var=var):
                                    return var.get('this$1').callprop('replace', var.get('$from').callprop('before', var.get('targetDepth')), (var.get('$to').callprop('after', var.get('targetDepth')) if var.get('expand') else var.get('to')), var.get('dist').get('Slice').create(var.get('closeFragment')(var.get('slice').get('content'), Js(0.0), var.get('slice').get('openStart'), var.get('openDepth')), var.get('openDepth'), var.get('slice').get('openEnd')))
                                return PyJs_LONG_471_()
                        finally:
                                (var.put('i$1',Js(var.get('i$1').to_number())+Js(1))-Js(1))
                finally:
                        (var.put('j',Js(var.get('j').to_number())-Js(1))+Js(1))
            return var.get(u"this").callprop('replace', var.get('from'), var.get('to'), var.get('slice'))
        PyJs_anonymous_470_._set_name('anonymous')
        var.get('Transform').get('prototype').put('replaceRange', PyJs_anonymous_470_)
        pass
        @Js
        def PyJs_anonymous_472_(PyJsArg_66726f6d_, to, node, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'node':node, 'this':this, 'arguments':arguments}, var)
            var.registers(['point', 'from', 'to', 'node'])
            if ((var.get('node').get('isInline').neg() and (var.get('from')==var.get('to'))) and var.get(u"this").get('doc').callprop('resolve', var.get('from')).get('parent').get('content').get('size')):
                var.put('point', var.get('insertPoint')(var.get(u"this").get('doc'), var.get('from'), var.get('node').get('type')))
                if (var.get('point')!=var.get(u"null")):
                    var.put('from', var.put('to', var.get('point')))
            return var.get(u"this").callprop('replaceRange', var.get('from'), var.get('to'), var.get('dist').get('Slice').create(var.get('dist').get('Fragment').callprop('from', var.get('node')), Js(0.0), Js(0.0)))
        PyJs_anonymous_472_._set_name('anonymous')
        var.get('Transform').get('prototype').put('replaceRangeWith', PyJs_anonymous_472_)
        @Js
        def PyJs_anonymous_473_(PyJsArg_66726f6d_, to, this, arguments, var=var):
            var = Scope({'from':PyJsArg_66726f6d_, 'to':to, 'this':this, 'arguments':arguments}, var)
            var.registers(['$to', '$from', 'this$1', 'last', 'covered', 'from', 'depth', 'i', 'to', 'd'])
            var.put('this$1', var.get(u"this"))
            var.put('$from', var.get(u"this").get('doc').callprop('resolve', var.get('from')))
            var.put('$to', var.get(u"this").get('doc').callprop('resolve', var.get('to')))
            var.put('covered', var.get('coveredDepths')(var.get('$from'), var.get('$to')))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('covered').get('length')):
                try:
                    var.put('depth', var.get('covered').get(var.get('i')))
                    var.put('last', (var.get('i')==(var.get('covered').get('length')-Js(1.0))))
                    if ((var.get('last') and (var.get('depth')==Js(0.0))) or var.get('$from').callprop('node', var.get('depth')).get('type').get('contentMatch').get('validEnd')):
                        return var.get('this$1').callprop('delete', var.get('$from').callprop('start', var.get('depth')), var.get('$to').callprop('end', var.get('depth')))
                    if ((var.get('depth')>Js(0.0)) and (var.get('last') or var.get('$from').callprop('node', (var.get('depth')-Js(1.0))).callprop('canReplace', var.get('$from').callprop('index', (var.get('depth')-Js(1.0))), var.get('$to').callprop('indexAfter', (var.get('depth')-Js(1.0)))))):
                        return var.get('this$1').callprop('delete', var.get('$from').callprop('before', var.get('depth')), var.get('$to').callprop('after', var.get('depth')))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            #for JS loop
            var.put('d', Js(1.0))
            while (var.get('d')<=var.get('$from').get('depth')):
                try:
                    if (((var.get('from')-var.get('$from').callprop('start', var.get('d')))==(var.get('$from').get('depth')-var.get('d'))) and (var.get('to')>var.get('$from').callprop('end', var.get('d')))):
                        return var.get('this$1').callprop('delete', var.get('$from').callprop('before', var.get('d')), var.get('to'))
                finally:
                        (var.put('d',Js(var.get('d').to_number())+Js(1))-Js(1))
            return var.get(u"this").callprop('delete', var.get('from'), var.get('to'))
        PyJs_anonymous_473_._set_name('anonymous')
        var.get('Transform').get('prototype').put('deleteRange', PyJs_anonymous_473_)
        pass
        var.get('exports').put('Transform', var.get('Transform'))
        var.get('exports').put('TransformError', var.get('TransformError'))
        var.get('exports').put('Step', var.get('Step'))
        var.get('exports').put('StepResult', var.get('StepResult'))
        var.get('exports').put('joinPoint', var.get('joinPoint'))
        var.get('exports').put('canJoin', var.get('canJoin'))
        var.get('exports').put('canSplit', var.get('canSplit'))
        var.get('exports').put('insertPoint', var.get('insertPoint'))
        var.get('exports').put('dropPoint', var.get('dropPoint'))
        var.get('exports').put('liftTarget', var.get('liftTarget'))
        var.get('exports').put('findWrapping', var.get('findWrapping'))
        var.get('exports').put('StepMap', var.get('StepMap'))
        var.get('exports').put('MapResult', var.get('MapResult'))
        var.get('exports').put('Mapping', var.get('Mapping'))
        var.get('exports').put('AddMarkStep', var.get('AddMarkStep'))
        var.get('exports').put('RemoveMarkStep', var.get('RemoveMarkStep'))
        var.get('exports').put('ReplaceStep', var.get('ReplaceStep'))
        var.get('exports').put('ReplaceAroundStep', var.get('ReplaceAroundStep'))
        var.get('exports').put('replaceStep', var.get('replaceStep'))
    PyJs_anonymous_355_._set_name('anonymous')
    var.put('dist$1', var.get('createCommonjsModule')(PyJs_anonymous_355_))
    var.get('unwrapExports')(var.get('dist$1'))
    var.put('dist_1$1', var.get('dist$1').get('Transform'))
    var.put('dist_2$1', var.get('dist$1').get('TransformError'))
    var.put('dist_3$1', var.get('dist$1').get('Step'))
    var.put('dist_4$1', var.get('dist$1').get('StepResult'))
    var.put('dist_5$1', var.get('dist$1').get('joinPoint'))
    var.put('dist_6$1', var.get('dist$1').get('canJoin'))
    var.put('dist_7$1', var.get('dist$1').get('canSplit'))
    var.put('dist_8$1', var.get('dist$1').get('insertPoint'))
    var.put('dist_9$1', var.get('dist$1').get('dropPoint'))
    var.put('dist_10$1', var.get('dist$1').get('liftTarget'))
    var.put('dist_11$1', var.get('dist$1').get('findWrapping'))
    var.put('dist_12$1', var.get('dist$1').get('StepMap'))
    var.put('dist_13$1', var.get('dist$1').get('MapResult'))
    var.put('dist_14', var.get('dist$1').get('Mapping'))
    var.put('dist_15', var.get('dist$1').get('AddMarkStep'))
    var.put('dist_16', var.get('dist$1').get('RemoveMarkStep'))
    var.put('dist_17', var.get('dist$1').get('ReplaceStep'))
    var.put('dist_18', var.get('dist$1').get('ReplaceAroundStep'))
    var.put('dist_19', var.get('dist$1').get('replaceStep'))
    @Js
    def PyJs_anonymous_475_(doc_data, spec_data, this, arguments, var=var):
        var = Scope({'doc_data':doc_data, 'spec_data':spec_data, 'this':this, 'arguments':arguments}, var)
        var.registers(['schema', 'doc_data', 'schemaSpec', 'spec_data'])
        PyJs_Object_476_ = Js({'marks':var.get('orderedmap').create(var.get('spec_data').get('marks').get('content')),'nodes':var.get('orderedmap').create(var.get('spec_data').get('nodes').get('content'))})
        var.put('schemaSpec', PyJs_Object_476_)
        var.put('schema', var.get('dist_8').create(var.get('schemaSpec')))
        return var.get('schema').callprop('nodeFromJSON', var.get('doc_data'))
    PyJs_anonymous_475_._set_name('anonymous')
    var.put('create_doc', PyJs_anonymous_475_)
    @Js
    def PyJs_anonymous_477_(steps_data, doc, this, arguments, var=var):
        var = Scope({'steps_data':steps_data, 'doc':doc, 'this':this, 'arguments':arguments}, var)
        var.registers(['steps_data', 'schema', 'steps', 'doc'])
        var.put('schema', var.get('doc').get('type').get('schema'))
        @Js
        def PyJs_anonymous_478_(s, this, arguments, var=var):
            var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
            var.registers(['s', 'assign'])
            pass
            return PyJsComma(PyJsComma(var.put('assign', var.get('dist_3$1').callprop('fromJSON', var.get('schema'), var.get('s')).callprop('apply', var.get('doc'))),var.put('doc', var.get('assign').get('doc'))),var.get('assign'))
        PyJs_anonymous_478_._set_name('anonymous')
        var.put('steps', var.get('steps_data').callprop('map', PyJs_anonymous_478_))
        return var.get('doc')
    PyJs_anonymous_477_._set_name('anonymous')
    var.put('transform_doc', PyJs_anonymous_477_)
    @Js
    def PyJs_anonymous_479_(doc_data_json, spec_data_json, this, arguments, var=var):
        var = Scope({'doc_data_json':doc_data_json, 'spec_data_json':spec_data_json, 'this':this, 'arguments':arguments}, var)
        var.registers(['doc_data_json', 'schema', 'spec_data_json', 'schemaSpec', 'doc_data', 'spec_data'])
        var.put('doc_data', var.get('JSON').callprop('parse', var.get('doc_data_json')))
        var.put('spec_data', var.get('JSON').callprop('parse', var.get('spec_data_json')))
        PyJs_Object_480_ = Js({'marks':var.get('orderedmap').create(var.get('spec_data').get('marks').get('content')),'nodes':var.get('orderedmap').create(var.get('spec_data').get('nodes').get('content'))})
        var.put('schemaSpec', PyJs_Object_480_)
        var.put('schema', var.get('dist_8').create(var.get('schemaSpec')))
        return var.get('schema').callprop('nodeFromJSON', var.get('doc_data'))
    PyJs_anonymous_479_._set_name('anonymous')
    var.put('create_doc_json', PyJs_anonymous_479_)
    @Js
    def PyJs_anonymous_481_(steps_data_json, doc, this, arguments, var=var):
        var = Scope({'steps_data_json':steps_data_json, 'doc':doc, 'this':this, 'arguments':arguments}, var)
        var.registers(['doc', 'steps_data', 'schema', 'steps_data_json', 'steps'])
        var.put('steps_data', var.get('JSON').callprop('parse', var.get('steps_data_json')))
        var.put('schema', var.get('doc').get('type').get('schema'))
        @Js
        def PyJs_anonymous_482_(s, this, arguments, var=var):
            var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
            var.registers(['s', 'assign'])
            pass
            return PyJsComma(PyJsComma(var.put('assign', var.get('dist_3$1').callprop('fromJSON', var.get('schema'), var.get('s')).callprop('apply', var.get('doc'))),var.put('doc', var.get('assign').get('doc'))),var.get('assign'))
        PyJs_anonymous_482_._set_name('anonymous')
        var.put('steps', var.get('steps_data').callprop('map', PyJs_anonymous_482_))
        return var.get('doc')
    PyJs_anonymous_481_._set_name('anonymous')
    var.put('transform_doc_json', PyJs_anonymous_481_)
    var.get('exports').put('create_doc', var.get('create_doc'))
    var.get('exports').put('transform_doc', var.get('transform_doc'))
    var.get('exports').put('create_doc_json', var.get('create_doc_json'))
    var.get('exports').put('transform_doc_json', var.get('transform_doc_json'))
    PyJs_Object_483_ = Js({'value':Js(True)})
    var.get('Object').callprop('defineProperty', var.get('exports'), Js('__esModule'), PyJs_Object_483_)
PyJs_anonymous_0_._set_name('anonymous')
@Js
def PyJs_anonymous_484_(PyJsArg_676c6f62616c_, factory, this, arguments, var=var):
    var = Scope({'global':PyJsArg_676c6f62616c_, 'factory':factory, 'this':this, 'arguments':arguments}, var)
    var.registers(['global', 'factory'])
    def PyJs_LONG_486_(var=var):
        PyJs_Object_485_ = Js({})
        return (var.get('factory')(var.get('exports')) if (PyJsStrictEq(var.get('exports',throw=False).typeof(),Js('object')) and PyJsStrictNeq(var.get('module',throw=False).typeof(),Js('undefined'))) else (var.get('define')(Js([Js('exports')]), var.get('factory')) if (PyJsStrictEq(var.get('define',throw=False).typeof(),Js('function')) and var.get('define').get('amd')) else var.get('factory')(var.get('global').put('prosemirror', PyJs_Object_485_))))
    PyJs_LONG_486_()
PyJs_anonymous_484_._set_name('anonymous')
PyJs_anonymous_484_(var.get(u"this"), PyJs_anonymous_0_)
pass


# Add lib to the module scope
js_lib = var.to_python()