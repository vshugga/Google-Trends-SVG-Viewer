//javascript/closure/base.js
/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Bootstrap for the Google JS Library (Closure).
 *
 * In uncompiled mode base.js will attempt to load Closure's deps file, unless
 * the global <code>CLOSURE_NO_DEPS</code> is set to true.  This allows projects
 * to include their own deps file(s) from different locations.
 *
 * Avoid including base.js more than once. This is strictly discouraged and not
 * supported. goog.require(...) won't work properly in that case.
 *
 * @provideGoog
 */


/**
 * @define {boolean} Overridden to true by the compiler.
 */
var COMPILED = false;


/**
 * Base namespace for the Closure library.  Checks to see goog is already
 * defined in the current scope before assigning to prevent clobbering if
 * base.js is loaded more than once.
 *
 * @const
 */
var goog = goog || {};

/**
 * Reference to the global object.
 * https://www.ecma-international.org/ecma-262/9.0/index.html#sec-global-object
 *
 * More info on this implementation here:
 * https://docs.google.com/document/d/1NAeW4Wk7I7FV0Y2tcUFvQdGMc89k2vdgSXInw8_nvCI/edit
 *
 * @const
 * @suppress {undefinedVars} self won't be referenced unless `this` is falsy.
 * @type {!Global}
 */
goog.global =
    // Check `this` first for backwards compatibility.
    // Valid unless running as an ES module or in a function wrapper called
    //   without setting `this` properly.
    // Note that base.js can't usefully be imported as an ES module, but it may
    // be compiled into bundles that are loadable as ES modules.
    this ||
    // https://developer.mozilla.org/en-US/docs/Web/API/Window/self
    // For in-page browser environments and workers.
    self;


/**
 * A hook for overriding the define values in uncompiled mode.
 *
 * In uncompiled mode, `CLOSURE_UNCOMPILED_DEFINES` may be defined before
 * loading base.js.  If a key is defined in `CLOSURE_UNCOMPILED_DEFINES`,
 * `goog.define` will use the value instead of the default value.  This
 * allows flags to be overwritten without compilation (this is normally
 * accomplished with the compiler's "define" flag).
 *
 * Example:
 * <pre>
 *   var CLOSURE_UNCOMPILED_DEFINES = {'goog.DEBUG': false};
 * </pre>
 *
 * @type {Object<string, (string|number|boolean)>|undefined}
 */
goog.global.CLOSURE_UNCOMPILED_DEFINES;


/**
 * A hook for overriding the define values in uncompiled or compiled mode,
 * like CLOSURE_UNCOMPILED_DEFINES but effective in compiled code.  In
 * uncompiled code CLOSURE_UNCOMPILED_DEFINES takes precedence.
 *
 * Also unlike CLOSURE_UNCOMPILED_DEFINES the values must be number, boolean or
 * string literals or the compiler will emit an error.
 *
 * While any @define value may be set, only those set with goog.define will be
 * effective for uncompiled code.
 *
 * Example:
 * <pre>
 *   var CLOSURE_DEFINES = {'goog.DEBUG': false} ;
 * </pre>
 *
 * @type {Object<string, (string|number|boolean)>|undefined}
 */
goog.global.CLOSURE_DEFINES;


/**
 * Builds an object structure for the provided namespace path, ensuring that
 * names that already exist are not overwritten. For example:
 * "a.b.c" -> a = {};a.b={};a.b.c={};
 * Used by goog.provide and goog.exportSymbol.
 * @param {string} name The name of the object that this file defines.
 * @param {*=} object The object to expose at the end of the path.
 * @param {boolean=} overwriteImplicit If object is set and a previous call
 *     implicitly constructed the namespace given by name, this parameter
 *     controls whether object should overwrite the implicitly constructed
 *     namespace or be merged into it. Defaults to false.
 * @param {?Object=} objectToExportTo The object to add the path to; if this
 *     field is not specified, its value defaults to `goog.global`.
 * @private
 */
goog.exportPath_ = function(name, object, overwriteImplicit, objectToExportTo) {
  var parts = name.split('.');
  var cur = objectToExportTo || goog.global;

  // Internet Explorer exhibits strange behavior when throwing errors from
  // methods externed in this manner.  See the testExportSymbolExceptions in
  // base_test.html for an example.
  if (!(parts[0] in cur) && typeof cur.execScript != 'undefined') {
    cur.execScript('var ' + parts[0]);
  }

  for (var part; parts.length && (part = parts.shift());) {
    if (!parts.length && object !== undefined) {
      if (!overwriteImplicit && goog.isObject(object) &&
          goog.isObject(cur[part])) {
        // Merge properties on object (the input parameter) with the existing
        // implicitly defined namespace, so as to not clobber previously
        // defined child namespaces.
        for (var prop in object) {
          if (object.hasOwnProperty(prop)) {
            cur[part][prop] = object[prop];
          }
        }
      } else {
        // Either there is no existing implicit namespace, or overwriteImplicit
        // is set to true, so directly assign object (the input parameter) to
        // the namespace.
        cur[part] = object;
      }
    } else if (cur[part] && cur[part] !== Object.prototype[part]) {
      cur = cur[part];
    } else {
      cur = cur[part] = {};
    }
  }
};


/**
 * Defines a named value. In uncompiled mode, the value is retrieved from
 * CLOSURE_DEFINES or CLOSURE_UNCOMPILED_DEFINES if the object is defined and
 * has the property specified, and otherwise used the defined defaultValue.
 * When compiled the default can be overridden using the compiler options or the
 * value set in the CLOSURE_DEFINES object. Returns the defined value so that it
 * can be used safely in modules. Note that the value type MUST be either
 * boolean, number, or string.
 *
 * @param {string} name The distinguished name to provide.
 * @param {T} defaultValue
 * @return {T} The defined value.
 * @template T
 */
goog.define = function(name, defaultValue) {
  var value = defaultValue;
  if (!COMPILED) {
    var uncompiledDefines = goog.global.CLOSURE_UNCOMPILED_DEFINES;
    var defines = goog.global.CLOSURE_DEFINES;
    if (uncompiledDefines &&
        // Anti DOM-clobbering runtime check (b/37736576).
        /** @type {?} */ (uncompiledDefines).nodeType === undefined &&
        Object.prototype.hasOwnProperty.call(uncompiledDefines, name)) {
      value = uncompiledDefines[name];
    } else if (
        defines &&
        // Anti DOM-clobbering runtime check (b/37736576).
        /** @type {?} */ (defines).nodeType === undefined &&
        Object.prototype.hasOwnProperty.call(defines, name)) {
      value = defines[name];
    }
  }
  return value;
};


/**
 * @define {number} Integer year indicating the set of browser features that are
 * guaranteed to be present.  This is defined to include exactly features that
 * work correctly on all "modern" browsers that are stable on January 1 of the
 * specified year.  For example,
 * ```js
 * if (goog.FEATURESET_YEAR >= 2019) {
 *   // use APIs known to be available on all major stable browsers Jan 1, 2019
 * } else {
 *   // polyfill for older browsers
 * }
 * ```
 * This is intended to be the primary define for removing
 * unnecessary browser compatibility code (such as ponyfills and workarounds),
 * and should inform the default value for most other defines:
 * ```js
 * const ASSUME_NATIVE_PROMISE =
 *     goog.define('ASSUME_NATIVE_PROMISE', goog.FEATURESET_YEAR >= 2016);
 * ```
 *
 * The default assumption is that IE9 is the lowest supported browser, which was
 * first available Jan 1, 2012.
 *
 * TODO(mathiasb): Reference more thorough documentation when it's available.
 */
goog.FEATURESET_YEAR = goog.define('goog.FEATURESET_YEAR', 2012);


/**
 * @define {boolean} DEBUG is provided as a convenience so that debugging code
 * that should not be included in a production. It can be easily stripped
 * by specifying --define goog.DEBUG=false to the Closure Compiler aka
 * JSCompiler. For example, most toString() methods should be declared inside an
 * "if (goog.DEBUG)" conditional because they are generally used for debugging
 * purposes and it is difficult for the JSCompiler to statically determine
 * whether they are used.
 */
goog.DEBUG = goog.define('goog.DEBUG', true);


/**
 * @define {string} LOCALE defines the locale being used for compilation. It is
 * used to select locale specific data to be compiled in js binary. BUILD rule
 * can specify this value by "--define goog.LOCALE=<locale_name>" as a compiler
 * option.
 *
 * Take into account that the locale code format is important. You should use
 * the canonical Unicode format with hyphen as a delimiter. Language must be
 * lowercase, Language Script - Capitalized, Region - UPPERCASE.
 * There are few examples: pt-BR, en, en-US, sr-Latin-BO, zh-Hans-CN.
 *
 * See more info about locale codes here:
 * http://www.unicode.org/reports/tr35/#Unicode_Language_and_Locale_Identifiers
 *
 * For language codes you should use values defined by ISO 693-1. See it here
 * http://www.w3.org/WAI/ER/IG/ert/iso639.htm. There is only one exception from
 * this rule: the Hebrew language. For legacy reasons the old code (iw) should
 * be used instead of the new code (he).
 *
 * MOE:begin_intracomment_strip
 * See http://g3doc/i18n/identifiers/g3doc/synonyms.
 * MOE:end_intracomment_strip
 */
goog.LOCALE = goog.define('goog.LOCALE', 'en');  // default to en


/**
 * This method is intended to be used for bookkeeping purposes.  We would
 * like to distinguish uses of goog.LOCALE used for code stripping purposes
 * and uses of goog.LOCALE for other uses (such as URL parameters).
 *
 * This allows us to ban direct uses of goog.LOCALE and to ensure that all
 * code has been transformed to our new localization build scheme.
 *
 * @return {string}
 *
 */
goog.getLocale = function() {
  return goog.LOCALE;
};


/**
 * @define {boolean} Whether this code is running on trusted sites.
 *
 * On untrusted sites, several native functions can be defined or overridden by
 * external libraries like Prototype, Datejs, and JQuery and setting this flag
 * to false forces closure to use its own implementations when possible.
 *
 * If your JavaScript can be loaded by a third party site and you are wary about
 * relying on non-standard implementations, specify
 * "--define goog.TRUSTED_SITE=false" to the compiler.
 */
goog.TRUSTED_SITE = goog.define('goog.TRUSTED_SITE', true);


/**
 * @define {boolean} Whether code that calls {@link goog.setTestOnly} should
 *     be disallowed in the compilation unit.
 */
goog.DISALLOW_TEST_ONLY_CODE =
    goog.define('goog.DISALLOW_TEST_ONLY_CODE', COMPILED && !goog.DEBUG);


/**
 * @define {boolean} Whether to use a Chrome app CSP-compliant method for
 *     loading scripts via goog.require. @see appendScriptSrcNode_.
 */
goog.ENABLE_CHROME_APP_SAFE_SCRIPT_LOADING =
    goog.define('goog.ENABLE_CHROME_APP_SAFE_SCRIPT_LOADING', false);


/**
 * Defines a namespace in Closure.
 *
 * A namespace may only be defined once in a codebase. It may be defined using
 * goog.provide() or goog.module().
 *
 * The presence of one or more goog.provide() calls in a file indicates
 * that the file defines the given objects/namespaces.
 * Provided symbols must not be null or undefined.
 *
 * In addition, goog.provide() creates the object stubs for a namespace
 * (for example, goog.provide("goog.foo.bar") will create the object
 * goog.foo.bar if it does not already exist).
 *
 * Build tools also scan for provide/require/module statements
 * to discern dependencies, build dependency files (see deps.js), etc.
 *
 * @see goog.require
 * @see goog.module
 * @param {string} name Namespace provided by this file in the form
 *     "goog.package.part".
 * deprecated Use goog.module (see b/159289405)
 */
goog.provide = function(name) {
  if (goog.isInModuleLoader_()) {
    throw new Error('goog.provide cannot be used within a module.');
  }
  if (!COMPILED) {
    // Ensure that the same namespace isn't provided twice.
    // A goog.module/goog.provide maps a goog.require to a specific file
    if (goog.isProvided_(name)) {
      throw new Error('Namespace "' + name + '" already declared.');
    }
  }

  goog.constructNamespace_(name);
};


/**
 * @param {string} name Namespace provided by this file in the form
 *     "goog.package.part".
 * @param {?Object=} object The object to embed in the namespace.
 * @param {boolean=} overwriteImplicit If object is set and a previous call
 *     implicitly constructed the namespace given by name, this parameter
 *     controls whether opt_obj should overwrite the implicitly constructed
 *     namespace or be merged into it. Defaults to false.
 * @private
 */
goog.constructNamespace_ = function(name, object, overwriteImplicit) {
  if (!COMPILED) {
    delete goog.implicitNamespaces_[name];

    var namespace = name;
    while ((namespace = namespace.substring(0, namespace.lastIndexOf('.')))) {
      if (goog.getObjectByName(namespace)) {
        break;
      }
      goog.implicitNamespaces_[namespace] = true;
    }
  }

  goog.exportPath_(name, object, overwriteImplicit);
};


/**
 * According to the CSP3 spec a nonce must be a valid base64 string.
 * @see https://www.w3.org/TR/CSP3/#grammardef-base64-value
 * @private @const
 */
goog.NONCE_PATTERN_ = /^[\w+/_-]+[=]{0,2}$/;


/**
 * Returns CSP nonce, if set for any script tag.
 * @param {?Window=} opt_window The window context used to retrieve the nonce.
 *     Defaults to global context.
 * @return {string} CSP nonce or empty string if no nonce is present.
 * @private
 */
goog.getScriptNonce_ = function(opt_window) {
  var doc = (opt_window || goog.global).document;
  var script = doc.querySelector && doc.querySelector('script[nonce]');
  if (script) {
    // Try to get the nonce from the IDL property first, because browsers that
    // implement additional nonce protection features (currently only Chrome) to
    // prevent nonce stealing via CSS do not expose the nonce via attributes.
    // See https://github.com/whatwg/html/issues/2369
    var nonce = script['nonce'] || script.getAttribute('nonce');
    if (nonce && goog.NONCE_PATTERN_.test(nonce)) {
      return nonce;
    }
  }
  return '';
};


/**
 * Module identifier validation regexp.
 * Note: This is a conservative check, it is very possible to be more lenient,
 *   the primary exclusion here is "/" and "\" and a leading ".", these
 *   restrictions are intended to leave the door open for using goog.require
 *   with relative file paths rather than module identifiers.
 * @private
 */
goog.VALID_MODULE_RE_ = /^[a-zA-Z_$][a-zA-Z0-9._$]*$/;


/**
 * Defines a module in Closure.
 *
 * Marks that this file must be loaded as a module and claims the namespace.
 *
 * A namespace may only be defined once in a codebase. It may be defined using
 * goog.provide() or goog.module().
 *
 * goog.module() has three requirements:
 * - goog.module may not be used in the same file as goog.provide.
 * - goog.module must be the first statement in the file.
 * - only one goog.module is allowed per file.
 *
 * When a goog.module annotated file is loaded, it is enclosed in
 * a strict function closure. This means that:
 * - any variables declared in a goog.module file are private to the file
 * (not global), though the compiler is expected to inline the module.
 * - The code must obey all the rules of "strict" JavaScript.
 * - the file will be marked as "use strict"
 *
 * NOTE: unlike goog.provide, goog.module does not declare any symbols by
 * itself. If declared symbols are desired, use
 * goog.module.declareLegacyNamespace().
 *
 * MOE:begin_intracomment_strip
 * See the goog.module announcement at http://go/goog.module-announce
 * MOE:end_intracomment_strip
 *
 * See the public goog.module proposal: http://goo.gl/Va1hin
 *
 * @param {string} name Namespace provided by this file in the form
 *     "goog.package.part", is expected but not required.
 * @return {void}
 */
goog.module = function(name) {
  if (typeof name !== 'string' || !name ||
      name.search(goog.VALID_MODULE_RE_) == -1) {
    throw new Error('Invalid module identifier');
  }
  if (!goog.isInGoogModuleLoader_()) {
    throw new Error(
        'Module ' + name + ' has been loaded incorrectly. Note, ' +
        'modules cannot be loaded as normal scripts. They require some kind of ' +
        'pre-processing step. You\'re likely trying to load a module via a ' +
        'script tag or as a part of a concatenated bundle without rewriting the ' +
        'module. For more info see: ' +
        'https://github.com/google/closure-library/wiki/goog.module:-an-ES6-module-like-alternative-to-goog.provide.');
  }
  if (goog.moduleLoaderState_.moduleName) {
    throw new Error('goog.module may only be called once per module.');
  }

  // Store the module name for the loader.
  goog.moduleLoaderState_.moduleName = name;
  if (!COMPILED) {
    // Ensure that the same namespace isn't provided twice.
    // A goog.module/goog.provide maps a goog.require to a specific file
    if (goog.isProvided_(name)) {
      throw new Error('Namespace "' + name + '" already declared.');
    }
    delete goog.implicitNamespaces_[name];
  }
};


/**
 * @param {string} name The module identifier.
 * @return {?} The module exports for an already loaded module or null.
 *
 * Note: This is not an alternative to goog.require, it does not
 * indicate a hard dependency, instead it is used to indicate
 * an optional dependency or to access the exports of a module
 * that has already been loaded.
 * @suppress {missingProvide}
 */
goog.module.get = function(name) {
  return goog.module.getInternal_(name);
};


/**
 * @param {string} name The module identifier.
 * @return {?} The module exports for an already loaded module or null.
 * @private
 */
goog.module.getInternal_ = function(name) {
  if (!COMPILED) {
    if (name in goog.loadedModules_) {
      return goog.loadedModules_[name].exports;
    } else if (!goog.implicitNamespaces_[name]) {
      var ns = goog.getObjectByName(name);
      return ns != null ? ns : null;
    }
  }
  return null;
};


/**
 * Types of modules the debug loader can load.
 * @enum {string}
 */
goog.ModuleType = {
  ES6: 'es6',
  GOOG: 'goog'
};


/**
 * @private {?{
 *   moduleName: (string|undefined),
 *   declareLegacyNamespace:boolean,
 *   type: ?goog.ModuleType
 * }}
 */
goog.moduleLoaderState_ = null;


/**
 * @private
 * @return {boolean} Whether a goog.module or an es6 module is currently being
 *     initialized.
 */
goog.isInModuleLoader_ = function() {
  return goog.isInGoogModuleLoader_() || goog.isInEs6ModuleLoader_();
};


/**
 * @private
 * @return {boolean} Whether a goog.module is currently being initialized.
 */
goog.isInGoogModuleLoader_ = function() {
  return !!goog.moduleLoaderState_ &&
      goog.moduleLoaderState_.type == goog.ModuleType.GOOG;
};


/**
 * @private
 * @return {boolean} Whether an es6 module is currently being initialized.
 */
goog.isInEs6ModuleLoader_ = function() {
  var inLoader = !!goog.moduleLoaderState_ &&
      goog.moduleLoaderState_.type == goog.ModuleType.ES6;

  if (inLoader) {
    return true;
  }

  var jscomp = goog.global['$jscomp'];

  if (jscomp) {
    // jscomp may not have getCurrentModulePath if this is a compiled bundle
    // that has some of the runtime, but not all of it. This can happen if
    // optimizations are turned on so the unused runtime is removed but renaming
    // and Closure pass are off (so $jscomp is still named $jscomp and the
    // goog.provide/require calls still exist).
    if (typeof jscomp.getCurrentModulePath != 'function') {
      return false;
    }

    // Bundled ES6 module.
    return !!jscomp.getCurrentModulePath();
  }

  return false;
};


/**
 * Provide the module's exports as a globally accessible object under the
 * module's declared name.  This is intended to ease migration to goog.module
 * for files that have existing usages.
 * @suppress {missingProvide}
 */
goog.module.declareLegacyNamespace = function() {
  if (!COMPILED && !goog.isInGoogModuleLoader_()) {
    throw new Error(
        'goog.module.declareLegacyNamespace must be called from ' +
        'within a goog.module');
  }
  if (!COMPILED && !goog.moduleLoaderState_.moduleName) {
    throw new Error(
        'goog.module must be called prior to ' +
        'goog.module.declareLegacyNamespace.');
  }
  goog.moduleLoaderState_.declareLegacyNamespace = true;
};


/**
 * Associates an ES6 module with a Closure module ID so that is available via
 * goog.require. The associated ID  acts like a goog.module ID - it does not
 * create any global names, it is merely available via goog.require /
 * goog.module.get / goog.forwardDeclare / goog.requireType. goog.require and
 * goog.module.get will return the entire module as if it was import *'d. This
 * allows Closure files to reference ES6 modules for the sake of migration.
 *
 * @param {string} namespace
 * @suppress {missingProvide}
 */
goog.declareModuleId = function(namespace) {
  if (!COMPILED) {
    if (!goog.isInEs6ModuleLoader_()) {
      throw new Error(
          'goog.declareModuleId may only be called from ' +
          'within an ES6 module');
    }
    if (goog.moduleLoaderState_ && goog.moduleLoaderState_.moduleName) {
      throw new Error(
          'goog.declareModuleId may only be called once per module.');
    }
    if (namespace in goog.loadedModules_) {
      throw new Error(
          'Module with namespace "' + namespace + '" already exists.');
    }
  }
  if (goog.moduleLoaderState_) {
    // Not bundled - debug loading.
    goog.moduleLoaderState_.moduleName = namespace;
  } else {
    // Bundled - not debug loading, no module loader state.
    var jscomp = goog.global['$jscomp'];
    if (!jscomp || typeof jscomp.getCurrentModulePath != 'function') {
      throw new Error(
          'Module with namespace "' + namespace +
          '" has been loaded incorrectly.');
    }
    var exports = jscomp.require(jscomp.getCurrentModulePath());
    goog.loadedModules_[namespace] = {
      exports: exports,
      type: goog.ModuleType.ES6,
      moduleId: namespace
    };
  }
};


/**
 * Marks that the current file should only be used for testing, and never for
 * live code in production.
 *
 * In the case of unit tests, the message may optionally be an exact namespace
 * for the test (e.g. 'goog.stringTest'). The linter will then ignore the extra
 * provide (if not explicitly defined in the code).
 *
 * @param {string=} opt_message Optional message to add to the error that's
 *     raised when used in production code.
 */
goog.setTestOnly = function(opt_message) {
  if (goog.DISALLOW_TEST_ONLY_CODE) {
    opt_message = opt_message || '';
    throw new Error(
        'Importing test-only code into non-debug environment' +
        (opt_message ? ': ' + opt_message : '.'));
  }
};


/**
 * Forward declares a symbol. This is an indication to the compiler that the
 * symbol may be used in the source yet is not required and may not be provided
 * in compilation.
 *
 * The most common usage of forward declaration is code that takes a type as a
 * function parameter but does not need to require it. By forward declaring
 * instead of requiring, no hard dependency is made, and (if not required
 * elsewhere) the namespace may never be required and thus, not be pulled
 * into the JavaScript binary. If it is required elsewhere, it will be type
 * checked as normal.
 *
 * Before using goog.forwardDeclare, please read the documentation at
 * https://github.com/google/closure-compiler/wiki/Bad-Type-Annotation to
 * understand the options and tradeoffs when working with forward declarations.
 *
 * @param {string} name The namespace to forward declare in the form of
 *     "goog.package.part".
 * @deprecated See go/noforwarddeclaration, Use `goog.requireType` instead.
 */
goog.forwardDeclare = function(name) {};


/**
 * Forward declare type information. Used to assign types to goog.global
 * referenced object that would otherwise result in unknown type references
 * and thus block property disambiguation.
 */
goog.forwardDeclare('Document');
goog.forwardDeclare('HTMLScriptElement');
goog.forwardDeclare('XMLHttpRequest');


if (!COMPILED) {
  /**
   * Check if the given name has been goog.provided. This will return false for
   * names that are available only as implicit namespaces.
   * @param {string} name name of the object to look for.
   * @return {boolean} Whether the name has been provided.
   * @private
   */
  goog.isProvided_ = function(name) {
    return (name in goog.loadedModules_) ||
        (!goog.implicitNamespaces_[name] && goog.getObjectByName(name) != null);
  };

  /**
   * Namespaces implicitly defined by goog.provide. For example,
   * goog.provide('goog.events.Event') implicitly declares that 'goog' and
   * 'goog.events' must be namespaces.
   *
   * @type {!Object<string, (boolean|undefined)>}
   * @private
   */
  goog.implicitNamespaces_ = {'goog.module': true};

  // NOTE: We add goog.module as an implicit namespace as goog.module is defined
  // here and because the existing module package has not been moved yet out of
  // the goog.module namespace. This satisifies both the debug loader and
  // ahead-of-time dependency management.
}


/**
 * Returns an object based on its fully qualified external name.  The object
 * is not found if null or undefined.  If you are using a compilation pass that
 * renames property names beware that using this function will not find renamed
 * properties.
 *
 * @param {string} name The fully qualified name.
 * @param {Object=} opt_obj The object within which to look; default is
 *     |goog.global|.
 * @return {?} The value (object or primitive) or, if not found, null.
 */
goog.getObjectByName = function(name, opt_obj) {
  var parts = name.split('.');
  var cur = opt_obj || goog.global;
  for (var i = 0; i < parts.length; i++) {
    cur = cur[parts[i]];
    if (cur == null) {
      return null;
    }
  }
  return cur;
};


/**
 * Adds a dependency from a file to the files it requires.
 * @param {string} relPath The path to the js file.
 * @param {!Array<string>} provides An array of strings with
 *     the names of the objects this file provides.
 * @param {!Array<string>} requires An array of strings with
 *     the names of the objects this file requires.
 * @param {boolean|!Object<string>=} opt_loadFlags Parameters indicating
 *     how the file must be loaded.  The boolean 'true' is equivalent
 *     to {'module': 'goog'} for backwards-compatibility.  Valid properties
 *     and values include {'module': 'goog'} and {'lang': 'es6'}.
 */
goog.addDependency = function(relPath, provides, requires, opt_loadFlags) {
  if (!COMPILED && goog.DEPENDENCIES_ENABLED) {
    goog.debugLoader_.addDependency(relPath, provides, requires, opt_loadFlags);
  }
};


// MOE:begin_strip
/**
 * Whether goog.require should throw an exception if it fails.
 * @type {boolean}
 */
goog.useStrictRequires = false;


// MOE:end_strip


// NOTE(nnaze): The debug DOM loader was included in base.js as an original way
// to do "debug-mode" development.  The dependency system can sometimes be
// confusing, as can the debug DOM loader's asynchronous nature.
//
// With the DOM loader, a call to goog.require() is not blocking -- the script
// will not load until some point after the current script.  If a namespace is
// needed at runtime, it needs to be defined in a previous script, or loaded via
// require() with its registered dependencies.
//
// User-defined namespaces may need their own deps file. For a reference on
// creating a deps file, see:
// MOE:begin_strip
// Internally: http://go/deps-files and http://go/be#js_deps
// MOE:end_strip
// Externally: https://developers.google.com/closure/library/docs/depswriter
//
// Because of legacy clients, the DOM loader can't be easily removed from
// base.js.  Work was done to make it disableable or replaceable for
// different environments (DOM-less JavaScript interpreters like Rhino or V8,
// for example). See bootstrap/ for more information.


/**
 * @define {boolean} Whether to enable the debug loader.
 *
 * If enabled, a call to goog.require() will attempt to load the namespace by
 * appending a script tag to the DOM (if the namespace has been registered).
 *
 * If disabled, goog.require() will simply assert that the namespace has been
 * provided (and depend on the fact that some outside tool correctly ordered
 * the script).
 */
goog.ENABLE_DEBUG_LOADER = goog.define('goog.ENABLE_DEBUG_LOADER', true);


/**
 * @param {string} msg
 * @private
 */
goog.logToConsole_ = function(msg) {
  if (goog.global.console) {
    goog.global.console['error'](msg);
  }
};


/**
 * Implements a system for the dynamic resolution of dependencies that works in
 * parallel with the BUILD system.
 *
 * Note that all calls to goog.require will be stripped by the compiler.
 *
 * @see goog.provide
 * @param {string} namespace Namespace (as was given in goog.provide,
 *     goog.module, or goog.declareModuleId) in the form
 *     "goog.package.part".
 * @return {?} If called within a goog.module or ES6 module file, the associated
 *     namespace or module otherwise null.
 */
goog.require = function(namespace) {
  if (!COMPILED) {
    // Might need to lazy load on old IE.
    if (goog.ENABLE_DEBUG_LOADER) {
      goog.debugLoader_.requested(namespace);
    }

    // If the object already exists we do not need to do anything.
    if (goog.isProvided_(namespace)) {
      if (goog.isInModuleLoader_()) {
        return goog.module.getInternal_(namespace);
      }
    } else if (goog.ENABLE_DEBUG_LOADER) {
      var moduleLoaderState = goog.moduleLoaderState_;
      goog.moduleLoaderState_ = null;
      try {
        goog.debugLoader_.load_(namespace);
      } finally {
        goog.moduleLoaderState_ = moduleLoaderState;
      }
    }

    return null;
  }
};


/**
 * Requires a symbol for its type information. This is an indication to the
 * compiler that the symbol may appear in type annotations, yet it is not
 * referenced at runtime.
 *
 * When called within a goog.module or ES6 module file, the return value may be
 * assigned to or destructured into a variable, but it may not be otherwise used
 * in code outside of a type annotation.
 *
 * Note that all calls to goog.requireType will be stripped by the compiler.
 *
 * @param {string} namespace Namespace (as was given in goog.provide,
 *     goog.module, or goog.declareModuleId) in the form
 *     "goog.package.part".
 * @return {?}
 */
goog.requireType = function(namespace) {
  // Return an empty object so that single-level destructuring of the return
  // value doesn't crash at runtime when using the debug loader. Multi-level
  // destructuring isn't supported.
  return {};
};


/**
 * Path for included scripts.
 * @type {string}
 */
goog.basePath = '';


/**
 * A hook for overriding the base path.
 * @type {string|undefined}
 */
goog.global.CLOSURE_BASE_PATH;


/**
 * Whether to attempt to load Closure's deps file. By default, when uncompiled,
 * deps files will attempt to be loaded.
 * @type {boolean|undefined}
 */
goog.global.CLOSURE_NO_DEPS;


/**
 * A function to import a single script. This is meant to be overridden when
 * Closure is being run in non-HTML contexts, such as web workers. It's defined
 * in the global scope so that it can be set before base.js is loaded, which
 * allows deps.js to be imported properly.
 *
 * The first parameter the script source, which is a relative URI. The second,
 * optional parameter is the script contents, in the event the script needed
 * transformation. It should return true if the script was imported, false
 * otherwise.
 * @type {(function(string, string=): boolean)|undefined}
 */
goog.global.CLOSURE_IMPORT_SCRIPT;


/**
 * Null function used for default values of callbacks, etc.
 * @return {void} Nothing.
 * @deprecated use '()=>{}' or 'function(){}' instead.
 */
goog.nullFunction = function() {};


/**
 * When defining a class Foo with an abstract method bar(), you can do:
 * Foo.prototype.bar = goog.abstractMethod
 *
 * Now if a subclass of Foo fails to override bar(), an error will be thrown
 * when bar() is invoked.
 *
 * @type {!Function}
 * @throws {Error} when invoked to indicate the method should be overridden.
 * @deprecated Use "@abstract" annotation instead of goog.abstractMethod in new
 *     code. See
 *     https://github.com/google/closure-compiler/wiki/@abstract-classes-and-methods
 */
goog.abstractMethod = function() {
  throw new Error('unimplemented abstract method');
};


/**
 * Adds a `getInstance` static method that always returns the same
 * instance object.
 * @param {!Function} ctor The constructor for the class to add the static
 *     method to.
 * @suppress {missingProperties} 'instance_' isn't a property on 'Function'
 *     but we don't have a better type to use here.
 */
goog.addSingletonGetter = function(ctor) {
  // instance_ is immediately set to prevent issues with sealed constructors
  // such as are encountered when a constructor is returned as the export object
  // of a goog.module in unoptimized code.
  // Delcare type to avoid conformance violations that ctor.instance_ is unknown
  /** @type {undefined|!Object} @suppress {underscore} */
  ctor.instance_ = undefined;
  ctor.getInstance = function() {
    if (ctor.instance_) {
      return ctor.instance_;
    }
    if (goog.DEBUG) {
      // NOTE: JSCompiler can't optimize away Array#push.
      goog.instantiatedSingletons_[goog.instantiatedSingletons_.length] = ctor;
    }
    // Cast to avoid conformance violations that ctor.instance_ is unknown
    return /** @type {!Object|undefined} */ (ctor.instance_) = new ctor;
  };
};


/**
 * All singleton classes that have been instantiated, for testing. Don't read
 * it directly, use the `goog.testing.singleton` module. The compiler
 * removes this variable if unused.
 * @type {!Array<!Function>}
 * @private
 */
goog.instantiatedSingletons_ = [];


/**
 * @define {boolean} Whether to load goog.modules using `eval` when using
 * the debug loader.  This provides a better debugging experience as the
 * source is unmodified and can be edited using Chrome Workspaces or similar.
 * However in some environments the use of `eval` is banned
 * so we provide an alternative.
 */
goog.LOAD_MODULE_USING_EVAL = goog.define('goog.LOAD_MODULE_USING_EVAL', true);


/**
 * @define {boolean} Whether the exports of goog.modules should be sealed when
 * possible.
 */
goog.SEAL_MODULE_EXPORTS = goog.define('goog.SEAL_MODULE_EXPORTS', goog.DEBUG);


/**
 * The registry of initialized modules:
 * The module identifier or path to module exports map.
 * @private @const {!Object<string, {exports:?,type:string,moduleId:string}>}
 */
goog.loadedModules_ = {};


/**
 * True if the debug loader enabled and used.
 * @const {boolean}
 */
goog.DEPENDENCIES_ENABLED = !COMPILED && goog.ENABLE_DEBUG_LOADER;


/**
 * @define {string} How to decide whether to transpile.  Valid values
 * are 'always', 'never', and 'detect'.  The default ('detect') is to
 * use feature detection to determine which language levels need
 * transpilation.
 */
// NOTE(sdh): we could expand this to accept a language level to bypass
// detection: e.g. goog.TRANSPILE == 'es5' would transpile ES6 files but
// would leave ES3 and ES5 files alone.
goog.TRANSPILE = goog.define('goog.TRANSPILE', 'detect');

/**
 * @define {boolean} If true assume that ES modules have already been
 * transpiled by the jscompiler (in the same way that transpile.js would
 * transpile them - to jscomp modules). Useful only for servers that wish to use
 * the debug loader and transpile server side. Thus this is only respected if
 * goog.TRANSPILE is "never".
 */
goog.ASSUME_ES_MODULES_TRANSPILED =
    goog.define('goog.ASSUME_ES_MODULES_TRANSPILED', false);


/**
 * @define {string} If a file needs to be transpiled what the output language
 * should be. By default this is the highest language level this file detects
 * the current environment supports. Generally this flag should not be set, but
 * it could be useful to override. Example: If the current environment supports
 * ES6 then by default ES7+ files will be transpiled to ES6, unless this is
 * overridden.
 *
 * Valid values include: es3, es5, es6, es7, and es8. Anything not recognized
 * is treated as es3.
 *
 * Note that setting this value does not force transpilation. Just if
 * transpilation occurs this will be the output. So this is most useful when
 * goog.TRANSPILE is set to 'always' and then forcing the language level to be
 * something lower than what the environment detects.
 */
goog.TRANSPILE_TO_LANGUAGE = goog.define('goog.TRANSPILE_TO_LANGUAGE', '');


/**
 * @define {string} Path to the transpiler.  Executing the script at this
 * path (relative to base.js) should define a function $jscomp.transpile.
 */
goog.TRANSPILER = goog.define('goog.TRANSPILER', 'transpile.js');


/**
 * @define {string} Trusted Types policy name. If non-empty then Closure will
 * use Trusted Types.
 */
goog.TRUSTED_TYPES_POLICY_NAME =
    goog.define('goog.TRUSTED_TYPES_POLICY_NAME', 'goog');


/**
 * @package {?boolean}
 * Visible for testing.
 */
goog.hasBadLetScoping = null;


/**
 * @param {function(?):?|string} moduleDef The module definition.
 */
goog.loadModule = function(moduleDef) {
  // NOTE: we allow function definitions to be either in the from
  // of a string to eval (which keeps the original source intact) or
  // in a eval forbidden environment (CSP) we allow a function definition
  // which in its body must call `goog.module`, and return the exports
  // of the module.
  var previousState = goog.moduleLoaderState_;
  try {
    goog.moduleLoaderState_ = {
      moduleName: '',
      declareLegacyNamespace: false,
      type: goog.ModuleType.GOOG
    };
    var origExports = {};
    var exports = origExports;
    if (typeof moduleDef === 'function') {
      exports = moduleDef.call(undefined, exports);
    } else if (typeof moduleDef === 'string') {
      exports = goog.loadModuleFromSource_.call(undefined, exports, moduleDef);
    } else {
      throw new Error('Invalid module definition');
    }

    var moduleName = goog.moduleLoaderState_.moduleName;
    if (typeof moduleName === 'string' && moduleName) {
      // Don't seal legacy namespaces as they may be used as a parent of
      // another namespace
      if (goog.moduleLoaderState_.declareLegacyNamespace) {
        // Whether exports was overwritten via default export assignment.
        // This is important for legacy namespaces as it dictates whether
        // previously a previously loaded implicit namespace should be clobbered
        // or not.
        var isDefaultExport = origExports !== exports;
        goog.constructNamespace_(moduleName, exports, isDefaultExport);
      } else if (
          goog.SEAL_MODULE_EXPORTS && Object.seal &&
          typeof exports == 'object' && exports != null) {
        Object.seal(exports);
      }

      var data = {
        exports: exports,
        type: goog.ModuleType.GOOG,
        moduleId: goog.moduleLoaderState_.moduleName
      };
      goog.loadedModules_[moduleName] = data;
    } else {
      throw new Error('Invalid module name \"' + moduleName + '\"');
    }
  } finally {
    goog.moduleLoaderState_ = previousState;
  }
};


/**
 * @private @const
 */
goog.loadModuleFromSource_ =
    /** @type {function(!Object, string):?} */ (function(exports) {
      // NOTE: we avoid declaring parameters or local variables here to avoid
      // masking globals or leaking values into the module definition.
      'use strict';
      eval(goog.CLOSURE_EVAL_PREFILTER_.createScript(arguments[1]));
      return exports;
    });


/**
 * Normalize a file path by removing redundant ".." and extraneous "." file
 * path components.
 * @param {string} path
 * @return {string}
 * @private
 */
goog.normalizePath_ = function(path) {
  var components = path.split('/');
  var i = 0;
  while (i < components.length) {
    if (components[i] == '.') {
      components.splice(i, 1);
    } else if (
        i && components[i] == '..' && components[i - 1] &&
        components[i - 1] != '..') {
      components.splice(--i, 2);
    } else {
      i++;
    }
  }
  return components.join('/');
};


/**
 * Provides a hook for loading a file when using Closure's goog.require() API
 * with goog.modules.  In particular this hook is provided to support Node.js.
 *
 * @type {(function(string):string)|undefined}
 */
goog.global.CLOSURE_LOAD_FILE_SYNC;


/**
 * Loads file by synchronous XHR. Should not be used in production environments.
 * @param {string} src Source URL.
 * @return {?string} File contents, or null if load failed.
 * @private
 */
goog.loadFileSync_ = function(src) {
  if (goog.global.CLOSURE_LOAD_FILE_SYNC) {
    return goog.global.CLOSURE_LOAD_FILE_SYNC(src);
  } else {
    try {
      /** @type {XMLHttpRequest} */
      var xhr = new goog.global['XMLHttpRequest']();
      xhr.open('get', src, false);
      xhr.send();
      // NOTE: Successful http: requests have a status of 200, but successful
      // file: requests may have a status of zero.  Any other status, or a
      // thrown exception (particularly in case of file: requests) indicates
      // some sort of error, which we treat as a missing or unavailable file.
      return xhr.status == 0 || xhr.status == 200 ? xhr.responseText : null;
    } catch (err) {
      // No need to rethrow or log, since errors should show up on their own.
      return null;
    }
  }
};


/**
 * Lazily retrieves the transpiler and applies it to the source.
 * @param {string} code JS code.
 * @param {string} path Path to the code.
 * @param {string} target Language level output.
 * @return {string} The transpiled code.
 * @private
 */
goog.transpile_ = function(code, path, target) {
  var jscomp = goog.global['$jscomp'];
  if (!jscomp) {
    goog.global['$jscomp'] = jscomp = {};
  }
  var transpile = jscomp.transpile;
  if (!transpile) {
    var transpilerPath = goog.basePath + goog.TRANSPILER;
    var transpilerCode = goog.loadFileSync_(transpilerPath);
    if (transpilerCode) {
      // This must be executed synchronously, since by the time we know we
      // need it, we're about to load and write the ES6 code synchronously,
      // so a normal script-tag load will be too slow. Wrapped in a function
      // so that code is eval'd in the global scope.
      (function() {
        (0, eval)(transpilerCode + '\n//# sourceURL=' + transpilerPath);
      }).call(goog.global);
      // Even though the transpiler is optional, if $gwtExport is found, it's
      // a sign the transpiler was loaded and the $jscomp.transpile *should*
      // be there.
      if (goog.global['$gwtExport'] && goog.global['$gwtExport']['$jscomp'] &&
          !goog.global['$gwtExport']['$jscomp']['transpile']) {
        throw new Error(
            'The transpiler did not properly export the "transpile" ' +
            'method. $gwtExport: ' + JSON.stringify(goog.global['$gwtExport']));
      }
      // transpile.js only exports a single $jscomp function, transpile. We
      // grab just that and add it to the existing definition of $jscomp which
      // contains the polyfills.
      goog.global['$jscomp'].transpile =
          goog.global['$gwtExport']['$jscomp']['transpile'];
      jscomp = goog.global['$jscomp'];
      transpile = jscomp.transpile;
    }
  }
  if (!transpile) {
    // The transpiler is an optional component.  If it's not available then
    // replace it with a pass-through function that simply logs.
    var suffix = ' requires transpilation but no transpiler was found.';
    // MOE:begin_strip
    suffix +=  // Provide a more appropriate message internally.
        ' Please add "//javascript/closure:transpiler" as a data ' +
        'dependency to ensure it is included.';
    // MOE:end_strip
    transpile = jscomp.transpile = function(code, path) {
      // TODO(sdh): figure out some way to get this error to show up
      // in test results, noting that the failure may occur in many
      // different ways, including in loadModule() before the test
      // runner even comes up.
      goog.logToConsole_(path + suffix);
      return code;
    };
  }
  // Note: any transpilation errors/warnings will be logged to the console.
  return transpile(code, path, target);
};

//==============================================================================
// Language Enhancements
//==============================================================================


/**
 * This is a "fixed" version of the typeof operator.  It differs from the typeof
 * operator in such a way that null returns 'null' and arrays return 'array'.
 * @param {?} value The value to get the type of.
 * @return {string} The name of the type.
 */
goog.typeOf = function(value) {
  var s = typeof value;

  if (s != 'object') {
    return s;
  }

  if (!value) {
    return 'null';
  }

  if (Array.isArray(value)) {
    return 'array';
  }
  return s;
};


/**
 * Returns true if the object looks like an array. To qualify as array like
 * the value needs to be either a NodeList or an object with a Number length
 * property. Note that for this function neither strings nor functions are
 * considered "array-like".
 *
 * @param {?} val Variable to test.
 * @return {boolean} Whether variable is an array.
 */
goog.isArrayLike = function(val) {
  var type = goog.typeOf(val);
  // We do not use goog.isObject here in order to exclude function values.
  return type == 'array' || type == 'object' && typeof val.length == 'number';
};


/**
 * Returns true if the object looks like a Date. To qualify as Date-like the
 * value needs to be an object and have a getFullYear() function.
 * @param {?} val Variable to test.
 * @return {boolean} Whether variable is a like a Date.
 */
goog.isDateLike = function(val) {
  return goog.isObject(val) && typeof val.getFullYear == 'function';
};


/**
 * Returns true if the specified value is an object.  This includes arrays and
 * functions.
 * @param {?} val Variable to test.
 * @return {boolean} Whether variable is an object.
 */
goog.isObject = function(val) {
  var type = typeof val;
  return type == 'object' && val != null || type == 'function';
  // return Object(val) === val also works, but is slower, especially if val is
  // not an object.
};


/**
 * Gets a unique ID for an object. This mutates the object so that further calls
 * with the same object as a parameter returns the same value. The unique ID is
 * guaranteed to be unique across the current session amongst objects that are
 * passed into `getUid`. There is no guarantee that the ID is unique or
 * consistent across sessions. It is unsafe to generate unique ID for function
 * prototypes.
 *
 * @param {Object} obj The object to get the unique ID for.
 * @return {number} The unique ID for the object.
 */
goog.getUid = function(obj) {
  // TODO(arv): Make the type stricter, do not accept null.
  return Object.prototype.hasOwnProperty.call(obj, goog.UID_PROPERTY_) &&
      obj[goog.UID_PROPERTY_] ||
      (obj[goog.UID_PROPERTY_] = ++goog.uidCounter_);
};


/**
 * Whether the given object is already assigned a unique ID.
 *
 * This does not modify the object.
 *
 * @param {!Object} obj The object to check.
 * @return {boolean} Whether there is an assigned unique id for the object.
 */
goog.hasUid = function(obj) {
  return !!obj[goog.UID_PROPERTY_];
};


/**
 * Removes the unique ID from an object. This is useful if the object was
 * previously mutated using `goog.getUid` in which case the mutation is
 * undone.
 * @param {Object} obj The object to remove the unique ID field from.
 */
goog.removeUid = function(obj) {
  // TODO(arv): Make the type stricter, do not accept null.

  // In IE, DOM nodes are not instances of Object and throw an exception if we
  // try to delete.  Instead we try to use removeAttribute.
  if (obj !== null && 'removeAttribute' in obj) {
    obj.removeAttribute(goog.UID_PROPERTY_);
  }

  try {
    delete obj[goog.UID_PROPERTY_];
  } catch (ex) {
  }
};


/**
 * Name for unique ID property. Initialized in a way to help avoid collisions
 * with other closure JavaScript on the same page.
 * @type {string}
 * @private
 */
goog.UID_PROPERTY_ = 'closure_uid_' + ((Math.random() * 1e9) >>> 0);


/**
 * Counter for UID.
 * @type {number}
 * @private
 */
goog.uidCounter_ = 0;


/**
 * Clones a value. The input may be an Object, Array, or basic type. Objects and
 * arrays will be cloned recursively.
 *
 * WARNINGS:
 * <code>goog.cloneObject</code> does not detect reference loops. Objects that
 * refer to themselves will cause infinite recursion.
 *
 * <code>goog.cloneObject</code> is unaware of unique identifiers, and copies
 * UIDs created by <code>getUid</code> into cloned results.
 *
 * @param {*} obj The value to clone.
 * @return {*} A clone of the input value.
 * @deprecated goog.cloneObject is unsafe. Prefer the goog.object methods.
 */
goog.cloneObject = function(obj) {
  var type = goog.typeOf(obj);
  if (type == 'object' || type == 'array') {
    if (typeof obj.clone === 'function') {
      return obj.clone();
    }
    if (typeof Map !== 'undefined' && obj instanceof Map) {
      return new Map(obj);
    } else if (typeof Set !== 'undefined' && obj instanceof Set) {
      return new Set(obj);
    }
    var clone = type == 'array' ? [] : {};
    for (var key in obj) {
      clone[key] = goog.cloneObject(obj[key]);
    }
    return clone;
  }

  return obj;
};


/**
 * A native implementation of goog.bind.
 * @param {?function(this:T, ...)} fn A function to partially apply.
 * @param {T} selfObj Specifies the object which this should point to when the
 *     function is run.
 * @param {...*} var_args Additional arguments that are partially applied to the
 *     function.
 * @return {!Function} A partially-applied form of the function goog.bind() was
 *     invoked as a method of.
 * @template T
 * @private
 */
goog.bindNative_ = function(fn, selfObj, var_args) {
  return /** @type {!Function} */ (fn.call.apply(fn.bind, arguments));
};


/**
 * A pure-JS implementation of goog.bind.
 * @param {?function(this:T, ...)} fn A function to partially apply.
 * @param {T} selfObj Specifies the object which this should point to when the
 *     function is run.
 * @param {...*} var_args Additional arguments that are partially applied to the
 *     function.
 * @return {!Function} A partially-applied form of the function goog.bind() was
 *     invoked as a method of.
 * @template T
 * @private
 */
goog.bindJs_ = function(fn, selfObj, var_args) {
  if (!fn) {
    throw new Error();
  }

  if (arguments.length > 2) {
    var boundArgs = Array.prototype.slice.call(arguments, 2);
    return function() {
      // Prepend the bound arguments to the current arguments.
      var newArgs = Array.prototype.slice.call(arguments);
      Array.prototype.unshift.apply(newArgs, boundArgs);
      return fn.apply(selfObj, newArgs);
    };

  } else {
    return function() {
      return fn.apply(selfObj, arguments);
    };
  }
};


/**
 * Partially applies this function to a particular 'this object' and zero or
 * more arguments. The result is a new function with some arguments of the first
 * function pre-filled and the value of this 'pre-specified'.
 *
 * Remaining arguments specified at call-time are appended to the pre-specified
 * ones.
 *
 * Also see: {@link #partial}.
 *
 * Usage:
 * <pre>var barMethBound = goog.bind(myFunction, myObj, 'arg1', 'arg2');
 * barMethBound('arg3', 'arg4');</pre>
 *
 * @param {?function(this:T, ...)} fn A function to partially apply.
 * @param {T} selfObj Specifies the object which this should point to when the
 *     function is run.
 * @param {...*} var_args Additional arguments that are partially applied to the
 *     function.
 * @return {!Function} A partially-applied form of the function goog.bind() was
 *     invoked as a method of.
 * @template T
 * @suppress {deprecated} See above.
 * @deprecated use `=> {}` or Function.prototype.bind instead.
 */
goog.bind = function(fn, selfObj, var_args) {
  // TODO(nicksantos): narrow the type signature.
  if (Function.prototype.bind &&
      // NOTE(nicksantos): Somebody pulled base.js into the default Chrome
      // extension environment. This means that for Chrome extensions, they get
      // the implementation of Function.prototype.bind that calls goog.bind
      // instead of the native one. Even worse, we don't want to introduce a
      // circular dependency between goog.bind and Function.prototype.bind, so
      // we have to hack this to make sure it works correctly.
      Function.prototype.bind.toString().indexOf('native code') != -1) {
    goog.bind = goog.bindNative_;
  } else {
    goog.bind = goog.bindJs_;
  }
  return goog.bind.apply(null, arguments);
};


/**
 * Like goog.bind(), except that a 'this object' is not required. Useful when
 * the target function is already bound.
 *
 * Usage:
 * var g = goog.partial(f, arg1, arg2);
 * g(arg3, arg4);
 *
 * @param {Function} fn A function to partially apply.
 * @param {...*} var_args Additional arguments that are partially applied to fn.
 * @return {!Function} A partially-applied form of the function goog.partial()
 *     was invoked as a method of.
 */
goog.partial = function(fn, var_args) {
  var args = Array.prototype.slice.call(arguments, 1);
  return function() {
    // Clone the array (with slice()) and append additional arguments
    // to the existing arguments.
    var newArgs = args.slice();
    newArgs.push.apply(newArgs, arguments);
    return fn.apply(/** @type {?} */ (this), newArgs);
  };
};


/**
 * Copies all the members of a source object to a target object. This method
 * does not work on all browsers for all objects that contain keys such as
 * toString or hasOwnProperty. Use goog.object.extend for this purpose.
 *
 * NOTE: Some have advocated for the use of goog.mixin to setup classes
 * with multiple inheritence (traits, mixins, etc).  However, as it simply
 * uses "for in", this is not compatible with ES6 classes whose methods are
 * non-enumerable.  Changing this, would break cases where non-enumerable
 * properties are not expected.
 *
 * @param {Object} target Target.
 * @param {Object} source Source.
 * @deprecated Prefer Object.assign
 */
goog.mixin = function(target, source) {
  for (var x in source) {
    target[x] = source[x];
  }

  // For IE7 or lower, the for-in-loop does not contain any properties that are
  // not enumerable on the prototype object (for example, isPrototypeOf from
  // Object.prototype) but also it will not include 'replace' on objects that
  // extend String and change 'replace' (not that it is common for anyone to
  // extend anything except Object).
};


/**
 * @return {number} An integer value representing the number of milliseconds
 *     between midnight, January 1, 1970 and the current time.
 * @deprecated Use Date.now
 */
goog.now = function() {
  return Date.now();
};


/**
 * Evals JavaScript in the global scope.
 *
 * Throws an exception if neither execScript or eval is defined.
 * @param {string|!TrustedScript} script JavaScript string.
 */
goog.globalEval = function(script) {
  (0, eval)(script);
};


/**
 * Optional map of CSS class names to obfuscated names used with
 * goog.getCssName().
 * @private {!Object<string, string>|undefined}
 * @see goog.setCssNameMapping
 */
goog.cssNameMapping_;


/**
 * Optional obfuscation style for CSS class names. Should be set to either
 * 'BY_WHOLE' or 'BY_PART' if defined.
 * @type {string|undefined}
 * @private
 * @see goog.setCssNameMapping
 */
goog.cssNameMappingStyle_;



/**
 * A hook for modifying the default behavior goog.getCssName. The function
 * if present, will receive the standard output of the goog.getCssName as
 * its input.
 *
 * @type {(function(string):string)|undefined}
 */
goog.global.CLOSURE_CSS_NAME_MAP_FN;


/**
 * Handles strings that are intended to be used as CSS class names.
 *
 * This function works in tandem with @see goog.setCssNameMapping.
 *
 * Without any mapping set, the arguments are simple joined with a hyphen and
 * passed through unaltered.
 *
 * When there is a mapping, there are two possible styles in which these
 * mappings are used. In the BY_PART style, each part (i.e. in between hyphens)
 * of the passed in css name is rewritten according to the map. In the BY_WHOLE
 * style, the full css name is looked up in the map directly. If a rewrite is
 * not specified by the map, the compiler will output a warning.
 *
 * When the mapping is passed to the compiler, it will replace calls to
 * goog.getCssName with the strings from the mapping, e.g.
 *     var x = goog.getCssName('foo');
 *     var y = goog.getCssName(this.baseClass, 'active');
 *  becomes:
 *     var x = 'foo';
 *     var y = this.baseClass + '-active';
 *
 * If one argument is passed it will be processed, if two are passed only the
 * modifier will be processed, as it is assumed the first argument was generated
 * as a result of calling goog.getCssName.
 *
 * @param {string} className The class name.
 * @param {string=} opt_modifier A modifier to be appended to the class name.
 * @return {string} The class name or the concatenation of the class name and
 *     the modifier.
 */
goog.getCssName = function(className, opt_modifier) {
  // String() is used for compatibility with compiled soy where the passed
  // className can be non-string objects.
  if (String(className).charAt(0) == '.') {
    throw new Error(
        'className passed in goog.getCssName must not start with ".".' +
        ' You passed: ' + className);
  }

  var getMapping = function(cssName) {
    return goog.cssNameMapping_[cssName] || cssName;
  };

  var renameByParts = function(cssName) {
    // Remap all the parts individually.
    var parts = cssName.split('-');
    var mapped = [];
    for (var i = 0; i < parts.length; i++) {
      mapped.push(getMapping(parts[i]));
    }
    return mapped.join('-');
  };

  var rename;
  if (goog.cssNameMapping_) {
    rename =
        goog.cssNameMappingStyle_ == 'BY_WHOLE' ? getMapping : renameByParts;
  } else {
    rename = function(a) {
      return a;
    };
  }

  var result =
      opt_modifier ? className + '-' + rename(opt_modifier) : rename(className);

  // The special CLOSURE_CSS_NAME_MAP_FN allows users to specify further
  // processing of the class name.
  if (goog.global.CLOSURE_CSS_NAME_MAP_FN) {
    return goog.global.CLOSURE_CSS_NAME_MAP_FN(result);
  }

  return result;
};


/**
 * Sets the map to check when returning a value from goog.getCssName(). Example:
 * <pre>
 * goog.setCssNameMapping({
 *   "goog": "a",
 *   "disabled": "b",
 * });
 *
 * var x = goog.getCssName('goog');
 * // The following evaluates to: "a a-b".
 * goog.getCssName('goog') + ' ' + goog.getCssName(x, 'disabled')
 * </pre>
 * When declared as a map of string literals to string literals, the JSCompiler
 * will replace all calls to goog.getCssName() using the supplied map if the
 * --process_closure_primitives flag is set.
 *
 * @param {!Object} mapping A map of strings to strings where keys are possible
 *     arguments to goog.getCssName() and values are the corresponding values
 *     that should be returned.
 * @param {string=} opt_style The style of css name mapping. There are two valid
 *     options: 'BY_PART', and 'BY_WHOLE'.
 * @see goog.getCssName for a description.
 */
goog.setCssNameMapping = function(mapping, opt_style) {
  goog.cssNameMapping_ = mapping;
  goog.cssNameMappingStyle_ = opt_style;
};


/**
 * To use CSS renaming in compiled mode, one of the input files should have a
 * call to goog.setCssNameMapping() with an object literal that the JSCompiler
 * can extract and use to replace all calls to goog.getCssName(). In uncompiled
 * mode, JavaScript code should be loaded before this base.js file that declares
 * a global variable, CLOSURE_CSS_NAME_MAPPING, which is used below. This is
 * to ensure that the mapping is loaded before any calls to goog.getCssName()
 * are made in uncompiled mode.
 *
 * A hook for overriding the CSS name mapping.
 * @type {!Object<string, string>|undefined}
 */
goog.global.CLOSURE_CSS_NAME_MAPPING;


if (!COMPILED && goog.global.CLOSURE_CSS_NAME_MAPPING) {
  // This does not call goog.setCssNameMapping() because the JSCompiler
  // requires that goog.setCssNameMapping() be called with an object literal.
  goog.cssNameMapping_ = goog.global.CLOSURE_CSS_NAME_MAPPING;
}


/**
 * Gets a localized message.
 *
 * This function is a compiler primitive. If you give the compiler a localized
 * message bundle, it will replace the string at compile-time with a localized
 * version, and expand goog.getMsg call to a concatenated string.
 *
 * Messages must be initialized in the form:
 * <code>
 * var MSG_NAME = goog.getMsg('Hello {$placeholder}', {'placeholder': 'world'});
 * </code>
 *
 * This function produces a string which should be treated as plain text. Use
 * {@link goog.html.SafeHtmlFormatter} in conjunction with goog.getMsg to
 * produce SafeHtml.
 *
 * @param {string} str Translatable string, places holders in the form {$foo}.
 * @param {Object<string, string>=} opt_values Maps place holder name to value.
 * @param {{html: (boolean|undefined),
 *         unescapeHtmlEntities: (boolean|undefined)}=} opt_options Options:
 *     html: Escape '<' in str to '&lt;'. Used by Closure Templates where the
 *     generated code size and performance is critical which is why {@link
 *     goog.html.SafeHtmlFormatter} is not used. The value must be literal true
 *     or false.
 *     unescapeHtmlEntities: Unescape common html entities: &gt;, &lt;, &apos;,
 *     &quot; and &amp;. Used for messages not in HTML context, such as with
 *     `textContent` property.
 * @return {string} message with placeholders filled.
 */
goog.getMsg = function(str, opt_values, opt_options) {
  if (opt_options && opt_options.html) {
    // Note that '&' is not replaced because the translation can contain HTML
    // entities.
    str = str.replace(/</g, '&lt;');
  }
  if (opt_options && opt_options.unescapeHtmlEntities) {
    // Note that "&amp;" must be the last to avoid "creating" new entities.
    str = str.replace(/&lt;/g, '<')
              .replace(/&gt;/g, '>')
              .replace(/&apos;/g, '\'')
              .replace(/&quot;/g, '"')
              .replace(/&amp;/g, '&');
  }
  if (opt_values) {
    str = str.replace(/\{\$([^}]+)}/g, function(match, key) {
      return (opt_values != null && key in opt_values) ? opt_values[key] :
                                                         match;
    });
  }
  return str;
};


/**
 * Gets a localized message. If the message does not have a translation, gives a
 * fallback message.
 *
 * This is useful when introducing a new message that has not yet been
 * translated into all languages.
 *
 * This function is a compiler primitive. Must be used in the form:
 * <code>var x = goog.getMsgWithFallback(MSG_A, MSG_B);</code>
 * where MSG_A and MSG_B were initialized with goog.getMsg.
 *
 * @param {string} a The preferred message.
 * @param {string} b The fallback message.
 * @return {string} The best translated message.
 */
goog.getMsgWithFallback = function(a, b) {
  return a;
};


/**
 * Exposes an unobfuscated global namespace path for the given object.
 * Note that fields of the exported object *will* be obfuscated, unless they are
 * exported in turn via this function or goog.exportProperty.
 *
 * Also handy for making public items that are defined in anonymous closures.
 *
 * ex. goog.exportSymbol('public.path.Foo', Foo);
 *
 * ex. goog.exportSymbol('public.path.Foo.staticFunction', Foo.staticFunction);
 *     public.path.Foo.staticFunction();
 *
 * ex. goog.exportSymbol('public.path.Foo.prototype.myMethod',
 *                       Foo.prototype.myMethod);
 *     new public.path.Foo().myMethod();
 *
 * @param {string} publicPath Unobfuscated name to export.
 * @param {*} object Object the name should point to.
 * @param {?Object=} objectToExportTo The object to add the path to; default
 *     is goog.global.
 */
goog.exportSymbol = function(publicPath, object, objectToExportTo) {
  goog.exportPath_(
      publicPath, object, /* overwriteImplicit= */ true, objectToExportTo);
};


/**
 * Exports a property unobfuscated into the object's namespace.
 * ex. goog.exportProperty(Foo, 'staticFunction', Foo.staticFunction);
 * ex. goog.exportProperty(Foo.prototype, 'myMethod', Foo.prototype.myMethod);
 * @param {Object} object Object whose static property is being exported.
 * @param {string} publicName Unobfuscated name to export.
 * @param {*} symbol Object the name should point to.
 */
goog.exportProperty = function(object, publicName, symbol) {
  object[publicName] = symbol;
};


/**
 * Inherit the prototype methods from one constructor into another.
 *
 * Usage:
 * <pre>
 * function ParentClass(a, b) { }
 * ParentClass.prototype.foo = function(a) { };
 *
 * function ChildClass(a, b, c) {
 *   ChildClass.base(this, 'constructor', a, b);
 * }
 * goog.inherits(ChildClass, ParentClass);
 *
 * var child = new ChildClass('a', 'b', 'see');
 * child.foo(); // This works.
 * </pre>
 *
 * @param {!Function} childCtor Child class.
 * @param {!Function} parentCtor Parent class.
 * @suppress {strictMissingProperties} superClass_ and base is not defined on
 *    Function.
 * @deprecated Use ECMAScript class syntax instead.
 */
goog.inherits = function(childCtor, parentCtor) {
  /** @constructor */
  function tempCtor() {}
  tempCtor.prototype = parentCtor.prototype;
  childCtor.superClass_ = parentCtor.prototype;
  childCtor.prototype = new tempCtor();
  /** @override */
  childCtor.prototype.constructor = childCtor;

  /**
   * Calls superclass constructor/method.
   *
   * This function is only available if you use goog.inherits to
   * express inheritance relationships between classes.
   *
   * NOTE: This is a replacement for goog.base and for superClass_
   * property defined in childCtor.
   *
   * @param {!Object} me Should always be "this".
   * @param {string} methodName The method name to call. Calling
   *     superclass constructor can be done with the special string
   *     'constructor'.
   * @param {...*} var_args The arguments to pass to superclass
   *     method/constructor.
   * @return {*} The return value of the superclass method/constructor.
   */
  childCtor.base = function(me, methodName, var_args) {
    // Copying using loop to avoid deop due to passing arguments object to
    // function. This is faster in many JS engines as of late 2014.
    var args = new Array(arguments.length - 2);
    for (var i = 2; i < arguments.length; i++) {
      args[i - 2] = arguments[i];
    }
    return parentCtor.prototype[methodName].apply(me, args);
  };
};


/**
 * Allow for aliasing within scope functions.  This function exists for
 * uncompiled code - in compiled code the calls will be inlined and the aliases
 * applied.  In uncompiled code the function is simply run since the aliases as
 * written are valid JavaScript.
 *
 * MOE:begin_intracomment_strip
 * See the goog.scope document at http://go/goog.scope
 *
 * For more on goog.scope deprecation, see the style guide entry:
 * http://go/jsstyle#appendices-legacy-exceptions-goog-scope
 * MOE:end_intracomment_strip
 *
 * @param {function()} fn Function to call.  This function can contain aliases
 *     to namespaces (e.g. "var dom = goog.dom") or classes
 *     (e.g. "var Timer = goog.Timer").
 * @deprecated Use goog.module instead.
 */
goog.scope = function(fn) {
  if (goog.isInModuleLoader_()) {
    throw new Error('goog.scope is not supported within a module.');
  }
  fn.call(goog.global);
};


/*
 * To support uncompiled, strict mode bundles that use eval to divide source
 * like so:
 *    eval('someSource;//# sourceUrl sourcefile.js');
 * We need to export the globally defined symbols "goog" and "COMPILED".
 * Exporting "goog" breaks the compiler optimizations, so we required that
 * be defined externally.
 * NOTE: We don't use goog.exportSymbol here because we don't want to trigger
 * extern generation when that compiler option is enabled.
 */
if (!COMPILED) {
  goog.global['COMPILED'] = COMPILED;
}


//==============================================================================
// goog.defineClass implementation
//==============================================================================


/**
 * Creates a restricted form of a Closure "class":
 *   - from the compiler's perspective, the instance returned from the
 *     constructor is sealed (no new properties may be added).  This enables
 *     better checks.
 *   - the compiler will rewrite this definition to a form that is optimal
 *     for type checking and optimization (initially this will be a more
 *     traditional form).
 *
 * @param {Function} superClass The superclass, Object or null.
 * @param {goog.defineClass.ClassDescriptor} def
 *     An object literal describing
 *     the class.  It may have the following properties:
 *     "constructor": the constructor function
 *     "statics": an object literal containing methods to add to the constructor
 *        as "static" methods or a function that will receive the constructor
 *        function as its only parameter to which static properties can
 *        be added.
 *     all other properties are added to the prototype.
 * @return {!Function} The class constructor.
 * @deprecated Use ECMAScript class syntax instead.
 */
goog.defineClass = function(superClass, def) {
  // TODO(johnlenz): consider making the superClass an optional parameter.
  var constructor = def.constructor;
  var statics = def.statics;
  // Wrap the constructor prior to setting up the prototype and static methods.
  if (!constructor || constructor == Object.prototype.constructor) {
    constructor = function() {
      throw new Error(
          'cannot instantiate an interface (no constructor defined).');
    };
  }

  var cls = goog.defineClass.createSealingConstructor_(constructor, superClass);
  if (superClass) {
    goog.inherits(cls, superClass);
  }

  // Remove all the properties that should not be copied to the prototype.
  delete def.constructor;
  delete def.statics;

  goog.defineClass.applyProperties_(cls.prototype, def);
  if (statics != null) {
    if (statics instanceof Function) {
      statics(cls);
    } else {
      goog.defineClass.applyProperties_(cls, statics);
    }
  }

  return cls;
};


/**
 * @typedef {{
 *   constructor: (!Function|undefined),
 *   statics: (Object|undefined|function(Function):void)
 * }}
 */
goog.defineClass.ClassDescriptor;


/**
 * @define {boolean} Whether the instances returned by goog.defineClass should
 *     be sealed when possible.
 *
 * When sealing is disabled the constructor function will not be wrapped by
 * goog.defineClass, making it incompatible with ES6 class methods.
 */
goog.defineClass.SEAL_CLASS_INSTANCES =
    goog.define('goog.defineClass.SEAL_CLASS_INSTANCES', goog.DEBUG);


/**
 * If goog.defineClass.SEAL_CLASS_INSTANCES is enabled and Object.seal is
 * defined, this function will wrap the constructor in a function that seals the
 * results of the provided constructor function.
 *
 * @param {!Function} ctr The constructor whose results maybe be sealed.
 * @param {Function} superClass The superclass constructor.
 * @return {!Function} The replacement constructor.
 * @private
 */
goog.defineClass.createSealingConstructor_ = function(ctr, superClass) {
  if (!goog.defineClass.SEAL_CLASS_INSTANCES) {
    // Do now wrap the constructor when sealing is disabled. Angular code
    // depends on this for injection to work properly.
    return ctr;
  }

  // NOTE: The sealing behavior has been removed

  /**
   * @this {Object}
   * @return {?}
   */
  var wrappedCtr = function() {
    // Don't seal an instance of a subclass when it calls the constructor of
    // its super class as there is most likely still setup to do.
    var instance = ctr.apply(this, arguments) || this;
    instance[goog.UID_PROPERTY_] = instance[goog.UID_PROPERTY_];

    return instance;
  };

  return wrappedCtr;
};



// TODO(johnlenz): share these values with the goog.object
/**
 * The names of the fields that are defined on Object.prototype.
 * @type {!Array<string>}
 * @private
 * @const
 */
goog.defineClass.OBJECT_PROTOTYPE_FIELDS_ = [
  'constructor', 'hasOwnProperty', 'isPrototypeOf', 'propertyIsEnumerable',
  'toLocaleString', 'toString', 'valueOf'
];


// TODO(johnlenz): share this function with the goog.object
/**
 * @param {!Object} target The object to add properties to.
 * @param {!Object} source The object to copy properties from.
 * @private
 */
goog.defineClass.applyProperties_ = function(target, source) {
  // TODO(johnlenz): update this to support ES5 getters/setters

  var key;
  for (key in source) {
    if (Object.prototype.hasOwnProperty.call(source, key)) {
      target[key] = source[key];
    }
  }

  // For IE the for-in-loop does not contain any properties that are not
  // enumerable on the prototype object (for example isPrototypeOf from
  // Object.prototype) and it will also not include 'replace' on objects that
  // extend String and change 'replace' (not that it is common for anyone to
  // extend anything except Object).
  for (var i = 0; i < goog.defineClass.OBJECT_PROTOTYPE_FIELDS_.length; i++) {
    key = goog.defineClass.OBJECT_PROTOTYPE_FIELDS_[i];
    if (Object.prototype.hasOwnProperty.call(source, key)) {
      target[key] = source[key];
    }
  }
};

/**
 * Returns the parameter.
 * @param {string} s
 * @return {string}
 * @private
 */
goog.identity_ = function(s) {
  return s;
};


/**
 * Creates Trusted Types policy if Trusted Types are supported by the browser.
 * The policy just blesses any string as a Trusted Type. It is not visibility
 * restricted because anyone can also call trustedTypes.createPolicy directly.
 * However, the allowed names should be restricted by a HTTP header and the
 * reference to the created policy should be visibility restricted.
 * @param {string} name
 * @return {?TrustedTypePolicy}
 */
goog.createTrustedTypesPolicy = function(name) {
  var policy = null;
  var policyFactory = goog.global.trustedTypes;
  if (!policyFactory || !policyFactory.createPolicy) {
    return policy;
  }
  // trustedTypes.createPolicy throws if called with a name that is already
  // registered, even in report-only mode. Until the API changes, catch the
  // error not to break the applications functionally. In such case, the code
  // will fall back to using regular Safe Types.
  // TODO(koto): Remove catching once createPolicy API stops throwing.
  try {
    policy = policyFactory.createPolicy(name, {
      createHTML: goog.identity_,
      createScript: goog.identity_,
      createScriptURL: goog.identity_
    });
  } catch (e) {
    goog.logToConsole_(e.message);
  }
  return policy;
};

// There's a bug in the compiler where without collapse properties the
// Closure namespace defines do not guard code correctly. To help reduce code
// size also check for !COMPILED even though it redundant until this is fixed.
if (!COMPILED && goog.DEPENDENCIES_ENABLED) {
  // MOE:begin_strip
  // TODO(b/67050526) This object is obsolete but some people are relying on
  // it internally. Keep it around until we migrate them.
  /**
   * @private
   * @type {{
   *   loadFlags: !Object<string, !Object<string, string>>,
   *   nameToPath: !Object<string, string>,
   *   requires: !Object<string, !Object<string, boolean>>,
   *   visited: !Object<string, boolean>,
   *   written: !Object<string, boolean>,
   *   deferred: !Object<string, string>
   * }}
   */
  goog.dependencies_ = {
    loadFlags: {},  // 1 to 1

    nameToPath: {},  // 1 to 1

    requires: {},  // 1 to many

    // Used when resolving dependencies to prevent us from visiting file
    // twice.
    visited: {},

    written: {},  // Used to keep track of script files we have written.

    deferred: {}  // Used to track deferred module evaluations in old IEs
  };

  /**
   * @return {!Object}
   * @private
   */
  goog.getLoader_ = function() {
    return {
      dependencies_: goog.dependencies_,
      writeScriptTag_: goog.writeScriptTag_
    };
  };


  /**
   * @param {string} src The script url.
   * @param {string=} opt_sourceText The optionally source text to evaluate
   * @return {boolean} True if the script was imported, false otherwise.
   * @private
   */
  goog.writeScriptTag_ = function(src, opt_sourceText) {
    if (goog.inHtmlDocument_()) {
      /** @type {!HTMLDocument} */
      var doc = goog.global.document;

      // If the user tries to require a new symbol after document load,
      // something has gone terribly wrong. Doing a document.write would
      // wipe out the page. This does not apply to the CSP-compliant method
      // of writing script tags.
      if (!goog.ENABLE_CHROME_APP_SAFE_SCRIPT_LOADING &&
          doc.readyState == 'complete') {
        // Certain test frameworks load base.js multiple times, which tries
        // to write deps.js each time. If that happens, just fail silently.
        // These frameworks wipe the page between each load of base.js, so this
        // is OK.
        var isDeps = /\bdeps.js$/.test(src);
        if (isDeps) {
          return false;
        } else {
          throw Error('Cannot write "' + src + '" after document load');
        }
      }

      var nonceAttr = '';
      var nonce = goog.getScriptNonce_();
      if (nonce) {
        nonceAttr = ' nonce="' + nonce + '"';
      }

      if (opt_sourceText === undefined) {
        var script = '<script src="' + src + '"' + nonceAttr + '></' +
            'script>';
        doc.write(
            goog.TRUSTED_TYPES_POLICY_ ?
                goog.TRUSTED_TYPES_POLICY_.createHTML(script) :
                script);
      } else {
        var script = '<script' + nonceAttr + '>' +
            goog.protectScriptTag_(opt_sourceText) + '</' +
            'script>';
        doc.write(
            goog.TRUSTED_TYPES_POLICY_ ?
                goog.TRUSTED_TYPES_POLICY_.createHTML(script) :
                script);
      }
      return true;
    } else {
      return false;
    }
  };
  // MOE:end_strip


  /**
   * Tries to detect whether the current browser is Edge, based on the user
   * agent. This matches only pre-Chromium Edge.
   * @see https://docs.microsoft.com/en-us/microsoft-edge/web-platform/user-agent-string
   * @return {boolean} True if the current browser is Edge.
   * @private
   */
  goog.isEdge_ = function() {
    var userAgent = goog.global.navigator && goog.global.navigator.userAgent ?
        goog.global.navigator.userAgent :
        '';
    var edgeRe = /Edge\/(\d+)(\.\d)*/i;
    return !!userAgent.match(edgeRe);
  };


  /**
   * Tries to detect whether is in the context of an HTML document.
   * @return {boolean} True if it looks like HTML document.
   * @private
   */
  goog.inHtmlDocument_ = function() {
    /** @type {!Document} */
    var doc = goog.global.document;
    return doc != null && 'write' in doc;  // XULDocument misses write.
  };


  /**
   * We'd like to check for if the document readyState is 'loading'; however
   * there are bugs on IE 10 and below where the readyState being anything other
   * than 'complete' is not reliable.
   * @return {boolean}
   * @private
   */
  goog.isDocumentLoading_ = function() {
    // attachEvent is available on IE 6 thru 10 only, and thus can be used to
    // detect those browsers.
    /** @type {!HTMLDocument} */
    var doc = goog.global.document;
    return doc.attachEvent ? doc.readyState != 'complete' :
                             doc.readyState == 'loading';
  };


  /**
   * Tries to detect the base path of base.js script that bootstraps Closure.
   * @private
   */
  goog.findBasePath_ = function() {
    if (goog.global.CLOSURE_BASE_PATH != undefined &&
        // Anti DOM-clobbering runtime check (b/37736576).
        typeof goog.global.CLOSURE_BASE_PATH === 'string') {
      goog.basePath = goog.global.CLOSURE_BASE_PATH;
      return;
    } else if (!goog.inHtmlDocument_()) {
      return;
    }
    /** @type {!Document} */
    var doc = goog.global.document;
    // If we have a currentScript available, use it exclusively.
    var currentScript = doc.currentScript;
    if (currentScript) {
      var scripts = [currentScript];
    } else {
      var scripts = doc.getElementsByTagName('SCRIPT');
    }
    // Search backwards since the current script is in almost all cases the one
    // that has base.js.
    for (var i = scripts.length - 1; i >= 0; --i) {
      var script = /** @type {!HTMLScriptElement} */ (scripts[i]);
      var src = script.src;
      var qmark = src.lastIndexOf('?');
      var l = qmark == -1 ? src.length : qmark;
      if (src.substr(l - 7, 7) == 'base.js') {
        goog.basePath = src.substr(0, l - 7);
        return;
      }
    }
  };

  goog.findBasePath_();

  /** @struct @constructor @final */
  goog.Transpiler = function() {
    /** @private {?Object<string, boolean>} */
    this.requiresTranspilation_ = null;
    /** @private {string} */
    this.transpilationTarget_ = goog.TRANSPILE_TO_LANGUAGE;
  };


  // MOE:begin_strip
  // LINT.IfChange
  // MOE:end_strip
  /**
   * Returns a newly created map from language mode string to a boolean
   * indicating whether transpilation should be done for that mode as well as
   * the highest level language that this environment supports.
   *
   * Guaranteed invariant:
   * For any two modes, l1 and l2 where l2 is a newer mode than l1,
   * `map[l1] == true` implies that `map[l2] == true`.
   *
   * Note this method is extracted and used elsewhere, so it cannot rely on
   * anything external (it should easily be able to be transformed into a
   * standalone, top level function).
   *
   * @private
   * @return {{
   *   target: string,
   *   map: !Object<string, boolean>
   * }}
   */
  goog.Transpiler.prototype.createRequiresTranspilation_ = function() {
    var transpilationTarget = 'es3';
    var /** !Object<string, boolean> */ requiresTranspilation = {'es3': false};
    var transpilationRequiredForAllLaterModes = false;

    /**
     * Adds an entry to requiresTranspliation for the given language mode.
     *
     * IMPORTANT: Calls must be made in order from oldest to newest language
     * mode.
     * @param {string} modeName
     * @param {function(): boolean} isSupported Returns true if the JS engine
     *     supports the given mode.
     */
    function addNewerLanguageTranspilationCheck(modeName, isSupported) {
      if (transpilationRequiredForAllLaterModes) {
        requiresTranspilation[modeName] = true;
      } else if (isSupported()) {
        transpilationTarget = modeName;
        requiresTranspilation[modeName] = false;
      } else {
        requiresTranspilation[modeName] = true;
        transpilationRequiredForAllLaterModes = true;
      }
    }

    /**
     * Does the given code evaluate without syntax errors and return a truthy
     * result?
     */
    function /** boolean */ evalCheck(/** string */ code) {
      try {
        return !!eval(goog.CLOSURE_EVAL_PREFILTER_.createScript(code));
      } catch (ignored) {
        return false;
      }
    }

    // Identify ES3-only browsers by their incorrect treatment of commas.
    addNewerLanguageTranspilationCheck('es5', function() {
      return evalCheck('[1,].length==1');
    });
    addNewerLanguageTranspilationCheck('es6', function() {
      // Edge has a non-deterministic (i.e., not reproducible) bug with ES6:
      // https://github.com/Microsoft/ChakraCore/issues/1496.
      // MOE:begin_strip
      // TODO(joeltine): Our internal web-testing version of Edge will need to
      // be updated before we can remove this check. See http://b/34945376.
      // MOE:end_strip
      if (goog.isEdge_()) {
        // The Reflect.construct test below is flaky on Edge. It can sometimes
        // pass or fail on 40 15.15063, so just exit early for Edge and treat
        // it as ES5. Until we're on a more up to date version just always use
        // ES5. See https://github.com/Microsoft/ChakraCore/issues/3217.
        return false;
      }
      // Test es6: [FF50 (?), Edge 14 (?), Chrome 50]
      //   (a) default params (specifically shadowing locals),
      //   (b) destructuring, (c) block-scoped functions,
      //   (d) for-of (const), (e) new.target/Reflect.construct
      var es6fullTest =
          'class X{constructor(){if(new.target!=String)throw 1;this.x=42}}' +
          'let q=Reflect.construct(X,[],String);if(q.x!=42||!(q instanceof ' +
          'String))throw 1;for(const a of[2,3]){if(a==2)continue;function ' +
          'f(z={a}){let a=0;return z.a}{function f(){return 0;}}return f()' +
          '==3}';

      return evalCheck('(()=>{"use strict";' + es6fullTest + '})()');
    });
    // ** and **= are the only new features in 'es7'
    addNewerLanguageTranspilationCheck('es7', function() {
      return evalCheck('2**3==8');
    });
    // async functions are the only new features in 'es8'
    addNewerLanguageTranspilationCheck('es8', function() {
      return evalCheck('async()=>1,1');
    });
    addNewerLanguageTranspilationCheck('es9', function() {
      return evalCheck('({...rest}={}),1');
    });
    // optional catch binding, unescaped unicode paragraph separator in strings
    addNewerLanguageTranspilationCheck('es_2019', function() {
      return evalCheck('let r;try{r="\u2029"}catch{};r');
    });
    // optional chaining, nullish coalescing
    // untested/unsupported: bigint, import meta
    addNewerLanguageTranspilationCheck('es_2020', function() {
      return evalCheck('null?.x??1');
    });
    addNewerLanguageTranspilationCheck('es_next', function() {
      return false;  // assume it always need to transpile
    });
    return {target: transpilationTarget, map: requiresTranspilation};
  };
  // MOE:begin_strip
  // LINT.ThenChange(//depot/google3/java/com/google/testing/web/devtools/updatebrowserinfo/requires_transpilation.js)
  // MOE:end_strip


  /**
   * Determines whether the given language needs to be transpiled.
   * @param {string} lang
   * @param {string|undefined} module
   * @return {boolean}
   */
  goog.Transpiler.prototype.needsTranspile = function(lang, module) {
    if (goog.TRANSPILE == 'always') {
      return true;
    } else if (goog.TRANSPILE == 'never') {
      return false;
    } else if (!this.requiresTranspilation_) {
      var obj = this.createRequiresTranspilation_();
      this.requiresTranspilation_ = obj.map;
      this.transpilationTarget_ = this.transpilationTarget_ || obj.target;
    }
    if (lang in this.requiresTranspilation_) {
      if (this.requiresTranspilation_[lang]) {
        return true;
      } else if (
          goog.inHtmlDocument_() && module == 'es6' &&
          !('noModule' in goog.global.document.createElement('script'))) {
        return true;
      } else {
        return false;
      }
    } else {
      throw new Error('Unknown language mode: ' + lang);
    }
  };


  /**
   * Lazily retrieves the transpiler and applies it to the source.
   * @param {string} code JS code.
   * @param {string} path Path to the code.
   * @return {string} The transpiled code.
   */
  goog.Transpiler.prototype.transpile = function(code, path) {
    // TODO(johnplaisted): We should delete goog.transpile_ and just have this
    // function. But there's some compile error atm where goog.global is being
    // stripped incorrectly without this.
    return goog.transpile_(code, path, this.transpilationTarget_);
  };


  /** @private @final {!goog.Transpiler} */
  goog.transpiler_ = new goog.Transpiler();

  /**
   * Rewrites closing script tags in input to avoid ending an enclosing script
   * tag.
   *
   * @param {string} str
   * @return {string}
   * @private
   */
  goog.protectScriptTag_ = function(str) {
    return str.replace(/<\/(SCRIPT)/ig, '\\x3c/$1');
  };


  /**
   * A debug loader is responsible for downloading and executing javascript
   * files in an unbundled, uncompiled environment.
   *
   * This can be custimized via the setDependencyFactory method, or by
   * CLOSURE_IMPORT_SCRIPT/CLOSURE_LOAD_FILE_SYNC.
   *
   * @struct @constructor @final @private
   */
  goog.DebugLoader_ = function() {
    /** @private @const {!Object<string, !goog.Dependency>} */
    this.dependencies_ = {};
    /** @private @const {!Object<string, string>} */
    this.idToPath_ = {};
    /** @private @const {!Object<string, boolean>} */
    this.written_ = {};
    /** @private @const {!Array<!goog.Dependency>} */
    this.loadingDeps_ = [];
    /** @private {!Array<!goog.Dependency>} */
    this.depsToLoad_ = [];
    /** @private {boolean} */
    this.paused_ = false;
    /** @private {!goog.DependencyFactory} */
    this.factory_ = new goog.DependencyFactory(goog.transpiler_);
    /** @private @const {!Object<string, !Function>} */
    this.deferredCallbacks_ = {};
    /** @private @const {!Array<string>} */
    this.deferredQueue_ = [];
  };

  /**
   * @param {!Array<string>} namespaces
   * @param {function(): undefined} callback Function to call once all the
   *     namespaces have loaded.
   */
  goog.DebugLoader_.prototype.bootstrap = function(namespaces, callback) {
    var cb = callback;
    function resolve() {
      if (cb) {
        goog.global.setTimeout(cb, 0);
        cb = null;
      }
    }

    if (!namespaces.length) {
      resolve();
      return;
    }

    var deps = [];
    for (var i = 0; i < namespaces.length; i++) {
      var path = this.getPathFromDeps_(namespaces[i]);
      if (!path) {
        throw new Error('Unregonized namespace: ' + namespaces[i]);
      }
      deps.push(this.dependencies_[path]);
    }

    var require = goog.require;
    var loaded = 0;
    for (var i = 0; i < namespaces.length; i++) {
      require(namespaces[i]);
      deps[i].onLoad(function() {
        if (++loaded == namespaces.length) {
          resolve();
        }
      });
    }
  };


  /**
   * Loads the Closure Dependency file.
   *
   * Exposed a public function so CLOSURE_NO_DEPS can be set to false, base
   * loaded, setDependencyFactory called, and then this called. i.e. allows
   * custom loading of the deps file.
   */
  goog.DebugLoader_.prototype.loadClosureDeps = function() {
    // Circumvent addDependency, which would try to transpile deps.js if
    // transpile is set to always.
    var relPath = 'deps.js';
    this.depsToLoad_.push(this.factory_.createDependency(
        goog.normalizePath_(goog.basePath + relPath), relPath, [], [], {},
        false));
    this.loadDeps_();
  };


  /**
   * Notifies the debug loader when a dependency has been requested.
   *
   * @param {string} absPathOrId Path of the dependency or goog id.
   * @param {boolean=} opt_force
   */
  goog.DebugLoader_.prototype.requested = function(absPathOrId, opt_force) {
    var path = this.getPathFromDeps_(absPathOrId);
    if (path &&
        (opt_force || this.areDepsLoaded_(this.dependencies_[path].requires))) {
      var callback = this.deferredCallbacks_[path];
      if (callback) {
        delete this.deferredCallbacks_[path];
        callback();
      }
    }
  };


  /**
   * Sets the dependency factory, which can be used to create custom
   * goog.Dependency implementations to control how dependencies are loaded.
   *
   * @param {!goog.DependencyFactory} factory
   */
  goog.DebugLoader_.prototype.setDependencyFactory = function(factory) {
    this.factory_ = factory;
  };


  /**
   * Travserses the dependency graph and queues the given dependency, and all of
   * its transitive dependencies, for loading and then starts loading if not
   * paused.
   *
   * @param {string} namespace
   * @private
   */
  goog.DebugLoader_.prototype.load_ = function(namespace) {
    if (!this.getPathFromDeps_(namespace)) {
      var errorMessage = 'goog.require could not find: ' + namespace;
      goog.logToConsole_(errorMessage);
    } else {
      var loader = this;

      var deps = [];

      /** @param {string} namespace */
      var visit = function(namespace) {
        var path = loader.getPathFromDeps_(namespace);

        if (!path) {
          throw new Error('Bad dependency path or symbol: ' + namespace);
        }

        if (loader.written_[path]) {
          return;
        }

        loader.written_[path] = true;

        var dep = loader.dependencies_[path];
        // MOE:begin_strip
        if (goog.dependencies_.written[dep.relativePath]) {
          return;
        }
        // MOE:end_strip
        for (var i = 0; i < dep.requires.length; i++) {
          if (!goog.isProvided_(dep.requires[i])) {
            visit(dep.requires[i]);
          }
        }

        deps.push(dep);
      };

      visit(namespace);

      var wasLoading = !!this.depsToLoad_.length;
      this.depsToLoad_ = this.depsToLoad_.concat(deps);

      if (!this.paused_ && !wasLoading) {
        this.loadDeps_();
      }
    }
  };


  /**
   * Loads any queued dependencies until they are all loaded or paused.
   *
   * @private
   */
  goog.DebugLoader_.prototype.loadDeps_ = function() {
    var loader = this;
    var paused = this.paused_;

    while (this.depsToLoad_.length && !paused) {
      (function() {
        var loadCallDone = false;
        var dep = loader.depsToLoad_.shift();

        var loaded = false;
        loader.loading_(dep);

        var controller = {
          pause: function() {
            if (loadCallDone) {
              throw new Error('Cannot call pause after the call to load.');
            } else {
              paused = true;
            }
          },
          resume: function() {
            if (loadCallDone) {
              loader.resume_();
            } else {
              // Some dep called pause and then resume in the same load call.
              // Just keep running this same loop.
              paused = false;
            }
          },
          loaded: function() {
            if (loaded) {
              throw new Error('Double call to loaded.');
            }

            loaded = true;
            loader.loaded_(dep);
          },
          pending: function() {
            // Defensive copy.
            var pending = [];
            for (var i = 0; i < loader.loadingDeps_.length; i++) {
              pending.push(loader.loadingDeps_[i]);
            }
            return pending;
          },
          /**
           * @param {goog.ModuleType} type
           */
          setModuleState: function(type) {
            goog.moduleLoaderState_ = {
              type: type,
              moduleName: '',
              declareLegacyNamespace: false
            };
          },
          /** @type {function(string, string, string=)} */
          registerEs6ModuleExports: function(
              path, exports, opt_closureNamespace) {
            if (opt_closureNamespace) {
              goog.loadedModules_[opt_closureNamespace] = {
                exports: exports,
                type: goog.ModuleType.ES6,
                moduleId: opt_closureNamespace || ''
              };
            }
          },
          /** @type {function(string, ?)} */
          registerGoogModuleExports: function(moduleId, exports) {
            goog.loadedModules_[moduleId] = {
              exports: exports,
              type: goog.ModuleType.GOOG,
              moduleId: moduleId
            };
          },
          clearModuleState: function() {
            goog.moduleLoaderState_ = null;
          },
          defer: function(callback) {
            if (loadCallDone) {
              throw new Error(
                  'Cannot register with defer after the call to load.');
            }
            loader.defer_(dep, callback);
          },
          areDepsLoaded: function() {
            return loader.areDepsLoaded_(dep.requires);
          }
        };

        try {
          dep.load(controller);
        } finally {
          loadCallDone = true;
        }
      })();
    }

    if (paused) {
      this.pause_();
    }
  };


  /** @private */
  goog.DebugLoader_.prototype.pause_ = function() {
    this.paused_ = true;
  };


  /** @private */
  goog.DebugLoader_.prototype.resume_ = function() {
    if (this.paused_) {
      this.paused_ = false;
      this.loadDeps_();
    }
  };


  /**
   * Marks the given dependency as loading (load has been called but it has not
   * yet marked itself as finished). Useful for dependencies that want to know
   * what else is loading. Example: goog.modules cannot eval if there are
   * loading dependencies.
   *
   * @param {!goog.Dependency} dep
   * @private
   */
  goog.DebugLoader_.prototype.loading_ = function(dep) {
    this.loadingDeps_.push(dep);
  };


  /**
   * Marks the given dependency as having finished loading and being available
   * for require.
   *
   * @param {!goog.Dependency} dep
   * @private
   */
  goog.DebugLoader_.prototype.loaded_ = function(dep) {
    for (var i = 0; i < this.loadingDeps_.length; i++) {
      if (this.loadingDeps_[i] == dep) {
        this.loadingDeps_.splice(i, 1);
        break;
      }
    }

    for (var i = 0; i < this.deferredQueue_.length; i++) {
      if (this.deferredQueue_[i] == dep.path) {
        this.deferredQueue_.splice(i, 1);
        break;
      }
    }

    if (this.loadingDeps_.length == this.deferredQueue_.length &&
        !this.depsToLoad_.length) {
      // Something has asked to load these, but they may not be directly
      // required again later, so load them now that we know we're done loading
      // everything else. e.g. a goog module entry point.
      while (this.deferredQueue_.length) {
        this.requested(this.deferredQueue_.shift(), true);
      }
    }

    dep.loaded();
  };


  /**
   * @param {!Array<string>} pathsOrIds
   * @return {boolean}
   * @private
   */
  goog.DebugLoader_.prototype.areDepsLoaded_ = function(pathsOrIds) {
    for (var i = 0; i < pathsOrIds.length; i++) {
      var path = this.getPathFromDeps_(pathsOrIds[i]);
      if (!path ||
          (!(path in this.deferredCallbacks_) &&
           !goog.isProvided_(pathsOrIds[i]))) {
        return false;
      }
    }

    return true;
  };


  /**
   * @param {string} absPathOrId
   * @return {?string}
   * @private
   */
  goog.DebugLoader_.prototype.getPathFromDeps_ = function(absPathOrId) {
    if (absPathOrId in this.idToPath_) {
      return this.idToPath_[absPathOrId];
    } else if (absPathOrId in this.dependencies_) {
      return absPathOrId;
    } else {
      return null;
    }
  };


  /**
   * @param {!goog.Dependency} dependency
   * @param {!Function} callback
   * @private
   */
  goog.DebugLoader_.prototype.defer_ = function(dependency, callback) {
    this.deferredCallbacks_[dependency.path] = callback;
    this.deferredQueue_.push(dependency.path);
  };


  /**
   * Interface for goog.Dependency implementations to have some control over
   * loading of dependencies.
   *
   * @record
   */
  goog.LoadController = function() {};


  /**
   * Tells the controller to halt loading of more dependencies.
   */
  goog.LoadController.prototype.pause = function() {};


  /**
   * Tells the controller to resume loading of more dependencies if paused.
   */
  goog.LoadController.prototype.resume = function() {};


  /**
   * Tells the controller that this dependency has finished loading.
   *
   * This causes this to be removed from pending() and any load callbacks to
   * fire.
   */
  goog.LoadController.prototype.loaded = function() {};


  /**
   * List of dependencies on which load has been called but which have not
   * called loaded on their controller. This includes the current dependency.
   *
   * @return {!Array<!goog.Dependency>}
   */
  goog.LoadController.prototype.pending = function() {};


  /**
   * Registers an object as an ES6 module's exports so that goog.modules may
   * require it by path.
   *
   * @param {string} path Full path of the module.
   * @param {?} exports
   * @param {string=} opt_closureNamespace Closure namespace to associate with
   *     this module.
   */
  goog.LoadController.prototype.registerEs6ModuleExports = function(
      path, exports, opt_closureNamespace) {};


  /**
   * Sets the current module state.
   *
   * @param {goog.ModuleType} type Type of module.
   */
  goog.LoadController.prototype.setModuleState = function(type) {};


  /**
   * Clears the current module state.
   */
  goog.LoadController.prototype.clearModuleState = function() {};


  /**
   * Registers a callback to call once the dependency is actually requested
   * via goog.require + all of the immediate dependencies have been loaded or
   * all other files have been loaded. Allows for lazy loading until
   * require'd without pausing dependency loading, which is needed on old IE.
   *
   * @param {!Function} callback
   */
  goog.LoadController.prototype.defer = function(callback) {};


  /**
   * @return {boolean}
   */
  goog.LoadController.prototype.areDepsLoaded = function() {};


  /**
   * Basic super class for all dependencies Closure Library can load.
   *
   * This default implementation is designed to load untranspiled, non-module
   * scripts in a web broswer.
   *
   * For transpiled non-goog.module files {@see goog.TranspiledDependency}.
   * For goog.modules see {@see goog.GoogModuleDependency}.
   * For untranspiled ES6 modules {@see goog.Es6ModuleDependency}.
   *
   * @param {string} path Absolute path of this script.
   * @param {string} relativePath Path of this script relative to goog.basePath.
   * @param {!Array<string>} provides goog.provided or goog.module symbols
   *     in this file.
   * @param {!Array<string>} requires goog symbols or relative paths to Closure
   *     this depends on.
   * @param {!Object<string, string>} loadFlags
   * @struct @constructor
   */
  goog.Dependency = function(
      path, relativePath, provides, requires, loadFlags) {
    /** @const */
    this.path = path;
    /** @const */
    this.relativePath = relativePath;
    /** @const */
    this.provides = provides;
    /** @const */
    this.requires = requires;
    /** @const */
    this.loadFlags = loadFlags;
    /** @private {boolean} */
    this.loaded_ = false;
    /** @private {!Array<function()>} */
    this.loadCallbacks_ = [];
  };


  /**
   * @return {string} The pathname part of this dependency's path if it is a
   *     URI.
   */
  goog.Dependency.prototype.getPathName = function() {
    var pathName = this.path;
    var protocolIndex = pathName.indexOf('://');
    if (protocolIndex >= 0) {
      pathName = pathName.substring(protocolIndex + 3);
      var slashIndex = pathName.indexOf('/');
      if (slashIndex >= 0) {
        pathName = pathName.substring(slashIndex + 1);
      }
    }
    return pathName;
  };


  /**
   * @param {function()} callback Callback to fire as soon as this has loaded.
   * @final
   */
  goog.Dependency.prototype.onLoad = function(callback) {
    if (this.loaded_) {
      callback();
    } else {
      this.loadCallbacks_.push(callback);
    }
  };


  /**
   * Marks this dependency as loaded and fires any callbacks registered with
   * onLoad.
   * @final
   */
  goog.Dependency.prototype.loaded = function() {
    this.loaded_ = true;
    var callbacks = this.loadCallbacks_;
    this.loadCallbacks_ = [];
    for (var i = 0; i < callbacks.length; i++) {
      callbacks[i]();
    }
  };


  /**
   * Whether or not document.written / appended script tags should be deferred.
   *
   * @private {boolean}
   */
  goog.Dependency.defer_ = false;


  /**
   * Map of script ready / state change callbacks. Old IE cannot handle putting
   * these properties on goog.global.
   *
   * @private @const {!Object<string, function(?):undefined>}
   */
  goog.Dependency.callbackMap_ = {};


  /**
   * @param {function(...?):?} callback
   * @return {string}
   * @private
   */
  goog.Dependency.registerCallback_ = function(callback) {
    var key = Math.random().toString(32);
    goog.Dependency.callbackMap_[key] = callback;
    return key;
  };


  /**
   * @param {string} key
   * @private
   */
  goog.Dependency.unregisterCallback_ = function(key) {
    delete goog.Dependency.callbackMap_[key];
  };


  /**
   * @param {string} key
   * @param {...?} var_args
   * @private
   * @suppress {unusedPrivateMembers}
   */
  goog.Dependency.callback_ = function(key, var_args) {
    if (key in goog.Dependency.callbackMap_) {
      var callback = goog.Dependency.callbackMap_[key];
      var args = [];
      for (var i = 1; i < arguments.length; i++) {
        args.push(arguments[i]);
      }
      callback.apply(undefined, args);
    } else {
      var errorMessage = 'Callback key ' + key +
          ' does not exist (was base.js loaded more than once?).';
      // MOE:begin_strip
      // TODO(johnplaisted): Some people internally are mistakenly loading
      // base.js twice, and this can happen while a dependency is loading,
      // wiping out state.
      goog.logToConsole_(errorMessage);
      // MOE:end_strip
      // MOE:insert throw Error(errorMessage);
    }
  };


  /**
   * Starts loading this dependency. This dependency can pause loading if it
   * needs to and resume it later via the controller interface.
   *
   * When this is loaded it should call controller.loaded(). Note that this will
   * end up calling the loaded method of this dependency; there is no need to
   * call it explicitly.
   *
   * @param {!goog.LoadController} controller
   */
  goog.Dependency.prototype.load = function(controller) {
    if (goog.global.CLOSURE_IMPORT_SCRIPT) {
      if (goog.global.CLOSURE_IMPORT_SCRIPT(this.path)) {
        controller.loaded();
      } else {
        controller.pause();
      }
      return;
    }

    if (!goog.inHtmlDocument_()) {
      goog.logToConsole_(
          'Cannot use default debug loader outside of HTML documents.');
      if (this.relativePath == 'deps.js') {
        // Some old code is relying on base.js auto loading deps.js failing with
        // no error before later setting CLOSURE_IMPORT_SCRIPT.
        // CLOSURE_IMPORT_SCRIPT should be set *before* base.js is loaded, or
        // CLOSURE_NO_DEPS set to true.
        goog.logToConsole_(
            'Consider setting CLOSURE_IMPORT_SCRIPT before loading base.js, ' +
            'or setting CLOSURE_NO_DEPS to true.');
        controller.loaded();
      } else {
        controller.pause();
      }
      return;
    }

    /** @type {!HTMLDocument} */
    var doc = goog.global.document;

    // If the user tries to require a new symbol after document load,
    // something has gone terribly wrong. Doing a document.write would
    // wipe out the page. This does not apply to the CSP-compliant method
    // of writing script tags.
    if (doc.readyState == 'complete' &&
        !goog.ENABLE_CHROME_APP_SAFE_SCRIPT_LOADING) {
      // Certain test frameworks load base.js multiple times, which tries
      // to write deps.js each time. If that happens, just fail silently.
      // These frameworks wipe the page between each load of base.js, so this
      // is OK.
      var isDeps = /\bdeps.js$/.test(this.path);
      if (isDeps) {
        controller.loaded();
        return;
      } else {
        throw Error('Cannot write "' + this.path + '" after document load');
      }
    }

    var nonce = goog.getScriptNonce_();
    if (!goog.ENABLE_CHROME_APP_SAFE_SCRIPT_LOADING &&
        goog.isDocumentLoading_()) {
      var key;
      var callback = function(script) {
        if (script.readyState && script.readyState != 'complete') {
          script.onload = callback;
          return;
        }
        goog.Dependency.unregisterCallback_(key);
        controller.loaded();
      };
      key = goog.Dependency.registerCallback_(callback);

      var defer = goog.Dependency.defer_ ? ' defer' : '';
      var nonceAttr = nonce ? ' nonce="' + nonce + '"' : '';
      var script = '<script src="' + this.path + '"' + nonceAttr + defer +
          ' id="script-' + key + '"><\/script>';

      script += '<script' + nonceAttr + '>';

      if (goog.Dependency.defer_) {
        script += 'document.getElementById(\'script-' + key +
            '\').onload = function() {\n' +
            '  goog.Dependency.callback_(\'' + key + '\', this);\n' +
            '};\n';
      } else {
        script += 'goog.Dependency.callback_(\'' + key +
            '\', document.getElementById(\'script-' + key + '\'));';
      }

      script += '<\/script>';

      doc.write(
          goog.TRUSTED_TYPES_POLICY_ ?
              goog.TRUSTED_TYPES_POLICY_.createHTML(script) :
              script);
    } else {
      var scriptEl =
          /** @type {!HTMLScriptElement} */ (doc.createElement('script'));
      scriptEl.defer = goog.Dependency.defer_;
      scriptEl.async = false;

      // If CSP nonces are used, propagate them to dynamically created scripts.
      // This is necessary to allow nonce-based CSPs without 'strict-dynamic'.
      if (nonce) {
        scriptEl.nonce = nonce;
      }

      if (goog.DebugLoader_.IS_OLD_IE_) {
        // Execution order is not guaranteed on old IE, halt loading and write
        // these scripts one at a time, after each loads.
        controller.pause();
        scriptEl.onreadystatechange = function() {
          if (scriptEl.readyState == 'loaded' ||
              scriptEl.readyState == 'complete') {
            controller.loaded();
            controller.resume();
          }
        };
      } else {
        scriptEl.onload = function() {
          scriptEl.onload = null;
          controller.loaded();
        };
      }

      scriptEl.src = goog.TRUSTED_TYPES_POLICY_ ?
          goog.TRUSTED_TYPES_POLICY_.createScriptURL(this.path) :
          this.path;
      doc.head.appendChild(scriptEl);
    }
  };


  /**
   * @param {string} path Absolute path of this script.
   * @param {string} relativePath Path of this script relative to goog.basePath.
   * @param {!Array<string>} provides Should be an empty array.
   *     TODO(johnplaisted) add support for adding closure namespaces to ES6
   *     modules for interop purposes.
   * @param {!Array<string>} requires goog symbols or relative paths to Closure
   *     this depends on.
   * @param {!Object<string, string>} loadFlags
   * @struct @constructor
   * @extends {goog.Dependency}
   */
  goog.Es6ModuleDependency = function(
      path, relativePath, provides, requires, loadFlags) {
    goog.Es6ModuleDependency.base(
        this, 'constructor', path, relativePath, provides, requires, loadFlags);
  };
  goog.inherits(goog.Es6ModuleDependency, goog.Dependency);


  /**
   * @override
   * @param {!goog.LoadController} controller
   */
  goog.Es6ModuleDependency.prototype.load = function(controller) {
    if (goog.global.CLOSURE_IMPORT_SCRIPT) {
      if (goog.global.CLOSURE_IMPORT_SCRIPT(this.path)) {
        controller.loaded();
      } else {
        controller.pause();
      }
      return;
    }

    if (!goog.inHtmlDocument_()) {
      goog.logToConsole_(
          'Cannot use default debug loader outside of HTML documents.');
      controller.pause();
      return;
    }

    /** @type {!HTMLDocument} */
    var doc = goog.global.document;

    var dep = this;

    // TODO(johnplaisted): Does document.writing really speed up anything? Any
    // difference between this and just waiting for interactive mode and then
    // appending?
    function write(src, contents) {
      var nonceAttr = '';
      var nonce = goog.getScriptNonce_();
      if (nonce) {
        nonceAttr = ' nonce="' + nonce + '"';
      }

      if (contents) {
        var script = '<script type="module" crossorigin' + nonceAttr + '>' +
            contents + '</' +
            'script>';
        doc.write(
            goog.TRUSTED_TYPES_POLICY_ ?
                goog.TRUSTED_TYPES_POLICY_.createHTML(script) :
                script);
      } else {
        var script = '<script type="module" crossorigin src="' + src + '"' +
            nonceAttr + '></' +
            'script>';
        doc.write(
            goog.TRUSTED_TYPES_POLICY_ ?
                goog.TRUSTED_TYPES_POLICY_.createHTML(script) :
                script);
      }
    }

    function append(src, contents) {
      var scriptEl =
          /** @type {!HTMLScriptElement} */ (doc.createElement('script'));
      scriptEl.defer = true;
      scriptEl.async = false;
      scriptEl.type = 'module';
      scriptEl.setAttribute('crossorigin', true);

      // If CSP nonces are used, propagate them to dynamically created scripts.
      // This is necessary to allow nonce-based CSPs without 'strict-dynamic'.
      var nonce = goog.getScriptNonce_();
      if (nonce) {
        scriptEl.nonce = nonce;
      }

      if (contents) {
        scriptEl.text = goog.TRUSTED_TYPES_POLICY_ ?
            goog.TRUSTED_TYPES_POLICY_.createScript(contents) :
            contents;
      } else {
        scriptEl.src = goog.TRUSTED_TYPES_POLICY_ ?
            goog.TRUSTED_TYPES_POLICY_.createScriptURL(src) :
            src;
      }

      doc.head.appendChild(scriptEl);
    }

    var create;

    if (goog.isDocumentLoading_()) {
      create = write;
      // We can ONLY call document.write if we are guaranteed that any
      // non-module script tags document.written after this are deferred.
      // Small optimization, in theory document.writing is faster.
      goog.Dependency.defer_ = true;
    } else {
      create = append;
    }

    // Write 4 separate tags here:
    // 1) Sets the module state at the correct time (just before execution).
    // 2) A src node for this, which just hopefully lets the browser load it a
    //    little early (no need to parse #3).
    // 3) Import the module and register it.
    // 4) Clear the module state at the correct time. Guaranteed to run even
    //    if there is an error in the module (#3 will not run if there is an
    //    error in the module).
    var beforeKey = goog.Dependency.registerCallback_(function() {
      goog.Dependency.unregisterCallback_(beforeKey);
      controller.setModuleState(goog.ModuleType.ES6);
    });
    create(undefined, 'goog.Dependency.callback_("' + beforeKey + '")');

    // TODO(johnplaisted): Does this really speed up anything?
    create(this.path, undefined);

    var registerKey = goog.Dependency.registerCallback_(function(exports) {
      goog.Dependency.unregisterCallback_(registerKey);
      controller.registerEs6ModuleExports(
          dep.path, exports, goog.moduleLoaderState_.moduleName);
    });
    create(
        undefined,
        'import * as m from "' + this.path + '"; goog.Dependency.callback_("' +
            registerKey + '", m)');

    var afterKey = goog.Dependency.registerCallback_(function() {
      goog.Dependency.unregisterCallback_(afterKey);
      controller.clearModuleState();
      controller.loaded();
    });
    create(undefined, 'goog.Dependency.callback_("' + afterKey + '")');
  };


  /**
   * Superclass of any dependency that needs to be loaded into memory,
   * transformed, and then eval'd (goog.modules and transpiled files).
   *
   * @param {string} path Absolute path of this script.
   * @param {string} relativePath Path of this script relative to goog.basePath.
   * @param {!Array<string>} provides goog.provided or goog.module symbols
   *     in this file.
   * @param {!Array<string>} requires goog symbols or relative paths to Closure
   *     this depends on.
   * @param {!Object<string, string>} loadFlags
   * @struct @constructor @abstract
   * @extends {goog.Dependency}
   */
  goog.TransformedDependency = function(
      path, relativePath, provides, requires, loadFlags) {
    goog.TransformedDependency.base(
        this, 'constructor', path, relativePath, provides, requires, loadFlags);
    /** @private {?string} */
    this.contents_ = null;

    /**
     * Whether to lazily make the synchronous XHR (when goog.require'd) or make
     * the synchronous XHR when initially loading. On FireFox 61 there is a bug
     * where an ES6 module cannot make a synchronous XHR (rather, it can, but if
     * it does then no other ES6 modules will load after).
     *
     * tl;dr we lazy load due to bugs on older browsers and eager load due to
     * bugs on newer ones.
     *
     * https://bugzilla.mozilla.org/show_bug.cgi?id=1477090
     *
     * @private @const {boolean}
     */
    this.lazyFetch_ = !goog.inHtmlDocument_() ||
        !('noModule' in goog.global.document.createElement('script'));
  };
  goog.inherits(goog.TransformedDependency, goog.Dependency);


  /**
   * @override
   * @param {!goog.LoadController} controller
   */
  goog.TransformedDependency.prototype.load = function(controller) {
    var dep = this;

    function fetch() {
      dep.contents_ = goog.loadFileSync_(dep.path);

      if (dep.contents_) {
        dep.contents_ = dep.transform(dep.contents_);
        if (dep.contents_) {
          dep.contents_ += '\n//# sourceURL=' + dep.path;
        }
      }
    }

    if (goog.global.CLOSURE_IMPORT_SCRIPT) {
      fetch();
      if (this.contents_ &&
          goog.global.CLOSURE_IMPORT_SCRIPT('', this.contents_)) {
        this.contents_ = null;
        controller.loaded();
      } else {
        controller.pause();
      }
      return;
    }


    var isEs6 = this.loadFlags['module'] == goog.ModuleType.ES6;

    if (!this.lazyFetch_) {
      fetch();
    }

    function load() {
      if (dep.lazyFetch_) {
        fetch();
      }

      if (!dep.contents_) {
        // loadFileSync_ or transform are responsible. Assume they logged an
        // error.
        return;
      }

      if (isEs6) {
        controller.setModuleState(goog.ModuleType.ES6);
      }

      var namespace;

      try {
        var contents = dep.contents_;
        dep.contents_ = null;
        goog.globalEval(goog.CLOSURE_EVAL_PREFILTER_.createScript(contents));
        if (isEs6) {
          namespace = goog.moduleLoaderState_.moduleName;
        }
      } finally {
        if (isEs6) {
          controller.clearModuleState();
        }
      }

      if (isEs6) {
        // Due to circular dependencies this may not be available for require
        // right now.
        goog.global['$jscomp']['require']['ensure'](
            [dep.getPathName()], function() {
              controller.registerEs6ModuleExports(
                  dep.path,
                  goog.global['$jscomp']['require'](dep.getPathName()),
                  namespace);
            });
      }

      controller.loaded();
    }

    // Do not fetch now; in FireFox 47 the synchronous XHR doesn't block all
    // events. If we fetched now and then document.write'd the contents the
    // document.write would be an eval and would execute too soon! Instead write
    // a script tag to fetch and eval synchronously at the correct time.
    function fetchInOwnScriptThenLoad() {
      /** @type {!HTMLDocument} */
      var doc = goog.global.document;

      var key = goog.Dependency.registerCallback_(function() {
        goog.Dependency.unregisterCallback_(key);
        load();
      });

      var nonce = goog.getScriptNonce_();
      var nonceAttr = nonce ? ' nonce="' + nonce + '"' : '';
      var script = '<script' + nonceAttr + '>' +
          goog.protectScriptTag_('goog.Dependency.callback_("' + key + '");') +
          '</' +
          'script>';
      doc.write(
          goog.TRUSTED_TYPES_POLICY_ ?
              goog.TRUSTED_TYPES_POLICY_.createHTML(script) :
              script);
    }

    // If one thing is pending it is this.
    var anythingElsePending = controller.pending().length > 1;

    // If anything else is loading we need to lazy load due to bugs in old IE.
    // Specifically script tags with src and script tags with contents could
    // execute out of order if document.write is used, so we cannot use
    // document.write. Do not pause here; it breaks old IE as well.
    var useOldIeWorkAround =
        anythingElsePending && goog.DebugLoader_.IS_OLD_IE_;

    // Additionally if we are meant to defer scripts but the page is still
    // loading (e.g. an ES6 module is loading) then also defer. Or if we are
    // meant to defer and anything else is pending then defer (those may be
    // scripts that did not need transformation and are just script tags with
    // defer set to true, and we need to evaluate after that deferred script).
    var needsAsyncLoading = goog.Dependency.defer_ &&
        (anythingElsePending || goog.isDocumentLoading_());

    if (useOldIeWorkAround || needsAsyncLoading) {
      // Note that we only defer when we have to rather than 100% of the time.
      // Always defering would work, but then in theory the order of
      // goog.require calls would then matter. We want to enforce that most of
      // the time the order of the require calls does not matter.
      controller.defer(function() {
        load();
      });
      return;
    }
    // TODO(johnplaisted): Externs are missing onreadystatechange for
    // HTMLDocument.
    /** @type {?} */
    var doc = goog.global.document;

    var isInternetExplorerOrEdge = goog.inHtmlDocument_() &&
        ('ActiveXObject' in goog.global || goog.isEdge_());

    // Don't delay in any version of IE or pre-Chromium Edge. There's a bug
    // around this that will cause out of order script execution. This means
    // that on older IE ES6 modules will load too early (while the document is
    // still loading + the dom is not available). The other option is to load
    // too late (when the document is complete and the onload even will never
    // fire). This seems to be the lesser of two evils as scripts already act
    // like the former.
    if (isEs6 && goog.inHtmlDocument_() && goog.isDocumentLoading_() &&
        !isInternetExplorerOrEdge) {
      goog.Dependency.defer_ = true;
      // Transpiled ES6 modules still need to load like regular ES6 modules,
      // aka only after the document is interactive.
      controller.pause();
      var oldCallback = doc.onreadystatechange;
      doc.onreadystatechange = function() {
        if (doc.readyState == 'interactive') {
          doc.onreadystatechange = oldCallback;
          load();
          controller.resume();
        }
        if (typeof oldCallback === 'function') {
          oldCallback.apply(undefined, arguments);
        }
      };
    } else {
      // Always eval on old IE.
      if (goog.DebugLoader_.IS_OLD_IE_ || !goog.inHtmlDocument_() ||
          !goog.isDocumentLoading_()) {
        load();
      } else {
        fetchInOwnScriptThenLoad();
      }
    }
  };


  /**
   * @param {string} contents
   * @return {string}
   * @abstract
   */
  goog.TransformedDependency.prototype.transform = function(contents) {};


  /**
   * Any non-goog.module dependency which needs to be transpiled before eval.
   *
   * @param {string} path Absolute path of this script.
   * @param {string} relativePath Path of this script relative to goog.basePath.
   * @param {!Array<string>} provides goog.provided or goog.module symbols
   *     in this file.
   * @param {!Array<string>} requires goog symbols or relative paths to Closure
   *     this depends on.
   * @param {!Object<string, string>} loadFlags
   * @param {!goog.Transpiler} transpiler
   * @struct @constructor
   * @extends {goog.TransformedDependency}
   */
  goog.TranspiledDependency = function(
      path, relativePath, provides, requires, loadFlags, transpiler) {
    goog.TranspiledDependency.base(
        this, 'constructor', path, relativePath, provides, requires, loadFlags);
    /** @protected @const*/
    this.transpiler = transpiler;
  };
  goog.inherits(goog.TranspiledDependency, goog.TransformedDependency);


  /**
   * @override
   * @param {string} contents
   * @return {string}
   */
  goog.TranspiledDependency.prototype.transform = function(contents) {
    // Transpile with the pathname so that ES6 modules are domain agnostic.
    return this.transpiler.transpile(contents, this.getPathName());
  };


  /**
   * An ES6 module dependency that was transpiled to a jscomp module outside
   * of the debug loader, e.g. server side.
   *
   * @param {string} path Absolute path of this script.
   * @param {string} relativePath Path of this script relative to goog.basePath.
   * @param {!Array<string>} provides goog.provided or goog.module symbols
   *     in this file.
   * @param {!Array<string>} requires goog symbols or relative paths to Closure
   *     this depends on.
   * @param {!Object<string, string>} loadFlags
   * @struct @constructor
   * @extends {goog.TransformedDependency}
   */
  goog.PreTranspiledEs6ModuleDependency = function(
      path, relativePath, provides, requires, loadFlags) {
    goog.PreTranspiledEs6ModuleDependency.base(
        this, 'constructor', path, relativePath, provides, requires, loadFlags);
  };
  goog.inherits(
      goog.PreTranspiledEs6ModuleDependency, goog.TransformedDependency);


  /**
   * @override
   * @param {string} contents
   * @return {string}
   */
  goog.PreTranspiledEs6ModuleDependency.prototype.transform = function(
      contents) {
    return contents;
  };


  /**
   * A goog.module, transpiled or not. Will always perform some minimal
   * transformation even when not transpiled to wrap in a goog.loadModule
   * statement.
   *
   * @param {string} path Absolute path of this script.
   * @param {string} relativePath Path of this script relative to goog.basePath.
   * @param {!Array<string>} provides goog.provided or goog.module symbols
   *     in this file.
   * @param {!Array<string>} requires goog symbols or relative paths to Closure
   *     this depends on.
   * @param {!Object<string, string>} loadFlags
   * @param {boolean} needsTranspile
   * @param {!goog.Transpiler} transpiler
   * @struct @constructor
   * @extends {goog.TransformedDependency}
   */
  goog.GoogModuleDependency = function(
      path, relativePath, provides, requires, loadFlags, needsTranspile,
      transpiler) {
    goog.GoogModuleDependency.base(
        this, 'constructor', path, relativePath, provides, requires, loadFlags);
    /** @private @const */
    this.needsTranspile_ = needsTranspile;
    /** @private @const */
    this.transpiler_ = transpiler;
  };
  goog.inherits(goog.GoogModuleDependency, goog.TransformedDependency);


  /**
   * @override
   * @param {string} contents
   * @return {string}
   */
  goog.GoogModuleDependency.prototype.transform = function(contents) {
    if (this.needsTranspile_) {
      contents = this.transpiler_.transpile(contents, this.getPathName());
    }

    if (!goog.LOAD_MODULE_USING_EVAL || goog.global.JSON === undefined) {
      return '' +
          'goog.loadModule(function(exports) {' +
          '"use strict";' + contents +
          '\n' +  // terminate any trailing single line comment.
          ';return exports' +
          '});' +
          '\n//# sourceURL=' + this.path + '\n';
    } else {
      return '' +
          'goog.loadModule(' +
          goog.global.JSON.stringify(
              contents + '\n//# sourceURL=' + this.path + '\n') +
          ');';
    }
  };


  /**
   * Whether the browser is IE9 or earlier, which needs special handling
   * for deferred modules.
   * @const @private {boolean}
   */
  goog.DebugLoader_.IS_OLD_IE_ = !!(
      !goog.global.atob && goog.global.document && goog.global.document['all']);


  /**
   * @param {string} relPath
   * @param {!Array<string>|undefined} provides
   * @param {!Array<string>} requires
   * @param {boolean|!Object<string>=} opt_loadFlags
   * @see goog.addDependency
   */
  goog.DebugLoader_.prototype.addDependency = function(
      relPath, provides, requires, opt_loadFlags) {
    provides = provides || [];
    relPath = relPath.replace(/\\/g, '/');
    var path = goog.normalizePath_(goog.basePath + relPath);
    if (!opt_loadFlags || typeof opt_loadFlags === 'boolean') {
      opt_loadFlags = opt_loadFlags ? {'module': goog.ModuleType.GOOG} : {};
    }
    var dep = this.factory_.createDependency(
        path, relPath, provides, requires, opt_loadFlags,
        goog.transpiler_.needsTranspile(
            opt_loadFlags['lang'] || 'es3', opt_loadFlags['module']));
    this.dependencies_[path] = dep;
    for (var i = 0; i < provides.length; i++) {
      this.idToPath_[provides[i]] = path;
    }
    this.idToPath_[relPath] = path;
  };


  /**
   * Creates goog.Dependency instances for the debug loader to load.
   *
   * Should be overridden to have the debug loader use custom subclasses of
   * goog.Dependency.
   *
   * @param {!goog.Transpiler} transpiler
   * @struct @constructor
   */
  goog.DependencyFactory = function(transpiler) {
    /** @protected @const */
    this.transpiler = transpiler;
  };


  /**
   * @param {string} path Absolute path of the file.
   * @param {string} relativePath Path relative to closure’s base.js.
   * @param {!Array<string>} provides Array of provided goog.provide/module ids.
   * @param {!Array<string>} requires Array of required goog.provide/module /
   *     relative ES6 module paths.
   * @param {!Object<string, string>} loadFlags
   * @param {boolean} needsTranspile True if the file needs to be transpiled
   *     per the goog.Transpiler.
   * @return {!goog.Dependency}
   */
  goog.DependencyFactory.prototype.createDependency = function(
      path, relativePath, provides, requires, loadFlags, needsTranspile) {
    // MOE:begin_strip
    var provide, require;
    for (var i = 0; provide = provides[i]; i++) {
      goog.dependencies_.nameToPath[provide] = relativePath;
      goog.dependencies_.loadFlags[relativePath] = loadFlags;
    }
    for (var j = 0; require = requires[j]; j++) {
      if (!(relativePath in goog.dependencies_.requires)) {
        goog.dependencies_.requires[relativePath] = {};
      }
      goog.dependencies_.requires[relativePath][require] = true;
    }
    // MOE:end_strip

    if (loadFlags['module'] == goog.ModuleType.GOOG) {
      return new goog.GoogModuleDependency(
          path, relativePath, provides, requires, loadFlags, needsTranspile,
          this.transpiler);
    } else if (needsTranspile) {
      return new goog.TranspiledDependency(
          path, relativePath, provides, requires, loadFlags, this.transpiler);
    } else {
      if (loadFlags['module'] == goog.ModuleType.ES6) {
        if (goog.TRANSPILE == 'never' && goog.ASSUME_ES_MODULES_TRANSPILED) {
          return new goog.PreTranspiledEs6ModuleDependency(
              path, relativePath, provides, requires, loadFlags);
        } else {
          return new goog.Es6ModuleDependency(
              path, relativePath, provides, requires, loadFlags);
        }
      } else {
        return new goog.Dependency(
            path, relativePath, provides, requires, loadFlags);
      }
    }
  };


  /** @private @const */
  goog.debugLoader_ = new goog.DebugLoader_();


  /**
   * Loads the Closure Dependency file.
   *
   * Exposed a public function so CLOSURE_NO_DEPS can be set to false, base
   * loaded, setDependencyFactory called, and then this called. i.e. allows
   * custom loading of the deps file.
   */
  goog.loadClosureDeps = function() {
    goog.debugLoader_.loadClosureDeps();
  };


  /**
   * Sets the dependency factory, which can be used to create custom
   * goog.Dependency implementations to control how dependencies are loaded.
   *
   * Note: if you wish to call this function and provide your own implemnetation
   * it is a wise idea to set CLOSURE_NO_DEPS to true, otherwise the dependency
   * file and all of its goog.addDependency calls will use the default factory.
   * You can call goog.loadClosureDeps to load the Closure dependency file
   * later, after your factory is injected.
   *
   * @param {!goog.DependencyFactory} factory
   */
  goog.setDependencyFactory = function(factory) {
    goog.debugLoader_.setDependencyFactory(factory);
  };


  /**
   * Trusted Types policy for the debug loader.
   * @private @const {?TrustedTypePolicy}
   */
  goog.TRUSTED_TYPES_POLICY_ = goog.TRUSTED_TYPES_POLICY_NAME ?
      goog.createTrustedTypesPolicy(goog.TRUSTED_TYPES_POLICY_NAME + '#base') :
      null;

  if (!goog.global.CLOSURE_NO_DEPS) {
    goog.debugLoader_.loadClosureDeps();
  }


  /**
   * Bootstraps the given namespaces and calls the callback once they are
   * available either via goog.require. This is a replacement for using
   * `goog.require` to bootstrap Closure JavaScript. Previously a `goog.require`
   * in an HTML file would guarantee that the require'd namespace was available
   * in the next immediate script tag. With ES6 modules this no longer a
   * guarantee.
   *
   * @param {!Array<string>} namespaces
   * @param {function(): ?} callback Function to call once all the namespaces
   *     have loaded. Always called asynchronously.
   */
  goog.bootstrap = function(namespaces, callback) {
    goog.debugLoader_.bootstrap(namespaces, callback);
  };
}


if (!COMPILED) {
  var isChrome87 = false;
  // Cannot run check for Chrome <87 bug in case of strict CSP environments.
  // TODO(aaronshim): Remove once Chrome <87 bug is no longer a problem.
  try {
    isChrome87 = eval(goog.global.trustedTypes.emptyScript) !==
        goog.global.trustedTypes.emptyScript;
  } catch (err) {
  }

  /**
   * Trusted Types for running dev servers.
   *
   * @private @const
   */
  goog.CLOSURE_EVAL_PREFILTER_ =
      // Detect Chrome <87 bug with TT and eval.
      goog.global.trustedTypes && isChrome87 &&
          goog.createTrustedTypesPolicy('goog#base#devonly#eval') ||
      {createScript: goog.identity_};
}

//third_party/javascript/lodash/lodash.4.min.js
/**
 * @license
 * Lodash lodash.com/license | Underscore.js 1.8.3 underscorejs.org/LICENSE
 */
;
(/** @suppress {checkTypes|suspiciousCode|uselessCode|globalThis|checkVars} */
function(){function n(n,t,r){switch(r.length){case 0:return n.call(t);case 1:return n.call(t,r[0]);case 2:return n.call(t,r[0],r[1]);case 3:return n.call(t,r[0],r[1],r[2])}return n.apply(t,r)}function t(n,t,r,e){for(var u=-1,i=null==n?0:n.length;++u<i;){var o=n[u];t(e,o,r(o),n)}return e}function r(n,t){for(var r=-1,e=null==n?0:n.length;++r<e&&false!==t(n[r],r,n););return n}function e(n,t){for(var r=null==n?0:n.length;r--&&false!==t(n[r],r,n););return n}function u(n,t){for(var r=-1,e=null==n?0:n.length;++r<e;)if(!t(n[r],r,n))return false;
return true}function i(n,t){for(var r=-1,e=null==n?0:n.length,u=0,i=[];++r<e;){var o=n[r];t(o,r,n)&&(i[u++]=o)}return i}function o(n,t){return!(null==n||!n.length)&&-1<v(n,t,0)}function f(n,t,r){for(var e=-1,u=null==n?0:n.length;++e<u;)if(r(t,n[e]))return true;return false}function c(n,t){for(var r=-1,e=null==n?0:n.length,u=Array(e);++r<e;)u[r]=t(n[r],r,n);return u}function a(n,t){for(var r=-1,e=t.length,u=n.length;++r<e;)n[u+r]=t[r];return n}function l(n,t,r,e){var u=-1,i=null==n?0:n.length;for(e&&i&&(r=n[++u]);++u<i;)r=t(r,n[u],u,n);
return r}function s(n,t,r,e){var u=null==n?0:n.length;for(e&&u&&(r=n[--u]);u--;)r=t(r,n[u],u,n);return r}function h(n,t){for(var r=-1,e=null==n?0:n.length;++r<e;)if(t(n[r],r,n))return true;return false}function p(n,t,r){var e;return r(n,function(n,r,u){if(t(n,r,u))return e=r,false}),e}function _(n,t,r,e){var u=n.length;for(r+=e?1:-1;e?r--:++r<u;)if(t(n[r],r,n))return r;return-1}function v(n,t,r){if(t===t)n:{--r;for(var e=n.length;++r<e;)if(n[r]===t){n=r;break n}n=-1}else n=_(n,d,r);return n}function g(n,t,r,e){
--r;for(var u=n.length;++r<u;)if(e(n[r],t))return r;return-1}function d(n){return n!==n}function y(n,t){var r=null==n?0:n.length;return r?m(n,t)/r:F}function b(n){return function(t){return null==t?T:t[n]}}function x(n){return function(t){return null==n?T:n[t]}}function j(n,t,r,e,u){return u(n,function(n,u,i){r=e?(e=false,n):t(r,n,u,i)}),r}function w(n,t){var r=n.length;for(n.sort(t);r--;)n[r]=n[r].c;return n}function m(n,t){for(var r,e=-1,u=n.length;++e<u;){var i=t(n[e]);i!==T&&(r=r===T?i:r+i)}return r;
}function A(n,t){for(var r=-1,e=Array(n);++r<n;)e[r]=t(r);return e}function E(n,t){return c(t,function(t){return[t,n[t]]})}function k(n){return function(t){return n(t)}}function S(n,t){return c(t,function(t){return n[t]})}function O(n,t){return n.has(t)}function I(n,t){for(var r=-1,e=n.length;++r<e&&-1<v(t,n[r],0););return r}function R(n,t){for(var r=n.length;r--&&-1<v(t,n[r],0););return r}function z(n){return"\\"+Un[n]}function W(n){var t=-1,r=Array(n.size);return n.forEach(function(n,e){r[++t]=[e,n];
}),r}function B(n,t){return function(r){return n(t(r))}}function L(n,t){for(var r=-1,e=n.length,u=0,i=[];++r<e;){var o=n[r];o!==t&&"__lodash_placeholder__"!==o||(n[r]="__lodash_placeholder__",i[u++]=r)}return i}function U(n){var t=-1,r=Array(n.size);return n.forEach(function(n){r[++t]=n}),r}function C(n){var t=-1,r=Array(n.size);return n.forEach(function(n){r[++t]=[n,n]}),r}function D(n){if(Rn.test(n)){for(var t=On.lastIndex=0;On.test(n);)++t;n=t}else n=Qn(n);return n}function M(n){return Rn.test(n)?n.match(On)||[]:n.split("");
}var T,$=1/0,F=NaN,N=[["ary",128],["bind",1],["bindKey",2],["curry",8],["curryRight",16],["flip",512],["partial",32],["partialRight",64],["rearg",256]],P=/\b__p\+='';/g,Z=/\b(__p\+=)''\+/g,q=/(__e\(.*?\)|\b__t\))\+'';/g,V=/&(?:amp|lt|gt|quot|#39);/g,K=/[&<>"']/g,G=RegExp(V.source),H=RegExp(K.source),J=/<%-([\s\S]+?)%>/g,Y=/<%([\s\S]+?)%>/g,Q=/<%=([\s\S]+?)%>/g,X=/\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/,nn=/^\w*$/,tn=/[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g,rn=/[\\^$.*+?()[\]{}|]/g,en=RegExp(rn.source),un=/^\s+|\s+$/g,on=/^\s+/,fn=/\s+$/,cn=/\{(?:\n\/\* \[wrapped with .+\] \*\/)?\n?/,an=/\{\n\/\* \[wrapped with (.+)\] \*/,ln=/,? & /,sn=/[^\x00-\x2f\x3a-\x40\x5b-\x60\x7b-\x7f]+/g,hn=/\\(\\)?/g,pn=/\$\{([^\\}]*(?:\\.[^\\}]*)*)\}/g,_n=/\w*$/,vn=/^[-+]0x[0-9a-f]+$/i,gn=/^0b[01]+$/i,dn=/^\[object .+?Constructor\]$/,yn=/^0o[0-7]+$/i,bn=/^(?:0|[1-9]\d*)$/,xn=/[\xc0-\xd6\xd8-\xf6\xf8-\xff\u0100-\u017f]/g,jn=/($^)/,wn=/['\n\r\u2028\u2029\\]/g,mn="[\\ufe0e\\ufe0f]?(?:[\\u0300-\\u036f\\ufe20-\\ufe2f\\u20d0-\\u20ff]|\\ud83c[\\udffb-\\udfff])?(?:\\u200d(?:[^\\ud800-\\udfff]|(?:\\ud83c[\\udde6-\\uddff]){2}|[\\ud800-\\udbff][\\udc00-\\udfff])[\\ufe0e\\ufe0f]?(?:[\\u0300-\\u036f\\ufe20-\\ufe2f\\u20d0-\\u20ff]|\\ud83c[\\udffb-\\udfff])?)*",An="(?:[\\u2700-\\u27bf]|(?:\\ud83c[\\udde6-\\uddff]){2}|[\\ud800-\\udbff][\\udc00-\\udfff])"+mn,En="(?:[^\\ud800-\\udfff][\\u0300-\\u036f\\ufe20-\\ufe2f\\u20d0-\\u20ff]?|[\\u0300-\\u036f\\ufe20-\\ufe2f\\u20d0-\\u20ff]|(?:\\ud83c[\\udde6-\\uddff]){2}|[\\ud800-\\udbff][\\udc00-\\udfff]|[\\ud800-\\udfff])",kn=RegExp("['\u2019]","g"),Sn=RegExp("[\\u0300-\\u036f\\ufe20-\\ufe2f\\u20d0-\\u20ff]","g"),On=RegExp("\\ud83c[\\udffb-\\udfff](?=\\ud83c[\\udffb-\\udfff])|"+En+mn,"g"),In=RegExp(["[A-Z\\xc0-\\xd6\\xd8-\\xde]?[a-z\\xdf-\\xf6\\xf8-\\xff]+(?:['\u2019](?:d|ll|m|re|s|t|ve))?(?=[\\xac\\xb1\\xd7\\xf7\\x00-\\x2f\\x3a-\\x40\\x5b-\\x60\\x7b-\\xbf\\u2000-\\u206f \\t\\x0b\\f\\xa0\\ufeff\\n\\r\\u2028\\u2029\\u1680\\u180e\\u2000\\u2001\\u2002\\u2003\\u2004\\u2005\\u2006\\u2007\\u2008\\u2009\\u200a\\u202f\\u205f\\u3000]|[A-Z\\xc0-\\xd6\\xd8-\\xde]|$)|(?:[A-Z\\xc0-\\xd6\\xd8-\\xde]|[^\\ud800-\\udfff\\xac\\xb1\\xd7\\xf7\\x00-\\x2f\\x3a-\\x40\\x5b-\\x60\\x7b-\\xbf\\u2000-\\u206f \\t\\x0b\\f\\xa0\\ufeff\\n\\r\\u2028\\u2029\\u1680\\u180e\\u2000\\u2001\\u2002\\u2003\\u2004\\u2005\\u2006\\u2007\\u2008\\u2009\\u200a\\u202f\\u205f\\u3000\\d+\\u2700-\\u27bfa-z\\xdf-\\xf6\\xf8-\\xffA-Z\\xc0-\\xd6\\xd8-\\xde])+(?:['\u2019](?:D|LL|M|RE|S|T|VE))?(?=[\\xac\\xb1\\xd7\\xf7\\x00-\\x2f\\x3a-\\x40\\x5b-\\x60\\x7b-\\xbf\\u2000-\\u206f \\t\\x0b\\f\\xa0\\ufeff\\n\\r\\u2028\\u2029\\u1680\\u180e\\u2000\\u2001\\u2002\\u2003\\u2004\\u2005\\u2006\\u2007\\u2008\\u2009\\u200a\\u202f\\u205f\\u3000]|[A-Z\\xc0-\\xd6\\xd8-\\xde](?:[a-z\\xdf-\\xf6\\xf8-\\xff]|[^\\ud800-\\udfff\\xac\\xb1\\xd7\\xf7\\x00-\\x2f\\x3a-\\x40\\x5b-\\x60\\x7b-\\xbf\\u2000-\\u206f \\t\\x0b\\f\\xa0\\ufeff\\n\\r\\u2028\\u2029\\u1680\\u180e\\u2000\\u2001\\u2002\\u2003\\u2004\\u2005\\u2006\\u2007\\u2008\\u2009\\u200a\\u202f\\u205f\\u3000\\d+\\u2700-\\u27bfa-z\\xdf-\\xf6\\xf8-\\xffA-Z\\xc0-\\xd6\\xd8-\\xde])|$)|[A-Z\\xc0-\\xd6\\xd8-\\xde]?(?:[a-z\\xdf-\\xf6\\xf8-\\xff]|[^\\ud800-\\udfff\\xac\\xb1\\xd7\\xf7\\x00-\\x2f\\x3a-\\x40\\x5b-\\x60\\x7b-\\xbf\\u2000-\\u206f \\t\\x0b\\f\\xa0\\ufeff\\n\\r\\u2028\\u2029\\u1680\\u180e\\u2000\\u2001\\u2002\\u2003\\u2004\\u2005\\u2006\\u2007\\u2008\\u2009\\u200a\\u202f\\u205f\\u3000\\d+\\u2700-\\u27bfa-z\\xdf-\\xf6\\xf8-\\xffA-Z\\xc0-\\xd6\\xd8-\\xde])+(?:['\u2019](?:d|ll|m|re|s|t|ve))?|[A-Z\\xc0-\\xd6\\xd8-\\xde]+(?:['\u2019](?:D|LL|M|RE|S|T|VE))?|\\d*(?:1ST|2ND|3RD|(?![123])\\dTH)(?=\\b|[a-z_])|\\d*(?:1st|2nd|3rd|(?![123])\\dth)(?=\\b|[A-Z_])|\\d+",An].join("|"),"g"),Rn=RegExp("[\\u200d\\ud800-\\udfff\\u0300-\\u036f\\ufe20-\\ufe2f\\u20d0-\\u20ff\\ufe0e\\ufe0f]"),zn=/[a-z][A-Z]|[A-Z]{2}[a-z]|[0-9][a-zA-Z]|[a-zA-Z][0-9]|[^a-zA-Z0-9 ]/,Wn="Array Buffer DataView Date Error Float32Array Float64Array Function Int8Array Int16Array Int32Array Map Math Object Promise RegExp Set String Symbol TypeError Uint8Array Uint8ClampedArray Uint16Array Uint32Array WeakMap _ clearTimeout isFinite parseInt setTimeout".split(" "),Bn={};
Bn["[object Float32Array]"]=Bn["[object Float64Array]"]=Bn["[object Int8Array]"]=Bn["[object Int16Array]"]=Bn["[object Int32Array]"]=Bn["[object Uint8Array]"]=Bn["[object Uint8ClampedArray]"]=Bn["[object Uint16Array]"]=Bn["[object Uint32Array]"]=true,Bn["[object Arguments]"]=Bn["[object Array]"]=Bn["[object ArrayBuffer]"]=Bn["[object Boolean]"]=Bn["[object DataView]"]=Bn["[object Date]"]=Bn["[object Error]"]=Bn["[object Function]"]=Bn["[object Map]"]=Bn["[object Number]"]=Bn["[object Object]"]=Bn["[object RegExp]"]=Bn["[object Set]"]=Bn["[object String]"]=Bn["[object WeakMap]"]=false;
var Ln={};Ln["[object Arguments]"]=Ln["[object Array]"]=Ln["[object ArrayBuffer]"]=Ln["[object DataView]"]=Ln["[object Boolean]"]=Ln["[object Date]"]=Ln["[object Float32Array]"]=Ln["[object Float64Array]"]=Ln["[object Int8Array]"]=Ln["[object Int16Array]"]=Ln["[object Int32Array]"]=Ln["[object Map]"]=Ln["[object Number]"]=Ln["[object Object]"]=Ln["[object RegExp]"]=Ln["[object Set]"]=Ln["[object String]"]=Ln["[object Symbol]"]=Ln["[object Uint8Array]"]=Ln["[object Uint8ClampedArray]"]=Ln["[object Uint16Array]"]=Ln["[object Uint32Array]"]=true,
Ln["[object Error]"]=Ln["[object Function]"]=Ln["[object WeakMap]"]=false;var Un={"\\":"\\","'":"'","\n":"n","\r":"r","\u2028":"u2028","\u2029":"u2029"},Cn=parseFloat,Dn=parseInt,Mn=typeof global=="object"&&global&&global.Object===Object&&global,Tn=typeof self=="object"&&self&&self.Object===Object&&self,$n=Mn||Tn||Function("return this")(),Fn=typeof exports=="object"&&exports&&!exports.nodeType&&exports,Nn=Fn&&typeof module=="object"&&module&&!module.nodeType&&module,Pn=Nn&&Nn.exports===Fn,Zn=Pn&&Mn.process,qn=function(){
try{var n=Nn&&Nn.f&&Nn.f("util").types;return n?n:Zn&&Zn.binding&&Zn.binding("util")}catch(n){}}(),Vn=qn&&qn.isArrayBuffer,Kn=qn&&qn.isDate,Gn=qn&&qn.isMap,Hn=qn&&qn.isRegExp,Jn=qn&&qn.isSet,Yn=qn&&qn.isTypedArray,Qn=b("length"),Xn=x({"\xc0":"A","\xc1":"A","\xc2":"A","\xc3":"A","\xc4":"A","\xc5":"A","\xe0":"a","\xe1":"a","\xe2":"a","\xe3":"a","\xe4":"a","\xe5":"a","\xc7":"C","\xe7":"c","\xd0":"D","\xf0":"d","\xc8":"E","\xc9":"E","\xca":"E","\xcb":"E","\xe8":"e","\xe9":"e","\xea":"e","\xeb":"e","\xcc":"I",
"\xcd":"I","\xce":"I","\xcf":"I","\xec":"i","\xed":"i","\xee":"i","\xef":"i","\xd1":"N","\xf1":"n","\xd2":"O","\xd3":"O","\xd4":"O","\xd5":"O","\xd6":"O","\xd8":"O","\xf2":"o","\xf3":"o","\xf4":"o","\xf5":"o","\xf6":"o","\xf8":"o","\xd9":"U","\xda":"U","\xdb":"U","\xdc":"U","\xf9":"u","\xfa":"u","\xfb":"u","\xfc":"u","\xdd":"Y","\xfd":"y","\xff":"y","\xc6":"Ae","\xe6":"ae","\xde":"Th","\xfe":"th","\xdf":"ss","\u0100":"A","\u0102":"A","\u0104":"A","\u0101":"a","\u0103":"a","\u0105":"a","\u0106":"C",
"\u0108":"C","\u010a":"C","\u010c":"C","\u0107":"c","\u0109":"c","\u010b":"c","\u010d":"c","\u010e":"D","\u0110":"D","\u010f":"d","\u0111":"d","\u0112":"E","\u0114":"E","\u0116":"E","\u0118":"E","\u011a":"E","\u0113":"e","\u0115":"e","\u0117":"e","\u0119":"e","\u011b":"e","\u011c":"G","\u011e":"G","\u0120":"G","\u0122":"G","\u011d":"g","\u011f":"g","\u0121":"g","\u0123":"g","\u0124":"H","\u0126":"H","\u0125":"h","\u0127":"h","\u0128":"I","\u012a":"I","\u012c":"I","\u012e":"I","\u0130":"I","\u0129":"i",
"\u012b":"i","\u012d":"i","\u012f":"i","\u0131":"i","\u0134":"J","\u0135":"j","\u0136":"K","\u0137":"k","\u0138":"k","\u0139":"L","\u013b":"L","\u013d":"L","\u013f":"L","\u0141":"L","\u013a":"l","\u013c":"l","\u013e":"l","\u0140":"l","\u0142":"l","\u0143":"N","\u0145":"N","\u0147":"N","\u014a":"N","\u0144":"n","\u0146":"n","\u0148":"n","\u014b":"n","\u014c":"O","\u014e":"O","\u0150":"O","\u014d":"o","\u014f":"o","\u0151":"o","\u0154":"R","\u0156":"R","\u0158":"R","\u0155":"r","\u0157":"r","\u0159":"r",
"\u015a":"S","\u015c":"S","\u015e":"S","\u0160":"S","\u015b":"s","\u015d":"s","\u015f":"s","\u0161":"s","\u0162":"T","\u0164":"T","\u0166":"T","\u0163":"t","\u0165":"t","\u0167":"t","\u0168":"U","\u016a":"U","\u016c":"U","\u016e":"U","\u0170":"U","\u0172":"U","\u0169":"u","\u016b":"u","\u016d":"u","\u016f":"u","\u0171":"u","\u0173":"u","\u0174":"W","\u0175":"w","\u0176":"Y","\u0177":"y","\u0178":"Y","\u0179":"Z","\u017b":"Z","\u017d":"Z","\u017a":"z","\u017c":"z","\u017e":"z","\u0132":"IJ","\u0133":"ij",
"\u0152":"Oe","\u0153":"oe","\u0149":"'n","\u017f":"s"}),nt=x({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}),tt=x({"&amp;":"&","&lt;":"<","&gt;":">","&quot;":'"',"&#39;":"'"}),rt=function x(mn){function An(n){if(yu(n)&&!ff(n)&&!(n instanceof Un)){if(n instanceof On)return n;if(oi.call(n,"__wrapped__"))return Fe(n)}return new On(n)}function En(){}function On(n,t){this.__wrapped__=n,this.__actions__=[],this.__chain__=!!t,this.__index__=0,this.__values__=T}function Un(n){this.__wrapped__=n,
this.__actions__=[],this.__dir__=1,this.__filtered__=false,this.__iteratees__=[],this.__takeCount__=4294967295,this.__views__=[]}function Mn(n){var t=-1,r=null==n?0:n.length;for(this.clear();++t<r;){var e=n[t];this.set(e[0],e[1])}}function Tn(n){var t=-1,r=null==n?0:n.length;for(this.clear();++t<r;){var e=n[t];this.set(e[0],e[1])}}function Fn(n){var t=-1,r=null==n?0:n.length;for(this.clear();++t<r;){var e=n[t];this.set(e[0],e[1])}}function Nn(n){var t=-1,r=null==n?0:n.length;for(this.__data__=new Fn;++t<r;)this.add(n[t]);
}function Zn(n){this.size=(this.__data__=new Tn(n)).size}function qn(n,t){var r,e=ff(n),u=!e&&of(n),i=!e&&!u&&af(n),o=!e&&!u&&!i&&_f(n),u=(e=e||u||i||o)?A(n.length,ni):[],f=u.length;for(r in n)!t&&!oi.call(n,r)||e&&("length"==r||i&&("offset"==r||"parent"==r)||o&&("buffer"==r||"byteLength"==r||"byteOffset"==r)||Se(r,f))||u.push(r);return u}function Qn(n){var t=n.length;return t?n[ir(0,t-1)]:T}function et(n,t){return De(Ur(n),pt(t,0,n.length))}function ut(n){return De(Ur(n))}function it(n,t,r){(r===T||lu(n[t],r))&&(r!==T||t in n)||st(n,t,r);
}function ot(n,t,r){var e=n[t];oi.call(n,t)&&lu(e,r)&&(r!==T||t in n)||st(n,t,r)}function ft(n,t){for(var r=n.length;r--;)if(lu(n[r][0],t))return r;return-1}function ct(n,t,r,e){return uo(n,function(n,u,i){t(e,n,r(n),i)}),e}function at(n,t){return n&&Cr(t,Wu(t),n)}function lt(n,t){return n&&Cr(t,Bu(t),n)}function st(n,t,r){"__proto__"==t&&Ai?Ai(n,t,{configurable:true,enumerable:true,value:r,writable:true}):n[t]=r}function ht(n,t){for(var r=-1,e=t.length,u=Ku(e),i=null==n;++r<e;)u[r]=i?T:Ru(n,t[r]);return u;
}function pt(n,t,r){return n===n&&(r!==T&&(n=n<=r?n:r),t!==T&&(n=n>=t?n:t)),n}function _t(n,t,e,u,i,o){var f,c=1&t,a=2&t,l=4&t;if(e&&(f=i?e(n,u,i,o):e(n)),f!==T)return f;if(!du(n))return n;if(u=ff(n)){if(f=me(n),!c)return Ur(n,f)}else{var s=vo(n),h="[object Function]"==s||"[object GeneratorFunction]"==s;if(af(n))return Ir(n,c);if("[object Object]"==s||"[object Arguments]"==s||h&&!i){if(f=a||h?{}:Ae(n),!c)return a?Mr(n,lt(f,n)):Dr(n,at(f,n))}else{if(!Ln[s])return i?n:{};f=Ee(n,s,c)}}if(o||(o=new Zn),
i=o.get(n))return i;o.set(n,f),pf(n)?n.forEach(function(r){f.add(_t(r,t,e,r,n,o))}):sf(n)&&n.forEach(function(r,u){f.set(u,_t(r,t,e,u,n,o))});var a=l?a?ve:_e:a?Bu:Wu,p=u?T:a(n);return r(p||n,function(r,u){p&&(u=r,r=n[u]),ot(f,u,_t(r,t,e,u,n,o))}),f}function vt(n){var t=Wu(n);return function(r){return gt(r,n,t)}}function gt(n,t,r){var e=r.length;if(null==n)return!e;for(n=Qu(n);e--;){var u=r[e],i=t[u],o=n[u];if(o===T&&!(u in n)||!i(o))return false}return true}function dt(n,t,r){if(typeof n!="function")throw new ti("Expected a function");
return bo(function(){n.apply(T,r)},t)}function yt(n,t,r,e){var u=-1,i=o,a=true,l=n.length,s=[],h=t.length;if(!l)return s;r&&(t=c(t,k(r))),e?(i=f,a=false):200<=t.length&&(i=O,a=false,t=new Nn(t));n:for(;++u<l;){var p=n[u],_=null==r?p:r(p),p=e||0!==p?p:0;if(a&&_===_){for(var v=h;v--;)if(t[v]===_)continue n;s.push(p)}else i(t,_,e)||s.push(p)}return s}function bt(n,t){var r=true;return uo(n,function(n,e,u){return r=!!t(n,e,u)}),r}function xt(n,t,r){for(var e=-1,u=n.length;++e<u;){var i=n[e],o=t(i);if(null!=o&&(f===T?o===o&&!wu(o):r(o,f)))var f=o,c=i;
}return c}function jt(n,t){var r=[];return uo(n,function(n,e,u){t(n,e,u)&&r.push(n)}),r}function wt(n,t,r,e,u){var i=-1,o=n.length;for(r||(r=ke),u||(u=[]);++i<o;){var f=n[i];0<t&&r(f)?1<t?wt(f,t-1,r,e,u):a(u,f):e||(u[u.length]=f)}return u}function mt(n,t){return n&&oo(n,t,Wu)}function At(n,t){return n&&fo(n,t,Wu)}function Et(n,t){return i(t,function(t){return _u(n[t])})}function kt(n,t){t=Sr(t,n);for(var r=0,e=t.length;null!=n&&r<e;)n=n[Me(t[r++])];return r&&r==e?n:T}function St(n,t,r){return t=t(n),
ff(n)?t:a(t,r(n))}function Ot(n){if(null==n)n=n===T?"[object Undefined]":"[object Null]";else if(mi&&mi in Qu(n)){var t=oi.call(n,mi),r=n[mi];try{n[mi]=T;var e=true}catch(n){}var u=ai.call(n);e&&(t?n[mi]=r:delete n[mi]),n=u}else n=ai.call(n);return n}function It(n,t){return n>t}function Rt(n,t){return null!=n&&oi.call(n,t)}function zt(n,t){return null!=n&&t in Qu(n)}function Wt(n,t,r){for(var e=r?f:o,u=n[0].length,i=n.length,a=i,l=Ku(i),s=1/0,h=[];a--;){var p=n[a];a&&t&&(p=c(p,k(t))),s=Ci(p.length,s),
l[a]=!r&&(t||120<=u&&120<=p.length)?new Nn(a&&p):T}var p=n[0],_=-1,v=l[0];n:for(;++_<u&&h.length<s;){var g=p[_],d=t?t(g):g,g=r||0!==g?g:0;if(v?!O(v,d):!e(h,d,r)){for(a=i;--a;){var y=l[a];if(y?!O(y,d):!e(n[a],d,r))continue n}v&&v.push(d),h.push(g)}}return h}function Bt(n,t,r){var e={};return mt(n,function(n,u,i){t(e,r(n),u,i)}),e}function Lt(t,r,e){return r=Sr(r,t),t=2>r.length?t:kt(t,hr(r,0,-1)),r=null==t?t:t[Me(Ve(r))],null==r?T:n(r,t,e)}function Ut(n){return yu(n)&&"[object Arguments]"==Ot(n)}function Ct(n){
return yu(n)&&"[object ArrayBuffer]"==Ot(n)}function Dt(n){return yu(n)&&"[object Date]"==Ot(n)}function Mt(n,t,r,e,u){if(n===t)t=true;else if(null==n||null==t||!yu(n)&&!yu(t))t=n!==n&&t!==t;else n:{var i=ff(n),o=ff(t),f=i?"[object Array]":vo(n),c=o?"[object Array]":vo(t),f="[object Arguments]"==f?"[object Object]":f,c="[object Arguments]"==c?"[object Object]":c,a="[object Object]"==f,o="[object Object]"==c;if((c=f==c)&&af(n)){if(!af(t)){t=false;break n}i=true,a=false}if(c&&!a)u||(u=new Zn),t=i||_f(n)?se(n,t,r,e,Mt,u):he(n,t,f,r,e,Mt,u);else{
if(!(1&r)&&(i=a&&oi.call(n,"__wrapped__"),f=o&&oi.call(t,"__wrapped__"),i||f)){n=i?n.value():n,t=f?t.value():t,u||(u=new Zn),t=Mt(n,t,r,e,u);break n}if(c)t:if(u||(u=new Zn),i=1&r,f=_e(n),o=f.length,c=_e(t).length,o==c||i){for(a=o;a--;){var l=f[a];if(!(i?l in t:oi.call(t,l))){t=false;break t}}if((c=u.get(n))&&u.get(t))t=c==t;else{c=true,u.set(n,t),u.set(t,n);for(var s=i;++a<o;){var l=f[a],h=n[l],p=t[l];if(e)var _=i?e(p,h,l,t,n,u):e(h,p,l,n,t,u);if(_===T?h!==p&&!Mt(h,p,r,e,u):!_){c=false;break}s||(s="constructor"==l);
}c&&!s&&(r=n.constructor,e=t.constructor,r!=e&&"constructor"in n&&"constructor"in t&&!(typeof r=="function"&&r instanceof r&&typeof e=="function"&&e instanceof e)&&(c=false)),u.delete(n),u.delete(t),t=c}}else t=false;else t=false}}return t}function Tt(n){return yu(n)&&"[object Map]"==vo(n)}function $t(n,t,r,e){var u=r.length,i=u,o=!e;if(null==n)return!i;for(n=Qu(n);u--;){var f=r[u];if(o&&f[2]?f[1]!==n[f[0]]:!(f[0]in n))return false}for(;++u<i;){var f=r[u],c=f[0],a=n[c],l=f[1];if(o&&f[2]){if(a===T&&!(c in n))return false;
}else{if(f=new Zn,e)var s=e(a,l,c,n,t,f);if(s===T?!Mt(l,a,3,e,f):!s)return false}}return true}function Ft(n){return!(!du(n)||ci&&ci in n)&&(_u(n)?hi:dn).test(Te(n))}function Nt(n){return yu(n)&&"[object RegExp]"==Ot(n)}function Pt(n){return yu(n)&&"[object Set]"==vo(n)}function Zt(n){return yu(n)&&gu(n.length)&&!!Bn[Ot(n)]}function qt(n){return typeof n=="function"?n:null==n?$u:typeof n=="object"?ff(n)?Jt(n[0],n[1]):Ht(n):Zu(n)}function Vt(n){if(!ze(n))return Li(n);var t,r=[];for(t in Qu(n))oi.call(n,t)&&"constructor"!=t&&r.push(t);
return r}function Kt(n,t){return n<t}function Gt(n,t){var r=-1,e=su(n)?Ku(n.length):[];return uo(n,function(n,u,i){e[++r]=t(n,u,i)}),e}function Ht(n){var t=xe(n);return 1==t.length&&t[0][2]?We(t[0][0],t[0][1]):function(r){return r===n||$t(r,n,t)}}function Jt(n,t){return Ie(n)&&t===t&&!du(t)?We(Me(n),t):function(r){var e=Ru(r,n);return e===T&&e===t?zu(r,n):Mt(t,e,3)}}function Yt(n,t,r,e,u){n!==t&&oo(t,function(i,o){if(u||(u=new Zn),du(i)){var f=u,c=Le(n,o),a=Le(t,o),l=f.get(a);if(l)it(n,o,l);else{
var l=e?e(c,a,o+"",n,t,f):T,s=l===T;if(s){var h=ff(a),p=!h&&af(a),_=!h&&!p&&_f(a),l=a;h||p||_?ff(c)?l=c:hu(c)?l=Ur(c):p?(s=false,l=Ir(a,true)):_?(s=false,l=zr(a,true)):l=[]:xu(a)||of(a)?(l=c,of(c)?l=Ou(c):du(c)&&!_u(c)||(l=Ae(a))):s=false}s&&(f.set(a,l),Yt(l,a,r,e,f),f.delete(a)),it(n,o,l)}}else f=e?e(Le(n,o),i,o+"",n,t,u):T,f===T&&(f=i),it(n,o,f)},Bu)}function Qt(n,t){var r=n.length;if(r)return t+=0>t?r:0,Se(t,r)?n[t]:T}function Xt(n,t,r){var e=-1;return t=c(t.length?t:[$u],k(ye())),n=Gt(n,function(n){return{
a:c(t,function(t){return t(n)}),b:++e,c:n}}),w(n,function(n,t){var e;n:{e=-1;for(var u=n.a,i=t.a,o=u.length,f=r.length;++e<o;){var c=Wr(u[e],i[e]);if(c){e=e>=f?c:c*("desc"==r[e]?-1:1);break n}}e=n.b-t.b}return e})}function nr(n,t){return tr(n,t,function(t,r){return zu(n,r)})}function tr(n,t,r){for(var e=-1,u=t.length,i={};++e<u;){var o=t[e],f=kt(n,o);r(f,o)&&lr(i,Sr(o,n),f)}return i}function rr(n){return function(t){return kt(t,n)}}function er(n,t,r,e){var u=e?g:v,i=-1,o=t.length,f=n;for(n===t&&(t=Ur(t)),
r&&(f=c(n,k(r)));++i<o;)for(var a=0,l=t[i],l=r?r(l):l;-1<(a=u(f,l,a,e));)f!==n&&xi.call(f,a,1),xi.call(n,a,1);return n}function ur(n,t){for(var r=n?t.length:0,e=r-1;r--;){var u=t[r];if(r==e||u!==i){var i=u;Se(u)?xi.call(n,u,1):xr(n,u)}}}function ir(n,t){return n+Ii(Ti()*(t-n+1))}function or(n,t){var r="";if(!n||1>t||9007199254740991<t)return r;do t%2&&(r+=n),(t=Ii(t/2))&&(n+=n);while(t);return r}function fr(n,t){return xo(Be(n,t,$u),n+"")}function cr(n){return Qn(Uu(n))}function ar(n,t){var r=Uu(n);
return De(r,pt(t,0,r.length))}function lr(n,t,r,e){if(!du(n))return n;t=Sr(t,n);for(var u=-1,i=t.length,o=i-1,f=n;null!=f&&++u<i;){var c=Me(t[u]),a=r;if(u!=o){var l=f[c],a=e?e(l,c,f):T;a===T&&(a=du(l)?l:Se(t[u+1])?[]:{})}ot(f,c,a),f=f[c]}return n}function sr(n){return De(Uu(n))}function hr(n,t,r){var e=-1,u=n.length;for(0>t&&(t=-t>u?0:u+t),r=r>u?u:r,0>r&&(r+=u),u=t>r?0:r-t>>>0,t>>>=0,r=Ku(u);++e<u;)r[e]=n[e+t];return r}function pr(n,t){var r;return uo(n,function(n,e,u){return r=t(n,e,u),!r}),!!r}
function _r(n,t,r){var e=0,u=null==n?e:n.length;if(typeof t=="number"&&t===t&&2147483647>=u){for(;e<u;){var i=e+u>>>1,o=n[i];null!==o&&!wu(o)&&(r?o<=t:o<t)?e=i+1:u=i}return u}return vr(n,t,$u,r)}function vr(n,t,r,e){t=r(t);for(var u=0,i=null==n?0:n.length,o=t!==t,f=null===t,c=wu(t),a=t===T;u<i;){var l=Ii((u+i)/2),s=r(n[l]),h=s!==T,p=null===s,_=s===s,v=wu(s);(o?e||_:a?_&&(e||h):f?_&&h&&(e||!p):c?_&&h&&!p&&(e||!v):p||v?0:e?s<=t:s<t)?u=l+1:i=l}return Ci(i,4294967294)}function gr(n,t){for(var r=-1,e=n.length,u=0,i=[];++r<e;){
var o=n[r],f=t?t(o):o;if(!r||!lu(f,c)){var c=f;i[u++]=0===o?0:o}}return i}function dr(n){return typeof n=="number"?n:wu(n)?F:+n}function yr(n){if(typeof n=="string")return n;if(ff(n))return c(n,yr)+"";if(wu(n))return ro?ro.call(n):"";var t=n+"";return"0"==t&&1/n==-$?"-0":t}function br(n,t,r){var e=-1,u=o,i=n.length,c=true,a=[],l=a;if(r)c=false,u=f;else if(200<=i){if(u=t?null:so(n))return U(u);c=false,u=O,l=new Nn}else l=t?[]:a;n:for(;++e<i;){var s=n[e],h=t?t(s):s,s=r||0!==s?s:0;if(c&&h===h){for(var p=l.length;p--;)if(l[p]===h)continue n;
t&&l.push(h),a.push(s)}else u(l,h,r)||(l!==a&&l.push(h),a.push(s))}return a}function xr(n,t){return t=Sr(t,n),n=2>t.length?n:kt(n,hr(t,0,-1)),null==n||delete n[Me(Ve(t))]}function jr(n,t,r,e){for(var u=n.length,i=e?u:-1;(e?i--:++i<u)&&t(n[i],i,n););return r?hr(n,e?0:i,e?i+1:u):hr(n,e?i+1:0,e?u:i)}function wr(n,t){var r=n;return r instanceof Un&&(r=r.value()),l(t,function(n,t){return t.func.apply(t.thisArg,a([n],t.args))},r)}function mr(n,t,r){var e=n.length;if(2>e)return e?br(n[0]):[];for(var u=-1,i=Ku(e);++u<e;)for(var o=n[u],f=-1;++f<e;)f!=u&&(i[u]=yt(i[u]||o,n[f],t,r));
return br(wt(i,1),t,r)}function Ar(n,t,r){for(var e=-1,u=n.length,i=t.length,o={};++e<u;)r(o,n[e],e<i?t[e]:T);return o}function Er(n){return hu(n)?n:[]}function kr(n){return typeof n=="function"?n:$u}function Sr(n,t){return ff(n)?n:Ie(n,t)?[n]:jo(Iu(n))}function Or(n,t,r){var e=n.length;return r=r===T?e:r,!t&&r>=e?n:hr(n,t,r)}function Ir(n,t){if(t)return n.slice();var r=n.length,r=gi?gi(r):new n.constructor(r);return n.copy(r),r}function Rr(n){var t=new n.constructor(n.byteLength);return new vi(t).set(new vi(n)),
t}function zr(n,t){return new n.constructor(t?Rr(n.buffer):n.buffer,n.byteOffset,n.length)}function Wr(n,t){if(n!==t){var r=n!==T,e=null===n,u=n===n,i=wu(n),o=t!==T,f=null===t,c=t===t,a=wu(t);if(!f&&!a&&!i&&n>t||i&&o&&c&&!f&&!a||e&&o&&c||!r&&c||!u)return 1;if(!e&&!i&&!a&&n<t||a&&r&&u&&!e&&!i||f&&r&&u||!o&&u||!c)return-1}return 0}function Br(n,t,r,e){var u=-1,i=n.length,o=r.length,f=-1,c=t.length,a=Ui(i-o,0),l=Ku(c+a);for(e=!e;++f<c;)l[f]=t[f];for(;++u<o;)(e||u<i)&&(l[r[u]]=n[u]);for(;a--;)l[f++]=n[u++];
return l}function Lr(n,t,r,e){var u=-1,i=n.length,o=-1,f=r.length,c=-1,a=t.length,l=Ui(i-f,0),s=Ku(l+a);for(e=!e;++u<l;)s[u]=n[u];for(l=u;++c<a;)s[l+c]=t[c];for(;++o<f;)(e||u<i)&&(s[l+r[o]]=n[u++]);return s}function Ur(n,t){var r=-1,e=n.length;for(t||(t=Ku(e));++r<e;)t[r]=n[r];return t}function Cr(n,t,r,e){var u=!r;r||(r={});for(var i=-1,o=t.length;++i<o;){var f=t[i],c=e?e(r[f],n[f],f,r,n):T;c===T&&(c=n[f]),u?st(r,f,c):ot(r,f,c)}return r}function Dr(n,t){return Cr(n,po(n),t)}function Mr(n,t){return Cr(n,_o(n),t);
}function Tr(n,r){return function(e,u){var i=ff(e)?t:ct,o=r?r():{};return i(e,n,ye(u,2),o)}}function $r(n){return fr(function(t,r){var e=-1,u=r.length,i=1<u?r[u-1]:T,o=2<u?r[2]:T,i=3<n.length&&typeof i=="function"?(u--,i):T;for(o&&Oe(r[0],r[1],o)&&(i=3>u?T:i,u=1),t=Qu(t);++e<u;)(o=r[e])&&n(t,o,e,i);return t})}function Fr(n,t){return function(r,e){if(null==r)return r;if(!su(r))return n(r,e);for(var u=r.length,i=t?u:-1,o=Qu(r);(t?i--:++i<u)&&false!==e(o[i],i,o););return r}}function Nr(n){return function(t,r,e){
var u=-1,i=Qu(t);e=e(t);for(var o=e.length;o--;){var f=e[n?o:++u];if(false===r(i[f],f,i))break}return t}}function Pr(n,t,r){function e(){return(this&&this!==$n&&this instanceof e?i:n).apply(u?r:this,arguments)}var u=1&t,i=Vr(n);return e}function Zr(n){return function(t){t=Iu(t);var r=Rn.test(t)?M(t):T,e=r?r[0]:t.charAt(0);return t=r?Or(r,1).join(""):t.slice(1),e[n]()+t}}function qr(n){return function(t){return l(Mu(Du(t).replace(kn,"")),n,"")}}function Vr(n){return function(){var t=arguments;switch(t.length){
case 0:return new n;case 1:return new n(t[0]);case 2:return new n(t[0],t[1]);case 3:return new n(t[0],t[1],t[2]);case 4:return new n(t[0],t[1],t[2],t[3]);case 5:return new n(t[0],t[1],t[2],t[3],t[4]);case 6:return new n(t[0],t[1],t[2],t[3],t[4],t[5]);case 7:return new n(t[0],t[1],t[2],t[3],t[4],t[5],t[6])}var r=eo(n.prototype),t=n.apply(r,t);return du(t)?t:r}}function Kr(t,r,e){function u(){for(var o=arguments.length,f=Ku(o),c=o,a=de(u);c--;)f[c]=arguments[c];return c=3>o&&f[0]!==a&&f[o-1]!==a?[]:L(f,a),
o-=c.length,o<e?ue(t,r,Jr,u.placeholder,T,f,c,T,T,e-o):n(this&&this!==$n&&this instanceof u?i:t,this,f)}var i=Vr(t);return u}function Gr(n){return function(t,r,e){var u=Qu(t);if(!su(t)){var i=ye(r,3);t=Wu(t),r=function(n){return i(u[n],n,u)}}return r=n(t,r,e),-1<r?u[i?t[r]:r]:T}}function Hr(n){return pe(function(t){var r=t.length,e=r,u=On.prototype.thru;for(n&&t.reverse();e--;){var i=t[e];if(typeof i!="function")throw new ti("Expected a function");if(u&&!o&&"wrapper"==ge(i))var o=new On([],true)}for(e=o?e:r;++e<r;)var i=t[e],u=ge(i),f="wrapper"==u?ho(i):T,o=f&&Re(f[0])&&424==f[1]&&!f[4].length&&1==f[9]?o[ge(f[0])].apply(o,f[3]):1==i.length&&Re(i)?o[u]():o.thru(i);
return function(){var n=arguments,e=n[0];if(o&&1==n.length&&ff(e))return o.plant(e).value();for(var u=0,n=r?t[u].apply(this,n):e;++u<r;)n=t[u].call(this,n);return n}})}function Jr(n,t,r,e,u,i,o,f,c,a){function l(){for(var d=arguments.length,y=Ku(d),b=d;b--;)y[b]=arguments[b];if(_){var x,j=de(l),b=y.length;for(x=0;b--;)y[b]===j&&++x}if(e&&(y=Br(y,e,u,_)),i&&(y=Lr(y,i,o,_)),d-=x,_&&d<a)return j=L(y,j),ue(n,t,Jr,l.placeholder,r,y,j,f,c,a-d);if(j=h?r:this,b=p?j[n]:n,d=y.length,f){x=y.length;for(var w=Ci(f.length,x),m=Ur(y);w--;){
var A=f[w];y[w]=Se(A,x)?m[A]:T}}else v&&1<d&&y.reverse();return s&&c<d&&(y.length=c),this&&this!==$n&&this instanceof l&&(b=g||Vr(b)),b.apply(j,y)}var s=128&t,h=1&t,p=2&t,_=24&t,v=512&t,g=p?T:Vr(n);return l}function Yr(n,t){return function(r,e){return Bt(r,n,t(e))}}function Qr(n,t){return function(r,e){var u;if(r===T&&e===T)return t;if(r!==T&&(u=r),e!==T){if(u===T)return e;typeof r=="string"||typeof e=="string"?(r=yr(r),e=yr(e)):(r=dr(r),e=dr(e)),u=n(r,e)}return u}}function Xr(t){return pe(function(r){
return r=c(r,k(ye())),fr(function(e){var u=this;return t(r,function(t){return n(t,u,e)})})})}function ne(n,t){t=t===T?" ":yr(t);var r=t.length;return 2>r?r?or(t,n):t:(r=or(t,Oi(n/D(t))),Rn.test(t)?Or(M(r),0,n).join(""):r.slice(0,n))}function te(t,r,e,u){function i(){for(var r=-1,c=arguments.length,a=-1,l=u.length,s=Ku(l+c),h=this&&this!==$n&&this instanceof i?f:t;++a<l;)s[a]=u[a];for(;c--;)s[a++]=arguments[++r];return n(h,o?e:this,s)}var o=1&r,f=Vr(t);return i}function re(n){return function(t,r,e){
e&&typeof e!="number"&&Oe(t,r,e)&&(r=e=T),t=Au(t),r===T?(r=t,t=0):r=Au(r),e=e===T?t<r?1:-1:Au(e);var u=-1;r=Ui(Oi((r-t)/(e||1)),0);for(var i=Ku(r);r--;)i[n?r:++u]=t,t+=e;return i}}function ee(n){return function(t,r){return typeof t=="string"&&typeof r=="string"||(t=Su(t),r=Su(r)),n(t,r)}}function ue(n,t,r,e,u,i,o,f,c,a){var l=8&t,s=l?o:T;o=l?T:o;var h=l?i:T;return i=l?T:i,t=(t|(l?32:64))&~(l?64:32),4&t||(t&=-4),u=[n,t,u,h,s,i,o,f,c,a],r=r.apply(T,u),Re(n)&&yo(r,u),r.placeholder=e,Ue(r,n,t)}function ie(n){
var t=Yu[n];return function(n,r){if(n=Su(n),(r=null==r?0:Ci(Eu(r),292))&&Wi(n)){var e=(Iu(n)+"e").split("e"),e=t(e[0]+"e"+(+e[1]+r)),e=(Iu(e)+"e").split("e");return+(e[0]+"e"+(+e[1]-r))}return t(n)}}function oe(n){return function(t){var r=vo(t);return"[object Map]"==r?W(t):"[object Set]"==r?C(t):E(t,n(t))}}function fe(n,t,r,e,u,i,o,f){var c=2&t;if(!c&&typeof n!="function")throw new ti("Expected a function");var a=e?e.length:0;if(a||(t&=-97,e=u=T),o=o===T?o:Ui(Eu(o),0),f=f===T?f:Eu(f),a-=u?u.length:0,
64&t){var l=e,s=u;e=u=T}var h=c?T:ho(n);return i=[n,t,r,e,u,l,s,i,o,f],h&&(r=i[1],n=h[1],t=r|n,e=128==n&&8==r||128==n&&256==r&&i[7].length<=h[8]||384==n&&h[7].length<=h[8]&&8==r,131>t||e)&&(1&n&&(i[2]=h[2],t|=1&r?0:4),(r=h[3])&&(e=i[3],i[3]=e?Br(e,r,h[4]):r,i[4]=e?L(i[3],"__lodash_placeholder__"):h[4]),(r=h[5])&&(e=i[5],i[5]=e?Lr(e,r,h[6]):r,i[6]=e?L(i[5],"__lodash_placeholder__"):h[6]),(r=h[7])&&(i[7]=r),128&n&&(i[8]=null==i[8]?h[8]:Ci(i[8],h[8])),null==i[9]&&(i[9]=h[9]),i[0]=h[0],i[1]=t),n=i[0],
t=i[1],r=i[2],e=i[3],u=i[4],f=i[9]=i[9]===T?c?0:n.length:Ui(i[9]-a,0),!f&&24&t&&(t&=-25),Ue((h?co:yo)(t&&1!=t?8==t||16==t?Kr(n,t,f):32!=t&&33!=t||u.length?Jr.apply(T,i):te(n,t,r,e):Pr(n,t,r),i),n,t)}function ce(n,t,r,e){return n===T||lu(n,ei[r])&&!oi.call(e,r)?t:n}function ae(n,t,r,e,u,i){return du(n)&&du(t)&&(i.set(t,n),Yt(n,t,T,ae,i),i.delete(t)),n}function le(n){return xu(n)?T:n}function se(n,t,r,e,u,i){var o=1&r,f=n.length,c=t.length;if(f!=c&&!(o&&c>f))return false;if((c=i.get(n))&&i.get(t))return c==t;
var c=-1,a=true,l=2&r?new Nn:T;for(i.set(n,t),i.set(t,n);++c<f;){var s=n[c],p=t[c];if(e)var _=o?e(p,s,c,t,n,i):e(s,p,c,n,t,i);if(_!==T){if(_)continue;a=false;break}if(l){if(!h(t,function(n,t){if(!O(l,t)&&(s===n||u(s,n,r,e,i)))return l.push(t)})){a=false;break}}else if(s!==p&&!u(s,p,r,e,i)){a=false;break}}return i.delete(n),i.delete(t),a}function he(n,t,r,e,u,i,o){switch(r){case"[object DataView]":if(n.byteLength!=t.byteLength||n.byteOffset!=t.byteOffset)break;n=n.buffer,t=t.buffer;case"[object ArrayBuffer]":
if(n.byteLength!=t.byteLength||!i(new vi(n),new vi(t)))break;return true;case"[object Boolean]":case"[object Date]":case"[object Number]":return lu(+n,+t);case"[object Error]":return n.name==t.name&&n.message==t.message;case"[object RegExp]":case"[object String]":return n==t+"";case"[object Map]":var f=W;case"[object Set]":if(f||(f=U),n.size!=t.size&&!(1&e))break;return(r=o.get(n))?r==t:(e|=2,o.set(n,t),t=se(f(n),f(t),e,u,i,o),o.delete(n),t);case"[object Symbol]":if(to)return to.call(n)==to.call(t)}
return false}function pe(n){return xo(Be(n,T,Ze),n+"")}function _e(n){return St(n,Wu,po)}function ve(n){return St(n,Bu,_o)}function ge(n){for(var t=n.name+"",r=Gi[t],e=oi.call(Gi,t)?r.length:0;e--;){var u=r[e],i=u.func;if(null==i||i==n)return u.name}return t}function de(n){return(oi.call(An,"placeholder")?An:n).placeholder}function ye(){var n=An.iteratee||Fu,n=n===Fu?qt:n;return arguments.length?n(arguments[0],arguments[1]):n}function be(n,t){var r=n.__data__,e=typeof t;return("string"==e||"number"==e||"symbol"==e||"boolean"==e?"__proto__"!==t:null===t)?r[typeof t=="string"?"string":"hash"]:r.map;
}function xe(n){for(var t=Wu(n),r=t.length;r--;){var e=t[r],u=n[e];t[r]=[e,u,u===u&&!du(u)]}return t}function je(n,t){var r=null==n?T:n[t];return Ft(r)?r:T}function we(n,t,r){t=Sr(t,n);for(var e=-1,u=t.length,i=false;++e<u;){var o=Me(t[e]);if(!(i=null!=n&&r(n,o)))break;n=n[o]}return i||++e!=u?i:(u=null==n?0:n.length,!!u&&gu(u)&&Se(o,u)&&(ff(n)||of(n)))}function me(n){var t=n.length,r=new n.constructor(t);return t&&"string"==typeof n[0]&&oi.call(n,"index")&&(r.index=n.index,r.input=n.input),r}function Ae(n){
return typeof n.constructor!="function"||ze(n)?{}:eo(di(n))}function Ee(n,t,r){var e=n.constructor;switch(t){case"[object ArrayBuffer]":return Rr(n);case"[object Boolean]":case"[object Date]":return new e(+n);case"[object DataView]":return t=r?Rr(n.buffer):n.buffer,new n.constructor(t,n.byteOffset,n.byteLength);case"[object Float32Array]":case"[object Float64Array]":case"[object Int8Array]":case"[object Int16Array]":case"[object Int32Array]":case"[object Uint8Array]":case"[object Uint8ClampedArray]":
case"[object Uint16Array]":case"[object Uint32Array]":return zr(n,r);case"[object Map]":return new e;case"[object Number]":case"[object String]":return new e(n);case"[object RegExp]":return t=new n.constructor(n.source,_n.exec(n)),t.lastIndex=n.lastIndex,t;case"[object Set]":return new e;case"[object Symbol]":return to?Qu(to.call(n)):{}}}function ke(n){return ff(n)||of(n)||!!(ji&&n&&n[ji])}function Se(n,t){var r=typeof n;return t=null==t?9007199254740991:t,!!t&&("number"==r||"symbol"!=r&&bn.test(n))&&-1<n&&0==n%1&&n<t;
}function Oe(n,t,r){if(!du(r))return false;var e=typeof t;return!!("number"==e?su(r)&&Se(t,r.length):"string"==e&&t in r)&&lu(r[t],n)}function Ie(n,t){if(ff(n))return false;var r=typeof n;return!("number"!=r&&"symbol"!=r&&"boolean"!=r&&null!=n&&!wu(n))||(nn.test(n)||!X.test(n)||null!=t&&n in Qu(t))}function Re(n){var t=ge(n),r=An[t];return typeof r=="function"&&t in Un.prototype&&(n===r||(t=ho(r),!!t&&n===t[0]))}function ze(n){var t=n&&n.constructor;return n===(typeof t=="function"&&t.prototype||ei)}function We(n,t){
return function(r){return null!=r&&(r[n]===t&&(t!==T||n in Qu(r)))}}function Be(t,r,e){return r=Ui(r===T?t.length-1:r,0),function(){for(var u=arguments,i=-1,o=Ui(u.length-r,0),f=Ku(o);++i<o;)f[i]=u[r+i];for(i=-1,o=Ku(r+1);++i<r;)o[i]=u[i];return o[r]=e(f),n(t,this,o)}}function Le(n,t){if(("constructor"!==t||"function"!=typeof n[t])&&"__proto__"!=t)return n[t]}function Ue(n,t,r){var e=t+"";t=xo;var u,i=$e;return u=(u=e.match(an))?u[1].split(ln):[],r=i(u,r),(i=r.length)&&(u=i-1,r[u]=(1<i?"& ":"")+r[u],
r=r.join(2<i?", ":" "),e=e.replace(cn,"{\n/* [wrapped with "+r+"] */\n")),t(n,e)}function Ce(n){var t=0,r=0;return function(){var e=Di(),u=16-(e-r);if(r=e,0<u){if(800<=++t)return arguments[0]}else t=0;return n.apply(T,arguments)}}function De(n,t){var r=-1,e=n.length,u=e-1;for(t=t===T?e:t;++r<t;){var e=ir(r,u),i=n[e];n[e]=n[r],n[r]=i}return n.length=t,n}function Me(n){if(typeof n=="string"||wu(n))return n;var t=n+"";return"0"==t&&1/n==-$?"-0":t}function Te(n){if(null!=n){try{return ii.call(n)}catch(n){}
return n+""}return""}function $e(n,t){return r(N,function(r){var e="_."+r[0];t&r[1]&&!o(n,e)&&n.push(e)}),n.sort()}function Fe(n){if(n instanceof Un)return n.clone();var t=new On(n.__wrapped__,n.__chain__);return t.__actions__=Ur(n.__actions__),t.__index__=n.__index__,t.__values__=n.__values__,t}function Ne(n,t,r){var e=null==n?0:n.length;return e?(r=null==r?0:Eu(r),0>r&&(r=Ui(e+r,0)),_(n,ye(t,3),r)):-1}function Pe(n,t,r){var e=null==n?0:n.length;if(!e)return-1;var u=e-1;return r!==T&&(u=Eu(r),u=0>r?Ui(e+u,0):Ci(u,e-1)),
_(n,ye(t,3),u,true)}function Ze(n){return(null==n?0:n.length)?wt(n,1):[]}function qe(n){return n&&n.length?n[0]:T}function Ve(n){var t=null==n?0:n.length;return t?n[t-1]:T}function Ke(n,t){return n&&n.length&&t&&t.length?er(n,t):n}function Ge(n){return null==n?n:$i.call(n)}function He(n){if(!n||!n.length)return[];var t=0;return n=i(n,function(n){if(hu(n))return t=Ui(n.length,t),true}),A(t,function(t){return c(n,b(t))})}function Je(t,r){if(!t||!t.length)return[];var e=He(t);return null==r?e:c(e,function(t){
return n(r,T,t)})}function Ye(n){return n=An(n),n.__chain__=true,n}function Qe(n,t){return t(n)}function Xe(){return this}function nu(n,t){return(ff(n)?r:uo)(n,ye(t,3))}function tu(n,t){return(ff(n)?e:io)(n,ye(t,3))}function ru(n,t){return(ff(n)?c:Gt)(n,ye(t,3))}function eu(n,t,r){return t=r?T:t,t=n&&null==t?n.length:t,fe(n,128,T,T,T,T,t)}function uu(n,t){var r;if(typeof t!="function")throw new ti("Expected a function");return n=Eu(n),function(){return 0<--n&&(r=t.apply(this,arguments)),1>=n&&(t=T),
r}}function iu(n,t,r){return t=r?T:t,n=fe(n,8,T,T,T,T,T,t),n.placeholder=iu.placeholder,n}function ou(n,t,r){return t=r?T:t,n=fe(n,16,T,T,T,T,T,t),n.placeholder=ou.placeholder,n}function fu(n,t,r){function e(t){var r=c,e=a;return c=a=T,_=t,s=n.apply(e,r)}function u(n){var r=n-p;return n-=_,p===T||r>=t||0>r||g&&n>=l}function i(){var n=Go();if(u(n))return o(n);var r,e=bo;r=n-_,n=t-(n-p),r=g?Ci(n,l-r):n,h=e(i,r)}function o(n){return h=T,d&&c?e(n):(c=a=T,s)}function f(){var n=Go(),r=u(n);if(c=arguments,
a=this,p=n,r){if(h===T)return _=n=p,h=bo(i,t),v?e(n):s;if(g)return lo(h),h=bo(i,t),e(p)}return h===T&&(h=bo(i,t)),s}var c,a,l,s,h,p,_=0,v=false,g=false,d=true;if(typeof n!="function")throw new ti("Expected a function");return t=Su(t)||0,du(r)&&(v=!!r.leading,l=(g="maxWait"in r)?Ui(Su(r.maxWait)||0,t):l,d="trailing"in r?!!r.trailing:d),f.cancel=function(){h!==T&&lo(h),_=0,c=p=a=h=T},f.flush=function(){return h===T?s:o(Go())},f}function cu(n,t){function r(){var e=arguments,u=t?t.apply(this,e):e[0],i=r.cache;
return i.has(u)?i.get(u):(e=n.apply(this,e),r.cache=i.set(u,e)||i,e)}if(typeof n!="function"||null!=t&&typeof t!="function")throw new ti("Expected a function");return r.cache=new(cu.Cache||Fn),r}function au(n){if(typeof n!="function")throw new ti("Expected a function");return function(){var t=arguments;switch(t.length){case 0:return!n.call(this);case 1:return!n.call(this,t[0]);case 2:return!n.call(this,t[0],t[1]);case 3:return!n.call(this,t[0],t[1],t[2])}return!n.apply(this,t)}}function lu(n,t){return n===t||n!==n&&t!==t;
}function su(n){return null!=n&&gu(n.length)&&!_u(n)}function hu(n){return yu(n)&&su(n)}function pu(n){if(!yu(n))return false;var t=Ot(n);return"[object Error]"==t||"[object DOMException]"==t||typeof n.message=="string"&&typeof n.name=="string"&&!xu(n)}function _u(n){return!!du(n)&&(n=Ot(n),"[object Function]"==n||"[object GeneratorFunction]"==n||"[object AsyncFunction]"==n||"[object Proxy]"==n)}function vu(n){return typeof n=="number"&&n==Eu(n)}function gu(n){return typeof n=="number"&&-1<n&&0==n%1&&9007199254740991>=n;
}function du(n){var t=typeof n;return null!=n&&("object"==t||"function"==t)}function yu(n){return null!=n&&typeof n=="object"}function bu(n){return typeof n=="number"||yu(n)&&"[object Number]"==Ot(n)}function xu(n){return!(!yu(n)||"[object Object]"!=Ot(n))&&(n=di(n),null===n||(n=oi.call(n,"constructor")&&n.constructor,typeof n=="function"&&n instanceof n&&ii.call(n)==li))}function ju(n){return typeof n=="string"||!ff(n)&&yu(n)&&"[object String]"==Ot(n)}function wu(n){return typeof n=="symbol"||yu(n)&&"[object Symbol]"==Ot(n);
}function mu(n){if(!n)return[];if(su(n))return ju(n)?M(n):Ur(n);if(wi&&n[wi]){n=n[wi]();for(var t,r=[];!(t=n.next()).done;)r.push(t.value);return r}return t=vo(n),("[object Map]"==t?W:"[object Set]"==t?U:Uu)(n)}function Au(n){return n?(n=Su(n),n===$||n===-$?1.7976931348623157e308*(0>n?-1:1):n===n?n:0):0===n?n:0}function Eu(n){n=Au(n);var t=n%1;return n===n?t?n-t:n:0}function ku(n){return n?pt(Eu(n),0,4294967295):0}function Su(n){if(typeof n=="number")return n;if(wu(n))return F;if(du(n)&&(n=typeof n.valueOf=="function"?n.valueOf():n,
n=du(n)?n+"":n),typeof n!="string")return 0===n?n:+n;n=n.replace(un,"");var t=gn.test(n);return t||yn.test(n)?Dn(n.slice(2),t?2:8):vn.test(n)?F:+n}function Ou(n){return Cr(n,Bu(n))}function Iu(n){return null==n?"":yr(n)}function Ru(n,t,r){return n=null==n?T:kt(n,t),n===T?r:n}function zu(n,t){return null!=n&&we(n,t,zt)}function Wu(n){return su(n)?qn(n):Vt(n)}function Bu(n){if(su(n))n=qn(n,true);else if(du(n)){var t,r=ze(n),e=[];for(t in n)("constructor"!=t||!r&&oi.call(n,t))&&e.push(t);n=e}else{if(t=[],
null!=n)for(r in Qu(n))t.push(r);n=t}return n}function Lu(n,t){if(null==n)return{};var r=c(ve(n),function(n){return[n]});return t=ye(t),tr(n,r,function(n,r){return t(n,r[0])})}function Uu(n){return null==n?[]:S(n,Wu(n))}function Cu(n){return $f(Iu(n).toLowerCase())}function Du(n){return(n=Iu(n))&&n.replace(xn,Xn).replace(Sn,"")}function Mu(n,t,r){return n=Iu(n),t=r?T:t,t===T?zn.test(n)?n.match(In)||[]:n.match(sn)||[]:n.match(t)||[]}function Tu(n){return function(){return n}}function $u(n){return n;
}function Fu(n){return qt(typeof n=="function"?n:_t(n,1))}function Nu(n,t,e){var u=Wu(t),i=Et(t,u);null!=e||du(t)&&(i.length||!u.length)||(e=t,t=n,n=this,i=Et(t,Wu(t)));var o=!(du(e)&&"chain"in e&&!e.chain),f=_u(n);return r(i,function(r){var e=t[r];n[r]=e,f&&(n.prototype[r]=function(){var t=this.__chain__;if(o||t){var r=n(this.__wrapped__);return(r.__actions__=Ur(this.__actions__)).push({func:e,args:arguments,thisArg:n}),r.__chain__=t,r}return e.apply(n,a([this.value()],arguments))})}),n}function Pu(){}
function Zu(n){return Ie(n)?b(Me(n)):rr(n)}function qu(){return[]}function Vu(){return false}mn=null==mn?$n:rt.defaults($n.Object(),mn,rt.pick($n,Wn));var Ku=mn.Array,Gu=mn.Date,Hu=mn.Error,Ju=mn.Function,Yu=mn.Math,Qu=mn.Object,Xu=mn.RegExp,ni=mn.String,ti=mn.TypeError,ri=Ku.prototype,ei=Qu.prototype,ui=mn["__core-js_shared__"],ii=Ju.prototype.toString,oi=ei.hasOwnProperty,fi=0,ci=function(){var n=/[^.]+$/.exec(ui&&ui.keys&&ui.keys.IE_PROTO||"");return n?"Symbol(src)_1."+n:""}(),ai=ei.toString,li=ii.call(Qu),si=$n._,hi=Xu("^"+ii.call(oi).replace(rn,"\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g,"$1.*?")+"$"),pi=Pn?mn.Buffer:T,_i=mn.Symbol,vi=mn.Uint8Array,gi=pi?pi.g:T,di=B(Qu.getPrototypeOf,Qu),yi=Qu.create,bi=ei.propertyIsEnumerable,xi=ri.splice,ji=_i?_i.isConcatSpreadable:T,wi=_i?_i.iterator:T,mi=_i?_i.toStringTag:T,Ai=function(){
try{var n=je(Qu,"defineProperty");return n({},"",{}),n}catch(n){}}(),Ei=mn.clearTimeout!==$n.clearTimeout&&mn.clearTimeout,ki=Gu&&Gu.now!==$n.Date.now&&Gu.now,Si=mn.setTimeout!==$n.setTimeout&&mn.setTimeout,Oi=Yu.ceil,Ii=Yu.floor,Ri=Qu.getOwnPropertySymbols,zi=pi?pi.isBuffer:T,Wi=mn.isFinite,Bi=ri.join,Li=B(Qu.keys,Qu),Ui=Yu.max,Ci=Yu.min,Di=Gu.now,Mi=mn.parseInt,Ti=Yu.random,$i=ri.reverse,Fi=je(mn,"DataView"),Ni=je(mn,"Map"),Pi=je(mn,"Promise"),Zi=je(mn,"Set"),qi=je(mn,"WeakMap"),Vi=je(Qu,"create"),Ki=qi&&new qi,Gi={},Hi=Te(Fi),Ji=Te(Ni),Yi=Te(Pi),Qi=Te(Zi),Xi=Te(qi),no=_i?_i.prototype:T,to=no?no.valueOf:T,ro=no?no.toString:T,eo=function(){
function n(){}return function(t){return du(t)?yi?yi(t):(n.prototype=t,t=new n,n.prototype=T,t):{}}}();An.templateSettings={escape:J,evaluate:Y,interpolate:Q,variable:"",imports:{_:An}},An.prototype=En.prototype,An.prototype.constructor=An,On.prototype=eo(En.prototype),On.prototype.constructor=On,Un.prototype=eo(En.prototype),Un.prototype.constructor=Un,Mn.prototype.clear=function(){this.__data__=Vi?Vi(null):{},this.size=0},Mn.prototype.delete=function(n){return n=this.has(n)&&delete this.__data__[n],
this.size-=n?1:0,n},Mn.prototype.get=function(n){var t=this.__data__;return Vi?(n=t[n],"__lodash_hash_undefined__"===n?T:n):oi.call(t,n)?t[n]:T},Mn.prototype.has=function(n){var t=this.__data__;return Vi?t[n]!==T:oi.call(t,n)},Mn.prototype.set=function(n,t){var r=this.__data__;return this.size+=this.has(n)?0:1,r[n]=Vi&&t===T?"__lodash_hash_undefined__":t,this},Tn.prototype.clear=function(){this.__data__=[],this.size=0},Tn.prototype.delete=function(n){var t=this.__data__;return n=ft(t,n),!(0>n)&&(n==t.length-1?t.pop():xi.call(t,n,1),
--this.size,true)},Tn.prototype.get=function(n){var t=this.__data__;return n=ft(t,n),0>n?T:t[n][1]},Tn.prototype.has=function(n){return-1<ft(this.__data__,n)},Tn.prototype.set=function(n,t){var r=this.__data__,e=ft(r,n);return 0>e?(++this.size,r.push([n,t])):r[e][1]=t,this},Fn.prototype.clear=function(){this.size=0,this.__data__={hash:new Mn,map:new(Ni||Tn),string:new Mn}},Fn.prototype.delete=function(n){return n=be(this,n).delete(n),this.size-=n?1:0,n},Fn.prototype.get=function(n){return be(this,n).get(n);
},Fn.prototype.has=function(n){return be(this,n).has(n)},Fn.prototype.set=function(n,t){var r=be(this,n),e=r.size;return r.set(n,t),this.size+=r.size==e?0:1,this},Nn.prototype.add=Nn.prototype.push=function(n){return this.__data__.set(n,"__lodash_hash_undefined__"),this},Nn.prototype.has=function(n){return this.__data__.has(n)},Zn.prototype.clear=function(){this.__data__=new Tn,this.size=0},Zn.prototype.delete=function(n){var t=this.__data__;return n=t.delete(n),this.size=t.size,n},Zn.prototype.get=function(n){
return this.__data__.get(n)},Zn.prototype.has=function(n){return this.__data__.has(n)},Zn.prototype.set=function(n,t){var r=this.__data__;if(r instanceof Tn){var e=r.__data__;if(!Ni||199>e.length)return e.push([n,t]),this.size=++r.size,this;r=this.__data__=new Fn(e)}return r.set(n,t),this.size=r.size,this};var uo=Fr(mt),io=Fr(At,true),oo=Nr(),fo=Nr(true),co=Ki?function(n,t){return Ki.set(n,t),n}:$u,ao=Ai?function(n,t){return Ai(n,"toString",{configurable:true,enumerable:false,value:Tu(t),writable:true})}:$u,lo=Ei||function(n){
return $n.clearTimeout(n)},so=Zi&&1/U(new Zi([,-0]))[1]==$?function(n){return new Zi(n)}:Pu,ho=Ki?function(n){return Ki.get(n)}:Pu,po=Ri?function(n){return null==n?[]:(n=Qu(n),i(Ri(n),function(t){return bi.call(n,t)}))}:qu,_o=Ri?function(n){for(var t=[];n;)a(t,po(n)),n=di(n);return t}:qu,vo=Ot;(Fi&&"[object DataView]"!=vo(new Fi(new ArrayBuffer(1)))||Ni&&"[object Map]"!=vo(new Ni)||Pi&&"[object Promise]"!=vo(Pi.resolve())||Zi&&"[object Set]"!=vo(new Zi)||qi&&"[object WeakMap]"!=vo(new qi))&&(vo=function(n){
var t=Ot(n);if(n=(n="[object Object]"==t?n.constructor:T)?Te(n):"")switch(n){case Hi:return"[object DataView]";case Ji:return"[object Map]";case Yi:return"[object Promise]";case Qi:return"[object Set]";case Xi:return"[object WeakMap]"}return t});var go=ui?_u:Vu,yo=Ce(co),bo=Si||function(n,t){return $n.setTimeout(n,t)},xo=Ce(ao),jo=function(n){n=cu(n,function(n){return 500===t.size&&t.clear(),n});var t=n.cache;return n}(function(n){var t=[];return 46===n.charCodeAt(0)&&t.push(""),n.replace(tn,function(n,r,e,u){
t.push(e?u.replace(hn,"$1"):r||n)}),t}),wo=fr(function(n,t){return hu(n)?yt(n,wt(t,1,hu,true)):[]}),mo=fr(function(n,t){var r=Ve(t);return hu(r)&&(r=T),hu(n)?yt(n,wt(t,1,hu,true),ye(r,2)):[]}),Ao=fr(function(n,t){var r=Ve(t);return hu(r)&&(r=T),hu(n)?yt(n,wt(t,1,hu,true),T,r):[]}),Eo=fr(function(n){var t=c(n,Er);return t.length&&t[0]===n[0]?Wt(t):[]}),ko=fr(function(n){var t=Ve(n),r=c(n,Er);return t===Ve(r)?t=T:r.pop(),r.length&&r[0]===n[0]?Wt(r,ye(t,2)):[]}),So=fr(function(n){var t=Ve(n),r=c(n,Er);return(t=typeof t=="function"?t:T)&&r.pop(),
r.length&&r[0]===n[0]?Wt(r,T,t):[]}),Oo=fr(Ke),Io=pe(function(n,t){var r=null==n?0:n.length,e=ht(n,t);return ur(n,c(t,function(n){return Se(n,r)?+n:n}).sort(Wr)),e}),Ro=fr(function(n){return br(wt(n,1,hu,true))}),zo=fr(function(n){var t=Ve(n);return hu(t)&&(t=T),br(wt(n,1,hu,true),ye(t,2))}),Wo=fr(function(n){var t=Ve(n),t=typeof t=="function"?t:T;return br(wt(n,1,hu,true),T,t)}),Bo=fr(function(n,t){return hu(n)?yt(n,t):[]}),Lo=fr(function(n){return mr(i(n,hu))}),Uo=fr(function(n){var t=Ve(n);return hu(t)&&(t=T),
mr(i(n,hu),ye(t,2))}),Co=fr(function(n){var t=Ve(n),t=typeof t=="function"?t:T;return mr(i(n,hu),T,t)}),Do=fr(He),Mo=fr(function(n){var t=n.length,t=1<t?n[t-1]:T,t=typeof t=="function"?(n.pop(),t):T;return Je(n,t)}),To=pe(function(n){function t(t){return ht(t,n)}var r=n.length,e=r?n[0]:0,u=this.__wrapped__;return!(1<r||this.__actions__.length)&&u instanceof Un&&Se(e)?(u=u.slice(e,+e+(r?1:0)),u.__actions__.push({func:Qe,args:[t],thisArg:T}),new On(u,this.__chain__).thru(function(n){return r&&!n.length&&n.push(T),
n})):this.thru(t)}),$o=Tr(function(n,t,r){oi.call(n,r)?++n[r]:st(n,r,1)}),Fo=Gr(Ne),No=Gr(Pe),Po=Tr(function(n,t,r){oi.call(n,r)?n[r].push(t):st(n,r,[t])}),Zo=fr(function(t,r,e){var u=-1,i=typeof r=="function",o=su(t)?Ku(t.length):[];return uo(t,function(t){o[++u]=i?n(r,t,e):Lt(t,r,e)}),o}),qo=Tr(function(n,t,r){st(n,r,t)}),Vo=Tr(function(n,t,r){n[r?0:1].push(t)},function(){return[[],[]]}),Ko=fr(function(n,t){if(null==n)return[];var r=t.length;return 1<r&&Oe(n,t[0],t[1])?t=[]:2<r&&Oe(t[0],t[1],t[2])&&(t=[t[0]]),
Xt(n,wt(t,1),[])}),Go=ki||function(){return $n.Date.now()},Ho=fr(function(n,t,r){var e=1;if(r.length)var u=L(r,de(Ho)),e=32|e;return fe(n,e,t,r,u)}),Jo=fr(function(n,t,r){var e=3;if(r.length)var u=L(r,de(Jo)),e=32|e;return fe(t,e,n,r,u)}),Yo=fr(function(n,t){return dt(n,1,t)}),Qo=fr(function(n,t,r){return dt(n,Su(t)||0,r)});cu.Cache=Fn;var Xo=fr(function(t,r){r=1==r.length&&ff(r[0])?c(r[0],k(ye())):c(wt(r,1),k(ye()));var e=r.length;return fr(function(u){for(var i=-1,o=Ci(u.length,e);++i<o;)u[i]=r[i].call(this,u[i]);
return n(t,this,u)})}),nf=fr(function(n,t){return fe(n,32,T,t,L(t,de(nf)))}),tf=fr(function(n,t){return fe(n,64,T,t,L(t,de(tf)))}),rf=pe(function(n,t){return fe(n,256,T,T,T,t)}),ef=ee(It),uf=ee(function(n,t){return n>=t}),of=Ut(function(){return arguments}())?Ut:function(n){return yu(n)&&oi.call(n,"callee")&&!bi.call(n,"callee")},ff=Ku.isArray,cf=Vn?k(Vn):Ct,af=zi||Vu,lf=Kn?k(Kn):Dt,sf=Gn?k(Gn):Tt,hf=Hn?k(Hn):Nt,pf=Jn?k(Jn):Pt,_f=Yn?k(Yn):Zt,vf=ee(Kt),gf=ee(function(n,t){return n<=t}),df=$r(function(n,t){
if(ze(t)||su(t))Cr(t,Wu(t),n);else for(var r in t)oi.call(t,r)&&ot(n,r,t[r])}),yf=$r(function(n,t){Cr(t,Bu(t),n)}),bf=$r(function(n,t,r,e){Cr(t,Bu(t),n,e)}),xf=$r(function(n,t,r,e){Cr(t,Wu(t),n,e)}),jf=pe(ht),wf=fr(function(n,t){n=Qu(n);var r=-1,e=t.length,u=2<e?t[2]:T;for(u&&Oe(t[0],t[1],u)&&(e=1);++r<e;)for(var u=t[r],i=Bu(u),o=-1,f=i.length;++o<f;){var c=i[o],a=n[c];(a===T||lu(a,ei[c])&&!oi.call(n,c))&&(n[c]=u[c])}return n}),mf=fr(function(t){return t.push(T,ae),n(Of,T,t)}),Af=Yr(function(n,t,r){
null!=t&&typeof t.toString!="function"&&(t=ai.call(t)),n[t]=r},Tu($u)),Ef=Yr(function(n,t,r){null!=t&&typeof t.toString!="function"&&(t=ai.call(t)),oi.call(n,t)?n[t].push(r):n[t]=[r]},ye),kf=fr(Lt),Sf=$r(function(n,t,r){Yt(n,t,r)}),Of=$r(function(n,t,r,e){Yt(n,t,r,e)}),If=pe(function(n,t){var r={};if(null==n)return r;var e=false;t=c(t,function(t){return t=Sr(t,n),e||(e=1<t.length),t}),Cr(n,ve(n),r),e&&(r=_t(r,7,le));for(var u=t.length;u--;)xr(r,t[u]);return r}),Rf=pe(function(n,t){return null==n?{}:nr(n,t);
}),zf=oe(Wu),Wf=oe(Bu),Bf=qr(function(n,t,r){return t=t.toLowerCase(),n+(r?Cu(t):t)}),Lf=qr(function(n,t,r){return n+(r?"-":"")+t.toLowerCase()}),Uf=qr(function(n,t,r){return n+(r?" ":"")+t.toLowerCase()}),Cf=Zr("toLowerCase"),Df=qr(function(n,t,r){return n+(r?"_":"")+t.toLowerCase()}),Mf=qr(function(n,t,r){return n+(r?" ":"")+$f(t)}),Tf=qr(function(n,t,r){return n+(r?" ":"")+t.toUpperCase()}),$f=Zr("toUpperCase"),Ff=fr(function(t,r){try{return n(t,T,r)}catch(n){return pu(n)?n:new Hu(n)}}),Nf=pe(function(n,t){
return r(t,function(t){t=Me(t),st(n,t,Ho(n[t],n))}),n}),Pf=Hr(),Zf=Hr(true),qf=fr(function(n,t){return function(r){return Lt(r,n,t)}}),Vf=fr(function(n,t){return function(r){return Lt(n,r,t)}}),Kf=Xr(c),Gf=Xr(u),Hf=Xr(h),Jf=re(),Yf=re(true),Qf=Qr(function(n,t){return n+t},0),Xf=ie("ceil"),nc=Qr(function(n,t){return n/t},1),tc=ie("floor"),rc=Qr(function(n,t){return n*t},1),ec=ie("round"),uc=Qr(function(n,t){return n-t},0);return An.after=function(n,t){if(typeof t!="function")throw new ti("Expected a function");
return n=Eu(n),function(){if(1>--n)return t.apply(this,arguments)}},An.ary=eu,An.assign=df,An.assignIn=yf,An.assignInWith=bf,An.assignWith=xf,An.at=jf,An.before=uu,An.bind=Ho,An.bindAll=Nf,An.bindKey=Jo,An.castArray=function(){if(!arguments.length)return[];var n=arguments[0];return ff(n)?n:[n]},An.chain=Ye,An.chunk=function(n,t,r){if(t=(r?Oe(n,t,r):t===T)?1:Ui(Eu(t),0),r=null==n?0:n.length,!r||1>t)return[];for(var e=0,u=0,i=Ku(Oi(r/t));e<r;)i[u++]=hr(n,e,e+=t);return i},An.compact=function(n){for(var t=-1,r=null==n?0:n.length,e=0,u=[];++t<r;){
var i=n[t];i&&(u[e++]=i)}return u},An.concat=function(){var n=arguments.length;if(!n)return[];for(var t=Ku(n-1),r=arguments[0];n--;)t[n-1]=arguments[n];return a(ff(r)?Ur(r):[r],wt(t,1))},An.cond=function(t){var r=null==t?0:t.length,e=ye();return t=r?c(t,function(n){if("function"!=typeof n[1])throw new ti("Expected a function");return[e(n[0]),n[1]]}):[],fr(function(e){for(var u=-1;++u<r;){var i=t[u];if(n(i[0],this,e))return n(i[1],this,e)}})},An.conforms=function(n){return vt(_t(n,1))},An.constant=Tu,
An.countBy=$o,An.create=function(n,t){var r=eo(n);return null==t?r:at(r,t)},An.curry=iu,An.curryRight=ou,An.debounce=fu,An.defaults=wf,An.defaultsDeep=mf,An.defer=Yo,An.delay=Qo,An.difference=wo,An.differenceBy=mo,An.differenceWith=Ao,An.drop=function(n,t,r){var e=null==n?0:n.length;return e?(t=r||t===T?1:Eu(t),hr(n,0>t?0:t,e)):[]},An.dropRight=function(n,t,r){var e=null==n?0:n.length;return e?(t=r||t===T?1:Eu(t),t=e-t,hr(n,0,0>t?0:t)):[]},An.dropRightWhile=function(n,t){return n&&n.length?jr(n,ye(t,3),true,true):[];
},An.dropWhile=function(n,t){return n&&n.length?jr(n,ye(t,3),true):[]},An.fill=function(n,t,r,e){var u=null==n?0:n.length;if(!u)return[];for(r&&typeof r!="number"&&Oe(n,t,r)&&(r=0,e=u),u=n.length,r=Eu(r),0>r&&(r=-r>u?0:u+r),e=e===T||e>u?u:Eu(e),0>e&&(e+=u),e=r>e?0:ku(e);r<e;)n[r++]=t;return n},An.filter=function(n,t){return(ff(n)?i:jt)(n,ye(t,3))},An.flatMap=function(n,t){return wt(ru(n,t),1)},An.flatMapDeep=function(n,t){return wt(ru(n,t),$)},An.flatMapDepth=function(n,t,r){return r=r===T?1:Eu(r),
wt(ru(n,t),r)},An.flatten=Ze,An.flattenDeep=function(n){return(null==n?0:n.length)?wt(n,$):[]},An.flattenDepth=function(n,t){return null!=n&&n.length?(t=t===T?1:Eu(t),wt(n,t)):[]},An.flip=function(n){return fe(n,512)},An.flow=Pf,An.flowRight=Zf,An.fromPairs=function(n){for(var t=-1,r=null==n?0:n.length,e={};++t<r;){var u=n[t];e[u[0]]=u[1]}return e},An.functions=function(n){return null==n?[]:Et(n,Wu(n))},An.functionsIn=function(n){return null==n?[]:Et(n,Bu(n))},An.groupBy=Po,An.initial=function(n){
return(null==n?0:n.length)?hr(n,0,-1):[]},An.intersection=Eo,An.intersectionBy=ko,An.intersectionWith=So,An.invert=Af,An.invertBy=Ef,An.invokeMap=Zo,An.iteratee=Fu,An.keyBy=qo,An.keys=Wu,An.keysIn=Bu,An.map=ru,An.mapKeys=function(n,t){var r={};return t=ye(t,3),mt(n,function(n,e,u){st(r,t(n,e,u),n)}),r},An.mapValues=function(n,t){var r={};return t=ye(t,3),mt(n,function(n,e,u){st(r,e,t(n,e,u))}),r},An.matches=function(n){return Ht(_t(n,1))},An.matchesProperty=function(n,t){return Jt(n,_t(t,1))},An.memoize=cu,
An.merge=Sf,An.mergeWith=Of,An.method=qf,An.methodOf=Vf,An.mixin=Nu,An.negate=au,An.nthArg=function(n){return n=Eu(n),fr(function(t){return Qt(t,n)})},An.omit=If,An.omitBy=function(n,t){return Lu(n,au(ye(t)))},An.once=function(n){return uu(2,n)},An.orderBy=function(n,t,r,e){return null==n?[]:(ff(t)||(t=null==t?[]:[t]),r=e?T:r,ff(r)||(r=null==r?[]:[r]),Xt(n,t,r))},An.over=Kf,An.overArgs=Xo,An.overEvery=Gf,An.overSome=Hf,An.partial=nf,An.partialRight=tf,An.partition=Vo,An.pick=Rf,An.pickBy=Lu,An.property=Zu,
An.propertyOf=function(n){return function(t){return null==n?T:kt(n,t)}},An.pull=Oo,An.pullAll=Ke,An.pullAllBy=function(n,t,r){return n&&n.length&&t&&t.length?er(n,t,ye(r,2)):n},An.pullAllWith=function(n,t,r){return n&&n.length&&t&&t.length?er(n,t,T,r):n},An.pullAt=Io,An.range=Jf,An.rangeRight=Yf,An.rearg=rf,An.reject=function(n,t){return(ff(n)?i:jt)(n,au(ye(t,3)))},An.remove=function(n,t){var r=[];if(!n||!n.length)return r;var e=-1,u=[],i=n.length;for(t=ye(t,3);++e<i;){var o=n[e];t(o,e,n)&&(r.push(o),
u.push(e))}return ur(n,u),r},An.rest=function(n,t){if(typeof n!="function")throw new ti("Expected a function");return t=t===T?t:Eu(t),fr(n,t)},An.reverse=Ge,An.sampleSize=function(n,t,r){return t=(r?Oe(n,t,r):t===T)?1:Eu(t),(ff(n)?et:ar)(n,t)},An.set=function(n,t,r){return null==n?n:lr(n,t,r)},An.setWith=function(n,t,r,e){return e=typeof e=="function"?e:T,null==n?n:lr(n,t,r,e)},An.shuffle=function(n){return(ff(n)?ut:sr)(n)},An.slice=function(n,t,r){var e=null==n?0:n.length;return e?(r&&typeof r!="number"&&Oe(n,t,r)?(t=0,
r=e):(t=null==t?0:Eu(t),r=r===T?e:Eu(r)),hr(n,t,r)):[]},An.sortBy=Ko,An.sortedUniq=function(n){return n&&n.length?gr(n):[]},An.sortedUniqBy=function(n,t){return n&&n.length?gr(n,ye(t,2)):[]},An.split=function(n,t,r){return r&&typeof r!="number"&&Oe(n,t,r)&&(t=r=T),r=r===T?4294967295:r>>>0,r?(n=Iu(n))&&(typeof t=="string"||null!=t&&!hf(t))&&(t=yr(t),!t&&Rn.test(n))?Or(M(n),0,r):n.split(t,r):[]},An.spread=function(t,r){if(typeof t!="function")throw new ti("Expected a function");return r=null==r?0:Ui(Eu(r),0),
fr(function(e){var u=e[r];return e=Or(e,0,r),u&&a(e,u),n(t,this,e)})},An.tail=function(n){var t=null==n?0:n.length;return t?hr(n,1,t):[]},An.take=function(n,t,r){return n&&n.length?(t=r||t===T?1:Eu(t),hr(n,0,0>t?0:t)):[]},An.takeRight=function(n,t,r){var e=null==n?0:n.length;return e?(t=r||t===T?1:Eu(t),t=e-t,hr(n,0>t?0:t,e)):[]},An.takeRightWhile=function(n,t){return n&&n.length?jr(n,ye(t,3),false,true):[]},An.takeWhile=function(n,t){return n&&n.length?jr(n,ye(t,3)):[]},An.tap=function(n,t){return t(n),
n},An.throttle=function(n,t,r){var e=true,u=true;if(typeof n!="function")throw new ti("Expected a function");return du(r)&&(e="leading"in r?!!r.leading:e,u="trailing"in r?!!r.trailing:u),fu(n,t,{leading:e,maxWait:t,trailing:u})},An.thru=Qe,An.toArray=mu,An.toPairs=zf,An.toPairsIn=Wf,An.toPath=function(n){return ff(n)?c(n,Me):wu(n)?[n]:Ur(jo(Iu(n)))},An.toPlainObject=Ou,An.transform=function(n,t,e){var u=ff(n),i=u||af(n)||_f(n);if(t=ye(t,4),null==e){var o=n&&n.constructor;e=i?u?new o:[]:du(n)&&_u(o)?eo(di(n)):{};
}return(i?r:mt)(n,function(n,r,u){return t(e,n,r,u)}),e},An.unary=function(n){return eu(n,1)},An.union=Ro,An.unionBy=zo,An.unionWith=Wo,An.uniq=function(n){return n&&n.length?br(n):[]},An.uniqBy=function(n,t){return n&&n.length?br(n,ye(t,2)):[]},An.uniqWith=function(n,t){return t=typeof t=="function"?t:T,n&&n.length?br(n,T,t):[]},An.unset=function(n,t){return null==n||xr(n,t)},An.unzip=He,An.unzipWith=Je,An.update=function(n,t,r){return null==n?n:lr(n,t,kr(r)(kt(n,t)),void 0)},An.updateWith=function(n,t,r,e){
return e=typeof e=="function"?e:T,null!=n&&(n=lr(n,t,kr(r)(kt(n,t)),e)),n},An.values=Uu,An.valuesIn=function(n){return null==n?[]:S(n,Bu(n))},An.without=Bo,An.words=Mu,An.wrap=function(n,t){return nf(kr(t),n)},An.xor=Lo,An.xorBy=Uo,An.xorWith=Co,An.zip=Do,An.zipObject=function(n,t){return Ar(n||[],t||[],ot)},An.zipObjectDeep=function(n,t){return Ar(n||[],t||[],lr)},An.zipWith=Mo,An.entries=zf,An.entriesIn=Wf,An.extend=yf,An.extendWith=bf,Nu(An,An),An.add=Qf,An.attempt=Ff,An.camelCase=Bf,An.capitalize=Cu,
An.ceil=Xf,An.clamp=function(n,t,r){return r===T&&(r=t,t=T),r!==T&&(r=Su(r),r=r===r?r:0),t!==T&&(t=Su(t),t=t===t?t:0),pt(Su(n),t,r)},An.clone=function(n){return _t(n,4)},An.cloneDeep=function(n){return _t(n,5)},An.cloneDeepWith=function(n,t){return t=typeof t=="function"?t:T,_t(n,5,t)},An.cloneWith=function(n,t){return t=typeof t=="function"?t:T,_t(n,4,t)},An.conformsTo=function(n,t){return null==t||gt(n,t,Wu(t))},An.deburr=Du,An.defaultTo=function(n,t){return null==n||n!==n?t:n},An.divide=nc,An.endsWith=function(n,t,r){
n=Iu(n),t=yr(t);var e=n.length,e=r=r===T?e:pt(Eu(r),0,e);return r-=t.length,0<=r&&n.slice(r,e)==t},An.eq=lu,An.escape=function(n){return(n=Iu(n))&&H.test(n)?n.replace(K,nt):n},An.escapeRegExp=function(n){return(n=Iu(n))&&en.test(n)?n.replace(rn,"\\$&"):n},An.every=function(n,t,r){var e=ff(n)?u:bt;return r&&Oe(n,t,r)&&(t=T),e(n,ye(t,3))},An.find=Fo,An.findIndex=Ne,An.findKey=function(n,t){return p(n,ye(t,3),mt)},An.findLast=No,An.findLastIndex=Pe,An.findLastKey=function(n,t){return p(n,ye(t,3),At);
},An.floor=tc,An.forEach=nu,An.forEachRight=tu,An.forIn=function(n,t){return null==n?n:oo(n,ye(t,3),Bu)},An.forInRight=function(n,t){return null==n?n:fo(n,ye(t,3),Bu)},An.forOwn=function(n,t){return n&&mt(n,ye(t,3))},An.forOwnRight=function(n,t){return n&&At(n,ye(t,3))},An.get=Ru,An.gt=ef,An.gte=uf,An.has=function(n,t){return null!=n&&we(n,t,Rt)},An.hasIn=zu,An.head=qe,An.identity=$u,An.includes=function(n,t,r,e){return n=su(n)?n:Uu(n),r=r&&!e?Eu(r):0,e=n.length,0>r&&(r=Ui(e+r,0)),ju(n)?r<=e&&-1<n.indexOf(t,r):!!e&&-1<v(n,t,r);
},An.indexOf=function(n,t,r){var e=null==n?0:n.length;return e?(r=null==r?0:Eu(r),0>r&&(r=Ui(e+r,0)),v(n,t,r)):-1},An.inRange=function(n,t,r){return t=Au(t),r===T?(r=t,t=0):r=Au(r),n=Su(n),n>=Ci(t,r)&&n<Ui(t,r)},An.invoke=kf,An.isArguments=of,An.isArray=ff,An.isArrayBuffer=cf,An.isArrayLike=su,An.isArrayLikeObject=hu,An.isBoolean=function(n){return true===n||false===n||yu(n)&&"[object Boolean]"==Ot(n)},An.isBuffer=af,An.isDate=lf,An.isElement=function(n){return yu(n)&&1===n.nodeType&&!xu(n)},An.isEmpty=function(n){
if(null==n)return true;if(su(n)&&(ff(n)||typeof n=="string"||typeof n.splice=="function"||af(n)||_f(n)||of(n)))return!n.length;var t=vo(n);if("[object Map]"==t||"[object Set]"==t)return!n.size;if(ze(n))return!Vt(n).length;for(var r in n)if(oi.call(n,r))return false;return true},An.isEqual=function(n,t){return Mt(n,t)},An.isEqualWith=function(n,t,r){var e=(r=typeof r=="function"?r:T)?r(n,t):T;return e===T?Mt(n,t,T,r):!!e},An.isError=pu,An.isFinite=function(n){return typeof n=="number"&&Wi(n)},An.isFunction=_u,
An.isInteger=vu,An.isLength=gu,An.isMap=sf,An.isMatch=function(n,t){return n===t||$t(n,t,xe(t))},An.isMatchWith=function(n,t,r){return r=typeof r=="function"?r:T,$t(n,t,xe(t),r)},An.isNaN=function(n){return bu(n)&&n!=+n},An.isNative=function(n){if(go(n))throw new Hu("Unsupported core-js use. Try https://npms.io/search?q=ponyfill.");return Ft(n)},An.isNil=function(n){return null==n},An.isNull=function(n){return null===n},An.isNumber=bu,An.isObject=du,An.isObjectLike=yu,An.isPlainObject=xu,An.isRegExp=hf,
An.isSafeInteger=function(n){return vu(n)&&-9007199254740991<=n&&9007199254740991>=n},An.isSet=pf,An.isString=ju,An.isSymbol=wu,An.isTypedArray=_f,An.isUndefined=function(n){return n===T},An.isWeakMap=function(n){return yu(n)&&"[object WeakMap]"==vo(n)},An.isWeakSet=function(n){return yu(n)&&"[object WeakSet]"==Ot(n)},An.join=function(n,t){return null==n?"":Bi.call(n,t)},An.kebabCase=Lf,An.last=Ve,An.lastIndexOf=function(n,t,r){var e=null==n?0:n.length;if(!e)return-1;var u=e;if(r!==T&&(u=Eu(r),u=0>u?Ui(e+u,0):Ci(u,e-1)),
t===t){for(r=u+1;r--&&n[r]!==t;);n=r}else n=_(n,d,u,true);return n},An.lowerCase=Uf,An.lowerFirst=Cf,An.lt=vf,An.lte=gf,An.max=function(n){return n&&n.length?xt(n,$u,It):T},An.maxBy=function(n,t){return n&&n.length?xt(n,ye(t,2),It):T},An.mean=function(n){return y(n,$u)},An.meanBy=function(n,t){return y(n,ye(t,2))},An.min=function(n){return n&&n.length?xt(n,$u,Kt):T},An.minBy=function(n,t){return n&&n.length?xt(n,ye(t,2),Kt):T},An.stubArray=qu,An.stubFalse=Vu,An.stubObject=function(){return{}},An.stubString=function(){
return""},An.stubTrue=function(){return true},An.multiply=rc,An.nth=function(n,t){return n&&n.length?Qt(n,Eu(t)):T},An.noConflict=function(){return $n._===this&&($n._=si),this},An.noop=Pu,An.now=Go,An.pad=function(n,t,r){n=Iu(n);var e=(t=Eu(t))?D(n):0;return!t||e>=t?n:(t=(t-e)/2,ne(Ii(t),r)+n+ne(Oi(t),r))},An.padEnd=function(n,t,r){n=Iu(n);var e=(t=Eu(t))?D(n):0;return t&&e<t?n+ne(t-e,r):n},An.padStart=function(n,t,r){n=Iu(n);var e=(t=Eu(t))?D(n):0;return t&&e<t?ne(t-e,r)+n:n},An.parseInt=function(n,t,r){
return r||null==t?t=0:t&&(t=+t),Mi(Iu(n).replace(on,""),t||0)},An.random=function(n,t,r){if(r&&typeof r!="boolean"&&Oe(n,t,r)&&(t=r=T),r===T&&(typeof t=="boolean"?(r=t,t=T):typeof n=="boolean"&&(r=n,n=T)),n===T&&t===T?(n=0,t=1):(n=Au(n),t===T?(t=n,n=0):t=Au(t)),n>t){var e=n;n=t,t=e}return r||n%1||t%1?(r=Ti(),Ci(n+r*(t-n+Cn("1e-"+((r+"").length-1))),t)):ir(n,t)},An.reduce=function(n,t,r){var e=ff(n)?l:j,u=3>arguments.length;return e(n,ye(t,4),r,u,uo)},An.reduceRight=function(n,t,r){var e=ff(n)?s:j,u=3>arguments.length;
return e(n,ye(t,4),r,u,io)},An.repeat=function(n,t,r){return t=(r?Oe(n,t,r):t===T)?1:Eu(t),or(Iu(n),t)},An.replace=function(){var n=arguments,t=Iu(n[0]);return 3>n.length?t:t.replace(n[1],n[2])},An.result=function(n,t,r){t=Sr(t,n);var e=-1,u=t.length;for(u||(u=1,n=T);++e<u;){var i=null==n?T:n[Me(t[e])];i===T&&(e=u,i=r),n=_u(i)?i.call(n):i}return n},An.round=ec,An.runInContext=x,An.sample=function(n){return(ff(n)?Qn:cr)(n)},An.size=function(n){if(null==n)return 0;if(su(n))return ju(n)?D(n):n.length;
var t=vo(n);return"[object Map]"==t||"[object Set]"==t?n.size:Vt(n).length},An.snakeCase=Df,An.some=function(n,t,r){var e=ff(n)?h:pr;return r&&Oe(n,t,r)&&(t=T),e(n,ye(t,3))},An.sortedIndex=function(n,t){return _r(n,t)},An.sortedIndexBy=function(n,t,r){return vr(n,t,ye(r,2))},An.sortedIndexOf=function(n,t){var r=null==n?0:n.length;if(r){var e=_r(n,t);if(e<r&&lu(n[e],t))return e}return-1},An.sortedLastIndex=function(n,t){return _r(n,t,true)},An.sortedLastIndexBy=function(n,t,r){return vr(n,t,ye(r,2),true);
},An.sortedLastIndexOf=function(n,t){if(null==n?0:n.length){var r=_r(n,t,true)-1;if(lu(n[r],t))return r}return-1},An.startCase=Mf,An.startsWith=function(n,t,r){return n=Iu(n),r=null==r?0:pt(Eu(r),0,n.length),t=yr(t),n.slice(r,r+t.length)==t},An.subtract=uc,An.sum=function(n){return n&&n.length?m(n,$u):0},An.sumBy=function(n,t){return n&&n.length?m(n,ye(t,2)):0},An.template=function(n,t,r){var e=An.templateSettings;r&&Oe(n,t,r)&&(t=T),n=Iu(n),t=bf({},t,e,ce),r=bf({},t.imports,e.imports,ce);var u,i,o=Wu(r),f=S(r,o),c=0;
r=t.interpolate||jn;var a="__p+='";r=Xu((t.escape||jn).source+"|"+r.source+"|"+(r===Q?pn:jn).source+"|"+(t.evaluate||jn).source+"|$","g");var l=oi.call(t,"sourceURL")?"//# sourceURL="+(t.sourceURL+"").replace(/[\r\n]/g," ")+"\n":"";if(n.replace(r,function(t,r,e,o,f,l){return e||(e=o),a+=n.slice(c,l).replace(wn,z),r&&(u=true,a+="'+__e("+r+")+'"),f&&(i=true,a+="';"+f+";\n__p+='"),e&&(a+="'+((__t=("+e+"))==null?'':__t)+'"),c=l+t.length,t}),a+="';",(t=oi.call(t,"variable")&&t.variable)||(a="with(obj){"+a+"}"),
a=(i?a.replace(P,""):a).replace(Z,"$1").replace(q,"$1;"),a="function("+(t||"obj")+"){"+(t?"":"obj||(obj={});")+"var __t,__p=''"+(u?",__e=_.escape":"")+(i?",__j=Array.prototype.join;function print(){__p+=__j.call(arguments,'')}":";")+a+"return __p}",t=Ff(function(){return Ju(o,l+"return "+a).apply(T,f)}),t.source=a,pu(t))throw t;return t},An.times=function(n,t){if(n=Eu(n),1>n||9007199254740991<n)return[];var r=4294967295,e=Ci(n,4294967295);for(t=ye(t),n-=4294967295,e=A(e,t);++r<n;)t(r);return e},An.toFinite=Au,
An.toInteger=Eu,An.toLength=ku,An.toLower=function(n){return Iu(n).toLowerCase()},An.toNumber=Su,An.toSafeInteger=function(n){return n?pt(Eu(n),-9007199254740991,9007199254740991):0===n?n:0},An.toString=Iu,An.toUpper=function(n){return Iu(n).toUpperCase()},An.trim=function(n,t,r){return(n=Iu(n))&&(r||t===T)?n.replace(un,""):n&&(t=yr(t))?(n=M(n),r=M(t),t=I(n,r),r=R(n,r)+1,Or(n,t,r).join("")):n},An.trimEnd=function(n,t,r){return(n=Iu(n))&&(r||t===T)?n.replace(fn,""):n&&(t=yr(t))?(n=M(n),t=R(n,M(t))+1,
Or(n,0,t).join("")):n},An.trimStart=function(n,t,r){return(n=Iu(n))&&(r||t===T)?n.replace(on,""):n&&(t=yr(t))?(n=M(n),t=I(n,M(t)),Or(n,t).join("")):n},An.truncate=function(n,t){var r=30,e="...";if(du(t))var u="separator"in t?t.separator:u,r="length"in t?Eu(t.length):r,e="omission"in t?yr(t.omission):e;n=Iu(n);var i=n.length;if(Rn.test(n))var o=M(n),i=o.length;if(r>=i)return n;if(i=r-D(e),1>i)return e;if(r=o?Or(o,0,i).join(""):n.slice(0,i),u===T)return r+e;if(o&&(i+=r.length-i),hf(u)){if(n.slice(i).search(u)){
var f=r;for(u.global||(u=Xu(u.source,Iu(_n.exec(u))+"g")),u.lastIndex=0;o=u.exec(f);)var c=o.index;r=r.slice(0,c===T?i:c)}}else n.indexOf(yr(u),i)!=i&&(u=r.lastIndexOf(u),-1<u&&(r=r.slice(0,u)));return r+e},An.unescape=function(n){return(n=Iu(n))&&G.test(n)?n.replace(V,tt):n},An.uniqueId=function(n){var t=++fi;return Iu(n)+t},An.upperCase=Tf,An.upperFirst=$f,An.each=nu,An.eachRight=tu,An.first=qe,Nu(An,function(){var n={};return mt(An,function(t,r){oi.call(An.prototype,r)||(n[r]=t)}),n}(),{chain:false
}),An.VERSION="4.17.15",r("bind bindKey curry curryRight partial partialRight".split(" "),function(n){An[n].placeholder=An}),r(["drop","take"],function(n,t){Un.prototype[n]=function(r){r=r===T?1:Ui(Eu(r),0);var e=this.__filtered__&&!t?new Un(this):this.clone();return e.__filtered__?e.__takeCount__=Ci(r,e.__takeCount__):e.__views__.push({size:Ci(r,4294967295),type:n+(0>e.__dir__?"Right":"")}),e},Un.prototype[n+"Right"]=function(t){return this.reverse()[n](t).reverse()}}),r(["filter","map","takeWhile"],function(n,t){
var r=t+1,e=1==r||3==r;Un.prototype[n]=function(n){var t=this.clone();return t.__iteratees__.push({iteratee:ye(n,3),type:r}),t.__filtered__=t.__filtered__||e,t}}),r(["head","last"],function(n,t){var r="take"+(t?"Right":"");Un.prototype[n]=function(){return this[r](1).value()[0]}}),r(["initial","tail"],function(n,t){var r="drop"+(t?"":"Right");Un.prototype[n]=function(){return this.__filtered__?new Un(this):this[r](1)}}),Un.prototype.compact=function(){return this.filter($u)},Un.prototype.find=function(n){
return this.filter(n).head()},Un.prototype.findLast=function(n){return this.reverse().find(n)},Un.prototype.invokeMap=fr(function(n,t){return typeof n=="function"?new Un(this):this.map(function(r){return Lt(r,n,t)})}),Un.prototype.reject=function(n){return this.filter(au(ye(n)))},Un.prototype.slice=function(n,t){n=Eu(n);var r=this;return r.__filtered__&&(0<n||0>t)?new Un(r):(0>n?r=r.takeRight(-n):n&&(r=r.drop(n)),t!==T&&(t=Eu(t),r=0>t?r.dropRight(-t):r.take(t-n)),r)},Un.prototype.takeRightWhile=function(n){
return this.reverse().takeWhile(n).reverse()},Un.prototype.toArray=function(){return this.take(4294967295)},mt(Un.prototype,function(n,t){var r=/^(?:filter|find|map|reject)|While$/.test(t),e=/^(?:head|last)$/.test(t),u=An[e?"take"+("last"==t?"Right":""):t],i=e||/^find/.test(t);u&&(An.prototype[t]=function(){function t(n){return n=u.apply(An,a([n],f)),e&&h?n[0]:n}var o=this.__wrapped__,f=e?[1]:arguments,c=o instanceof Un,l=f[0],s=c||ff(o);s&&r&&typeof l=="function"&&1!=l.length&&(c=s=false);var h=this.__chain__,p=!!this.__actions__.length,l=i&&!h,c=c&&!p;
return!i&&s?(o=c?o:new Un(this),o=n.apply(o,f),o.__actions__.push({func:Qe,args:[t],thisArg:T}),new On(o,h)):l&&c?n.apply(this,f):(o=this.thru(t),l?e?o.value()[0]:o.value():o)})}),r("pop push shift sort splice unshift".split(" "),function(n){var t=ri[n],r=/^(?:push|sort|unshift)$/.test(n)?"tap":"thru",e=/^(?:pop|shift)$/.test(n);An.prototype[n]=function(){var n=arguments;if(e&&!this.__chain__){var u=this.value();return t.apply(ff(u)?u:[],n)}return this[r](function(r){return t.apply(ff(r)?r:[],n)});
}}),mt(Un.prototype,function(n,t){var r=An[t];if(r){var e=r.name+"";oi.call(Gi,e)||(Gi[e]=[]),Gi[e].push({name:t,func:r})}}),Gi[Jr(T,2).name]=[{name:"wrapper",func:T}],Un.prototype.clone=function(){var n=new Un(this.__wrapped__);return n.__actions__=Ur(this.__actions__),n.__dir__=this.__dir__,n.__filtered__=this.__filtered__,n.__iteratees__=Ur(this.__iteratees__),n.__takeCount__=this.__takeCount__,n.__views__=Ur(this.__views__),n},Un.prototype.reverse=function(){if(this.__filtered__){var n=new Un(this);
n.__dir__=-1,n.__filtered__=true}else n=this.clone(),n.__dir__*=-1;return n},Un.prototype.value=function(){var n,t=this.__wrapped__.value(),r=this.__dir__,e=ff(t),u=0>r,i=e?t.length:0;n=i;for(var o=this.__views__,f=0,c=-1,a=o.length;++c<a;){var l=o[c],s=l.size;switch(l.type){case"drop":f+=s;break;case"dropRight":n-=s;break;case"take":n=Ci(n,f+s);break;case"takeRight":f=Ui(f,n-s)}}if(n={start:f,end:n},o=n.start,f=n.end,n=f-o,o=u?f:o-1,f=this.__iteratees__,c=f.length,a=0,l=Ci(n,this.__takeCount__),!e||!u&&i==n&&l==n)return wr(t,this.__actions__);
e=[];n:for(;n--&&a<l;){for(o+=r,u=-1,i=t[o];++u<c;){var h=f[u],s=h.type,h=(0,h.iteratee)(i);if(2==s)i=h;else if(!h){if(1==s)continue n;break n}}e[a++]=i}return e},An.prototype.at=To,An.prototype.chain=function(){return Ye(this)},An.prototype.commit=function(){return new On(this.value(),this.__chain__)},An.prototype.next=function(){this.__values__===T&&(this.__values__=mu(this.value()));var n=this.__index__>=this.__values__.length;return{done:n,value:n?T:this.__values__[this.__index__++]}},An.prototype.plant=function(n){
for(var t,r=this;r instanceof En;){var e=Fe(r);e.__index__=0,e.__values__=T,t?u.__wrapped__=e:t=e;var u=e,r=r.__wrapped__}return u.__wrapped__=n,t},An.prototype.reverse=function(){var n=this.__wrapped__;return n instanceof Un?(this.__actions__.length&&(n=new Un(this)),n=n.reverse(),n.__actions__.push({func:Qe,args:[Ge],thisArg:T}),new On(n,this.__chain__)):this.thru(Ge)},An.prototype.toJSON=An.prototype.valueOf=An.prototype.value=function(){return wr(this.__wrapped__,this.__actions__)},An.prototype.first=An.prototype.head,
wi&&(An.prototype[wi]=Xe),An}();typeof define=="function"&&typeof define.amd=="object"&&define.amd?($n._=rt, define(function(){return rt})):Nn?((Nn.exports=rt)._=rt,Fn._=rt):$n._=rt}).call(this);

//third_party/javascript/angular/v1_6/angular.min.js
/*
 AngularJS v1.6.4-local+sha.617b36117
 (c) 2010-2018 Google, Inc. http://angularjs.org
 License: MIT

 Copyright 2013 Google, Inc. http://angularjs.org
 SPDX-License-Identifier: MIT
*/
'use strict';(function(ia){'use strict';function Rf(a){if(fa(a))R(a.objectMaxDepth)&&(de.objectMaxDepth=fd(a.objectMaxDepth)?a.objectMaxDepth:NaN);else return de}function fd(a){return Pa(a)&&0<a}function va(a){return function(){var b=arguments[0];var d="["+(a?a+":":"")+b+"] http://errors.angularjs.org/1.6.4-local+sha.617b36117/"+(a?a+"/":"")+b;for(b=1;b<arguments.length;b++){d=d+(1==b?"?":"&")+"p"+(b-1)+"=";var c=encodeURIComponent;var e=arguments[b];e="function"==typeof e?e.toString().replace(/ \{[\s\S]*$/,""):
"undefined"==typeof e?"undefined":"string"!=typeof e?JSON.stringify(e):e;d+=c(e)}return Error(d)}}function ub(a){if(null==a||ac(a))return!1;if(oa(a)||na(a)||da&&a instanceof da)return!0;var b="length"in Object(a)&&a.length;return Pa(b)&&(0<=b&&(b-1 in a||a instanceof Array)||"function"===typeof a.item)}function I(a,b,d){var c;if(a)if(ca(a))for(g in a)"prototype"!==g&&"length"!==g&&"name"!==g&&a.hasOwnProperty(g)&&b.call(d,a[g],g,a);else if(oa(a)||ub(a)){var e="object"!==typeof a;var g=0;for(c=a.length;g<
c;g++)(e||g in a)&&b.call(d,a[g],g,a)}else if(a.forEach&&a.forEach!==I)a.forEach(b,d,a);else if(ee(a))for(g in a)b.call(d,a[g],g,a);else if("function"===typeof a.hasOwnProperty)for(g in a)a.hasOwnProperty(g)&&b.call(d,a[g],g,a);else for(g in a)bb.call(a,g)&&b.call(d,a[g],g,a);return a}function fe(a,b,d){for(var c=Object.keys(a).sort(),e=0;e<c.length;e++)b.call(d,a[c[e]],c[e]);return c}function gd(a){return function(b,d){a(d,b)}}function Sf(){return++sc}function hd(a,b,d){for(var c=a.$$hashKey,e=0,
g=b.length;e<g;++e){var f=b[e];if(fa(f)||ca(f))for(var k=Object.keys(f),h=0,l=k.length;h<l;h++){var n=k[h],q=f[n];d&&fa(q)?Xa(q)?a[n]=new Date(q.valueOf()):tc(q)?a[n]=new RegExp(q):q.nodeName?a[n]=q.cloneNode(!0):id(q)?a[n]=q.clone():(fa(a[n])||(a[n]=oa(q)?[]:{}),hd(a[n],[q],!0)):a[n]=q}}c?a.$$hashKey=c:delete a.$$hashKey;return a}function Aa(a){return hd(a,hb.call(arguments,1),!1)}function Tf(a){return hd(a,hb.call(arguments,1),!0)}function jd(a,b){return Aa(Object.create(a),b)}function ja(){}function uc(a){return a}
function cb(a){return function(){return a}}function kd(a){return ca(a.toString)&&a.toString!==Ta}function U(a){return"undefined"===typeof a}function R(a){return"undefined"!==typeof a}function fa(a){return null!==a&&"object"===typeof a}function ee(a){return null!==a&&"object"===typeof a&&!ge(a)}function na(a){return"string"===typeof a}function Pa(a){return"number"===typeof a}function Xa(a){return"[object Date]"===Ta.call(a)}function ld(a){switch(Ta.call(a)){case "[object Error]":return!0;case "[object Exception]":return!0;
case "[object DOMException]":return!0;default:return a instanceof Error}}function ca(a){return"function"===typeof a}function tc(a){return"[object RegExp]"===Ta.call(a)}function ac(a){return a&&a.window===a}function bc(a){return a&&a.$evalAsync&&a.$watch}function vb(a){return"boolean"===typeof a}function Uf(a){return a&&Pa(a.length)&&Vf.test(Ta.call(a))}function id(a){return!(!a||!(a.nodeName||a.prop&&a.attr&&a.find))}function Wf(a){var b={};a=a.split(",");var d;for(d=0;d<a.length;d++)b[a[d]]=!0;return b}
function ib(a){return xa(a.nodeName||a[0]&&a[0].nodeName)}function cc(a,b){b=a.indexOf(b);0<=b&&a.splice(b,1);return b}function Bb(a,b,d){function c(h,l,n){n--;if(0>n)return"...";var q=l.$$hashKey;if(oa(h)){var t=0;for(var w=h.length;t<w;t++)l.push(e(h[t],n))}else if(ee(h))for(t in h)l[t]=e(h[t],n);else if(h&&"function"===typeof h.hasOwnProperty)for(t in h)h.hasOwnProperty(t)&&(l[t]=e(h[t],n));else for(t in h)bb.call(h,t)&&(l[t]=e(h[t],n));q?l.$$hashKey=q:delete l.$$hashKey;return l}function e(h,
l){if(!fa(h))return h;var n=f.indexOf(h);if(-1!==n)return k[n];if(ac(h)||bc(h))throw Cb("cpws");n=!1;var q=g(h);void 0===q&&(q=oa(h)?[]:Object.create(ge(h)),n=!0);f.push(h);k.push(q);return n?c(h,q,l):q}function g(h){switch(Ta.call(h)){case "[object Int8Array]":case "[object Int16Array]":case "[object Int32Array]":case "[object Float32Array]":case "[object Float64Array]":case "[object Uint8Array]":case "[object Uint8ClampedArray]":case "[object Uint16Array]":case "[object Uint32Array]":return new h.constructor(e(h.buffer),
h.byteOffset,h.length);case "[object ArrayBuffer]":if(!h.slice){var l=new ArrayBuffer(h.byteLength);(new Uint8Array(l)).set(new Uint8Array(h));return l}return h.slice(0);case "[object Boolean]":case "[object Number]":case "[object String]":case "[object Date]":return new h.constructor(h.valueOf());case "[object RegExp]":return l=new RegExp(h.source,h.toString().match(/[^/]*$/)[0]),l.lastIndex=h.lastIndex,l;case "[object Blob]":return new h.constructor([h],{type:h.type})}if(ca(h.cloneNode))return h.cloneNode(!0)}
var f=[],k=[];d=fd(d)?d:NaN;if(b){if(Uf(b)||"[object ArrayBuffer]"===Ta.call(b))throw Cb("cpta");if(a===b)throw Cb("cpi");oa(b)?b.length=0:I(b,function(h,l){"$$hashKey"!==l&&delete b[l]});f.push(a);k.push(b);return c(a,b,d)}return e(a,d)}function md(a,b){return a===b||a!==a&&b!==b}function db(a,b){if(a===b)return!0;if(null===a||null===b)return!1;if(a!==a&&b!==b)return!0;var d=typeof a,c;if(d===typeof b&&"object"===d)if(oa(a)){if(!oa(b))return!1;if((d=a.length)===b.length){for(c=0;c<d;c++)if(!db(a[c],
b[c]))return!1;return!0}}else{if(Xa(a))return Xa(b)?md(a.getTime(),b.getTime()):!1;if(tc(a))return tc(b)?a.toString()===b.toString():!1;if(bc(a)||bc(b)||ac(a)||ac(b)||oa(b)||Xa(b)||tc(b))return!1;d=Ea();for(c in a)if("$"!==c.charAt(0)&&!ca(a[c])){if(!db(a[c],b[c]))return!1;d[c]=!0}for(c in b)if(!(c in d)&&"$"!==c.charAt(0)&&R(b[c])&&!ca(b[c]))return!1;return!0}return!1}function dc(a,b,d){return a.concat(hb.call(b,d))}function Mb(a,b){var d=2<arguments.length?hb.call(arguments,2):[];return!ca(b)||
b instanceof RegExp?b:d.length?function(){return arguments.length?b.apply(a,dc(d,arguments,0)):b.apply(a,d)}:function(){return arguments.length?b.apply(a,arguments):b.call(a)}}function he(a,b){var d=b;"string"===typeof a&&"$"===a.charAt(0)&&"$"===a.charAt(1)?d=void 0:ac(b)?d="$WINDOW":b&&ia.document===b?d="$DOCUMENT":bc(b)&&(d="$SCOPE");return d}function ec(a,b){if(!U(a))return Pa(b)||(b=b?2:null),JSON.stringify(a,he,b)}function ie(a){return na(a)?JSON.parse(a):a}function nd(a,b){a=a.replace(Xf,"");
a=Date.parse("Jan 01, 1970 00:00:00 "+a)/6E4;return Ua(a)?b:a}function je(a,b){a=new Date(a.getTime());a.setMinutes(a.getMinutes()+b);return a}function od(a,b,d){d=d?-1:1;var c=a.getTimezoneOffset();b=nd(b,c);return je(a,d*(b-c))}function jb(a){a=da(a).clone().empty();var b=da("<div></div>").append(a).html();try{return a[0].nodeType===wb?xa(b):b.match(/^(<[^>]+>)/)[1].replace(/^<([\w-]+)/,function(d,c){return"<"+xa(c)})}catch(d){return xa(b)}}function ke(a){try{return decodeURIComponent(a)}catch(b){}}
function pd(a){var b={};I((a||"").split("&"),function(d){if(d){var c=d=d.replace(/\+/g,"%20");var e=d.indexOf("=");if(-1!==e){c=d.substring(0,e);var g=d.substring(e+1)}c=ke(c);R(c)&&(g=R(g)?ke(g):!0,bb.call(b,c)?oa(b[c])?b[c].push(g):b[c]=[b[c],g]:b[c]=g)}});return b}function qd(a){var b=[];I(a,function(d,c){oa(d)?I(d,function(e){b.push(Za(c,!0)+(!0===e?"":"="+Za(e,!0)))}):b.push(Za(c,!0)+(!0===d?"":"="+Za(d,!0)))});return b.length?b.join("&"):""}function fc(a){return Za(a,!0).replace(/%26/gi,"&").replace(/%3D/gi,
"=").replace(/%2B/gi,"+")}function Za(a,b){return encodeURIComponent(a).replace(/%40/gi,"@").replace(/%3A/gi,":").replace(/%24/g,"$").replace(/%2C/gi,",").replace(/%3B/gi,";").replace(/%20/g,b?"%20":"+")}function Yf(a,b){var d,c=Nb.length;for(d=0;d<c;++d){var e=Nb[d]+b;if(na(e=a.getAttribute(e)))return e}return null}function Zf(a,b){var d,c,e={};I(Nb,function(g){g+="app";!d&&a.hasAttribute&&a.hasAttribute(g)&&(d=a,c=a.getAttribute(g))});I(Nb,function(g){g+="app";var f;!d&&(f=a.querySelector("["+g.replace(":",
"\\:")+"]"))&&(d=f,c=f.getAttribute(g))});d&&($f?(e.strictDi=null!==Yf(d,"strict-di"),b(d,c?[c]:[],e)):ia.console.error("AngularJS: disabling automatic bootstrap. <script> protocol indicates an extension, document.location.href does not match."))}function le(a,b,d){fa(d)||(d={});d=Aa({strictDi:!1},d);var c=function(){a=da(a);if(a.injector()){var f=a[0]===ia.document?"document":jb(a);throw Cb("btstrpd",f.replace(/</,"&lt;").replace(/>/,"&gt;"));}b=b||[];b.unshift(["$provide",function(k){k.value("$rootElement",
a)}]);d.debugInfoEnabled&&b.push(["$compileProvider",function(k){k.debugInfoEnabled(!0)}]);b.unshift("ng");f=gc(b,d.strictDi);f.invoke(["$rootScope","$rootElement","$compile","$injector",function(k,h,l,n){k.$apply(function(){h.data("$injector",n);l(h)(k)})}]);return f},e=/^NG_ENABLE_DEBUG_INFO!/,g=/^NG_DEFER_BOOTSTRAP!/;ia&&e.test(ia.name)&&(d.debugInfoEnabled=!0,ia.name=ia.name.replace(e,""));if(ia&&!g.test(ia.name))return c();ia.name=ia.name.replace(g,"");Va.resumeBootstrap=function(f){I(f,function(k){b.push(k)});
return c()};ca(Va.resumeDeferredBootstrap)&&Va.resumeDeferredBootstrap()}function ag(){ia.name="NG_ENABLE_DEBUG_INFO!"+ia.name;ia.location.reload()}function bg(a){a=Va.element(a).injector();if(!a)throw Cb("test");return a.get("$$testability")}function me(a,b){b=b||"_";return a.replace(cg,function(d,c){return(c?b:"")+d.toLowerCase()})}function hc(a,b,d){if(!a)throw Cb("areq",b||"?",d||"required");return a}function vc(a,b,d){d&&oa(a)&&(a=a[a.length-1]);hc(ca(a),b,"not a function, got "+(a&&"object"===
typeof a?a.constructor.name||"Object":typeof a));return a}function Ob(a,b){if("hasOwnProperty"===a)throw Cb("badname",b);}function ne(a,b,d){if(!b)return a;b=b.split(".");for(var c,e=a,g=b.length,f=0;f<g;f++)c=b[f],a&&(a=(e=a)[c]);return!d&&ca(a)?Mb(e,a):a}function wc(a){for(var b=a[0],d=a[a.length-1],c,e=1;b!==d&&(b=b.nextSibling);e++)if(c||a[e]!==b)c||(c=da(hb.call(a,0,e))),c.push(b);return c||a}function Ea(){return Object.create(null)}function rd(a){if(null==a)return"";switch(typeof a){case "string":break;
case "number":a=""+a;break;default:a=!kd(a)||oa(a)||Xa(a)?ec(a):a.toString()}return a}function dg(a){function b(e,g,f){return e[g]||(e[g]=f())}var d=va("$injector"),c=va("ng");a=b(a,"angular",Object);a.$$minErr=a.$$minErr||va;return b(a,"module",function(){var e={};return function(g,f,k){var h={};if("hasOwnProperty"===g)throw c("badname","module");f&&e.hasOwnProperty(g)&&(e[g]=null);return b(e,g,function(){function l(C,D,y,v){v||(v=q);return function(){v[y||"push"]([C,D,arguments]);return F}}function n(C,
D,y){y||(y=q);return function(v,p){p&&ca(p)&&(p.$$moduleName=g);y.push([C,D,arguments]);return F}}if(!f)throw d("nomod",g);var q=[],t=[],w=[],H=l("$injector","invoke","push",t),F={_invokeQueue:q,_configBlocks:t,_runBlocks:w,info:function(C){if(R(C)){if(!fa(C))throw c("aobj","value");h=C;return this}return h},requires:f,name:g,provider:n("$provide","provider"),factory:n("$provide","factory"),service:n("$provide","service"),value:l("$provide","value"),constant:l("$provide","constant","unshift"),decorator:n("$provide",
"decorator",t),animation:n("$animateProvider","register"),filter:n("$filterProvider","register"),controller:n("$controllerProvider","register"),directive:n("$compileProvider","directive"),component:n("$compileProvider","component"),config:H,run:function(C){w.push(C);return this}};k&&H(k);return F})}})}function kb(a,b){if(oa(a)){b=b||[];for(var d=0,c=a.length;d<c;d++)b[d]=a[d]}else if(fa(a))for(d in b=b||{},a)if("$"!==d.charAt(0)||"$"!==d.charAt(1))b[d]=a[d];return b||a}function eg(a,b){var d=[];fd(b)&&
(a=Va.copy(a,null,b));return JSON.stringify(a,function(c,e){e=he(c,e);if(fa(e)){if(0<=d.indexOf(e))return"...";d.push(e)}return e})}function Db(a,b){return b.toUpperCase()}function sd(a){a=a.nodeType;return 1===a||!a||9===a}function oe(a,b){var d=b.createDocumentFragment(),c=[];if(td.test(a)){b=d.appendChild(b.createElement("div"));var e=(fg.exec(a)||["",""])[1].toLowerCase();e=eb[e]||eb._default;b.innerHTML=e[1]+a.replace(gg,"<$1></$2>")+e[2];for(a=e[0];a--;)b=b.lastChild;c=dc(c,b.childNodes);b=
d.firstChild;b.textContent=""}else c.push(b.createTextNode(a));d.textContent="";d.innerHTML="";I(c,function(g){d.appendChild(g)});return d}function Ha(a){if(a instanceof Ha)return a;if(na(a)){a=Ca(a);var b=!0}if(!(this instanceof Ha)){if(b&&"<"!==a.charAt(0))throw ud("nosel");return new Ha(a)}if(b){b=ia.document;var d;a=(d=hg.exec(a))?[b.createElement(d[1])]:(d=oe(a,b))?d.childNodes:[];vd(this,a)}else ca(a)?pe(a):vd(this,a)}function wd(a){return a.cloneNode(!0)}function xc(a,b){!b&&sd(a)&&da.cleanData([a]);
a.querySelectorAll&&da.cleanData(a.querySelectorAll("*"))}function qe(a,b,d,c){if(R(c))throw ud("offargs");var e=(c=yc(a))&&c.events,g=c&&c.handle;if(g)if(b){var f=function(k){var h=e[k];R(d)&&cc(h||[],d);R(d)&&h&&0<h.length||(a.removeEventListener(k,g),delete e[k])};I(b.split(" "),function(k){f(k);zc[k]&&f(zc[k])})}else for(b in e)"$destroy"!==b&&a.removeEventListener(b,g),delete e[b]}function xd(a,b){var d=a.ng339,c=d&&ic[d];c&&(b?delete c.data[b]:(c.handle&&(c.events.$destroy&&c.handle({},"$destroy"),
qe(a)),delete ic[d],a.ng339=void 0))}function yc(a,b){var d=a.ng339;d=d&&ic[d];b&&!d&&(a.ng339=d=++ig,d=ic[d]={events:{},data:{},handle:void 0});return d}function yd(a,b,d){if(sd(a)){var c,e=R(d),g=!e&&b&&!fa(b),f=!b;a=(a=yc(a,!g))&&a.data;if(e)a[b.replace(Ac,Db)]=d;else{if(f)return a;if(g)return a&&a[b.replace(Ac,Db)];for(c in b)a[c.replace(Ac,Db)]=b[c]}}}function Bc(a,b){return a.getAttribute?-1<(" "+(a.getAttribute("class")||"")+" ").replace(/[\n\t]/g," ").indexOf(" "+b+" "):!1}function Cc(a,b){if(b&&
a.setAttribute){var d=(" "+(a.getAttribute("class")||"")+" ").replace(/[\n\t]/g," "),c=d;I(b.split(" "),function(e){e=Ca(e);c=c.replace(" "+e+" "," ")});c!==d&&a.setAttribute("class",Ca(c))}}function Dc(a,b){if(b&&a.setAttribute){var d=(" "+(a.getAttribute("class")||"")+" ").replace(/[\n\t]/g," "),c=d;I(b.split(" "),function(e){e=Ca(e);-1===c.indexOf(" "+e+" ")&&(c+=e+" ")});c!==d&&a.setAttribute("class",Ca(c))}}function vd(a,b){if(b)if(b.nodeType)a[a.length++]=b;else{var d=b.length;if("number"===
typeof d&&b.window!==b){if(d)for(var c=0;c<d;c++)a[a.length++]=b[c]}else a[a.length++]=b}}function re(a,b){return Ec(a,"$"+(b||"ngController")+"Controller")}function Ec(a,b,d){9===a.nodeType&&(a=a.documentElement);for(b=oa(b)?b:[b];a;){for(var c=0,e=b.length;c<e;c++)if(R(d=da.data(a,b[c])))return d;a=a.parentNode||11===a.nodeType&&a.host}}function se(a){for(xc(a,!0);a.firstChild;)a.removeChild(a.firstChild)}function Fc(a,b){b||xc(a);(b=a.parentNode)&&b.removeChild(a)}function jg(a,b){b=b||ia;if("complete"===
b.document.readyState)b.setTimeout(a);else da(b).on("load",a)}function pe(a){function b(){ia.document.removeEventListener("DOMContentLoaded",b);ia.removeEventListener("load",b);a()}"complete"===ia.document.readyState?ia.setTimeout(a):(ia.document.addEventListener("DOMContentLoaded",b),ia.addEventListener("load",b))}function te(a,b){return(b=Gc[b.toLowerCase()])&&ue[ib(a)]&&b}function kg(a,b){var d=function(c,e){c.isDefaultPrevented=function(){return c.defaultPrevented};var g=(e=b[e||c.type])?e.length:
0;if(g){if(U(c.immediatePropagationStopped)){var f=c.stopImmediatePropagation;c.stopImmediatePropagation=function(){c.immediatePropagationStopped=!0;c.stopPropagation&&c.stopPropagation();f&&f.call(c)}}c.isImmediatePropagationStopped=function(){return!0===c.immediatePropagationStopped};var k=e.specialHandlerWrapper||lg;1<g&&(e=kb(e));for(var h=0;h<g;h++)c.isImmediatePropagationStopped()||k(a,c,e[h])}};d.elem=a;return d}function lg(a,b,d){d.call(a,b)}function mg(a,b,d){var c=b.relatedTarget;c&&(c===
a||og.call(a,c))||d.call(a,b)}function pg(){this.$get=function(){return Aa(Ha,{hasClass:function(a,b){a.attr&&(a=a[0]);return Bc(a,b)},addClass:function(a,b){a.attr&&(a=a[0]);return Dc(a,b)},removeClass:function(a,b){a.attr&&(a=a[0]);return Cc(a,b)}})}}function Pb(a,b){var d=a&&a.$$hashKey;if(d)return"function"===typeof d&&(d=a.$$hashKey()),d;d=typeof a;return d="function"===d||"object"===d&&null!==a?a.$$hashKey=d+":"+(b||Sf)():d+":"+a}function ve(){this._keys=[];this._values=[];this._lastKey=NaN;
this._lastIndex=-1}function we(a){a=Function.prototype.toString.call(a).replace(qg,"");return a.match(rg)||a.match(sg)}function tg(a){return(a=we(a))?"function("+(a[1]||"").replace(/[\s\r\n]+/," ")+")":"fn"}function gc(a,b){function d(C){return function(D,y){if(fa(D))I(D,gd(C));else return C(D,y)}}function c(C,D){Ob(C,"service");if(ca(D)||oa(D))D=t.instantiate(D);if(!D.$get)throw Eb("pget",C);return q[C+"Provider"]=D}function e(C,D){return function(){var y=F.invoke(D,this);if(U(y))throw Eb("undef",
C);return y}}function g(C,D,y){return c(C,{$get:!1!==y?e(C,D):D})}function f(C){hc(U(C)||oa(C),"modulesToLoad","not an array");var D=[],y;I(C,function(v){function p(r){var m;var x=0;for(m=r.length;x<m;x++){var G=r[x],B=t.get(G[0]);B[G[1]].apply(B,G[2])}}if(!n.get(v)){n.set(v,!0);try{na(v)?(y=zd(v),F.modules[v]=y,D=D.concat(f(y.requires)).concat(y._runBlocks),p(y._invokeQueue),p(y._configBlocks)):ca(v)?D.push(t.invoke(v)):oa(v)?D.push(t.invoke(v)):vc(v,"module")}catch(r){throw oa(v)&&(v=v[v.length-
1]),r.message&&r.stack&&-1===r.stack.indexOf(r.message)&&(r=r.message+"\n"+r.stack),Eb("modulerr",v,r.stack||r.message||r);}}});return D}function k(C,D){function y(p,r){if(C.hasOwnProperty(p)){if(C[p]===h)throw Eb("cdep",p+" <- "+l.join(" <- "));return C[p]}try{return l.unshift(p),C[p]=h,C[p]=D(p,r),C[p]}catch(m){throw C[p]===h&&delete C[p],m;}finally{l.shift()}}function v(p,r,m){var x=[];p=gc.$$annotate(p,b,m);for(var G=0,B=p.length;G<B;G++){var A=p[G];if("string"!==typeof A)throw Eb("itkn",A);x.push(r&&
r.hasOwnProperty(A)?r[A]:y(A,m))}return x}return{invoke:function(p,r,m,x){"string"===typeof m&&(x=m,m=null);m=v(p,m,x);oa(p)&&(p=p[p.length-1]);x=p;if(qb||"function"!==typeof x)x=!1;else{var G=x.$$ngIsClass;vb(G)||(G=x.$$ngIsClass=/^(?:class\b|constructor\()/.test(Function.prototype.toString.call(x)));x=G}return x?(m.unshift(null),new (Function.prototype.bind.apply(p,m))):p.apply(r,m)},instantiate:function(p,r,m){var x=oa(p)?p[p.length-1]:p;p=v(p,r,m);p.unshift(null);return new (Function.prototype.bind.apply(x,
p))},get:y,annotate:gc.$$annotate,has:function(p){return q.hasOwnProperty(p+"Provider")||C.hasOwnProperty(p)}}}b=!0===b;var h={},l=[],n=new Hc,q={$provide:{provider:d(c),factory:d(g),service:d(function(C,D){return g(C,["$injector",function(y){return y.instantiate(D)}])}),value:d(function(C,D){return g(C,cb(D),!1)}),constant:d(function(C,D){Ob(C,"constant");q[C]=D;w[C]=D}),decorator:function(C,D){var y=t.get(C+"Provider"),v=y.$get;y.$get=function(){var p=F.invoke(v,y);return F.invoke(D,null,{$delegate:p})}}}},
t=q.$injector=k(q,function(C,D){Va.isString(D)&&l.push(D);throw Eb("unpr",l.join(" <- "));}),w={},H=k(w,function(C,D){D=t.get(C+"Provider",D);return F.invoke(D.$get,D,void 0,C)}),F=H;q.$injectorProvider={$get:cb(H)};F.modules=t.modules=Ea();a=f(a);F=H.get("$injector");F.strictDi=b;I(a,function(C){C&&F.invoke(C)});F.loadNewModules=function(C){I(f(C),function(D){D&&F.invoke(D)})};return F}function ug(){var a=!0;this.disableAutoScrolling=function(){a=!1};this.$get=["$window","$location","$rootScope",
function(b,d,c){function e(h){var l=null;Array.prototype.some.call(h,function(n){if("a"===ib(n))return l=n,!0});return l}function g(h){if(h){h.scrollIntoView();var l=f.yOffset;ca(l)?l=l():id(l)?(l=l[0],l="fixed"!==b.getComputedStyle(l).position?0:l.getBoundingClientRect().bottom):Pa(l)||(l=0);l&&(h=h.getBoundingClientRect().top,b.scrollBy(0,h-l))}else b.scrollTo(0,0)}function f(h){h=na(h)?h:Pa(h)?h.toString():d.hash();var l;h?(l=k.getElementById(h))?g(l):(l=e(k.getElementsByName(h)))?g(l):"top"===
h&&g(null):g(null)}var k=b.document;a&&c.$watch(function(){return d.hash()},function(h,l){h===l&&""===h||jg(function(){c.$evalAsync(f)})});return f}]}function jc(a,b){if(!a&&!b)return"";if(!a)return b;if(!b)return a;oa(a)&&(a=a.join(" "));oa(b)&&(b=b.join(" "));return a+" "+b}function vg(a){na(a)&&(a=a.split(" "));var b=Ea();I(a,function(d){d.length&&(b[d]=!0)});return b}function Fb(a){return fa(a)?a:{}}function wg(a,b,d,c){function e(B){try{B.apply(null,hb.call(arguments,1))}finally{if(H--,0===H)for(;F.length;)try{F.pop()()}catch(A){d.error(A)}}}
function g(){p=null;k()}function f(){C=r();C=U(C)?null:C;db(C,G)&&(C=G);D=G=C}function k(){var B=D;f();if(y!==h.url()||B!==C)y=h.url(),D=C,I(m,function(A){A(h.url(),C)})}var h=this,l=a.location,n=a.history,q=a.setTimeout,t=a.clearTimeout,w={};h.isMock=!1;var H=0,F=[];h.$$completeOutstandingRequest=e;h.$$incOutstandingRequestCount=function(){H++};h.notifyWhenNoOutstandingRequests=function(B){0===H?B():F.push(B)};var C,D,y=l.href,v=b.find("base"),p=null,r=c.history?function(){try{return n.state}catch(B){}}:
ja;f();h.url=function(B,A,E){U(E)&&(E=null);l!==a.location&&(l=a.location);n!==a.history&&(n=a.history);if(B){var L=D===E;if(y===B&&(!c.history||L))return h;var Q=y&&Gb(y)===Gb(B);y=B;D=E;!c.history||Q&&L?(Q||(p=B),A?l.replace(B):Q?(A=l,E=B.indexOf("#"),E=-1===E?"":B.substr(E),A.hash=E):l.href=B,l.href!==B&&(p=B)):(n[A?"replaceState":"pushState"](E,"",B),f());p&&(p=B);return h}return p||l.href.replace(/%27/g,"'")};h.state=function(){return C};var m=[],x=!1,G=null;h.onUrlChange=function(B){if(!x){if(c.history)da(a).on("popstate",
g);da(a).on("hashchange",g);x=!0}m.push(B);return B};h.$$applicationDestroyed=function(){da(a).off("hashchange popstate",g)};h.$$checkUrlChange=k;h.baseHref=function(){var B=v.attr("href");return B?B.replace(/^(https?:)?\/\/[^/]*/,""):""};h.defer=function(B,A){H++;var E=q(function(){delete w[E];e(B)},A||0);w[E]=!0;return E};h.defer.cancel=function(B){return w[B]?(delete w[B],t(B),e(ja),!0):!1}}function xg(){this.$get=["$window","$log","$sniffer","$document",function(a,b,d,c){return new wg(a,c,b,d)}]}
function yg(){this.$get=function(){function a(d,c){function e(w){w!==q&&(t?t===w&&(t=w.n):t=w,g(w.n,w.p),g(w,q),q=w,q.n=null)}function g(w,H){w!==H&&(w&&(w.p=H),H&&(H.n=w))}if(d in b)throw va("$cacheFactory")("iid",d);var f=0,k=Aa({},c,{id:d}),h=Ea(),l=c&&c.capacity||Number.MAX_VALUE,n=Ea(),q=null,t=null;return b[d]={put:function(w,H){if(!U(H)){if(l<Number.MAX_VALUE){var F=n[w]||(n[w]={key:w});e(F)}w in h||f++;h[w]=H;f>l&&this.remove(t.key);return H}},get:function(w){if(l<Number.MAX_VALUE){var H=
n[w];if(!H)return;e(H)}return h[w]},remove:function(w){if(l<Number.MAX_VALUE){var H=n[w];if(!H)return;H===q&&(q=H.p);H===t&&(t=H.n);g(H.n,H.p);delete n[w]}w in h&&(delete h[w],f--)},removeAll:function(){h=Ea();f=0;n=Ea();q=t=null},destroy:function(){n=k=h=null;delete b[d]},info:function(){return Aa({},k,{size:f})}}}var b={};a.info=function(){var d={};I(b,function(c,e){d[e]=c.info()});return d};a.get=function(d){return b[d]};return a}}function zg(){this.$get=["$cacheFactory",function(a){return a("templates")}]}
function xe(a,b){function d(y,v,p){var r=/^([@&<]|=(\*?))(\??)\s*([\w$]*)$/,m=Ea();I(y,function(x,G){x=x.trim();if(x in q)m[G]=q[x];else{var B=x.match(r);if(!B)throw Ka("iscp",v,G,x,p?"controller bindings definition":"isolate scope definition");m[G]={mode:B[1][0],collection:"*"===B[2],optional:"?"===B[3],attrName:B[4]||G};B[4]&&(q[x]=m[G])}});return m}function c(y){var v=y.charAt(0);if(!v||v!==xa(v))throw Ka("baddir",y);if(y!==y.trim())throw Ka("baddir",y);}function e(y){var v=y.require||y.controller&&
y.name;!oa(v)&&fa(v)&&I(v,function(p,r){var m=p.match(l);p.substring(m[0].length)||(v[r]=m[0]+r)});return v}var g={},f=/^\s*directive:\s*([\w-]+)\s+(.*)$/,k=/(([\w-]+)(?::([^;]+))?;?)/,h=Wf("ngSrc,ngSrcset,src,srcset"),l=/^(?:(\^\^?)?(\?)?(\^\^?)?)?/,n=/^(on[a-z]+|formaction)$/,q=Ea();this.directive=function r(v,p){hc(v,"name");Ob(v,"directive");na(v)?(c(v),hc(p,"directiveFactory"),g.hasOwnProperty(v)||(g[v]=[],a.factory(v+"Directive",["$injector","$exceptionHandler",function(m,x){var G=[];I(g[v],
function(B,A){try{var E=m.invoke(B);ca(E)?E={compile:cb(E)}:!E.compile&&E.link&&(E.compile=cb(E.link));E.priority=E.priority||0;E.index=A;E.name=E.name||v;E.require=e(E);A=E;var L=E.restrict;if(L&&(!na(L)||!/[EACM]/.test(L)))throw Ka("badrestrict",L,v);A.restrict=L||"EA";E.$$moduleName=B.$$moduleName;G.push(E)}catch(Q){x(Q)}});return G}])),g[v].push(p)):I(v,gd(r));return this};this.component=function m(p,r){function x(B){function A(Q){return ca(Q)||oa(Q)?function(S,X){return B.invoke(Q,this,{$element:S,
$attrs:X})}:Q}var E=r.template||r.templateUrl?r.template:"",L={controller:G,controllerAs:Ag(r.controller)||r.controllerAs||"$ctrl",template:A(E),templateUrl:A(r.templateUrl),transclude:r.transclude,scope:{},bindToController:r.bindings||{},restrict:"E",require:r.require};I(r,function(Q,S){"$"===S.charAt(0)&&(L[S]=Q)});return L}if(!na(p))return I(p,gd(Mb(this,m))),this;var G=r.controller||function(){};I(r,function(B,A){"$"===A.charAt(0)&&(x[A]=B,ca(G)&&(G[A]=B))});x.$inject=["$injector"];return this.directive(p,
x)};this.aHrefSanitizationWhitelist=function(p){return R(p)?(b.aHrefSanitizationWhitelist(p),this):b.aHrefSanitizationWhitelist()};this.imgSrcSanitizationWhitelist=function(p){return R(p)?(b.imgSrcSanitizationWhitelist(p),this):b.imgSrcSanitizationWhitelist()};var t=!0;this.debugInfoEnabled=function(p){return R(p)?(t=p,this):t};var w=!1;this.preAssignBindingsEnabled=function(p){return R(p)?(w=p,this):w};var H=!1;this.strictComponentBindingsEnabled=function(p){return R(p)?(H=p,this):H};var F=10;this.onChangesTtl=
function(p){return arguments.length?(F=p,this):F};var C=!0;this.commentDirectivesEnabled=function(p){return arguments.length?(C=p,this):C};var D=!0;this.cssClassDirectivesEnabled=function(p){return arguments.length?(D=p,this):D};this.$get=["$injector","$interpolate","$exceptionHandler","$templateRequest","$parse","$controller","$rootScope","$sce","$animate","$$sanitizeUri",function(p,r,m,x,G,B,A,E,L,Q){function S(){try{if(!--ye)throw Hb=void 0,Ka("infchng",F);A.$apply(function(){for(var u=0,z=Hb.length;u<
z;++u)try{Hb[u]()}catch(J){m(J)}Hb=void 0})}finally{ye++}}function X(u,z){if(z){var J=Object.keys(z),M;var N=0;for(M=J.length;N<M;N++){var K=J[N];this[K]=z[K]}}else this.$attr={};this.$$element=u}function ha(u,z,J){ze.innerHTML="<span "+z+">";z=ze.firstChild.attributes;var M=z[0];z.removeNamedItem(M.name);M.value=J;u.attributes.setNamedItem(M)}function ka(u,z){try{u.addClass(z)}catch(J){}}function ea(u,z,J,M,N){u instanceof da||(u=da(u));var K=ma(u,z,u,J,M,N);ea.$$addScopeClass(u);var aa=null;return function(O,
Z,V){if(!u)throw Ka("multilink");hc(O,"scope");N&&N.needsNewScope&&(O=O.$parent.$new());V=V||{};var W=V.parentBoundTranscludeFn,ba=V.transcludeControllers;V=V.futureParentElement;W&&W.$$boundTransclude&&(W=W.$$boundTransclude);aa||(aa=(V=V&&V[0])?"foreignobject"!==ib(V)&&Ta.call(V).match(/SVG/)?"svg":"html":"html");V="html"!==aa?da(Ad(aa,da("<div></div>").append(u).html())):Z?Qb.clone.call(u):u;if(ba)for(var T in ba)V.data("$"+T+"Controller",ba[T].instance);ea.$$addScopeInfo(V,O);Z&&Z(V,O);K&&K(O,
V,V,W);Z||(u=K=null);return V}}function ma(u,z,J,M,N,K){function aa(sa,pa,Ga,Fa){var za,qa;if(ta){var Y=Array(pa.length);for(za=0;za<O.length;za+=3){var La=O[za];Y[La]=pa[La]}}else Y=pa;za=0;for(qa=O.length;za<qa;){var Ia=Y[O[za++]];pa=O[za++];La=O[za++];if(pa){if(pa.scope){var $a=sa.$new();ea.$$addScopeInfo(da(Ia),$a)}else $a=sa;var xb=pa.transcludeOnThisElement?ya(sa,pa.transclude,Fa):!pa.templateOnThisElement&&Fa?Fa:!Fa&&z?ya(sa,z):null;pa(La,$a,Ia,Ga,xb)}else La&&La(sa,Ia.childNodes,void 0,Fa)}}
for(var O=[],Z=oa(u)||u instanceof da,V,W,ba,T,ta,ra=0;ra<u.length;ra++){V=new X;11===qb&&la(u,ra,Z);W=ua(u[ra],[],V,0===ra?M:void 0,N);(K=W.length?Ae(W,u[ra],V,z,J,null,[],[],K):null)&&K.scope&&ea.$$addScopeClass(V.$$element);V=K&&K.terminal||!(ba=u[ra].childNodes)||!ba.length?null:ma(ba,K?(K.transcludeOnThisElement||!K.templateOnThisElement)&&K.transclude:z);if(K||V)O.push(ra,K,V),T=!0,ta=ta||K;K=null}return T?aa:null}function la(u,z,J){var M=u[z],N=M.parentNode;if(M.nodeType===wb)for(;;){var K=
N?M.nextSibling:u[z+1];if(!K||K.nodeType!==wb)break;M.nodeValue+=K.nodeValue;K.parentNode&&K.parentNode.removeChild(K);J&&K===u[z+1]&&u.splice(z+1,1)}}function ya(u,z,J){function M(aa,O,Z,V,W){aa||(aa=u.$new(!1,W),aa.$$transcluded=!0);return z(aa,O,{parentBoundTranscludeFn:J,transcludeControllers:Z,futureParentElement:V})}var N=M.$$slots=Ea(),K;for(K in z.$$slots)N[K]=z.$$slots[K]?ya(u,z.$$slots[K],J):null;return M}function ua(u,z,J,M,N){var K=J.$attr;switch(u.nodeType){case 1:var aa=ib(u);Ic(z,lb(aa),
"E",M,N);for(var O,Z,V,W,ba=u.attributes,T=0,ta=ba&&ba.length;T<ta;T++){var ra=!1,sa=!1;O=ba[T];Z=O.name;V=O.value;O=lb(Z);(W=Bg.test(O))&&(Z=Z.replace(Be,"").substr(8).replace(/_(.)/g,function(pa,Ga){return Ga.toUpperCase()}));(O=O.match(Cg))&&Dg(O[1])&&(ra=Z,sa=Z.substr(0,Z.length-5)+"end",Z=Z.substr(0,Z.length-6));O=lb(Z.toLowerCase());K[O]=Z;if(W||!J.hasOwnProperty(O))J[O]=V,te(u,O)&&(J[O]=!0);Eg(u,z,V,O,W);Ic(z,O,"A",M,N,ra,sa)}"input"===aa&&"hidden"===u.getAttribute("type")&&u.setAttribute("autocomplete",
"off");if(!Fg)break;K=u.className;fa(K)&&(K=K.animVal);if(na(K)&&""!==K)for(;u=k.exec(K);)O=lb(u[2]),Ic(z,O,"C",M,N)&&(J[O]=Ca(u[3])),K=K.substr(u.index+u[0].length);break;case wb:Gg(z,u.nodeValue);break;case 8:Hg&&mb(u,z,J,M,N)}z.sort(Ig);return z}function mb(u,z,J,M,N){try{var K=f.exec(u.nodeValue);if(K){var aa=lb(K[1]);Ic(z,aa,"M",M,N)&&(J[aa]=Ca(K[2]))}}catch(O){}}function Ce(u,z,J){var M=[],N=0;if(z&&u.hasAttribute&&u.hasAttribute(z)){do{if(!u)throw Ka("uterdir",z,J);1===u.nodeType&&(u.hasAttribute(z)&&
N++,u.hasAttribute(J)&&N--);M.push(u);u=u.nextSibling}while(0<N)}else M.push(u);return da(M)}function De(u,z,J){return function(M,N,K,aa,O){N=Ce(N[0],z,J);return u(M,N,K,aa,O)}}function Bd(u,z,J,M,N,K){var aa;return u?ea(z,J,M,N,K):function(){aa||(aa=ea(z,J,M,N,K),z=J=K=null);return aa.apply(this,arguments)}}function Ae(u,z,J,M,N,K,aa,O,Z){function V(Da,wa,fb,ab){if(Da){fb&&(Da=De(Da,fb,ab));Da.require=Y.require;Da.directiveName=La;if(ra===Y||Y.$$isolateScope)Da=Ee(Da,{isolateScope:!0});aa.push(Da)}if(wa){fb&&
(wa=De(wa,fb,ab));wa.require=Y.require;wa.directiveName=La;if(ra===Y||Y.$$isolateScope)wa=Ee(wa,{isolateScope:!0});O.push(wa)}}function W(Da,wa,fb,ab,Rb){function Jg(Ma,Na,Wa,Jc){var Cd;bc(Ma)||(Jc=Wa,Wa=Na,Na=Ma,Ma=void 0);za&&(Cd=nb);Wa||(Wa=za?Sa.parent():Sa);if(Jc){var Dd=Rb.$$slots[Jc];if(Dd)return Dd(Ma,Na,Cd,Wa,Kc);if(U(Dd))throw Ka("noslot",Jc,jb(Sa));}else return Rb(Ma,Na,Cd,Wa,Kc)}var nb;if(z===fb){ab=J;var Sa=J.$$element}else Sa=da(fb),ab=new X(Sa,J);var Sb=wa;if(ra)var rb=wa.$new(!0);
else T&&(Sb=wa.$parent);if(Rb){var kc=Jg;kc.$$boundTransclude=Rb;kc.isSlotFilled=function(Ma){return!!Rb.$$slots[Ma]}}ta&&(nb=Kg(Sa,ab,kc,ta,rb,wa,ra));if(ra){ea.$$addScopeInfo(Sa,rb,!0,!(sa&&(sa===ra||sa===ra.$$originalDirective)));ea.$$addScopeClass(Sa,!0);rb.$$isolateBindings=ra.$$isolateBindings;var gb=Lc(wa,ab,rb,rb.$$isolateBindings,ra);gb.removeWatches&&rb.$on("$destroy",gb.removeWatches)}for(ob in nb){gb=ta[ob];var Ba=nb[ob];var Mc=gb.$$bindings.bindToController;if(w){Ba.bindingInfo=Mc?Lc(Sb,
ab,Ba.instance,Mc,gb):{};var Ed=Ba();Ed!==Ba.instance&&(Ba.instance=Ed,Sa.data("$"+gb.name+"Controller",Ed),Ba.bindingInfo.removeWatches&&Ba.bindingInfo.removeWatches(),Ba.bindingInfo=Lc(Sb,ab,Ba.instance,Mc,gb))}else Ba.instance=Ba(),Sa.data("$"+gb.name+"Controller",Ba.instance),Ba.bindingInfo=Lc(Sb,ab,Ba.instance,Mc,gb)}I(ta,function(Ma,Na){var Wa=Ma.require;Ma.bindToController&&!oa(Wa)&&fa(Wa)&&Aa(nb[Na].instance,lc(Na,Wa,Sa,nb))});I(nb,function(Ma){var Na=Ma.instance;if(ca(Na.$onChanges))try{Na.$onChanges(Ma.bindingInfo.initialChanges)}catch(Wa){m(Wa)}if(ca(Na.$onInit))try{Na.$onInit()}catch(Wa){m(Wa)}ca(Na.$doCheck)&&
(Sb.$watch(function(){Na.$doCheck()}),Na.$doCheck());ca(Na.$onDestroy)&&Sb.$on("$destroy",function(){Na.$onDestroy()})});var ob=0;for(gb=aa.length;ob<gb;ob++)Ba=aa[ob],Fe(Ba,Ba.isolateScope?rb:wa,Sa,ab,Ba.require&&lc(Ba.directiveName,Ba.require,Sa,nb),kc);var Kc=wa;ra&&(ra.template||null===ra.templateUrl)&&(Kc=rb);Da&&Da(Kc,fb.childNodes,void 0,Rb);for(ob=O.length-1;0<=ob;ob--)Ba=O[ob],Fe(Ba,Ba.isolateScope?rb:wa,Sa,ab,Ba.require&&lc(Ba.directiveName,Ba.require,Sa,nb),kc);I(nb,function(Ma){Ma=Ma.instance;
ca(Ma.$postLink)&&Ma.$postLink()})}Z=Z||{};for(var ba=-Number.MAX_VALUE,T=Z.newScopeDirective,ta=Z.controllerDirectives,ra=Z.newIsolateScopeDirective,sa=Z.templateDirective,pa=Z.nonTlbTranscludeDirective,Ga=!1,Fa=!1,za=Z.hasElementTranscludeDirective,qa=J.$$element=da(z),Y,La,Ia,$a=M,xb,yb=!1,Nc=!1,Oa,zb=0,Tb=u.length;zb<Tb;zb++){Y=u[zb];var Oc=Y.$$start,Fd=Y.$$end;Oc&&(qa=Ce(z,Oc,Fd));Ia=void 0;if(ba>Y.priority)break;if(Oa=Y.scope)Y.templateUrl||(fa(Oa)?(Ub("new/isolated scope",ra||T,Y,qa),ra=Y):
Ub("new/isolated scope",ra,Y,qa)),T=T||Y;La=Y.name;if(!yb&&(Y.replace&&(Y.templateUrl||Y.template)||Y.transclude&&!Y.$$tlb)){for(Oa=zb+1;yb=u[Oa++];)if(yb.transclude&&!yb.$$tlb||yb.replace&&(yb.templateUrl||yb.template)){Nc=!0;break}yb=!0}!Y.templateUrl&&Y.controller&&(ta=ta||Ea(),Ub("'"+La+"' controller",ta[La],Y,qa),ta[La]=Y);if(Oa=Y.transclude)if(Ga=!0,Y.$$tlb||(Ub("transclusion",pa,Y,qa),pa=Y),"element"===Oa)za=!0,ba=Y.priority,Ia=qa,qa=J.$$element=da(ea.$$createComment(La,J[La])),z=qa[0],Pc(N,
hb.call(Ia,0),z),Ia[0].$$parentNode=Ia[0].parentNode,$a=Bd(Nc,Ia,M,ba,K&&K.name,{nonTlbTranscludeDirective:pa});else{var sb=Ea();if(fa(Oa)){Ia=[];var Ge=Ea(),Gd=Ea();I(Oa,function(Da,wa){var fb="?"===Da.charAt(0);Da=fb?Da.substring(1):Da;Ge[Da]=wa;sb[wa]=null;Gd[wa]=fb});I(qa.contents(),function(Da){var wa=Ge[lb(ib(Da))];wa?(Gd[wa]=!0,sb[wa]=sb[wa]||[],sb[wa].push(Da)):Ia.push(Da)});I(Gd,function(Da,wa){if(!Da)throw Ka("reqslot",wa);});for(var Hd in sb)sb[Hd]&&(sb[Hd]=Bd(Nc,sb[Hd],M))}else Ia=da(wd(z)).contents();
qa.empty();$a=Bd(Nc,Ia,M,void 0,void 0,{needsNewScope:Y.$$isolateScope||Y.$$newScope});$a.$$slots=sb}if(Y.template)if(Fa=!0,Ub("template",sa,Y,qa),sa=Y,Oa=ca(Y.template)?Y.template(qa,J):Y.template,Oa=He(Oa),Y.replace){K=Y;Ia=td.test(Oa)?Ie(Ad(Y.templateNamespace,Ca(Oa))):[];z=Ia[0];if(1!==Ia.length||1!==z.nodeType)throw Ka("tplrt",La,"");Pc(N,qa,z);Tb={$attr:{}};Oa=ua(z,[],Tb);var Lg=u.splice(zb+1,u.length-(zb+1));(ra||T)&&Je(Oa,ra,T);u=u.concat(Oa).concat(Lg);Ke(J,Tb);Tb=u.length}else qa.html(Oa);
if(Y.templateUrl)Fa=!0,Ub("template",sa,Y,qa),sa=Y,Y.replace&&(K=Y),W=Mg(u.splice(zb,u.length-zb),qa,J,N,Ga&&$a,aa,O,{controllerDirectives:ta,newScopeDirective:T!==Y&&T,newIsolateScopeDirective:ra,templateDirective:sa,nonTlbTranscludeDirective:pa}),Tb=u.length;else if(Y.compile)try{xb=Y.compile(qa,J,$a);var Id=Y.$$originalDirective||Y;ca(xb)?V(null,Mb(Id,xb),Oc,Fd):xb&&V(Mb(Id,xb.pre),Mb(Id,xb.post),Oc,Fd)}catch(Da){m(Da,jb(qa))}Y.terminal&&(W.terminal=!0,ba=Math.max(ba,Y.priority))}W.scope=T&&!0===
T.scope;W.transcludeOnThisElement=Ga;W.templateOnThisElement=Fa;W.transclude=$a;Z.hasElementTranscludeDirective=za;return W}function lc(u,z,J,M){if(na(z)){var N=z.match(l);z=z.substring(N[0].length);var K=N[1]||N[3];N="?"===N[2];if("^^"===K)J=J.parent();else var aa=(aa=M&&M[z])&&aa.instance;if(!aa){var O="$"+z+"Controller";aa=K?J.inheritedData(O):J.data(O)}if(!aa&&!N)throw Ka("ctreq",z,u);}else if(oa(z))for(aa=[],K=0,N=z.length;K<N;K++)aa[K]=lc(u,z[K],J,M);else fa(z)&&(aa={},I(z,function(Z,V){aa[V]=
lc(u,Z,J,M)}));return aa||null}function Kg(u,z,J,M,N,K,aa){var O=Ea(),Z;for(Z in M){var V=M[Z],W={$scope:V===aa||V.$$isolateScope?N:K,$element:u,$attrs:z,$transclude:J},ba=V.controller;"@"===ba&&(ba=z[V.name]);W=B(ba,W,!0,V.controllerAs);O[V.name]=W;u.data("$"+V.name+"Controller",W.instance)}return O}function Je(u,z,J){for(var M=0,N=u.length;M<N;M++)u[M]=jd(u[M],{$$isolateScope:z,$$newScope:J})}function Ic(u,z,J,M,N,K,aa){if(z===N)return null;var O=null;if(g.hasOwnProperty(z)){N=p.get(z+"Directive");
for(var Z=0,V=N.length;Z<V;Z++)if(z=N[Z],(U(M)||M>z.priority)&&-1!==z.restrict.indexOf(J)){K&&(z=jd(z,{$$start:K,$$end:aa}));if(!z.$$bindings){var W=O=z,ba=z.name,T={isolateScope:null,bindToController:null};fa(W.scope)&&(!0===W.bindToController?(T.bindToController=d(W.scope,ba,!0),T.isolateScope={}):T.isolateScope=d(W.scope,ba,!1));fa(W.bindToController)&&(T.bindToController=d(W.bindToController,ba,!0));if(T.bindToController&&!W.controller)throw Ka("noctrl",ba);O=O.$$bindings=T;fa(O.isolateScope)&&
(z.$$isolateBindings=O.isolateScope)}u.push(z);O=z}}return O}function Dg(u){if(g.hasOwnProperty(u))for(var z=p.get(u+"Directive"),J=0,M=z.length;J<M;J++)if(u=z[J],u.multiElement)return!0;return!1}function Ke(u,z){var J=z.$attr,M=u.$attr;I(u,function(N,K){"$"!==K.charAt(0)&&(z[K]&&z[K]!==N&&(N=N.length?N+(("style"===K?";":" ")+z[K]):z[K]),u.$set(K,N,!0,J[K]))});I(z,function(N,K){u.hasOwnProperty(K)||"$"===K.charAt(0)||(u[K]=N,"class"!==K&&"style"!==K&&(M[K]=J[K]))})}function Mg(u,z,J,M,N,K,aa,O){var Z=
[],V,W,ba=z[0],T=u.shift(),ta=jd(T,{templateUrl:null,transclude:null,replace:null,$$originalDirective:T}),ra=ca(T.templateUrl)?T.templateUrl(z,J):T.templateUrl,sa=T.templateNamespace;z.empty();x(ra).then(function(pa){pa=He(pa);if(T.replace){pa=td.test(pa)?Ie(Ad(sa,Ca(pa))):[];var Ga=pa[0];if(1!==pa.length||1!==Ga.nodeType)throw Ka("tplrt",T.name,ra);pa={$attr:{}};Pc(M,z,Ga);var Fa=ua(Ga,[],pa);fa(T.scope)&&Je(Fa,!0);u=Fa.concat(u);Ke(J,pa)}else Ga=ba,z.html(pa);u.unshift(ta);V=Ae(u,Ga,J,N,z,T,K,aa,
O);I(M,function(Ia,$a){Ia===Ga&&(M[$a]=z[0])});for(W=ma(z[0].childNodes,N);Z.length;){pa=Z.shift();var za=Z.shift();var qa=Z.shift(),Y=Z.shift();Fa=z[0];if(!pa.$$destroyed){if(za!==ba){var La=za.className;O.hasElementTranscludeDirective&&T.replace||(Fa=wd(Ga));Pc(qa,da(za),Fa);ka(da(Fa),La)}za=V.transcludeOnThisElement?ya(pa,V.transclude,Y):Y;V(W,pa,Fa,M,za)}}Z=null}).catch(function(pa){ld(pa)&&m(pa)});return function(pa,Ga,Fa,za,qa){pa=qa;Ga.$$destroyed||(Z?Z.push(Ga,Fa,za,pa):(V.transcludeOnThisElement&&
(pa=ya(Ga,V.transclude,qa)),V(W,Ga,Fa,za,pa)))}}function Ig(u,z){var J=z.priority-u.priority;return 0!==J?J:u.name!==z.name?u.name<z.name?-1:1:u.index-z.index}function Ub(u,z,J,M){function N(K){return K?" (module: "+K+")":""}if(z)throw Ka("multidir",z.name,N(z.$$moduleName),J.name,N(J.$$moduleName),u,jb(M));}function Gg(u,z){var J=r(z,!0);J&&u.push({priority:0,compile:function(M){M=M.parent();var N=!!M.length;N&&ea.$$addBindingClass(M);return function(K,aa){var O=aa.parent();N||ea.$$addBindingClass(O);
ea.$$addBindingInfo(O,J.expressions);K.$watch(J,function(Z){aa[0].nodeValue=Z})}}})}function Ad(u,z){u=xa(u||"html");switch(u){case "svg":case "math":var J=ia.document.createElement("div");J.innerHTML="<"+u+">"+z+"</"+u+">";return J.childNodes[0].childNodes;default:return z}}function Ng(u,z){if("srcdoc"===z)return E.HTML;u=ib(u);if("src"===z||"ngSrc"===z){if(-1===["img","video","audio","source","track"].indexOf(u))return E.RESOURCE_URL}else if("xlinkHref"===z||"form"===u&&"action"===z||"link"===u&&
"href"===z)return E.RESOURCE_URL}function Eg(u,z,J,M,N){var K=Ng(u,M),aa=h[M]||N,O=r(J,!N,K,aa);if(O){if("multiple"===M&&"select"===ib(u))throw Ka("selmulti",jb(u));if(n.test(M))throw Ka("nodomevents");z.push({priority:100,compile:function(){return{pre:function(Z,V,W){V=W.$$observers||(W.$$observers=Ea());var ba=W[M];ba!==J&&(O=ba&&r(ba,!0,K,aa),J=ba);O&&(W[M]=O(Z),(V[M]||(V[M]=[])).$$inter=!0,(W.$$observers&&W.$$observers[M].$$scope||Z).$watch(O,function(T,ta){"class"===M&&T!==ta?W.$updateClass(T,
ta):W.$set(M,T)}))}}}})}}function Pc(u,z,J){var M=z[0],N=z.length,K=M.parentNode,aa;if(u){var O=0;for(aa=u.length;O<aa;O++)if(u[O]===M){u[O++]=J;aa=O+N-1;for(var Z=u.length;O<Z;O++,aa++)aa<Z?u[O]=u[aa]:delete u[O];u.length-=N-1;u.context===M&&(u.context=J);break}}K&&K.replaceChild(J,M);u=ia.document.createDocumentFragment();for(O=0;O<N;O++)u.appendChild(z[O]);da.hasData(M)&&(da.data(J,da.data(M)),da(M).off("$destroy"));da.cleanData(u.querySelectorAll("*"));for(O=1;O<N;O++)delete z[O];z[0]=J;z.length=
1}function Ee(u,z){return Aa(function(){return u.apply(null,arguments)},u,z)}function Fe(u,z,J,M,N,K){try{u(z,J,M,N,K)}catch(aa){m(aa,jb(J))}}function Qc(u,z){if(H)throw Ka("missingattr",u,z);}function Lc(u,z,J,M,N){function K(W,ba,T){ca(J.$onChanges)&&!md(ba,T)&&(Hb||(u.$$postDigest(S),Hb=[]),V||(V={},Hb.push(aa)),V[W]&&(T=V[W].previousValue),V[W]=new Rc(T,ba))}function aa(){J.$onChanges(V);V=void 0}var O=[],Z={},V;I(M,function(W,ba){var T=W.attrName,ta=W.optional;switch(W.mode){case "@":ta||bb.call(z,
T)||(Qc(T,N.name),J[ba]=z[T]=void 0);W=z.$observe(T,function(qa){if(na(qa)||vb(qa))K(ba,qa,J[ba]),J[ba]=qa});z.$$observers[T].$$scope=u;var ra=z[T];na(ra)?J[ba]=r(ra)(u):vb(ra)&&(J[ba]=ra);Z[ba]=new Rc(Jd,J[ba]);O.push(W);break;case "=":if(!bb.call(z,T)){if(ta)break;Qc(T,N.name);z[T]=void 0}if(ta&&!z[T])break;var sa=G(z[T]);var pa=sa.literal?db:md;var Ga=sa.assign||function(){ra=J[ba]=sa(u);throw Ka("nonassign",z[T],T,N.name);};ra=J[ba]=sa(u);ta=function(qa){pa(qa,J[ba])||(pa(qa,ra)?Ga(u,qa=J[ba]):
J[ba]=qa);return ra=qa};ta.$stateful=!0;W=W.collection?u.$watchCollection(z[T],ta):u.$watch(G(z[T],ta),null,sa.literal);O.push(W);break;case "<":if(!bb.call(z,T)){if(ta)break;Qc(T,N.name);z[T]=void 0}if(ta&&!z[T])break;sa=G(z[T]);var Fa=sa.literal,za=J[ba]=sa(u);Z[ba]=new Rc(Jd,J[ba]);W=u.$watch(sa,function(qa,Y){if(Y===qa){if(Y===za||Fa&&db(Y,za))return;Y=za}K(ba,qa,Y);J[ba]=qa},Fa);O.push(W);break;case "&":ta||bb.call(z,T)||Qc(T,N.name),sa=z.hasOwnProperty(T)?G(z[T]):ja,sa===ja&&ta||(J[ba]=function(qa){return sa(u,
qa)})}});return{initialChanges:Z,removeWatches:O.length&&function(){for(var W=0,ba=O.length;W<ba;++W)O[W]()}}}var Og=/^\w/,ze=ia.document.createElement("div"),Hg=C,Fg=D,ye=F,Hb;X.prototype={$normalize:lb,$addClass:function(u){u&&0<u.length&&L.addClass(this.$$element,u)},$removeClass:function(u){u&&0<u.length&&L.removeClass(this.$$element,u)},$updateClass:function(u,z){var J=Le(u,z);J&&J.length&&L.addClass(this.$$element,J);(u=Le(z,u))&&u.length&&L.removeClass(this.$$element,u)},$set:function(u,z,
J,M){var N=te(this.$$element[0],u),K=Me[u],aa=u;N?(this.$$element.prop(u,z),M=N):K&&(this[K]=z,aa=K);this[u]=z;M?this.$attr[u]=M:(M=this.$attr[u])||(this.$attr[u]=M=me(u,"-"));N=ib(this.$$element);if("a"===N&&("href"===u||"xlinkHref"===u)||"img"===N&&"src"===u)this[u]=z=null==z?z:Q(z,"src"===u);else if("img"===N&&"srcset"===u&&R(z)){N="";K=Ca(z);var O=/(\s+\d+x\s*,|\s+\d+w\s*,|\s+,|,\s+)/;O=/\s/.test(K)?O:/(,)/;K=K.split(O);O=Math.floor(K.length/2);for(var Z=0;Z<O;Z++){var V=2*Z;N+=Q(Ca(K[V]),!0);
N+=" "+Ca(K[V+1])}K=Ca(K[2*Z]).split(/\s/);N+=Q(Ca(K[0]),!0);2===K.length&&(N+=" "+Ca(K[1]));this[u]=z=N}!1!==J&&(null==z?this.$$element.removeAttr(M):Og.test(M)?this.$$element.attr(M,z):ha(this.$$element[0],M,z));(u=this.$$observers)&&I(u[aa],function(W){try{W(z)}catch(ba){m(ba)}})},$observe:function(u,z){var J=this,M=J.$$observers||(J.$$observers=Ea()),N=M[u]||(M[u]=[]);N.push(z);A.$evalAsync(function(){N.$$inter||!J.hasOwnProperty(u)||U(J[u])||z(J[u])});return function(){cc(N,z)}}};var Ne=r.startSymbol(),
Oe=r.endSymbol(),He="{{"===Ne&&"}}"===Oe?uc:function(u){return u.replace(/\{\{/g,Ne).replace(/}}/g,Oe)},Bg=/^ngAttr[A-Z]/,Cg=/^(.+)Start$/;ea.$$addBindingInfo=t?function(u,z){var J=u.data("$binding")||[];oa(z)?J=J.concat(z):J.push(z);u.data("$binding",J)}:ja;ea.$$addBindingClass=t?function(u){ka(u,"ng-binding")}:ja;ea.$$addScopeInfo=t?function(u,z,J,M){u.data(J?M?"$isolateScopeNoTemplate":"$isolateScope":"$scope",z)}:ja;ea.$$addScopeClass=t?function(u,z){ka(u,z?"ng-isolate-scope":"ng-scope")}:ja;
ea.$$createComment=function(u,z){var J="";t&&(J=" "+(u||"")+": ",z&&(J+=z+" "));return ia.document.createComment(J)};return ea}]}function Rc(a,b){this.previousValue=a;this.currentValue=b}function lb(a){return a.replace(Be,"").replace(Pg,function(b,d,c){return c?d.toUpperCase():d})}function Le(a,b){var d="";a=a.split(/\s+/);b=b.split(/\s+/);var c=0;a:for(;c<a.length;c++){for(var e=a[c],g=0;g<b.length;g++)if(e===b[g])continue a;d+=(0<d.length?" ":"")+e}return d}function Ie(a){a=da(a);var b=a.length;
if(1>=b)return a;for(;b--;){var d=a[b];(8===d.nodeType||d.nodeType===wb&&""===d.nodeValue.trim())&&Qg.call(a,b,1)}return a}function Ag(a,b){if(b&&na(b))return b;if(na(a)&&(a=Pe.exec(a)))return a[3]}function Rg(){var a={},b=!1;this.has=function(d){return a.hasOwnProperty(d)};this.register=function(d,c){Ob(d,"controller");fa(d)?Aa(a,d):a[d]=c};this.allowGlobals=function(){b=!0};this.$get=["$injector","$window",function(d,c){function e(g,f,k,h){if(!g||!fa(g.$scope))throw va("$controller")("noscp",h,
f);g.$scope[f]=k}return function(g,f,k,h){var l;k=!0===k;h&&na(h)&&(l=h);if(na(g)){h=g.match(Pe);if(!h)throw Qe("ctrlfmt",g);var n=h[1];l=l||h[3];g=a.hasOwnProperty(n)?a[n]:ne(f.$scope,n,!0)||(b?ne(c,n,!0):void 0);if(!g)throw Qe("ctrlreg",n);vc(g,n,!0)}if(k){k=(oa(g)?g[g.length-1]:g).prototype;var q=Object.create(k||null);l&&e(f,l,q,n||g.name);return Aa(function(){var t=d.invoke(g,q,f,n);t!==q&&(fa(t)||ca(t))&&(q=t,l&&e(f,l,q,n||g.name));return q},{instance:q,identifier:l})}q=d.instantiate(g,f,n);
l&&e(f,l,q,n||g.name);return q}}]}function Sg(){this.$get=["$window",function(a){return da(a.document)}]}function Tg(){this.$get=["$document","$rootScope",function(a,b){function d(){e=c.hidden}var c=a[0],e=c&&c.hidden;a.on("visibilitychange",d);b.$on("$destroy",function(){a.off("visibilitychange",d)});return function(){return e}}]}function Ug(){this.$get=["$log",function(a){return function(b,d){a.error.apply(a,arguments)}}]}function Kd(a){return fa(a)?Xa(a)?a.toISOString():ec(a):a}function Vg(){this.$get=
function(){return function(a){if(!a)return"";var b=[];fe(a,function(d,c){null===d||U(d)||ca(d)||(oa(d)?I(d,function(e){b.push(Za(c)+"="+Za(Kd(e)))}):b.push(Za(c)+"="+Za(Kd(d))))});return b.join("&")}}}function Wg(){this.$get=function(){return function(a){function b(c,e,g){null===c||U(c)||(oa(c)?I(c,function(f,k){b(f,e+"["+(fa(f)?k:"")+"]")}):fa(c)&&!Xa(c)?fe(c,function(f,k){b(f,e+(g?"":"[")+k+(g?"":"]"))}):d.push(Za(e)+"="+Za(Kd(c))))}if(!a)return"";var d=[];b(a,"",!0);return d.join("&")}}}function Ld(a,
b){if(na(a)){var d=a.replace(Xg,"").trim();if(d){b=(b=b("Content-Type"))&&0===b.indexOf(Re);var c;(c=b)||(c=(c=d.match(Yg))&&Zg[c[0]].test(d));if(c)try{a=ie(d)}catch(e){if(!b)return a;throw Sc("baddata",a,e);}}}return a}function Se(a){var b=Ea(),d;na(a)?I(a.split("\n"),function(c){d=c.indexOf(":");var e=xa(Ca(c.substr(0,d)));c=Ca(c.substr(d+1));e&&(b[e]=b[e]?b[e]+", "+c:c)}):fa(a)&&I(a,function(c,e){e=xa(e);c=Ca(c);e&&(b[e]=b[e]?b[e]+", "+c:c)});return b}function Te(a){var b;return function(d){b||
(b=Se(a));return d?(d=b[xa(d)],void 0===d&&(d=null),d):b}}function Ue(a,b,d,c){if(ca(c))return c(a,b,d);I(c,function(e){a=e(a,b,d)});return a}function $g(){var a=this.defaults={transformResponse:[Ld],transformRequest:[function(e){return fa(e)&&"[object File]"!==Ta.call(e)&&"[object Blob]"!==Ta.call(e)&&"[object FormData]"!==Ta.call(e)?ec(e):e}],headers:{common:{Accept:"application/json, text/plain, */*"},post:kb(Md),put:kb(Md),patch:kb(Md)},xsrfCookieName:"XSRF-TOKEN",xsrfHeaderName:"X-XSRF-TOKEN",
paramSerializer:"$httpParamSerializer",jsonpCallbackParam:"callback"},b=!1;this.useApplyAsync=function(e){return R(e)?(b=!!e,this):b};var d=this.interceptors=[],c=this.xsrfWhitelistedOrigins=[];this.$get=["$browser","$httpBackend","$$cookieReader","$cacheFactory","$rootScope","$q","$injector","$sce",function(e,g,f,k,h,l,n,q){function t(v){function p(A,E){for(var L=0,Q=E.length;L<Q;){var S=E[L++],X=E[L++];A=A.then(S,X)}E.length=0;return A}function r(A,E){var L,Q={};I(A,function(S,X){ca(S)?(L=S(E),
null!=L&&(Q[X]=L)):Q[X]=S});return Q}function m(A){var E=Aa({},A);E.data=Ue(A.data,A.headers,A.status,x.transformResponse);A=A.status;return 200<=A&&300>A?E:l.reject(E)}if(!fa(v))throw va("$http")("badreq",v);if(!na(q.valueOf(v.url)))throw va("$http")("badreq",v.url);var x=Aa({method:"get",transformRequest:a.transformRequest,transformResponse:a.transformResponse,paramSerializer:a.paramSerializer,jsonpCallbackParam:a.jsonpCallbackParam},v);x.headers=function(A){var E=a.headers,L=Aa({},A.headers),Q,
S;E=Aa({},E.common,E[xa(A.method)]);a:for(Q in E){var X=xa(Q);for(S in L)if(xa(S)===X)continue a;L[Q]=E[Q]}return r(L,kb(A))}(v);x.method=Tc(x.method);x.paramSerializer=na(x.paramSerializer)?n.get(x.paramSerializer):x.paramSerializer;e.$$incOutstandingRequestCount();var G=[],B=[];v=l.resolve(x);I(D,function(A){(A.request||A.requestError)&&G.unshift(A.request,A.requestError);(A.response||A.responseError)&&B.push(A.response,A.responseError)});v=p(v,G);v=v.then(function(A){var E=A.headers,L=Ue(A.data,
Te(E),void 0,A.transformRequest);U(L)&&I(E,function(Q,S){"content-type"===xa(S)&&delete E[S]});U(A.withCredentials)&&!U(a.withCredentials)&&(A.withCredentials=a.withCredentials);return w(A,L).then(m,m)});v=p(v,B);return v=v.finally(function(){e.$$completeOutstandingRequest(ja)})}function w(v,p){function r(ka){if(ka){var ea={};I(ka,function(ma,la){ea[la]=function(ya){function ua(){ma(ya)}b?h.$applyAsync(ua):h.$$phase?ua():h.$apply(ua)}});return ea}}function m(ka,ea,ma,la,ya){function ua(){x(ea,ka,
ma,la,ya)}L&&(200<=ka&&300>ka?L.put(X,[ka,ea,Se(ma),la,ya]):L.remove(X));b?h.$applyAsync(ua):(ua(),h.$$phase||h.$apply())}function x(ka,ea,ma,la,ya){ea=-1<=ea?ea:0;(200<=ea&&300>ea?A.resolve:A.reject)({data:ka,status:ea,headers:Te(ma),config:v,statusText:la,xhrStatus:ya})}function G(ka){x(ka.data,ka.status,kb(ka.headers()),ka.statusText,ka.xhrStatus)}function B(){var ka=t.pendingRequests.indexOf(v);-1!==ka&&t.pendingRequests.splice(ka,1)}var A=l.defer(),E=A.promise,L,Q=v.headers,S="jsonp"===xa(v.method),
X=v.url;S?X=q.getTrustedResourceUrl(X):na(X)||(X=q.valueOf(X));X=H(X,v.paramSerializer(v.params));S&&(X=F(X,v.jsonpCallbackParam));t.pendingRequests.push(v);E.then(B,B);!v.cache&&!a.cache||!1===v.cache||"GET"!==v.method&&"JSONP"!==v.method||(L=fa(v.cache)?v.cache:fa(a.cache)?a.cache:C);if(L){var ha=L.get(X);R(ha)?ha&&ca(ha.then)?ha.then(G,G):oa(ha)?x(ha[1],ha[0],kb(ha[2]),ha[3],ha[4]):x(ha,200,{},"OK","complete"):L.put(X,E)}U(ha)&&((ha=y(v.url)?f()[v.xsrfCookieName||a.xsrfCookieName]:void 0)&&(Q[v.xsrfHeaderName||
a.xsrfHeaderName]=ha),g(v.method,X,p,m,Q,v.timeout,v.withCredentials,v.responseType,r(v.eventHandlers),r(v.uploadEventHandlers)));return E}function H(v,p){0<p.length&&(v+=(-1===v.indexOf("?")?"?":"&")+p);return v}function F(v,p){var r=v.split("?");if(2<r.length)throw Sc("badjsonp",v);r=pd(r[1]);I(r,function(m,x){if("JSON_CALLBACK"===m)throw Sc("badjsonp",v);if(x===p)throw Sc("badjsonp",p,v);});return v+=(-1===v.indexOf("?")?"?":"&")+p+"=JSON_CALLBACK"}var C=k("$http");a.paramSerializer=na(a.paramSerializer)?
n.get(a.paramSerializer):a.paramSerializer;var D=[];I(d,function(v){D.unshift(na(v)?n.get(v):n.invoke(v))});var y=ah(c);t.pendingRequests=[];(function(v){I(arguments,function(p){t[p]=function(r,m){return t(Aa({},m||{},{method:p,url:r}))}})})("get","delete","head","jsonp");(function(v){I(arguments,function(p){t[p]=function(r,m,x){return t(Aa({},x||{},{method:p,url:r,data:m}))}})})("post","put","patch");t.defaults=a;return t}]}function bh(){this.$get=function(){return function(){return new ia.XMLHttpRequest}}}
function ch(){this.$get=["$browser","$jsonpCallbacks","$document","$xhrFactory",function(a,b,d,c){return dh(a,c,a.defer,b,d[0])}]}function dh(a,b,d,c,e){function g(f,k,h){f=f.replace("JSON_CALLBACK",k);var l=e.createElement("script"),n=null;l.type="text/javascript";l.src=f;l.async=!0;n=function(q){l.removeEventListener("load",n);l.removeEventListener("error",n);e.body.removeChild(l);l=null;var t=-1,w="unknown";q&&("load"!==q.type||c.wasCalled(k)||(q={type:"error"}),w=q.type,t="error"===q.type?404:
200);h&&h(t,w)};l.addEventListener("load",n);l.addEventListener("error",n);e.body.appendChild(l);return n}return function(f,k,h,l,n,q,t,w,H,F){function C(x){r="timeout"===x;v&&v();p&&p.abort()}function D(x,G,B,A,E,L){R(m)&&d.cancel(m);v=p=null;x(G,B,A,E,L)}k=k||a.url();if("jsonp"===xa(f))var y=c.createCallback(k),v=g(k,y,function(x,G){var B=200===x&&c.getResponse(y);D(l,x,B,"",G,"complete");c.removeCallback(y)});else{var p=b(f,k),r=!1;p.open(f,k,!0);I(n,function(x,G){R(x)&&p.setRequestHeader(G,x)});
p.onload=function(){var x=p.statusText||"",G="response"in p?p.response:p.responseText,B=1223===p.status?204:p.status;0===B&&(B=G?200:"file"===pb(k).protocol?404:0);D(l,B,G,p.getAllResponseHeaders(),x,"complete")};p.onerror=function(){D(l,-1,null,null,"","error")};p.ontimeout=function(){D(l,-1,null,null,"","timeout")};p.onabort=function(){D(l,-1,null,null,"",r?"timeout":"abort")};I(H,function(x,G){p.addEventListener(G,x)});I(F,function(x,G){p.upload.addEventListener(G,x)});t&&(p.withCredentials=!0);
if(w)try{p.responseType=w}catch(x){if("json"!==w)throw x;}p.send(U(h)?null:h)}if(0<q)var m=d(function(){C("timeout")},q);else q&&ca(q.then)&&q.then(function(){C(R(q.$$timeoutId)?"timeout":"abort")})}}function eh(){var a="{{",b="}}";this.startSymbol=function(d){return d?(a=d,this):a};this.endSymbol=function(d){return d?(b=d,this):b};this.$get=["$parse","$exceptionHandler","$sce",function(d,c,e){function g(w){return"\\\\\\"+w}function f(w){return w.replace(q,a).replace(t,b)}function k(w,H,F,C){var D=
w.$watch(function(y){D();return C(y)},H,F);return D}function h(w,H,F,C){function D(E){try{var L=E;E=F?e.getTrusted(F,L):e.valueOf(L);return C&&!R(E)?E:rd(E)}catch(Q){c(Ib.interr(w,Q))}}if(!w.length||-1===w.indexOf(a)){if(!H){H=f(w);var y=cb(H);y.exp=w;y.expressions=[];y.$$watchDelegate=k}return y}C=!!C;var v,p,r=0,m=[],x=[];y=w.length;for(var G=[],B=[];r<y;)if(-1!==(v=w.indexOf(a,r))&&-1!==(p=w.indexOf(b,v+l)))r!==v&&G.push(f(w.substring(r,v))),r=w.substring(v+l,p),m.push(r),x.push(d(r,D)),r=p+n,
B.push(G.length),G.push("");else{r!==y&&G.push(f(w.substring(r)));break}F&&1<G.length&&Ib.throwNoconcat(w);if(!H||m.length){var A=function(E){for(var L=0,Q=m.length;L<Q;L++){if(C&&U(E[L]))return;G[B[L]]=E[L]}return G.join("")};return Aa(function(E){var L=0,Q=m.length,S=Array(Q);try{for(;L<Q;L++)S[L]=x[L](E);return A(S)}catch(X){c(Ib.interr(w,X))}},{exp:w,expressions:m,$$watchDelegate:function(E,L){var Q;return E.$watchGroup(x,function(S,X){var ha=A(S);L.call(this,ha,S!==X?Q:ha,E);Q=ha})}})}}var l=
a.length,n=b.length,q=new RegExp(a.replace(/./g,g),"g"),t=new RegExp(b.replace(/./g,g),"g");h.startSymbol=function(){return a};h.endSymbol=function(){return b};return h}]}function fh(){this.$get=["$rootScope","$window","$q","$$q","$browser",function(a,b,d,c,e){function g(k,h,l,n){function q(){t?k.apply(null,w):k(C)}var t=4<arguments.length,w=t?hb.call(arguments,4):[],H=b.setInterval,F=b.clearInterval,C=0,D=R(n)&&!n,y=(D?c:d).defer(),v=y.promise;l=R(l)?l:0;v.$$intervalId=H(function(){D?e.defer(q):
a.$evalAsync(q);y.notify(C++);0<l&&C>=l&&(y.resolve(C),F(v.$$intervalId),delete f[v.$$intervalId]);D||a.$apply()},h);f[v.$$intervalId]=y;return v}var f={};g.cancel=function(k){return k&&k.$$intervalId in f?(f[k.$$intervalId].promise.$$state.pur=!0,f[k.$$intervalId].reject("canceled"),b.clearInterval(k.$$intervalId),delete f[k.$$intervalId],!0):!1};return g}]}function Nd(a){a=a.split("/");for(var b=a.length;b--;)a[b]=fc(a[b].replace(/%2F/g,"/"));return a.join("/")}function Ve(a,b){a=pb(a);b.$$protocol=
a.protocol;b.$$host=a.hostname;b.$$port=parseInt(a.port,10)||gh[a.protocol]||null}function We(a,b,d){if(hh.test(a))throw mc("badpath",a);var c="/"!==a.charAt(0);c&&(a="/"+a);a=pb(a);c=(c&&"/"===a.pathname.charAt(0)?a.pathname.substring(1):a.pathname).split("/");for(var e=c.length;e--;)c[e]=decodeURIComponent(c[e]),d&&(c[e]=c[e].replace(/\//g,"%2F"));d=c.join("/");b.$$path=d;b.$$search=pd(a.search);b.$$hash=decodeURIComponent(a.hash);b.$$path&&"/"!==b.$$path.charAt(0)&&(b.$$path="/"+b.$$path)}function Od(a,
b){return a.slice(0,b.length)===b}function tb(a,b){if(Od(b,a))return b.substr(a.length)}function Gb(a){var b=a.indexOf("#");return-1===b?a:a.substr(0,b)}function nc(a){return a.replace(/(#.+)|#$/,"$1")}function Pd(a,b,d){this.$$html5=!0;d=d||"";Ve(a,this);this.$$parse=function(c){var e=tb(b,c);if(!na(e))throw mc("ipthprfx",c,b);We(e,this,!0);this.$$path||(this.$$path="/");this.$$compose()};this.$$compose=function(){var c=qd(this.$$search),e=this.$$hash?"#"+fc(this.$$hash):"";this.$$url=Nd(this.$$path)+
(c?"?"+c:"")+e;this.$$absUrl=b+this.$$url.substr(1);this.$$urlUpdatedByLocation=!0};this.$$parseLinkUrl=function(c,e){if(e&&"#"===e[0])return this.hash(e.slice(1)),!0;if(R(e=tb(a,c))){c=e;var g=d&&R(e=tb(d,e))?b+(tb("/",e)||e):a+c}else R(e=tb(b,c))?g=b+e:b===c+"/"&&(g=b);g&&this.$$parse(g);return!!g}}function Qd(a,b,d){Ve(a,this);this.$$parse=function(c){var e=tb(a,c)||tb(b,c);if(U(e)||"#"!==e.charAt(0))if(this.$$html5)var g=e;else g="",U(e)&&(a=c,this.replace());else g=tb(d,e),U(g)&&(g=e);We(g,this,
!1);c=this.$$path;e=a;var f=/^\/[A-Z]:(\/.*)/;Od(g,e)&&(g=g.replace(e,""));f.exec(g)||(c=(g=f.exec(c))?g[1]:c);this.$$path=c;this.$$compose()};this.$$compose=function(){var c=qd(this.$$search),e=this.$$hash?"#"+fc(this.$$hash):"";this.$$url=Nd(this.$$path)+(c?"?"+c:"")+e;this.$$absUrl=a+(this.$$url?d+this.$$url:"");this.$$urlUpdatedByLocation=!0};this.$$parseLinkUrl=function(c,e){return Gb(a)===Gb(c)?(this.$$parse(c),!0):!1}}function Xe(a,b,d){this.$$html5=!0;Qd.apply(this,arguments);this.$$parseLinkUrl=
function(c,e){if(e&&"#"===e[0])return this.hash(e.slice(1)),!0;var g,f;a===Gb(c)?g=c:(f=tb(b,c))?g=a+d+f:b===c+"/"&&(g=b);g&&this.$$parse(g);return!!g};this.$$compose=function(){var c=qd(this.$$search),e=this.$$hash?"#"+fc(this.$$hash):"";this.$$url=Nd(this.$$path)+(c?"?"+c:"")+e;this.$$absUrl=a+d+this.$$url;this.$$urlUpdatedByLocation=!0}}function Uc(a){return function(){return this[a]}}function Ye(a,b){return function(d){if(U(d))return this[a];this[a]=b(d);this.$$compose();return this}}function ih(){var a=
"!",b={enabled:!1,requireBase:!0,rewriteLinks:!0},d=function(c,e,g){return c!==e};this.hashPrefix=function(c){return R(c)?(a=c,this):a};this.html5Mode=function(c){if(vb(c))return b.enabled=c,this;if(fa(c)){vb(c.enabled)&&(b.enabled=c.enabled);vb(c.requireBase)&&(b.requireBase=c.requireBase);if(vb(c.rewriteLinks)||na(c.rewriteLinks))b.rewriteLinks=c.rewriteLinks;return this}return b};this.compareUrls=function(c){return R(c)?(d=c,this):d};this.$get=["$rootScope","$browser","$sniffer","$rootElement",
"$window",function(c,e,g,f,k){function h(y,v,p){var r=F.url(),m=F.$$state;try{e.url(y,v,p),F.$$state=e.state()}catch(x){throw F.url(r),F.$$state=m,x;}}function l(y,v){c.$broadcast("$locationChangeSuccess",F.absUrl(),y,F.$$state,v)}var n=e.baseHref(),q=e.url();if(b.enabled){if(!n&&b.requireBase)throw mc("nobase");var t=q.substring(0,q.indexOf("/",q.indexOf("//")+2))+(n||"/");var w=g.history?Pd:Xe}else t=Gb(q),w=Qd;var H=t.substr(0,Gb(t).lastIndexOf("/")+1);var F=new w(t,H,"#"+a);F.$$parseLinkUrl(q,
q);F.$$state=e.state();var C=/^\s*(javascript|mailto):/i;f.on("click",function(y){var v=b.rewriteLinks;if(v&&!y.ctrlKey&&!y.metaKey&&!y.shiftKey&&2!==y.which&&2!==y.button){for(var p=da(y.target);"a"!==ib(p[0]);)if(p[0]===f[0]||!(p=p.parent())[0])return;if(!na(v)||!U(p.attr(v))){v=p.prop("href");var r=p.attr("href")||p.attr("xlink:href");fa(v)&&"[object SVGAnimatedString]"===v.toString()&&(v=pb(v.animVal).href);C.test(v)||!v||p.attr("target")||y.isDefaultPrevented()||!F.$$parseLinkUrl(v,r)||(y.preventDefault(),
F.absUrl()!==e.url()&&(c.$apply(),k.angular["ff-684208-preventDefault"]=!0))}}});nc(F.absUrl())!==nc(q)&&e.url(F.absUrl(),!0);var D=!0;e.onUrlChange(function(y,v){Od(y,H)?(c.$evalAsync(function(){var p=F.absUrl(),r=F.$$state;y=nc(y);F.$$parse(y);F.$$state=v;var m=c.$broadcast("$locationChangeStart",y,p,v,r).defaultPrevented;F.absUrl()===y&&(m?(F.$$parse(p),F.$$state=r,h(p,!1,r)):(D=!1,l(p,r)))}),c.$$phase||c.$digest()):k.location.href=y});c.$watch(function(){if(D||F.$$urlUpdatedByLocation){F.$$urlUpdatedByLocation=
!1;var y=nc(e.url()),v=nc(F.absUrl()),p=e.state(),r=F.$$replace,m=d(y,v,function(){return new w(t,H,"#"+a)}),x=F.$$html5&&g.history&&p!==F.$$state,G=y!==v||x;if(D||G)D=!1,c.$evalAsync(function(){var B=F.absUrl(),A=c.$broadcast("$locationChangeStart",B,y,F.$$state,p).defaultPrevented;F.absUrl()===B&&(A?(F.$$parse(y),F.$$state=p):((D||G&&m)&&h(B,r,p===F.$$state?null:F.$$state),l(y,p)))})}F.$$replace=!1});return F}]}function jh(){var a=!0,b=this;this.debugEnabled=function(d){return R(d)?(a=d,this):a};
this.$get=["$window",function(d){function c(g){var f=d.console||{},k=f[g]||f.log||ja;return function(){var h=[];I(arguments,function(l){var n=h.push;ld(l)&&(l.stack&&e?l=l.message&&-1===l.stack.indexOf(l.message)?"Error: "+l.message+"\n"+l.stack:l.stack:l.sourceURL&&(l=l.message+"\n"+l.sourceURL+":"+l.line));n.call(h,l)});return Function.prototype.apply.call(k,f,h)}}var e=qb||/\bEdge\//.test(d.navigator&&d.navigator.userAgent);return{log:c("log"),info:c("info"),warn:c("warn"),error:c("error"),debug:function(){var g=
c("debug");return function(){a&&g.apply(b,arguments)}}()}}]}function kh(a){return a+""}function lh(a,b){return"undefined"!==typeof a?a:b}function Ze(a,b){return"undefined"===typeof a?b:"undefined"===typeof b?a:a+b}function mh(a,b){switch(a.type){case P.MemberExpression:if(a.computed)return!1;break;case P.UnaryExpression:return 1;case P.BinaryExpression:return"+"!==a.operator?1:!1;case P.CallExpression:return!1}return void 0===b?$e:b}function Ja(a,b,d){var c=a.isPure=mh(a,d);switch(a.type){case P.Program:var e=
!0;I(a.body,function(f){Ja(f.expression,b,c);e=e&&f.expression.constant});a.constant=e;break;case P.Literal:a.constant=!0;a.toWatch=[];break;case P.UnaryExpression:Ja(a.argument,b,c);a.constant=a.argument.constant;a.toWatch=a.argument.toWatch;break;case P.BinaryExpression:Ja(a.left,b,c);Ja(a.right,b,c);a.constant=a.left.constant&&a.right.constant;a.toWatch=a.left.toWatch.concat(a.right.toWatch);break;case P.LogicalExpression:Ja(a.left,b,c);Ja(a.right,b,c);a.constant=a.left.constant&&a.right.constant;
a.toWatch=a.constant?[]:[a];break;case P.ConditionalExpression:Ja(a.test,b,c);Ja(a.alternate,b,c);Ja(a.consequent,b,c);a.constant=a.test.constant&&a.alternate.constant&&a.consequent.constant;a.toWatch=a.constant?[]:[a];break;case P.Identifier:a.constant=!1;a.toWatch=[a];break;case P.MemberExpression:Ja(a.object,b,c);a.computed&&Ja(a.property,b,c);a.constant=a.object.constant&&(!a.computed||a.property.constant);a.toWatch=a.constant?[]:[a];break;case P.CallExpression:e=d=a.filter?!b(a.callee.name).$stateful:
!1;var g=[];I(a.arguments,function(f){Ja(f,b,c);e=e&&f.constant;g.push.apply(g,f.toWatch)});a.constant=e;a.toWatch=d?g:[a];break;case P.AssignmentExpression:Ja(a.left,b,c);Ja(a.right,b,c);a.constant=a.left.constant&&a.right.constant;a.toWatch=[a];break;case P.ArrayExpression:e=!0;g=[];I(a.elements,function(f){Ja(f,b,c);e=e&&f.constant;g.push.apply(g,f.toWatch)});a.constant=e;a.toWatch=g;break;case P.ObjectExpression:e=!0;g=[];I(a.properties,function(f){Ja(f.value,b,c);e=e&&f.value.constant;g.push.apply(g,
f.value.toWatch);f.computed&&(Ja(f.key,b,!1),e=e&&f.key.constant,g.push.apply(g,f.key.toWatch))});a.constant=e;a.toWatch=g;break;case P.ThisExpression:a.constant=!1;a.toWatch=[];break;case P.LocalsExpression:a.constant=!1,a.toWatch=[]}}function af(a){if(1===a.length){a=a[0].expression;var b=a.toWatch;return 1!==b.length?b:b[0]!==a?b:void 0}}function bf(a){return a.type===P.Identifier||a.type===P.MemberExpression}function cf(a){if(1===a.body.length&&bf(a.body[0].expression))return{type:P.AssignmentExpression,
left:a.body[0].expression,right:{type:P.NGValueParameter},operator:"="}}function df(a){this.$filter=a}function ef(a){this.$filter=a}function Vc(a,b,d){this.ast=new P(a,d);this.astCompiler=d.csp?new ef(b):new df(b)}function Rd(a){return ca(a.valueOf)?a.valueOf():nh.call(a)}function oh(){var a=Ea(),b={"true":!0,"false":!1,"null":null,undefined:void 0},d,c;this.addLiteral=function(e,g){b[e]=g};this.setIdentifierFns=function(e,g){d=e;c=g;return this};this.$get=["$filter",function(e){function g(w,H){switch(typeof w){case "string":var F=
w=w.trim();var C=a[F];C||(C=new Wc(t),C=(new Vc(C,e,t)).parse(w),C.constant?C.$$watchDelegate=n:C.oneTime?C.$$watchDelegate=C.literal?l:h:C.inputs&&(C.$$watchDelegate=k),a[F]=C);return q(C,H);case "function":return q(w,H);default:return q(ja,H)}}function f(w,H,F){return null==w||null==H?w===H:"object"!==typeof w||(w=Rd(w),"object"!==typeof w||F)?w===H||w!==w&&H!==H:!1}function k(w,H,F,C,D){var y=C.inputs,v;if(1===y.length){var p=f;y=y[0];return w.$watch(function(B){var A=y(B);f(A,p,y.isPure)||(v=
C(B,void 0,void 0,[A]),p=A&&Rd(A));return v},H,F,D)}for(var r=[],m=[],x=0,G=y.length;x<G;x++)r[x]=f,m[x]=null;return w.$watch(function(B){for(var A=!1,E=0,L=y.length;E<L;E++){var Q=y[E](B);if(A||(A=!f(Q,r[E],y[E].isPure)))m[E]=Q,r[E]=Q&&Rd(Q)}A&&(v=C(B,void 0,void 0,m));return v},H,F,D)}function h(w,H,F,C,D){function y(m){return C(m)}function v(m,x,G){r=m;ca(H)&&H(m,x,G);R(m)&&G.$$postDigest(function(){R(r)&&p()})}var p,r;return p=C.inputs?k(w,v,F,C,D):w.$watch(y,v,F)}function l(w,H,F,C){function D(p){var r=
!0;I(p,function(m){R(m)||(r=!1)});return r}var y,v;return y=w.$watch(function(p){return C(p)},function(p,r,m){v=p;ca(H)&&H(p,r,m);D(p)&&m.$$postDigest(function(){D(v)&&y()})},F)}function n(w,H,F,C){var D=w.$watch(function(y){D();return C(y)},H,F);return D}function q(w,H){if(!H)return w;var F=w.$$watchDelegate,C=!1,D=F!==l&&F!==h?function(y,v,p,r){p=C&&r?r[0]:w(y,v,p,r);return H(p,y,v)}:function(y,v,p,r){p=w(y,v,p,r);y=H(p,y,v);return R(p)?y:p};C=!w.inputs;F&&F!==k?(D.$$watchDelegate=F,D.inputs=w.inputs):
H.$stateful||(D.$$watchDelegate=k,D.inputs=w.inputs?w.inputs:[w]);D.inputs&&(D.inputs=D.inputs.map(function(y){return y.isPure===$e?function(v){return y(v)}:y}));return D}var t={csp:Jb().noUnsafeEval,literals:Bb(b),isIdentifierStart:ca(d)&&d,isIdentifierContinue:ca(c)&&c};g.$$getAst=function(w){var H=new Wc(t);return(new Vc(H,e,t)).getAst(w).ast};return g}]}function ph(){var a=!0;this.$get=["$rootScope","$exceptionHandler",function(b,d){return ff(function(c){b.$evalAsync(c)},d,a)}];this.errorOnUnhandledRejections=
function(b){return R(b)?(a=b,this):a}}function qh(){var a=!0;this.$get=["$browser","$exceptionHandler",function(b,d){return ff(function(c){b.defer(c)},d,a)}];this.errorOnUnhandledRejections=function(b){return R(b)?(a=b,this):a}}function ff(a,b,d){function c(){return new e}function e(){var r=this.promise=new g;this.resolve=function(m){h(r,m)};this.reject=function(m){n(r,m)};this.notify=function(m){t(r,m)}}function g(){this.$$state={status:0}}function f(){for(;!y&&v.length;){var r=v.shift();if(!r.pur){r.pur=
!0;var m=r.value;m="Possibly unhandled rejection: "+("function"===typeof m?m.toString().replace(/ \{[\s\S]*$/,""):U(m)?"undefined":"string"!==typeof m?eg(m,void 0):m);ld(r.value)?b(r.value,m):b(m)}}}function k(r){!d||r.pending||2!==r.status||r.pur||(0===y&&0===v.length&&a(f),v.push(r));!r.processScheduled&&r.pending&&(r.processScheduled=!0,++y,a(function(){var m=r.pending;r.processScheduled=!1;r.pending=void 0;try{for(var x=0,G=m.length;x<G;++x){r.pur=!0;var B=m[x][0];var A=m[x][r.status];try{ca(A)?
h(B,A(r.value)):1===r.status?h(B,r.value):n(B,r.value)}catch(E){n(B,E),E&&!0===E.$$passToExceptionHandler&&b(E)}}}finally{--y,d&&0===y&&a(f)}}))}function h(r,m){r.$$state.status||(m===r?q(r,D("qcycle",m)):l(r,m))}function l(r,m){function x(L){A||(A=!0,l(r,L))}function G(L){A||(A=!0,q(r,L))}function B(L){t(r,L)}var A=!1;try{if(fa(m)||ca(m))var E=m.then;ca(E)?(r.$$state.status=-1,E.call(m,x,G,B)):(r.$$state.value=m,r.$$state.status=1,k(r.$$state))}catch(L){G(L)}}function n(r,m){r.$$state.status||q(r,
m)}function q(r,m){r.$$state.value=m;r.$$state.status=2;k(r.$$state)}function t(r,m){var x=r.$$state.pending;0>=r.$$state.status&&x&&x.length&&a(function(){for(var G,B,A=0,E=x.length;A<E;A++){B=x[A][0];G=x[A][3];try{t(B,ca(G)?G(m):m)}catch(L){b(L)}}})}function w(r){var m=new g;n(m,r);return m}function H(r,m,x){var G=null;try{ca(x)&&(G=x())}catch(B){return w(B)}return G&&ca(G.then)?G.then(function(){return m(r)},w):m(r)}function F(r,m,x,G){var B=new g;h(B,r);return B.then(m,x,G)}function C(r){if(!ca(r))throw D("norslvr",
r);var m=new g;r(function(x){h(m,x)},function(x){n(m,x)});return m}var D=va("$q",TypeError),y=0,v=[];Aa(g.prototype,{then:function(r,m,x){if(U(r)&&U(m)&&U(x))return this;var G=new g;this.$$state.pending=this.$$state.pending||[];this.$$state.pending.push([G,r,m,x]);0<this.$$state.status&&k(this.$$state);return G},"catch":function(r){return this.then(null,r)},"finally":function(r,m){return this.then(function(x){return H(x,p,r)},function(x){return H(x,w,r)},m)}});var p=F;C.prototype=g.prototype;C.defer=
c;C.reject=w;C.when=F;C.resolve=p;C.all=function(r){var m=new g,x=0,G=oa(r)?[]:{};I(r,function(B,A){x++;F(B).then(function(E){G[A]=E;--x||h(m,G)},function(E){n(m,E)})});0===x&&h(m,G);return m};C.race=function(r){var m=c();I(r,function(x){F(x).then(m.resolve,m.reject)});return m.promise};return C}function rh(){this.$get=["$window","$timeout",function(a,b){var d=a.requestAnimationFrame||a.webkitRequestAnimationFrame,c=a.cancelAnimationFrame||a.webkitCancelAnimationFrame||a.webkitCancelRequestAnimationFrame,
e=(a=!!d)?function(g){var f=d(g);return function(){c(f)}}:function(g){var f=b(g,16.66,!1);return function(){b.cancel(f)}};e.supported=a;return e}]}function sh(){function a(g){function f(){this.$$watchers=this.$$nextSibling=this.$$childHead=this.$$childTail=null;this.$$listeners={};this.$$listenerCount={};this.$$watchersCount=0;this.$id=++sc;this.$$ChildScope=null;this.$$suspended=!1}f.prototype=g;return f}var b=10,d=va("$rootScope"),c=null,e=null;this.digestTtl=function(g){arguments.length&&(b=g);
return b};this.$get=["$exceptionHandler","$parse","$browser",function(g,f,k){function h(m){m.currentScope.$$destroyed=!0}function l(m){9===qb&&(m.$$childHead&&l(m.$$childHead),m.$$nextSibling&&l(m.$$nextSibling));m.$parent=m.$$nextSibling=m.$$prevSibling=m.$$childHead=m.$$childTail=m.$root=m.$$watchers=null}function n(){this.$id=++sc;this.$$phase=this.$parent=this.$$watchers=this.$$nextSibling=this.$$prevSibling=this.$$childHead=this.$$childTail=null;this.$root=this;this.$$suspended=this.$$destroyed=
!1;this.$$listeners={};this.$$listenerCount={};this.$$watchersCount=0;this.$$isolateBindings=null}function q(m){if(D.$$phase)throw d("inprog",D.$$phase);D.$$phase=m}function t(m,x){do m.$$watchersCount+=x;while(m=m.$parent)}function w(m,x,G){do m.$$listenerCount[G]-=x,0===m.$$listenerCount[G]&&delete m.$$listenerCount[G];while(m=m.$parent)}function H(){}function F(){for(;p.length;)try{p.shift()()}catch(m){g(m)}e=null}function C(){null===e&&(e=k.defer(function(){D.$apply(F)}))}n.prototype={constructor:n,
$new:function(m,x){x=x||this;if(m){var G=new n;G.$root=this.$root}else this.$$ChildScope||(this.$$ChildScope=a(this)),G=new this.$$ChildScope;G.$parent=x;G.$$prevSibling=x.$$childTail;x.$$childHead?(x.$$childTail.$$nextSibling=G,x.$$childTail=G):x.$$childHead=x.$$childTail=G;(m||x!==this)&&G.$on("$destroy",h);return G},$watch:function(m,x,G,B){var A=f(m);x=ca(x)?x:ja;if(A.$$watchDelegate)return A.$$watchDelegate(this,x,G,A,m);var E=this,L=E.$$watchers,Q={fn:x,last:H,get:A,exp:B||m,eq:!!G};c=null;
L||(L=E.$$watchers=[],L.$$digestWatchIndex=-1);L.unshift(Q);L.$$digestWatchIndex++;t(this,1);return function(){var S=cc(L,Q);0<=S&&(t(E,-1),S<L.$$digestWatchIndex&&L.$$digestWatchIndex--);c=null}},$watchGroup:function(m,x){function G(){Q=!1;S?(S=!1,x(A,A,L)):x(A,B,L)}var B=Array(m.length),A=Array(m.length),E=[],L=this,Q=!1,S=!0;if(!m.length){var X=!0;L.$evalAsync(function(){X&&x(A,A,L)});return function(){X=!1}}if(1===m.length)return this.$watch(m[0],function(ha,ka,ea){A[0]=ha;B[0]=ka;x(A,ha===ka?
A:B,ea)});I(m,function(ha,ka){ha=L.$watch(ha,function(ea,ma){A[ka]=ea;B[ka]=ma;Q||(Q=!0,L.$evalAsync(G))});E.push(ha)});return function(){for(;E.length;)E.shift()()}},$watchCollection:function(m,x){function G(ma){A=ma;var la;if(!U(A)){if(fa(A))if(ub(A))for(E!==X&&(E=X,ea=E.length=0,S++),ma=A.length,ea!==ma&&(S++,E.length=ea=ma),la=0;la<ma;la++){var ya=E[la];var ua=A[la];var mb=ya!==ya&&ua!==ua;mb||ya===ua||(S++,E[la]=ua)}else{E!==ha&&(E=ha={},ea=0,S++);ma=0;for(la in A)bb.call(A,la)&&(ma++,ua=A[la],
ya=E[la],la in E?(mb=ya!==ya&&ua!==ua,mb||ya===ua||(S++,E[la]=ua)):(ea++,E[la]=ua,S++));if(ea>ma)for(la in S++,E)bb.call(A,la)||(ea--,delete E[la])}else E!==A&&(E=A,S++);return S}}G.$stateful=!0;var B=this,A,E,L,Q=1<x.length,S=0;m=f(m,G);var X=[],ha={},ka=!0,ea=0;return this.$watch(m,function(){ka?(ka=!1,x(A,A,B)):x(A,L,B);if(Q)if(fa(A))if(ub(A)){L=Array(A.length);for(var ma=0;ma<A.length;ma++)L[ma]=A[ma]}else for(ma in L={},A)bb.call(A,ma)&&(L[ma]=A[ma]);else L=A})},$digest:function(){var m,x,G,
B,A=b,E=[];q("$digest");k.$$checkUrlChange();this===D&&null!==e&&(k.defer.cancel(e),F());c=null;do{var L=!1;var Q=this;for(B=0;B<y.length;B++){try{var S=y[B];var X=S.fn;X(S.scope,S.locals)}catch(ea){g(ea)}c=null}y.length=0;a:do{if(B=!Q.$$suspended&&Q.$$watchers)for(B.$$digestWatchIndex=B.length;B.$$digestWatchIndex--;)try{if(m=B[B.$$digestWatchIndex]){var ha=m.get;if((x=ha(Q))!==(G=m.last)&&!(m.eq?db(x,G):Ua(x)&&Ua(G))){if(L=!0,c=m,m.last=m.eq?Bb(x,null):x,X=m.fn,X(x,G===H?x:G,Q),5>A){var ka=4-A;
E[ka]||(E[ka]=[]);E[ka].push({msg:ca(m.exp)?"fn: "+(m.exp.name||m.exp.toString()):m.exp,newVal:x,oldVal:G})}}else if(m===c){L=!1;break a}}}catch(ea){g(ea)}if(!(B=!Q.$$suspended&&Q.$$watchersCount&&Q.$$childHead||Q!==this&&Q.$$nextSibling))for(;Q!==this&&!(B=Q.$$nextSibling);)Q=Q.$parent}while(Q=B);if((L||y.length)&&!A--)throw D.$$phase=null,d("infdig",b,E);}while(L||y.length);for(D.$$phase=null;r<v.length;)try{v[r++]()}catch(ea){g(ea)}v.length=r=0;k.$$checkUrlChange()},$suspend:function(){this.$$suspended=
!0},$isSuspended:function(){return this.$$suspended},$resume:function(){this.$$suspended=!1},$destroy:function(){if(!this.$$destroyed){var m=this.$parent;this.$broadcast("$destroy");this.$$destroyed=!0;this===D&&k.$$applicationDestroyed();t(this,-this.$$watchersCount);for(var x in this.$$listenerCount)w(this,this.$$listenerCount[x],x);m&&m.$$childHead===this&&(m.$$childHead=this.$$nextSibling);m&&m.$$childTail===this&&(m.$$childTail=this.$$prevSibling);this.$$prevSibling&&(this.$$prevSibling.$$nextSibling=
this.$$nextSibling);this.$$nextSibling&&(this.$$nextSibling.$$prevSibling=this.$$prevSibling);this.$destroy=this.$digest=this.$apply=this.$evalAsync=this.$applyAsync=ja;this.$on=this.$watch=this.$watchGroup=function(){return ja};this.$$listeners={};this.$$nextSibling=null;l(this)}},$eval:function(m,x){return f(m)(this,x)},$evalAsync:function(m,x){D.$$phase||y.length||k.defer(function(){y.length&&D.$digest()});y.push({scope:this,fn:f(m),locals:x})},$$postDigest:function(m){v.push(m)},$apply:function(m){try{q("$apply");
try{return this.$eval(m)}finally{D.$$phase=null}}catch(x){g(x)}finally{try{D.$digest()}catch(x){throw g(x),x;}}},$applyAsync:function(m){function x(){G.$eval(m)}var G=this;m&&p.push(x);m=f(m);C()},$on:function(m,x){var G=this.$$listeners[m];G||(this.$$listeners[m]=G=[]);G.push(x);var B=this;do B.$$listenerCount[m]||(B.$$listenerCount[m]=0),B.$$listenerCount[m]++;while(B=B.$parent);var A=this;return function(){var E=G.indexOf(x);-1!==E&&(delete G[E],w(A,1,m))}},$emit:function(m,x){var G=[],B=this,
A=!1,E={name:m,targetScope:B,stopPropagation:function(){A=!0},preventDefault:function(){E.defaultPrevented=!0},defaultPrevented:!1},L=dc([E],arguments,1),Q;do{var S=B.$$listeners[m]||G;E.currentScope=B;var X=0;for(Q=S.length;X<Q;X++)if(S[X])try{S[X].apply(null,L)}catch(ha){g(ha)}else S.splice(X,1),X--,Q--;if(A)break;B=B.$parent}while(B);E.currentScope=null;return E},$broadcast:function(m,x){var G=this,B=this,A={name:m,targetScope:this,preventDefault:function(){A.defaultPrevented=!0},defaultPrevented:!1};
if(!this.$$listenerCount[m])return A;for(var E=dc([A],arguments,1),L,Q;G=B;){A.currentScope=G;B=G.$$listeners[m]||[];L=0;for(Q=B.length;L<Q;L++)if(B[L])try{B[L].apply(null,E)}catch(S){g(S)}else B.splice(L,1),L--,Q--;if(!(B=G.$$listenerCount[m]&&G.$$childHead||G!==this&&G.$$nextSibling))for(;G!==this&&!(B=G.$$nextSibling);)G=G.$parent}A.currentScope=null;return A}};var D=new n,y=D.$$asyncQueue=[],v=D.$$postDigestQueue=[],p=D.$$applyAsyncQueue=[],r=0;return D}]}function th(){var a=/^\s*(https?|s?ftp|mailto|tel|file):/,
b=/^\s*((https?|ftp|file|blob):|data:image\/)/;this.aHrefSanitizationWhitelist=function(d){return R(d)?(a=d,this):a};this.imgSrcSanitizationWhitelist=function(d){return R(d)?(b=d,this):b};this.$get=function(){return function(d,c){c=c?b:a;var e=pb(d&&d.trim()).href;return""===e||e.match(c)?d:"unsafe:"+e}}}function uh(){this.$get=["$window","$document",function(a,b){var d={},c=!((!a.nw||!a.nw.process)&&a.chrome&&(a.chrome.app&&a.chrome.app.runtime||!a.chrome.app&&a.chrome.runtime&&a.chrome.runtime.id))&&
a.history&&a.history.pushState,e=parseInt((/android (\d+)/.exec(xa((a.navigator||{}).userAgent))||[])[1],10);a=/Boxee/i.test((a.navigator||{}).userAgent);var g=b[0]||{};b=g.body&&g.body.style;var f=!1,k=!1;b&&(f=!!("transition"in b||"webkitTransition"in b),k=!!("animation"in b||"webkitAnimation"in b));return{history:!(!c||4>e||a),hasEvent:function(h){if("input"===h&&qb)return!1;if(U(d[h])){var l=g.createElement("div");d[h]="on"+h in l}return d[h]},csp:Jb(),transitions:f,animations:k,android:e}}]}
function vh(){this.$get=["$rootScope","$browser","$location",function(a,b,d){return{findBindings:function(c,e,g){c=c.getElementsByClassName("ng-binding");var f=[];I(c,function(k){var h=Va.element(k).data("$binding");h&&I(h,function(l){g?(new RegExp("(^|\\s)"+e.replace(/([-()[\]{}+?*.$^|,:#<!\\])/g,"\\$1").replace(/\x08/g,"\\x08")+"(\\s|\\||$)")).test(l)&&f.push(k):-1!==l.indexOf(e)&&f.push(k)})});return f},findModels:function(c,e,g){for(var f=["ng-","data-ng-","ng\\:"],k=0;k<f.length;++k){var h=c.querySelectorAll("["+
f[k]+"model"+(g?"=":"*=")+'"'+e+'"]');if(h.length)return h}},getLocation:function(){return d.url()},setLocation:function(c){c!==d.url()&&(d.url(c),a.$digest())},whenStable:function(c){b.notifyWhenNoOutstandingRequests(c)}}}]}function wh(){this.$get=["$rootScope","$browser","$q","$$q","$exceptionHandler",function(a,b,d,c,e){function g(k,h,l){ca(k)||(l=h,h=k,k=ja);var n=hb.call(arguments,3),q=R(l)&&!l,t=(q?c:d).defer(),w=t.promise;var H=b.defer(function(){try{t.resolve(k.apply(null,n))}catch(F){t.reject(F),
e(F)}finally{delete f[w.$$timeoutId]}q||a.$apply()},h);w.$$timeoutId=H;f[H]=t;return w}var f={};g.cancel=function(k){return k&&k.$$timeoutId in f?(f[k.$$timeoutId].promise.$$state.pur=!0,f[k.$$timeoutId].reject("canceled"),delete f[k.$$timeoutId],b.defer.cancel(k.$$timeoutId)):!1};return g}]}function pb(a){if(!na(a))return a;qb&&(Qa.setAttribute("href",a),a=Qa.href);Qa.setAttribute("href",a);return{href:Qa.href,protocol:Qa.protocol?Qa.protocol.replace(/:$/,""):"",host:Qa.host,search:Qa.search?Qa.search.replace(/^\?/,
""):"",hash:Qa.hash?Qa.hash.replace(/^#/,""):"",hostname:Qa.hostname,port:Qa.port,pathname:"/"===Qa.pathname.charAt(0)?Qa.pathname:"/"+Qa.pathname}}function ah(a){var b=[gf].concat(a.map(pb));return function(d){d=pb(d);return b.some(hf.bind(null,d))}}function hf(a,b){a=pb(a);b=pb(b);return a.protocol===b.protocol&&a.host===b.host}function xh(){this.$get=cb(ia)}function jf(a){function b(g){try{return decodeURIComponent(g)}catch(f){return g}}var d=a[0]||{},c={},e="";return function(){var g;try{var f=
d.cookie||""}catch(n){f=""}if(f!==e)for(e=f,f=e.split("; "),c={},g=0;g<f.length;g++){var k=f[g];var h=k.indexOf("=");if(0<h){var l=b(k.substring(0,h));U(c[l])&&(c[l]=b(k.substring(h+1)))}}return c}}function yh(){this.$get=jf}function kf(a){function b(d,c){if(fa(d)){var e={};I(d,function(g,f){e[f]=b(f,g)});return e}return a.factory(d+"Filter",c)}this.register=b;this.$get=["$injector",function(d){return function(c){return d.get(c+"Filter")}}];b("currency",lf);b("date",mf);b("filter",zh);b("json",Ah);
b("limitTo",Bh);b("lowercase",Ch);b("number",nf);b("orderBy",of);b("uppercase",Dh)}function zh(){return function(a,b,d,c){if(!ub(a)){if(null==a)return a;throw va("filter")("notarray",a);}c=c||"$";switch(Sd(b)){case "function":break;case "boolean":case "null":case "number":case "string":var e=!0;case "object":b=Eh(b,d,c,e);break;default:return a}return Array.prototype.filter.call(a,b)}}function Eh(a,b,d,c){var e=fa(a)&&d in a;!0===b?b=db:ca(b)||(b=function(g,f){if(U(g))return!1;if(null===g||null===
f)return g===f;if(fa(f)||fa(g)&&!kd(g))return!1;g=xa(""+g);f=xa(""+f);return-1!==g.indexOf(f)});return function(g){return e&&!fa(g)?Kb(g,a[d],b,d,!1):Kb(g,a,b,d,c)}}function Kb(a,b,d,c,e,g){var f=Sd(a),k=Sd(b);if("string"===k&&"!"===b.charAt(0))return!Kb(a,b.substring(1),d,c,e);if(oa(a))return a.some(function(l){return Kb(l,b,d,c,e)});switch(f){case "object":var h;if(e){for(h in a)if(h.charAt&&"$"!==h.charAt(0)&&Kb(a[h],b,d,c,!0))return!0;return g?!1:Kb(a,b,d,c,!1)}if("object"===k){for(h in b)if(g=
b[h],!ca(g)&&!U(g)&&(f=h===c,!Kb(f?a:a[h],g,d,c,f,f)))return!1;return!0}return d(a,b);case "function":return!1;default:return d(a,b)}}function Sd(a){return null===a?"null":typeof a}function lf(a){var b=a.NUMBER_FORMATS;return function(d,c,e){U(c)&&(c=b.CURRENCY_SYM);U(e)&&(e=b.PATTERNS[1].maxFrac);var g=c?/\u00A4/g:/\s*\u00A4\s*/g;return null==d?d:pf(d,b.PATTERNS[1],b.GROUP_SEP,b.DECIMAL_SEP,e).replace(g,c)}}function nf(a){var b=a.NUMBER_FORMATS;return function(d,c){return null==d?d:pf(d,b.PATTERNS[0],
b.GROUP_SEP,b.DECIMAL_SEP,c)}}function Fh(a){var b=0,d,c,e,g;-1<(d=a.indexOf(qf))&&(a=a.replace(qf,""));0<(c=a.search(/e/i))?(0>d&&(d=c),d+=+a.slice(c+1),a=a.substring(0,c)):0>d&&(d=a.length);for(c=0;a.charAt(c)===Td;c++);if(c===(g=a.length)){var f=[0];d=1}else{for(g--;a.charAt(g)===Td;)g--;d-=c;f=[];for(e=0;c<=g;c++,e++)f[e]=+a.charAt(c)}d>rf&&(f=f.splice(0,rf-1),b=d-1,d=1);return{d:f,e:b,i:d}}function Gh(a,b,d,c){var e=a.d,g=e.length-a.i;b=U(b)?Math.min(Math.max(d,g),c):+b;d=b+a.i;c=e[d];if(0<d){e.splice(Math.max(a.i,
d));for(var f=d;f<e.length;f++)e[f]=0}else for(g=Math.max(0,g),a.i=1,e.length=Math.max(1,d=b+1),e[0]=0,f=1;f<d;f++)e[f]=0;if(5<=c)if(0>d-1){for(c=0;c>d;c--)e.unshift(0),a.i++;e.unshift(1);a.i++}else e[d-1]++;for(;g<Math.max(0,b);g++)e.push(0);if(b=e.reduceRight(function(k,h,l,n){h+=k;n[l]=h%10;return Math.floor(h/10)},0))e.unshift(b),a.i++}function pf(a,b,d,c,e){if(!na(a)&&!Pa(a)||isNaN(a))return"";var g=!isFinite(a),f=!1,k=Math.abs(a)+"",h="";if(g)h="\u221e";else{f=Fh(k);Gh(f,e,b.minFrac,b.maxFrac);
h=f.d;k=f.i;e=f.e;g=[];for(f=h.reduce(function(l,n){return l&&!n},!0);0>k;)h.unshift(0),k++;0<k?g=h.splice(k,h.length):(g=h,h=[0]);k=[];for(h.length>=b.lgSize&&k.unshift(h.splice(-b.lgSize,h.length).join(""));h.length>b.gSize;)k.unshift(h.splice(-b.gSize,h.length).join(""));h.length&&k.unshift(h.join(""));h=k.join(d);g.length&&(h+=c+g.join(""));e&&(h+="e+"+e)}return 0>a&&!f?b.negPre+h+b.negSuf:b.posPre+h+b.posSuf}function Xc(a,b,d,c){var e="";if(0>a||c&&0>=a)c?a=-a+1:(a=-a,e="-");for(a=""+a;a.length<
b;)a=Td+a;d&&(a=a.substr(a.length-b));return e+a}function Ra(a,b,d,c,e){d=d||0;return function(g){g=g["get"+a]();if(0<d||g>-d)g+=d;0===g&&-12===d&&(g=12);return Xc(g,b,c,e)}}function oc(a,b,d){return function(c,e){c=c["get"+a]();var g=Tc((d?"STANDALONE":"")+(b?"SHORT":"")+a);return e[g][c]}}function sf(a){var b=(new Date(a,0,1)).getDay();return new Date(a,0,(4>=b?5:12)-b)}function tf(a){return function(b){var d=sf(b.getFullYear());b=new Date(b.getFullYear(),b.getMonth(),b.getDate()+(4-b.getDay()));
return Xc(1+Math.round((+b-+d)/6048E5),a)}}function Ud(a,b){return 0>=a.getFullYear()?b.ERAS[0]:b.ERAS[1]}function mf(a){function b(c){var e;if(e=c.match(d)){c=new Date(0);var g=0,f=0,k=e[8]?c.setUTCFullYear:c.setFullYear,h=e[8]?c.setUTCHours:c.setHours;e[9]&&(g=parseInt(e[9]+e[10],10),f=parseInt(e[9]+e[11],10));k.call(c,parseInt(e[1],10),parseInt(e[2],10)-1,parseInt(e[3],10));g=parseInt(e[4]||0,10)-g;f=parseInt(e[5]||0,10)-f;k=parseInt(e[6]||0,10);e=Math.round(1E3*parseFloat("0."+(e[7]||0)));h.call(c,
g,f,k,e);return c}return c}var d=/^(\d{4})-?(\d\d)-?(\d\d)(?:T(\d\d)(?::?(\d\d)(?::?(\d\d)(?:\.(\d+))?)?)?(Z|([+-])(\d\d):?(\d\d))?)?$/;return function(c,e,g){var f="",k=[],h,l;e=e||"mediumDate";e=a.DATETIME_FORMATS[e]||e;na(c)&&(c=Hh.test(c)?parseInt(c,10):b(c));Pa(c)&&(c=new Date(c));if(!Xa(c)||!isFinite(c.getTime()))return c;for(;e;)(l=Ih.exec(e))?(k=dc(k,l,1),e=k.pop()):(k.push(e),e=null);var n=c.getTimezoneOffset();g&&(n=nd(g,n),c=od(c,g,!0));I(k,function(q){h=Jh[q];f+=h?h(c,a.DATETIME_FORMATS,
n):"''"===q?"'":q.replace(/(^'|'$)/g,"").replace(/''/g,"'")});return f}}function Ah(){return function(a,b){U(b)&&(b=2);return ec(a,b)}}function Bh(){return function(a,b,d){b=Infinity===Math.abs(Number(b))?Number(b):parseInt(b,10);if(Ua(b))return a;Pa(a)&&(a=a.toString());if(!ub(a))return a;d=!d||isNaN(d)?0:parseInt(d,10);d=0>d?Math.max(0,a.length+d):d;return 0<=b?Vd(a,d,d+b):0===d?Vd(a,b,a.length):Vd(a,Math.max(0,d+b),d)}}function Vd(a,b,d){return na(a)?a.slice(b,d):hb.call(a,b,d)}function of(a){function b(e){return e.map(function(g){var f=
1,k=uc;if(ca(g))k=g;else if(na(g)){if("+"===g.charAt(0)||"-"===g.charAt(0))f="-"===g.charAt(0)?-1:1,g=g.substring(1);if(""!==g&&(k=a(g),k.constant)){var h=k();k=function(l){return l[h]}}}return{get:k,descending:f}})}function d(e){switch(typeof e){case "number":case "boolean":case "string":return!0;default:return!1}}function c(e,g){var f=0,k=e.type,h=g.type;if(k===h){h=e.value;var l=g.value;"string"===k?(h=h.toLowerCase(),l=l.toLowerCase()):"object"===k&&(fa(h)&&(h=e.index),fa(l)&&(l=g.index));h!==
l&&(f=h<l?-1:1)}else f=k<h?-1:1;return f}return function(e,g,f,k){if(null==e)return e;if(!ub(e))throw va("orderBy")("notarray",e);oa(g)||(g=[g]);0===g.length&&(g=["+"]);var h=b(g),l=f?-1:1,n=ca(k)?k:c;e=Array.prototype.map.call(e,function(q,t){return{value:q,tieBreaker:{value:t,type:"number",index:t},predicateValues:h.map(function(w){var H=w.get(q);w=typeof H;if(null===H)w="string",H="null";else if("object"===w)a:{if(ca(H.valueOf)&&(H=H.valueOf(),d(H)))break a;kd(H)&&(H=H.toString(),d(H))}return{value:H,
type:w,index:t}})}});e.sort(function(q,t){for(var w=0,H=h.length;w<H;w++){var F=n(q.predicateValues[w],t.predicateValues[w]);if(F)return F*h[w].descending*l}return(n(q.tieBreaker,t.tieBreaker)||c(q.tieBreaker,t.tieBreaker))*l});return e=e.map(function(q){return q.value})}}function Vb(a){ca(a)&&(a={link:a});a.restrict=a.restrict||"AC";return cb(a)}function Yc(a,b,d,c,e){this.$$controls=[];this.$error={};this.$$success={};this.$pending=void 0;this.$name=e(b.name||b.ngForm||"")(d);this.$dirty=!1;this.$valid=
this.$pristine=!0;this.$submitted=this.$invalid=!1;this.$$parentForm=Zc;this.$$element=a;this.$$animate=c;uf(this)}function uf(a){a.$$classCache={};a.$$classCache[vf]=!(a.$$classCache[pc]=a.$$element.hasClass(pc))}function wf(a){function b(g,f,k){k&&!g.$$classCache[f]?(g.$$animate.addClass(g.$$element,f),g.$$classCache[f]=!0):!k&&g.$$classCache[f]&&(g.$$animate.removeClass(g.$$element,f),g.$$classCache[f]=!1)}function d(g,f,k){f=f?"-"+me(f,"-"):"";b(g,pc+f,!0===k);b(g,vf+f,!1===k)}var c=a.set,e=a.unset;
a.clazz.prototype.$setValidity=function(g,f,k){U(f)?(this.$pending||(this.$pending={}),c(this.$pending,g,k)):(this.$pending&&e(this.$pending,g,k),xf(this.$pending)&&(this.$pending=void 0));vb(f)?f?(e(this.$error,g,k),c(this.$$success,g,k)):(c(this.$error,g,k),e(this.$$success,g,k)):(e(this.$error,g,k),e(this.$$success,g,k));this.$pending?(b(this,"ng-pending",!0),this.$valid=this.$invalid=void 0,d(this,"",null)):(b(this,"ng-pending",!1),this.$valid=xf(this.$error),this.$invalid=!this.$valid,d(this,
"",this.$valid));f=this.$pending&&this.$pending[g]?void 0:this.$error[g]?!1:this.$$success[g]?!0:null;d(this,g,f);this.$$parentForm.$setValidity(g,f,this)}}function xf(a){if(a)for(var b in a)if(a.hasOwnProperty(b))return!1;return!0}function Wd(a){a.$formatters.push(function(b){return a.$isEmpty(b)?b:b.toString()})}function Wb(a,b,d,c,e,g){var f=xa(b[0].type);if(!e.android){var k=!1;b.on("compositionstart",function(){k=!0});b.on("compositionupdate",function(q){if(U(q.data)||""===q.data)k=!1});b.on("compositionend",
function(){k=!1;l()})}var h,l=function(q){h&&(g.defer.cancel(h),h=null);if(!k){var t=b.val();q=q&&q.type;"password"===f||d.ngTrim&&"false"===d.ngTrim||(t=Ca(t));(c.$viewValue!==t||""===t&&c.$$hasNativeValidators)&&c.$setViewValue(t,q)}};if(e.hasEvent("input"))b.on("input",l);else{var n=function(q,t,w){h||(h=g.defer(function(){h=null;t&&t.value===w||l(q)}))};b.on("keydown",function(q){var t=q.keyCode;91===t||15<t&&19>t||37<=t&&40>=t||n(q,this,this.value)});if(e.hasEvent("paste"))b.on("paste cut drop",
n)}b.on("change",l);if(yf[f]&&c.$$hasNativeValidators&&f===d.type)b.on("keydown wheel mousedown",function(q){if(!h){var t=this.validity,w=t.badInput,H=t.typeMismatch;h=g.defer(function(){h=null;t.badInput===w&&t.typeMismatch===H||l(q)})}});c.$render=function(){var q=c.$isEmpty(c.$viewValue)?"":c.$viewValue;b.val()!==q&&b.val(q)}}function $c(a,b){return function(d,c){if(Xa(d))return d;if(na(d)){'"'===d.charAt(0)&&'"'===d.charAt(d.length-1)&&(d=d.substring(1,d.length-1));if(Kh.test(d))return new Date(d);
a.lastIndex=0;if(d=a.exec(d)){d.shift();var e=c?{yyyy:c.getFullYear(),MM:c.getMonth()+1,dd:c.getDate(),HH:c.getHours(),mm:c.getMinutes(),ss:c.getSeconds(),sss:c.getMilliseconds()/1E3}:{yyyy:1970,MM:1,dd:1,HH:0,mm:0,ss:0,sss:0};I(d,function(g,f){f<b.length&&(e[b[f]]=+g)});c=new Date(e.yyyy,e.MM-1,e.dd,e.HH,e.mm,e.ss||0,1E3*e.sss||0);100>e.yyyy&&c.setFullYear(e.yyyy);return c}}return NaN}}function qc(a,b,d,c){return function(e,g,f,k,h,l,n){function q(y){return y&&!(y.getTime&&y.getTime()!==y.getTime())}
function t(y){return R(y)&&!Xa(y)?w(y)||void 0:y}function w(y,v){var p=k.$options.getOption("timezone");F&&F!==p&&(v=je(v,nd(F)));y=d(y,v);!isNaN(y)&&p&&(y=od(y,p));return y}Xd(e,g,f,k);Wb(e,g,f,k,h,l);var H,F;k.$$parserName=a;k.$parsers.push(function(y){if(k.$isEmpty(y))return null;if(b.test(y))return w(y,H)});k.$formatters.push(function(y){if(y&&!Xa(y))throw rc("datefmt",y);if(q(y)){H=y;var v=k.$options.getOption("timezone");v&&(F=v,H=od(H,v,!0));return n("date")(y,c,v)}F=H=null;return""});if(R(f.min)||
f.ngMin){var C;k.$validators.min=function(y){return!q(y)||U(C)||d(y)>=C};f.$observe("min",function(y){C=t(y);k.$validate()})}if(R(f.max)||f.ngMax){var D;k.$validators.max=function(y){return!q(y)||U(D)||d(y)<=D};f.$observe("max",function(y){D=t(y);k.$validate()})}}}function Xd(a,b,d,c){(c.$$hasNativeValidators=fa(b[0].validity))&&c.$parsers.push(function(e){var g=b.prop("validity")||{};return g.badInput||g.typeMismatch?void 0:e})}function zf(a){a.$$parserName="number";a.$parsers.push(function(b){if(a.$isEmpty(b))return null;
if(Lh.test(b))return parseFloat(b)});a.$formatters.push(function(b){if(!a.$isEmpty(b)){if(!Pa(b))throw rc("numfmt",b);b=b.toString()}return b})}function Xb(a){R(a)&&!Pa(a)&&(a=parseFloat(a));return Ua(a)?void 0:a}function Yd(a){var b=a.toString(),d=b.indexOf(".");return-1===d?-1<a&&1>a&&(a=/e-(\d+)$/.exec(b))?Number(a[1]):0:b.length-d-1}function Af(a,b,d){a=Number(a);var c=(a|0)!==a,e=(b|0)!==b,g=(d|0)!==d;if(c||e||g){var f=c?Yd(a):0,k=e?Yd(b):0,h=g?Yd(d):0;f=Math.pow(10,Math.max(f,k,h));a*=f;b*=
f;d*=f;c&&(a=Math.round(a));e&&(b=Math.round(b));g&&(d=Math.round(d))}return 0===(a-b)%d}function Bf(a,b,d,c,e){if(R(c)){a=a(c);if(!a.constant)throw rc("constexpr",d,c);return a(b)}return e}function Zd(a,b){function d(f,k){if(!f||!f.length)return[];if(!k||!k.length)return f;var h=[],l=0;a:for(;l<f.length;l++){for(var n=f[l],q=0;q<k.length;q++)if(n===k[q])continue a;h.push(n)}return h}function c(f){var k=f;oa(f)?k=f.map(c).join(" "):fa(f)&&(k=Object.keys(f).filter(function(h){return f[h]}).join(" "));
return k}function e(f){var k=f;if(oa(f))k=f.map(e);else if(fa(f)){var h=!1;k=Object.keys(f).filter(function(l){l=f[l];!h&&U(l)&&(h=!0);return l});h&&k.push(void 0)}return k}a="ngClass"+a;var g;return["$parse",function(f){return{restrict:"AC",link:function(k,h,l){function n(p,r){var m=[];I(p,function(x){if(0<r||D[x])D[x]=(D[x]||0)+r,D[x]===+(0<r)&&m.push(x)});return m.join(" ")}function q(p){if(p===b){var r=v;r=n(r&&r.split(" "),1);l.$addClass(r)}else r=v,r=n(r&&r.split(" "),-1),l.$removeClass(r);
y=p}function t(p){p=c(p);p!==v&&w(p)}function w(p){if(y===b){var r=v&&v.split(" "),m=p&&p.split(" "),x=d(r,m);r=d(m,r);x=n(x,-1);r=n(r,1);l.$addClass(r);l.$removeClass(x)}v=p}var H=l[a].trim(),F=":"===H.charAt(0)&&":"===H.charAt(1);H=f(H,F?e:c);var C=F?t:w,D=h.data("$classCounts"),y=!0,v;D||(D=Ea(),h.data("$classCounts",D));"ngClass"!==a&&(g||(g=f("$index",function(p){return p&1})),k.$watch(g,q));k.$watch(H,C,F)}}}]}function ad(a,b,d,c,e,g,f,k,h){this.$modelValue=this.$viewValue=Number.NaN;this.$$rawModelValue=
void 0;this.$validators={};this.$asyncValidators={};this.$parsers=[];this.$formatters=[];this.$viewChangeListeners=[];this.$untouched=!0;this.$touched=!1;this.$pristine=!0;this.$dirty=!1;this.$valid=!0;this.$invalid=!1;this.$error={};this.$$success={};this.$pending=void 0;this.$name=h(d.name||"",!1)(a);this.$$parentForm=Zc;this.$options=$d;this.$$updateEvents="";this.$$updateEventHandler=this.$$updateEventHandler.bind(this);this.$$parsedNgModel=e(d.ngModel);this.$$parsedNgModelAssign=this.$$parsedNgModel.assign;
this.$$ngModelGet=this.$$parsedNgModel;this.$$ngModelSet=this.$$parsedNgModelAssign;this.$$pendingDebounce=null;this.$$parserValid=void 0;this.$$currentValidationRunId=0;Object.defineProperty(this,"$$scope",{value:a});this.$$attr=d;this.$$element=c;this.$$animate=g;this.$$timeout=f;this.$$parse=e;this.$$q=k;this.$$exceptionHandler=b;uf(this);Mh(this)}function Mh(a){a.$$scope.$watch(function(b){b=a.$$ngModelGet(b);b===a.$modelValue||a.$modelValue!==a.$modelValue&&b!==b||a.$$setModelValue(b);return b})}
function ae(a){this.$$options=a}function Cf(a,b){I(b,function(d,c){R(a[c])||(a[c]=d)})}function Lb(a,b){a.prop("selected",b);a.attr("selected",b)}function Nh(){this.SCE_CONTEXTS=Yb;this.resourceUrlWhitelist=function(a){throw Ya("noresourceurlwhitelist");};this.resourceUrlBlacklist=function(a){throw Ya("noresourceurlblacklist");};this.$get=["$injector",function(a){var b=function(d){throw Ya("unsafe");};a.has("$sanitize")&&(b=a.get("$sanitize"));return{trustAs:function(d,c){throw Ya("notrustas");},
getTrusted:function(d,c){if(null===c||U(c)||""===c)return c;if("string"==typeof c){if(d==Yb.TEMPLATE_URL){d=a.has("html2JsTemplatesCached")?!a.get("html2JsTemplatesCached")():!ng.safehtml.googSceHelper.isCOMPILED();if(d&&hf(c,gf))return c;throw Ya("insecurl",c);}if(d==Yb.RESOURCE_URL)throw Ya("insecurl",c);if(d==Yb.HTML)return b(c);throw Ya("unsafe",d);}if(ng.safehtml.googSceHelper.isGoogHtmlType(c))try{return ng.safehtml.googSceHelper.unwrapGivenContext(d,c)}catch(e){throw Ya("googhtml",c.toString(),
d);}else throw Ya("unsafe",d);},valueOf:function(d){if(ng.safehtml.googSceHelper.isGoogHtmlType(d))try{return ng.safehtml.googSceHelper.unwrapAny(d)}catch(c){throw Ya("googhtml",d.toString());}else return d}}}]}function Oh(){this.enabled=function(a){if(arguments.length)throw Ya("nodisabling");return!0};this.$get=["$parse","$sceDelegate",function(a,b){if(8>qb)throw Ya("iequirks");if("undefined"==typeof ng||!ng.safehtml||!ng.safehtml.googSceHelper)throw Ya("nodep");var d=kb(Yb);d.isEnabled=function(){return!0};
d.trustAs=b.trustAs;d.getTrusted=b.getTrusted;d.valueOf=b.valueOf;d.parseAs=function(f,k){var h=a(k);return h.literal&&h.constant?h:a(k,function(l){return d.getTrusted(f,l)})};var c=d.parseAs,e=d.getTrusted,g=d.trustAs;I(Yb,function(f,k){k=xa(k);d[("parse_as_"+k).replace(be,Db)]=function(h){return c(f,h)};d[("get_trusted_"+k).replace(be,Db)]=function(h){return e(f,h)};d[("trust_as_"+k).replace(be,Db)]=function(h){return g(f,h)}});return d}]}function Ph(){var a;this.httpOptions=function(b){return b?
(a=b,this):a};this.$get=["$exceptionHandler","$templateCache","$http","$q","$sce",function(b,d,c,e,g){function f(k,h){f.totalPendingRequests++;if(!na(k)||U(d.get(k)))k=g.getTrustedTemplateUrl(k);var l=c.defaults&&c.defaults.transformResponse;oa(l)?l=l.filter(function(n){return n!==Ld}):l===Ld&&(l=null);return c.get(k,Aa({cache:d,transformResponse:l},a)).finally(function(){f.totalPendingRequests--}).then(function(n){d.put(k,n.data);return n.data},function(n){h||(n=Qh("tpload",k,n.status,n.statusText),
b(n));return e.reject(n)})}f.totalPendingRequests=0;return f}]}var de={objectMaxDepth:5},Rh=/^\/(.+)\/([a-z]*)$/,bb=Object.prototype.hasOwnProperty,xa=function(a){return na(a)?a.toLowerCase():a},Tc=function(a){return na(a)?a.toUpperCase():a},da,Ab,hb=[].slice,Qg=[].splice,Sh=[].push,Ta=Object.prototype.toString,ge=Object.getPrototypeOf,Cb=va("ng"),Va=ia.angular||(ia.angular={}),zd,sc=0;var qb=ia.document.documentMode;var Ua=Number.isNaN||function(a){return a!==a};ja.$inject=[];uc.$inject=[];var oa=
Array.isArray,Vf=/^\[object (?:Uint8|Uint8Clamped|Uint16|Uint32|Int8|Int16|Int32|Float32|Float64)Array]$/,Ca=function(a){return na(a)?a.trim():a},Jb=function(){if(!R(Jb.rules)){var a=ia.document.querySelector("[ng-csp]")||ia.document.querySelector("[data-ng-csp]");if(a){var b=a.getAttribute("ng-csp")||a.getAttribute("data-ng-csp");Jb.rules={noUnsafeEval:!b||-1!==b.indexOf("no-unsafe-eval"),noInlineStyle:!b||-1!==b.indexOf("no-inline-style")}}else{a=Jb;try{new Function(""),b=!1}catch(d){b=!0}a.rules=
{noUnsafeEval:b,noInlineStyle:!1}}}return Jb.rules},bd=function(){if(R(bd.name_))return bd.name_;var a,b,d=Nb.length;for(b=0;b<d;++b){var c=Nb[b];if(a=ia.document.querySelector("["+c.replace(":","\\:")+"jq]")){var e=a.getAttribute(c+"jq");break}}return bd.name_=e},Xf=/:/g,Nb=["ng-","data-ng-","ng:","x-ng-"],$f=function(a){var b=a.currentScript;if(!b)return!0;if(!(b instanceof ia.HTMLScriptElement||b instanceof ia.SVGScriptElement))return!1;b=b.attributes;return[b.getNamedItem("src"),b.getNamedItem("href"),
b.getNamedItem("xlink:href")].every(function(d){if(!d)return!0;if(!d.value)return!1;var c=a.createElement("a");c.href=d.value;if(a.location.origin===c.origin)return!0;switch(c.protocol){case "http:":case "https:":case "ftp:":case "blob:":case "file:":case "data:":return!0;default:return!1}})}(ia.document),cg=/[A-Z]/g,Df=!1,wb=3,Th={full:"1.6.4-local+sha.617b36117",major:1,minor:6,dot:void 0,codeName:"undefined"};Ha.expando="ng339";var ic=Ha.cache={},ig=1;Ha._data=function(a){return this.cache[a[this.expando]]||
{}};var Ac=/-([a-z])/g,Uh=/^-ms-/,zc={mouseleave:"mouseout",mouseenter:"mouseover"},ud=va("jqLite"),hg=/^<([\w-]+)\s*\/?>(?:<\/\1>|)$/,td=/<|&#?\w+;/,fg=/<([\w:-]+)/,gg=/<(?!area|br|col|embed|hr|img|input|link|meta|param)(([\w:-]+)[^>]*)\/>/gi,eb={option:[1,'<select multiple="multiple">',"</select>"],thead:[1,"<table>","</table>"],col:[2,"<table><colgroup>","</colgroup></table>"],tr:[2,"<table><tbody>","</tbody></table>"],td:[3,"<table><tbody><tr>","</tr></tbody></table>"],_default:[0,"",""]};eb.optgroup=
eb.option;eb.tbody=eb.tfoot=eb.colgroup=eb.caption=eb.thead;eb.th=eb.td;var og=ia.Node.prototype.contains||function(a){return!!(this.compareDocumentPosition(a)&16)},Qb=Ha.prototype={ready:pe,toString:function(){var a=[];I(this,function(b){a.push(""+b)});return"["+a.join(", ")+"]"},eq:function(a){return 0<=a?da(this[a]):da(this[this.length+a])},length:0,push:Sh,sort:[].sort,splice:[].splice},Gc={};I("multiple selected checked disabled readOnly required open".split(" "),function(a){Gc[xa(a)]=a});var ue=
{};I("input select option textarea button form details".split(" "),function(a){ue[a]=!0});var Me={ngMinlength:"minlength",ngMaxlength:"maxlength",ngMin:"min",ngMax:"max",ngPattern:"pattern",ngStep:"step"};I({data:yd,removeData:xd,hasData:function(a){for(var b in ic[a.ng339])return!0;return!1},cleanData:function(a){for(var b=0,d=a.length;b<d;b++)xd(a[b])}},function(a,b){Ha[b]=a});I({data:yd,inheritedData:Ec,scope:function(a){return da.data(a,"$scope")||Ec(a.parentNode||a,["$isolateScope","$scope"])},
isolateScope:function(a){return da.data(a,"$isolateScope")||da.data(a,"$isolateScopeNoTemplate")},controller:re,injector:function(a){return Ec(a,"$injector")},removeAttr:function(a,b){a.removeAttribute(b)},hasClass:Bc,css:function(a,b,d){b=b.replace(Uh,"ms-").replace(Ac,Db);if(R(d))a.style[b]=d;else return a.style[b]},attr:function(a,b,d){var c=a.nodeType;if(c!==wb&&2!==c&&8!==c&&a.getAttribute){c=xa(b);var e=Gc[c];if(R(d))null===d||!1===d&&e?a.removeAttribute(b):a.setAttribute(b,e?c:d);else return a=
a.getAttribute(b),e&&null!==a&&(a=c),null===a?void 0:a}},prop:function(a,b,d){if(R(d))a[b]=d;else return a[b]},text:function(){function a(b,d){if(U(d))return d=b.nodeType,1===d||d===wb?b.textContent:"";b.textContent=d}a.$dv="";return a}(),val:function(a,b){if(U(b)){if(a.multiple&&"select"===ib(a)){var d=[];I(a.options,function(c){c.selected&&d.push(c.value||c.text)});return d}return a.value}a.value=b},html:function(a,b){if(U(b))return a.innerHTML;xc(a,!0);a.innerHTML=b},empty:se},function(a,b){Ha.prototype[b]=
function(d,c){var e,g,f=this.length;if(a!==se&&U(2===a.length&&a!==Bc&&a!==re?d:c)){if(fa(d)){for(e=0;e<f;e++)if(a===yd)a(this[e],d);else for(g in d)a(this[e],g,d[g]);return this}e=a.$dv;f=U(e)?Math.min(f,1):f;for(g=0;g<f;g++){var k=a(this[g],d,c);e=e?e+k:k}return e}for(e=0;e<f;e++)a(this[e],d,c);return this}});I({removeData:xd,on:function(a,b,d,c){if(R(c))throw ud("onargs");if(sd(a)){c=yc(a,!0);var e=c.events,g=c.handle;g||(g=c.handle=kg(a,e));c=0<=b.indexOf(" ")?b.split(" "):[b];for(var f=c.length,
k=function(h,l,n){var q=e[h];q||(q=e[h]=[],q.specialHandlerWrapper=l,"$destroy"===h||n||a.addEventListener(h,g));q.push(d)};f--;)b=c[f],zc[b]?(k(zc[b],mg),k(b,void 0,!0)):k(b)}},off:qe,one:function(a,b,d){a=da(a);a.on(b,function e(){a.off(b,d);a.off(b,e)});a.on(b,d)},replaceWith:function(a,b){var d,c=a.parentNode;xc(a);I(new Ha(b),function(e){d?c.insertBefore(e,d.nextSibling):c.replaceChild(e,a);d=e})},children:function(a){var b=[];I(a.childNodes,function(d){1===d.nodeType&&b.push(d)});return b},
contents:function(a){return a.contentDocument||a.childNodes||[]},append:function(a,b){var d=a.nodeType;if(1===d||11===d){b=new Ha(b);d=0;for(var c=b.length;d<c;d++)a.appendChild(b[d])}},prepend:function(a,b){if(1===a.nodeType){var d=a.firstChild;I(new Ha(b),function(c){a.insertBefore(c,d)})}},wrap:function(a,b){b=da(b).eq(0).clone()[0];var d=a.parentNode;d&&d.replaceChild(b,a);b.appendChild(a)},remove:Fc,detach:function(a){Fc(a,!0)},after:function(a,b){var d=a;if(a=a.parentNode){b=new Ha(b);for(var c=
0,e=b.length;c<e;c++){var g=b[c];a.insertBefore(g,d.nextSibling);d=g}}},addClass:Dc,removeClass:Cc,toggleClass:function(a,b,d){b&&I(b.split(" "),function(c){var e=d;U(e)&&(e=!Bc(a,c));(e?Dc:Cc)(a,c)})},parent:function(a){return(a=a.parentNode)&&11!==a.nodeType?a:null},next:function(a){return a.nextElementSibling},find:function(a,b){return a.getElementsByTagName?a.getElementsByTagName(b):[]},clone:wd,triggerHandler:function(a,b,d){var c=b.type||b,e=yc(a);if(e=(e=e&&e.events)&&e[c]){var g={preventDefault:function(){this.defaultPrevented=
!0},isDefaultPrevented:function(){return!0===this.defaultPrevented},stopImmediatePropagation:function(){this.immediatePropagationStopped=!0},isImmediatePropagationStopped:function(){return!0===this.immediatePropagationStopped},stopPropagation:ja,type:c,target:a};b.type&&(g=Aa(g,b));b=kb(e);var f=d?[g].concat(d):[g];I(b,function(k){g.isImmediatePropagationStopped()||k.apply(a,f)})}}},function(a,b){Ha.prototype[b]=function(d,c,e){for(var g,f=0,k=this.length;f<k;f++)U(g)?(g=a(this[f],d,c,e),R(g)&&(g=
da(g))):vd(g,a(this[f],d,c,e));return R(g)?g:this}});Ha.prototype.bind=Ha.prototype.on;Ha.prototype.unbind=Ha.prototype.off;var Vh=Object.create(null);ve.prototype={_idx:function(a){if(a===this._lastKey)return this._lastIndex;this._lastKey=a;return this._lastIndex=this._keys.indexOf(a)},_transformKey:function(a){return Ua(a)?Vh:a},get:function(a){a=this._transformKey(a);a=this._idx(a);if(-1!==a)return this._values[a]},set:function(a,b){a=this._transformKey(a);var d=this._idx(a);-1===d&&(d=this._lastIndex=
this._keys.length);this._keys[d]=a;this._values[d]=b},delete:function(a){a=this._transformKey(a);a=this._idx(a);if(-1===a)return!1;this._keys.splice(a,1);this._values.splice(a,1);this._lastKey=NaN;this._lastIndex=-1;return!0}};var Hc=ve,Wh=[function(){this.$get=[function(){return Hc}]}],rg=/^([^(]+?)=>/,sg=/^[^(]*\(\s*([^)]*)\)/m,Xh=/,/,Yh=/^\s*(_?)(\S+?)\1\s*$/,qg=/((\/\/.*$)|(\/\*[\s\S]*?\*\/))/mg,Eb=va("$injector");gc.$$annotate=function(a,b,d){var c;if("function"===typeof a){if(!(c=a.$inject)){c=
[];if(a.length){if(b)throw na(d)&&d||(d=a.name||tg(a)),Eb("strictdi",d);b=we(a);I(b[1].split(Xh),function(e){e.replace(Yh,function(g,f,k){c.push(k)})})}a.$inject=c}}else oa(a)?(b=a.length-1,vc(a[b],"fn"),c=a.slice(0,b)):vc(a,"fn",!0);return c};var Ef=va("$animate"),Zh=function(){this.$get=ja},$h=function(){var a=new Hc,b=[];this.$get=["$$AnimateRunner","$rootScope",function(d,c){function e(f,k,h){var l=!1;k&&(k=na(k)?k.split(" "):oa(k)?k:[],I(k,function(n){n&&(l=!0,f[n]=h)}));return l}function g(){I(b,
function(f){var k=a.get(f);if(k){var h=vg(f.attr("class")),l="",n="";I(k,function(q,t){q!==!!h[t]&&(q?l+=(l.length?" ":"")+t:n+=(n.length?" ":"")+t)});I(f,function(q){l&&Dc(q,l);n&&Cc(q,n)});a.delete(f)}});b.length=0}return{enabled:ja,on:ja,off:ja,pin:ja,push:function(f,k,h,l){l&&l();h=h||{};h.from&&f.css(h.from);h.to&&f.css(h.to);if(h.addClass||h.removeClass)if(k=h.addClass,l=h.removeClass,h=a.get(f)||{},k=e(h,k,!0),l=e(h,l,!1),k||l)a.set(f,h),b.push(f),1===b.length&&c.$$postDigest(g);f=new d;f.complete();
return f}}}]},ai=["$provide",function(a){var b=this,d=null,c=null;this.$$registeredAnimations=Object.create(null);this.register=function(e,g){if(e&&"."!==e.charAt(0))throw Ef("notcsel",e);var f=e+"-animation";b.$$registeredAnimations[e.substr(1)]=f;a.factory(f,g)};this.customFilter=function(e){1===arguments.length&&(c=ca(e)?e:null);return c};this.classNameFilter=function(e){if(1===arguments.length&&(d=e instanceof RegExp?e:null)&&/[(\s|\/)]ng-animate[(\s|\/)]/.test(d.toString()))throw d=null,Ef("nongcls",
"ng-animate");return d};this.$get=["$$animateQueue",function(e){function g(f,k,h){if(h){var l;a:{for(l=0;l<h.length;l++){var n=h[l];if(1===n.nodeType){l=n;break a}}l=void 0}!l||l.parentNode||l.previousElementSibling||(h=null)}h?h.after(f):k.prepend(f)}return{on:e.on,off:e.off,pin:e.pin,enabled:e.enabled,cancel:function(f){f.end&&f.end()},enter:function(f,k,h,l){k=k&&da(k);h=h&&da(h);k=k||h.parent();g(f,k,h);return e.push(f,"enter",Fb(l))},move:function(f,k,h,l){k=k&&da(k);h=h&&da(h);k=k||h.parent();
g(f,k,h);return e.push(f,"move",Fb(l))},leave:function(f,k){return e.push(f,"leave",Fb(k),function(){f.remove()})},addClass:function(f,k,h){h=Fb(h);h.addClass=jc(h.addclass,k);return e.push(f,"addClass",h)},removeClass:function(f,k,h){h=Fb(h);h.removeClass=jc(h.removeClass,k);return e.push(f,"removeClass",h)},setClass:function(f,k,h,l){l=Fb(l);l.addClass=jc(l.addClass,k);l.removeClass=jc(l.removeClass,h);return e.push(f,"setClass",l)},animate:function(f,k,h,l,n){n=Fb(n);n.from=n.from?Aa(n.from,k):
k;n.to=n.to?Aa(n.to,h):h;n.tempClasses=jc(n.tempClasses,l||"ng-inline-animate");return e.push(f,"animate",n)}}}]}],bi=function(){this.$get=["$$rAF",function(a){function b(c){d.push(c);1<d.length||a(function(){for(var e=0;e<d.length;e++)d[e]();d=[]})}var d=[];return function(){var c=!1;b(function(){c=!0});return function(e){c?e():b(e)}}}]},ci=function(){this.$get=["$q","$sniffer","$$animateAsyncRun","$$isDocumentHidden","$timeout",function(a,b,d,c,e){function g(f){this.setHost(f);var k=d();this._doneCallbacks=
[];this._tick=function(h){c()?e(h,0,!1):k(h)};this._state=0}g.chain=function(f,k){function h(){if(l===f.length)k(!0);else f[l](function(n){!1===n?k(!1):(l++,h())})}var l=0;h()};g.all=function(f,k){function h(q){n=n&&q;++l===f.length&&k(n)}var l=0,n=!0;I(f,function(q){q.done(h)})};g.prototype={setHost:function(f){this.host=f||{}},done:function(f){2===this._state?f():this._doneCallbacks.push(f)},progress:ja,getPromise:function(){if(!this.promise){var f=this;this.promise=a(function(k,h){f.done(function(l){!1===
l?h():k()})})}return this.promise},then:function(f,k){return this.getPromise().then(f,k)},"catch":function(f){return this.getPromise()["catch"](f)},"finally":function(f){return this.getPromise()["finally"](f)},pause:function(){this.host.pause&&this.host.pause()},resume:function(){this.host.resume&&this.host.resume()},end:function(){this.host.end&&this.host.end();this._resolve(!0)},cancel:function(){this.host.cancel&&this.host.cancel();this._resolve(!1)},complete:function(f){var k=this;0===k._state&&
(k._state=1,k._tick(function(){k._resolve(f)}))},_resolve:function(f){2!==this._state&&(I(this._doneCallbacks,function(k){k(f)}),this._doneCallbacks.length=0,this._state=2)}};return g}]},di=function(){this.$get=["$$rAF","$q","$$AnimateRunner",function(a,b,d){return function(c,e){function g(){a(function(){f.addClass&&(c.addClass(f.addClass),f.addClass=null);f.removeClass&&(c.removeClass(f.removeClass),f.removeClass=null);f.to&&(c.css(f.to),f.to=null);k||h.complete();k=!0});return h}var f=e||{};f.$$prepared||
(f=Bb(f));f.cleanupStyles&&(f.from=f.to=null);f.from&&(c.css(f.from),f.from=null);var k,h=new d;return{start:g,end:g}}}]},Ka=va("$compile"),Jd=new function(){};xe.$inject=["$provide","$$sanitizeUriProvider"];Rc.prototype.isFirstChange=function(){return this.previousValue===Jd};var Be=/^((?:x|data)[:\-_])/i,Pg=/[:\-_]+(.)/g,Qe=va("$controller"),Pe=/^(\S+)(\s+as\s+([\w$]+))?$/,ei=function(){this.$get=["$document",function(a){return function(b){b?!b.nodeType&&b instanceof da&&(b=b[0]):b=a[0].body;return b.offsetWidth+
1}}]},Re="application/json",Md={"Content-Type":Re+";charset=utf-8"},Yg=/^\[|^\{(?!\{)/,Zg={"[":/]$/,"{":/}$/},Xg=/^\)]\}',?\n/,Sc=va("$http"),Ib=Va.$interpolateMinErr=va("$interpolate");Ib.throwNoconcat=function(a){throw Ib("noconcat",a);};Ib.interr=function(a,b){return Ib("interr",a,b.toString())};var fi=function(){this.$get=function(){function a(c){var e=function(g){e.data=g;e.called=!0};e.id=c;return e}var b=Va.callbacks,d={};return{createCallback:function(c){c="_"+(b.$$counter++).toString(36);
var e="angular.callbacks."+c,g=a(c);d[e]=b[c]=g;return e},wasCalled:function(c){return d[c].called},getResponse:function(c){return d[c].data},removeCallback:function(c){delete b[d[c].id];delete d[c]}}}},gi=/^([^?#]*)(\?([^#]*))?(#(.*))?$/,gh={http:80,https:443,ftp:21},mc=va("$location"),hh=/^\s*[\\/]{2,}/,hi={$$absUrl:"",$$html5:!1,$$replace:!1,absUrl:Uc("$$absUrl"),url:function(a){if(U(a))return this.$$url;var b=gi.exec(a);(b[1]||""===a)&&this.path(decodeURIComponent(b[1]));(b[2]||b[1]||""===a)&&
this.search(b[3]||"");this.hash(b[5]||"");return this},protocol:Uc("$$protocol"),host:Uc("$$host"),port:Uc("$$port"),path:Ye("$$path",function(a){a=null!==a?a.toString():"";return"/"===a.charAt(0)?a:"/"+a}),search:function(a,b){switch(arguments.length){case 0:return this.$$search;case 1:if(na(a)||Pa(a))a=a.toString(),this.$$search=pd(a);else if(fa(a))a=Bb(a,{}),I(a,function(d,c){null==d&&delete a[c]}),this.$$search=a;else throw mc("isrcharg");break;default:U(b)||null===b?delete this.$$search[a]:this.$$search[a]=
b}this.$$compose();return this},hash:Ye("$$hash",function(a){return null!==a?a.toString():""}),replace:function(){this.$$replace=!0;return this}};I([Xe,Qd,Pd],function(a){a.prototype=Object.create(hi);a.prototype.state=function(b){if(!arguments.length)return this.$$state;if(a!==Pd||!this.$$html5)throw mc("nostate");this.$$state=U(b)?null:b;this.$$urlUpdatedByLocation=!0;return this}});var Zb=va("$parse"),nh={}.constructor.prototype.valueOf,cd=Ea();I("+ - * / % === !== == != < > <= >= && || ! = |".split(" "),
function(a){cd[a]=!0});var ii={n:"\n",f:"\f",r:"\r",t:"\t",v:"\v","'":"'",'"':'"'},Wc=function(a){this.options=a};Wc.prototype={constructor:Wc,lex:function(a){this.text=a;this.index=0;for(this.tokens=[];this.index<this.text.length;)if(a=this.text.charAt(this.index),'"'===a||"'"===a)this.readString(a);else if(this.isNumber(a)||"."===a&&this.isNumber(this.peek()))this.readNumber();else if(this.isIdentifierStart(this.peekMultichar()))this.readIdent();else if(this.is(a,"(){}[].,;:?"))this.tokens.push({index:this.index,
text:a}),this.index++;else if(this.isWhitespace(a))this.index++;else{var b=a+this.peek(),d=b+this.peek(2),c=cd[b],e=cd[d];cd[a]||c||e?(a=e?d:c?b:a,this.tokens.push({index:this.index,text:a,operator:!0}),this.index+=a.length):this.throwError("Unexpected next character ",this.index,this.index+1)}return this.tokens},is:function(a,b){return-1!==b.indexOf(a)},peek:function(a){a=a||1;return this.index+a<this.text.length?this.text.charAt(this.index+a):!1},isNumber:function(a){return"0"<=a&&"9">=a&&"string"===
typeof a},isWhitespace:function(a){return" "===a||"\r"===a||"\t"===a||"\n"===a||"\v"===a||"\u00a0"===a},isIdentifierStart:function(a){return this.options.isIdentifierStart?this.options.isIdentifierStart(a,this.codePointAt(a)):this.isValidIdentifierStart(a)},isValidIdentifierStart:function(a){return"a"<=a&&"z">=a||"A"<=a&&"Z">=a||"_"===a||"$"===a},isIdentifierContinue:function(a){return this.options.isIdentifierContinue?this.options.isIdentifierContinue(a,this.codePointAt(a)):this.isValidIdentifierContinue(a)},
isValidIdentifierContinue:function(a,b){return this.isValidIdentifierStart(a,b)||this.isNumber(a)},codePointAt:function(a){return 1===a.length?a.charCodeAt(0):(a.charCodeAt(0)<<10)+a.charCodeAt(1)-56613888},peekMultichar:function(){var a=this.text.charAt(this.index),b=this.peek();if(!b)return a;var d=a.charCodeAt(0),c=b.charCodeAt(0);return 55296<=d&&56319>=d&&56320<=c&&57343>=c?a+b:a},isExpOperator:function(a){return"-"===a||"+"===a||this.isNumber(a)},throwError:function(a,b,d){d=d||this.index;b=
R(b)?"s "+b+"-"+this.index+" ["+this.text.substring(b,d)+"]":" "+d;throw Zb("lexerr",a,b,this.text);},readNumber:function(){for(var a="",b=this.index;this.index<this.text.length;){var d=xa(this.text.charAt(this.index));if("."===d||this.isNumber(d))a+=d;else{var c=this.peek();if("e"===d&&this.isExpOperator(c))a+=d;else if(this.isExpOperator(d)&&c&&this.isNumber(c)&&"e"===a.charAt(a.length-1))a+=d;else if(!this.isExpOperator(d)||c&&this.isNumber(c)||"e"!==a.charAt(a.length-1))break;else this.throwError("Invalid exponent")}this.index++}this.tokens.push({index:b,
text:a,constant:!0,value:Number(a)})},readIdent:function(){var a=this.index;for(this.index+=this.peekMultichar().length;this.index<this.text.length;){var b=this.peekMultichar();if(!this.isIdentifierContinue(b))break;this.index+=b.length}this.tokens.push({index:a,text:this.text.slice(a,this.index),identifier:!0})},readString:function(a){var b=this.index;this.index++;for(var d="",c=a,e=!1;this.index<this.text.length;){var g=this.text.charAt(this.index);c+=g;if(e)"u"===g?(e=this.text.substring(this.index+
1,this.index+5),e.match(/[\da-f]{4}/i)||this.throwError("Invalid unicode escape [\\u"+e+"]"),this.index+=4,d+=String.fromCharCode(parseInt(e,16))):d+=ii[g]||g,e=!1;else if("\\"===g)e=!0;else{if(g===a){this.index++;this.tokens.push({index:b,text:c,constant:!0,value:d});return}d+=g}this.index++}this.throwError("Unterminated quote",b)}};var P=function(a,b){this.lexer=a;this.options=b};P.Program="Program";P.ExpressionStatement="ExpressionStatement";P.AssignmentExpression="AssignmentExpression";P.ConditionalExpression=
"ConditionalExpression";P.LogicalExpression="LogicalExpression";P.BinaryExpression="BinaryExpression";P.UnaryExpression="UnaryExpression";P.CallExpression="CallExpression";P.MemberExpression="MemberExpression";P.Identifier="Identifier";P.Literal="Literal";P.ArrayExpression="ArrayExpression";P.Property="Property";P.ObjectExpression="ObjectExpression";P.ThisExpression="ThisExpression";P.LocalsExpression="LocalsExpression";P.NGValueParameter="NGValueParameter";P.prototype={ast:function(a){this.text=
a;this.tokens=this.lexer.lex(a);a=this.program();0!==this.tokens.length&&this.throwError("is an unexpected token",this.tokens[0]);return a},program:function(){for(var a=[];;)if(0<this.tokens.length&&!this.peek("}",")",";","]")&&a.push(this.expressionStatement()),!this.expect(";"))return{type:P.Program,body:a}},expressionStatement:function(){return{type:P.ExpressionStatement,expression:this.filterChain()}},filterChain:function(){for(var a=this.expression();this.expect("|");)a=this.filter(a);return a},
expression:function(){return this.assignment()},assignment:function(){var a=this.ternary();if(this.expect("=")){if(!bf(a))throw Zb("lval");a={type:P.AssignmentExpression,left:a,right:this.assignment(),operator:"="}}return a},ternary:function(){var a=this.logicalOR();if(this.expect("?")){var b=this.expression();if(this.consume(":")){var d=this.expression();return{type:P.ConditionalExpression,test:a,alternate:b,consequent:d}}}return a},logicalOR:function(){for(var a=this.logicalAND();this.expect("||");)a=
{type:P.LogicalExpression,operator:"||",left:a,right:this.logicalAND()};return a},logicalAND:function(){for(var a=this.equality();this.expect("&&");)a={type:P.LogicalExpression,operator:"&&",left:a,right:this.equality()};return a},equality:function(){for(var a=this.relational(),b;b=this.expect("==","!=","===","!==");)a={type:P.BinaryExpression,operator:b.text,left:a,right:this.relational()};return a},relational:function(){for(var a=this.additive(),b;b=this.expect("<",">","<=",">=");)a={type:P.BinaryExpression,
operator:b.text,left:a,right:this.additive()};return a},additive:function(){for(var a=this.multiplicative(),b;b=this.expect("+","-");)a={type:P.BinaryExpression,operator:b.text,left:a,right:this.multiplicative()};return a},multiplicative:function(){for(var a=this.unary(),b;b=this.expect("*","/","%");)a={type:P.BinaryExpression,operator:b.text,left:a,right:this.unary()};return a},unary:function(){var a;return(a=this.expect("+","-","!"))?{type:P.UnaryExpression,operator:a.text,prefix:!0,argument:this.unary()}:
this.primary()},primary:function(){if(this.expect("(")){var a=this.filterChain();this.consume(")")}else this.expect("[")?a=this.arrayDeclaration():this.expect("{")?a=this.object():this.selfReferential.hasOwnProperty(this.peek().text)?a=Bb(this.selfReferential[this.consume().text]):this.options.literals.hasOwnProperty(this.peek().text)?a={type:P.Literal,value:this.options.literals[this.consume().text]}:this.peek().identifier?a=this.identifier():this.peek().constant?a=this.constant():this.throwError("not a primary expression",
this.peek());for(var b;b=this.expect("(","[",".");)"("===b.text?(a={type:P.CallExpression,callee:a,arguments:this.parseArguments()},this.consume(")")):"["===b.text?(a={type:P.MemberExpression,object:a,property:this.expression(),computed:!0},this.consume("]")):"."===b.text?a={type:P.MemberExpression,object:a,property:this.identifier(),computed:!1}:this.throwError("IMPOSSIBLE");return a},filter:function(a){a=[a];for(var b={type:P.CallExpression,callee:this.identifier(),arguments:a,filter:!0};this.expect(":");)a.push(this.expression());
return b},parseArguments:function(){var a=[];if(")"!==this.peekToken().text){do a.push(this.filterChain());while(this.expect(","))}return a},identifier:function(){var a=this.consume();a.identifier||this.throwError("is not a valid identifier",a);return{type:P.Identifier,name:a.text}},constant:function(){return{type:P.Literal,value:this.consume().value}},arrayDeclaration:function(){var a=[];if("]"!==this.peekToken().text){do{if(this.peek("]"))break;a.push(this.expression())}while(this.expect(","))}this.consume("]");
return{type:P.ArrayExpression,elements:a}},object:function(){var a=[];if("}"!==this.peekToken().text){do{if(this.peek("}"))break;var b={type:P.Property,kind:"init"};this.peek().constant?(b.key=this.constant(),b.computed=!1,this.consume(":"),b.value=this.expression()):this.peek().identifier?(b.key=this.identifier(),b.computed=!1,this.peek(":")?(this.consume(":"),b.value=this.expression()):b.value=b.key):this.peek("[")?(this.consume("["),b.key=this.expression(),this.consume("]"),b.computed=!0,this.consume(":"),
b.value=this.expression()):this.throwError("invalid key",this.peek());a.push(b)}while(this.expect(","))}this.consume("}");return{type:P.ObjectExpression,properties:a}},throwError:function(a,b){throw Zb("syntax",b.text,a,b.index+1,this.text,this.text.substring(b.index));},consume:function(a){if(0===this.tokens.length)throw Zb("ueoe",this.text);var b=this.expect(a);b||this.throwError("is unexpected, expecting ["+a+"]",this.peek());return b},peekToken:function(){if(0===this.tokens.length)throw Zb("ueoe",
this.text);return this.tokens[0]},peek:function(a,b,d,c){return this.peekAhead(0,a,b,d,c)},peekAhead:function(a,b,d,c,e){if(this.tokens.length>a){a=this.tokens[a];var g=a.text;if(g===b||g===d||g===c||g===e||!(b||d||c||e))return a}return!1},expect:function(a,b,d,c){return(a=this.peek(a,b,d,c))?(this.tokens.shift(),a):!1},selfReferential:{"this":{type:P.ThisExpression},$locals:{type:P.LocalsExpression}}};var $e=2;df.prototype={compile:function(a){var b=this;this.state={nextId:0,filters:{},fn:{vars:[],
body:[],own:{}},assign:{vars:[],body:[],own:{}},inputs:[]};Ja(a,b.$filter);var d="",c;this.stage="assign";if(c=cf(a))this.state.computing="assign",d=this.nextId(),this.recurse(c,d),this.return_(d),d="fn.assign="+this.generateFunction("assign","s,v,l");c=af(a.body);b.stage="inputs";I(c,function(e,g){var f="fn"+g;b.state[f]={vars:[],body:[],own:{}};b.state.computing=f;var k=b.nextId();b.recurse(e,k);b.return_(k);b.state.inputs.push({name:f,isPure:e.isPure});e.watchId=g});this.state.computing="fn";this.stage=
"main";this.recurse(a);a='"'+this.USE+" "+this.STRICT+'";\n'+this.filterPrefix()+"var fn="+this.generateFunction("fn","s,l,a,i")+d+this.watchFns()+"return fn;";a=(new Function("$filter","getStringValue","ifDefined","plus",a))(this.$filter,kh,lh,Ze);this.state=this.stage=void 0;return a},USE:"use",STRICT:"strict",watchFns:function(){var a=[],b=this.state.inputs,d=this;I(b,function(c){a.push("var "+c.name+"="+d.generateFunction(c.name,"s"));c.isPure&&a.push(c.name,".isPure="+JSON.stringify(c.isPure)+
";")});b.length&&a.push("fn.inputs=["+b.map(function(c){return c.name}).join(",")+"];");return a.join("")},generateFunction:function(a,b){return"function("+b+"){"+this.varsPrefix(a)+this.body(a)+"};"},filterPrefix:function(){var a=[],b=this;I(this.state.filters,function(d,c){a.push(d+"=$filter("+b.escape(c)+")")});return a.length?"var "+a.join(",")+";":""},varsPrefix:function(a){return this.state[a].vars.length?"var "+this.state[a].vars.join(",")+";":""},body:function(a){return this.state[a].body.join("")},
recurse:function(a,b,d,c,e,g){var f=this;c=c||ja;if(!g&&R(a.watchId))b=b||this.nextId(),this.if_("i",this.lazyAssign(b,this.computedMember("i",a.watchId)),this.lazyRecurse(a,b,d,c,e,!0));else switch(a.type){case P.Program:I(a.body,function(t,w){f.recurse(t.expression,void 0,void 0,function(H){l=H});w!==a.body.length-1?f.current().body.push(l,";"):f.return_(l)});break;case P.Literal:var k=this.escape(a.value);this.assign(b,k);c(b||k);break;case P.UnaryExpression:this.recurse(a.argument,void 0,void 0,
function(t){l=t});k=a.operator+"("+this.ifDefined(l,0)+")";this.assign(b,k);c(k);break;case P.BinaryExpression:this.recurse(a.left,void 0,void 0,function(t){h=t});this.recurse(a.right,void 0,void 0,function(t){l=t});k="+"===a.operator?this.plus(h,l):"-"===a.operator?this.ifDefined(h,0)+a.operator+this.ifDefined(l,0):"("+h+")"+a.operator+"("+l+")";this.assign(b,k);c(k);break;case P.LogicalExpression:b=b||this.nextId();f.recurse(a.left,b);f.if_("&&"===a.operator?b:f.not(b),f.lazyRecurse(a.right,b));
c(b);break;case P.ConditionalExpression:b=b||this.nextId();f.recurse(a.test,b);f.if_(b,f.lazyRecurse(a.alternate,b),f.lazyRecurse(a.consequent,b));c(b);break;case P.Identifier:b=b||this.nextId();d&&(d.context="inputs"===f.stage?"s":this.assign(this.nextId(),this.getHasOwnProperty("l",a.name)+"?l:s"),d.computed=!1,d.name=a.name);f.if_("inputs"===f.stage||f.not(f.getHasOwnProperty("l",a.name)),function(){f.if_("inputs"===f.stage||"s",function(){e&&1!==e&&f.if_(f.isNull(f.nonComputedMember("s",a.name)),
f.lazyAssign(f.nonComputedMember("s",a.name),"{}"));f.assign(b,f.nonComputedMember("s",a.name))})},b&&f.lazyAssign(b,f.nonComputedMember("l",a.name)));c(b);break;case P.MemberExpression:var h=d&&(d.context=this.nextId())||this.nextId();b=b||this.nextId();f.recurse(a.object,h,void 0,function(){f.if_(f.notNull(h),function(){a.computed?(l=f.nextId(),f.recurse(a.property,l),f.getStringValue(l),e&&1!==e&&f.if_(f.not(f.computedMember(h,l)),f.lazyAssign(f.computedMember(h,l),"{}")),k=f.computedMember(h,
l),f.assign(b,k),d&&(d.computed=!0,d.name=l)):(e&&1!==e&&f.if_(f.isNull(f.nonComputedMember(h,a.property.name)),f.lazyAssign(f.nonComputedMember(h,a.property.name),"{}")),k=f.nonComputedMember(h,a.property.name),f.assign(b,k),d&&(d.computed=!1,d.name=a.property.name))},function(){f.assign(b,"undefined")});c(b)},!!e);break;case P.CallExpression:b=b||this.nextId();if(a.filter){var l=f.filter(a.callee.name);var n=[];I(a.arguments,function(t){var w=f.nextId();f.recurse(t,w);n.push(w)});k=l+"("+n.join(",")+
")";f.assign(b,k);c(b)}else l=f.nextId(),h={},n=[],f.recurse(a.callee,l,h,function(){f.if_(f.notNull(l),function(){I(a.arguments,function(t){f.recurse(t,a.constant?void 0:f.nextId(),void 0,function(w){n.push(w)})});k=h.name?f.member(h.context,h.name,h.computed)+"("+n.join(",")+")":l+"("+n.join(",")+")";f.assign(b,k)},function(){f.assign(b,"undefined")});c(b)});break;case P.AssignmentExpression:l=this.nextId();h={};this.recurse(a.left,void 0,h,function(){f.if_(f.notNull(h.context),function(){f.recurse(a.right,
l);k=f.member(h.context,h.name,h.computed)+a.operator+l;f.assign(b,k);c(b||k)})},1);break;case P.ArrayExpression:n=[];I(a.elements,function(t){f.recurse(t,a.constant?void 0:f.nextId(),void 0,function(w){n.push(w)})});k="["+n.join(",")+"]";this.assign(b,k);c(b||k);break;case P.ObjectExpression:n=[];var q=!1;I(a.properties,function(t){t.computed&&(q=!0)});q?(b=b||this.nextId(),this.assign(b,"{}"),I(a.properties,function(t){t.computed?(h=f.nextId(),f.recurse(t.key,h)):h=t.key.type===P.Identifier?t.key.name:
""+t.key.value;l=f.nextId();f.recurse(t.value,l);f.assign(f.member(b,h,t.computed),l)})):(I(a.properties,function(t){f.recurse(t.value,a.constant?void 0:f.nextId(),void 0,function(w){n.push(f.escape(t.key.type===P.Identifier?t.key.name:""+t.key.value)+":"+w)})}),k="{"+n.join(",")+"}",this.assign(b,k));c(b||k);break;case P.ThisExpression:this.assign(b,"s");c(b||"s");break;case P.LocalsExpression:this.assign(b,"l");c(b||"l");break;case P.NGValueParameter:this.assign(b,"v"),c(b||"v")}},getHasOwnProperty:function(a,
b){var d=a+"."+b,c=this.current().own;c.hasOwnProperty(d)||(c[d]=this.nextId(!1,a+"&&("+this.escape(b)+" in "+a+")"));return c[d]},assign:function(a,b){if(a)return this.current().body.push(a,"=",b,";"),a},filter:function(a){this.state.filters.hasOwnProperty(a)||(this.state.filters[a]=this.nextId(!0));return this.state.filters[a]},ifDefined:function(a,b){return"ifDefined("+a+","+this.escape(b)+")"},plus:function(a,b){return"plus("+a+","+b+")"},return_:function(a){this.current().body.push("return ",
a,";")},if_:function(a,b,d){if(!0===a)b();else{var c=this.current().body;c.push("if(",a,"){");b();c.push("}");d&&(c.push("else{"),d(),c.push("}"))}},not:function(a){return"!("+a+")"},isNull:function(a){return a+"==null"},notNull:function(a){return a+"!=null"},nonComputedMember:function(a,b){var d=/[^$_a-zA-Z0-9]/g;return/^[$_a-zA-Z][$_a-zA-Z0-9]*$/.test(b)?a+"."+b:a+'["'+b.replace(d,this.stringEscapeFn)+'"]'},computedMember:function(a,b){return a+"["+b+"]"},member:function(a,b,d){return d?this.computedMember(a,
b):this.nonComputedMember(a,b)},getStringValue:function(a){this.assign(a,"getStringValue("+a+")")},lazyRecurse:function(a,b,d,c,e,g){var f=this;return function(){f.recurse(a,b,d,c,e,g)}},lazyAssign:function(a,b){var d=this;return function(){d.assign(a,b)}},stringEscapeRegex:/[^ a-zA-Z0-9]/g,stringEscapeFn:function(a){return"\\u"+("0000"+a.charCodeAt(0).toString(16)).slice(-4)},escape:function(a){if(na(a))return"'"+a.replace(this.stringEscapeRegex,this.stringEscapeFn)+"'";if(Pa(a))return a.toString();
if(!0===a)return"true";if(!1===a)return"false";if(null===a)return"null";if("undefined"===typeof a)return"undefined";throw Zb("esc");},nextId:function(a,b){var d="v"+this.state.nextId++;a||this.current().vars.push(d+(b?"="+b:""));return d},current:function(){return this.state[this.state.computing]}};ef.prototype={compile:function(a){var b=this;Ja(a,b.$filter);var d;if(d=cf(a))var c=this.recurse(d);d=af(a.body);if(d){var e=[];I(d,function(f,k){var h=b.recurse(f);h.isPure=f.isPure;f.input=h;e.push(h);
f.watchId=k})}var g=[];I(a.body,function(f){g.push(b.recurse(f.expression))});a=0===a.body.length?ja:1===a.body.length?g[0]:function(f,k){var h;I(g,function(l){h=l(f,k)});return h};c&&(a.assign=function(f,k,h){return c(f,h,k)});e&&(a.inputs=e);return a},recurse:function(a,b,d){var c=this;if(a.input)return this.inputs(a.input,a.watchId);switch(a.type){case P.Literal:return this.value(a.value,b);case P.UnaryExpression:var e=this.recurse(a.argument);return this["unary"+a.operator](e,b);case P.BinaryExpression:var g=
this.recurse(a.left);e=this.recurse(a.right);return this["binary"+a.operator](g,e,b);case P.LogicalExpression:return g=this.recurse(a.left),e=this.recurse(a.right),this["binary"+a.operator](g,e,b);case P.ConditionalExpression:return this["ternary?:"](this.recurse(a.test),this.recurse(a.alternate),this.recurse(a.consequent),b);case P.Identifier:return c.identifier(a.name,b,d);case P.MemberExpression:return g=this.recurse(a.object,!1,!!d),a.computed||(e=a.property.name),a.computed&&(e=this.recurse(a.property)),
a.computed?this.computedMember(g,e,b,d):this.nonComputedMember(g,e,b,d);case P.CallExpression:var f=[];I(a.arguments,function(k){f.push(c.recurse(k))});a.filter&&(e=this.$filter(a.callee.name));a.filter||(e=this.recurse(a.callee,!0));return a.filter?function(k,h,l,n){for(var q=[],t=0;t<f.length;++t)q.push(f[t](k,h,l,n));k=e.apply(void 0,q,n);return b?{context:void 0,name:void 0,value:k}:k}:function(k,h,l,n){var q=e(k,h,l,n);if(null!=q.value){var t=[];for(var w=0;w<f.length;++w)t.push(f[w](k,h,l,n));
t=q.value.apply(q.context,t)}return b?{value:t}:t};case P.AssignmentExpression:return g=this.recurse(a.left,!0,1),e=this.recurse(a.right),function(k,h,l,n){var q=g(k,h,l,n);k=e(k,h,l,n);q.context[q.name]=k;return b?{value:k}:k};case P.ArrayExpression:return f=[],I(a.elements,function(k){f.push(c.recurse(k))}),function(k,h,l,n){for(var q=[],t=0;t<f.length;++t)q.push(f[t](k,h,l,n));return b?{value:q}:q};case P.ObjectExpression:return f=[],I(a.properties,function(k){k.computed?f.push({key:c.recurse(k.key),
computed:!0,value:c.recurse(k.value)}):f.push({key:k.key.type===P.Identifier?k.key.name:""+k.key.value,computed:!1,value:c.recurse(k.value)})}),function(k,h,l,n){for(var q={},t=0;t<f.length;++t)f[t].computed?q[f[t].key(k,h,l,n)]=f[t].value(k,h,l,n):q[f[t].key]=f[t].value(k,h,l,n);return b?{value:q}:q};case P.ThisExpression:return function(k){return b?{value:k}:k};case P.LocalsExpression:return function(k,h){return b?{value:h}:h};case P.NGValueParameter:return function(k,h,l){return b?{value:l}:l}}},
"unary+":function(a,b){return function(d,c,e,g){d=a(d,c,e,g);d=R(d)?+d:0;return b?{value:d}:d}},"unary-":function(a,b){return function(d,c,e,g){d=a(d,c,e,g);d=R(d)?-d:-0;return b?{value:d}:d}},"unary!":function(a,b){return function(d,c,e,g){d=!a(d,c,e,g);return b?{value:d}:d}},"binary+":function(a,b,d){return function(c,e,g,f){var k=a(c,e,g,f);c=b(c,e,g,f);k=Ze(k,c);return d?{value:k}:k}},"binary-":function(a,b,d){return function(c,e,g,f){var k=a(c,e,g,f);c=b(c,e,g,f);k=(R(k)?k:0)-(R(c)?c:0);return d?
{value:k}:k}},"binary*":function(a,b,d){return function(c,e,g,f){c=a(c,e,g,f)*b(c,e,g,f);return d?{value:c}:c}},"binary/":function(a,b,d){return function(c,e,g,f){c=a(c,e,g,f)/b(c,e,g,f);return d?{value:c}:c}},"binary%":function(a,b,d){return function(c,e,g,f){c=a(c,e,g,f)%b(c,e,g,f);return d?{value:c}:c}},"binary===":function(a,b,d){return function(c,e,g,f){c=a(c,e,g,f)===b(c,e,g,f);return d?{value:c}:c}},"binary!==":function(a,b,d){return function(c,e,g,f){c=a(c,e,g,f)!==b(c,e,g,f);return d?{value:c}:
c}},"binary==":function(a,b,d){return function(c,e,g,f){c=a(c,e,g,f)==b(c,e,g,f);return d?{value:c}:c}},"binary!=":function(a,b,d){return function(c,e,g,f){c=a(c,e,g,f)!=b(c,e,g,f);return d?{value:c}:c}},"binary<":function(a,b,d){return function(c,e,g,f){c=a(c,e,g,f)<b(c,e,g,f);return d?{value:c}:c}},"binary>":function(a,b,d){return function(c,e,g,f){c=a(c,e,g,f)>b(c,e,g,f);return d?{value:c}:c}},"binary<=":function(a,b,d){return function(c,e,g,f){c=a(c,e,g,f)<=b(c,e,g,f);return d?{value:c}:c}},"binary>=":function(a,
b,d){return function(c,e,g,f){c=a(c,e,g,f)>=b(c,e,g,f);return d?{value:c}:c}},"binary&&":function(a,b,d){return function(c,e,g,f){c=a(c,e,g,f)&&b(c,e,g,f);return d?{value:c}:c}},"binary||":function(a,b,d){return function(c,e,g,f){c=a(c,e,g,f)||b(c,e,g,f);return d?{value:c}:c}},"ternary?:":function(a,b,d,c){return function(e,g,f,k){e=a(e,g,f,k)?b(e,g,f,k):d(e,g,f,k);return c?{value:e}:e}},value:function(a,b){return function(){return b?{context:void 0,name:void 0,value:a}:a}},identifier:function(a,
b,d){return function(c,e,g,f){c=e&&a in e?e:c;d&&1!==d&&c&&null==c[a]&&(c[a]={});e=c?c[a]:void 0;return b?{context:c,name:a,value:e}:e}},computedMember:function(a,b,d,c){return function(e,g,f,k){var h=a(e,g,f,k);if(null!=h){var l=b(e,g,f,k);l+="";c&&1!==c&&h&&!h[l]&&(h[l]={});var n=h[l]}return d?{context:h,name:l,value:n}:n}},nonComputedMember:function(a,b,d,c){return function(e,g,f,k){e=a(e,g,f,k);c&&1!==c&&e&&null==e[b]&&(e[b]={});g=null!=e?e[b]:void 0;return d?{context:e,name:b,value:g}:g}},inputs:function(a,
b){return function(d,c,e,g){return g?g[b]:a(d,c,e)}}};Vc.prototype={constructor:Vc,parse:function(a){a=this.getAst(a);var b=this.astCompiler.compile(a.ast),d=a.ast;b.literal=0===d.body.length||1===d.body.length&&(d.body[0].expression.type===P.Literal||d.body[0].expression.type===P.ArrayExpression||d.body[0].expression.type===P.ObjectExpression);b.constant=a.ast.constant;b.oneTime=a.oneTime;return b},getAst:function(a){var b=!1;a=a.trim();":"===a.charAt(0)&&":"===a.charAt(1)&&(b=!0,a=a.substring(2));
return{ast:this.ast.ast(a),oneTime:b}}};var Qa=ia.document.createElement("a"),gf=pb(ia.location.href);jf.$inject=["$document"];kf.$inject=["$provide"];var rf=22,qf=".",Td="0";lf.$inject=["$locale"];nf.$inject=["$locale"];var Jh={yyyy:Ra("FullYear",4,0,!1,!0),yy:Ra("FullYear",2,0,!0,!0),y:Ra("FullYear",1,0,!1,!0),MMMM:oc("Month"),MMM:oc("Month",!0),MM:Ra("Month",2,1),M:Ra("Month",1,1),LLLL:oc("Month",!1,!0),dd:Ra("Date",2),d:Ra("Date",1),HH:Ra("Hours",2),H:Ra("Hours",1),hh:Ra("Hours",2,-12),h:Ra("Hours",
1,-12),mm:Ra("Minutes",2),m:Ra("Minutes",1),ss:Ra("Seconds",2),s:Ra("Seconds",1),sss:Ra("Milliseconds",3),EEEE:oc("Day"),EEE:oc("Day",!0),a:function(a,b){return 12>a.getHours()?b.AMPMS[0]:b.AMPMS[1]},Z:function(a,b,d){a=-1*d;return(0<=a?"+":"")+(Xc(Math[0<a?"floor":"ceil"](a/60),2)+Xc(Math.abs(a%60),2))},ww:tf(2),w:tf(1),G:Ud,GG:Ud,GGG:Ud,GGGG:function(a,b){return 0>=a.getFullYear()?b.ERANAMES[0]:b.ERANAMES[1]}},Ih=/((?:[^yMLdHhmsaZEwG']+)|(?:'(?:[^']|'')*')|(?:E+|y+|M+|L+|d+|H+|h+|m+|s+|a|Z|G+|w+))([\s\S]*)/,
Hh=/^-?\d+$/;mf.$inject=["$locale"];var Ch=cb(xa),Dh=cb(Tc);of.$inject=["$parse"];var ji=cb({restrict:"E",compile:function(a,b){if(!b.href&&!b.xlinkHref)return function(d,c){if("a"===c[0].nodeName.toLowerCase()){var e="[object SVGAnimatedString]"===Ta.call(c.prop("href"))?"xlink:href":"href";c.on("click",function(g){c.attr(e)||g.preventDefault()})}}}}),dd={};I(Gc,function(a,b){function d(g,f,k){g.$watch(k[c],function(h){k.$set(b,!!h)})}if("multiple"!==a){var c=lb("ng-"+b),e=d;"checked"===a&&(e=function(g,
f,k){k.ngModel!==k[c]&&d(g,f,k)});dd[c]=function(){return{restrict:"A",priority:100,link:e}}}});I(Me,function(a,b){dd[b]=function(){return{priority:100,link:function(d,c,e){if("ngPattern"===b&&"/"===e.ngPattern.charAt(0)&&(c=e.ngPattern.match(Rh))){e.$set("ngPattern",new RegExp(c[1],c[2]));return}d.$watch(e[b],function(g){e.$set(b,g)})}}}});I(["src","srcset","href"],function(a){var b=lb("ng-"+a);dd[b]=function(){return{priority:99,link:function(d,c,e){var g=a,f=a;"href"===a&&"[object SVGAnimatedString]"===
Ta.call(c.prop("href"))&&(f="xlinkHref",e.$attr[f]="xlink:href",g=null);e.$observe(b,function(k){k?(e.$set(f,k),qb&&g&&c.prop(g,e[f])):"href"===a&&e.$set(f,null)})}}}});var Zc={$addControl:ja,$$renameControl:function(a,b){a.$name=b},$removeControl:ja,$setValidity:ja,$setDirty:ja,$setPristine:ja,$setSubmitted:ja};Yc.$inject=["$element","$attrs","$scope","$animate","$interpolate"];Yc.prototype={$rollbackViewValue:function(){I(this.$$controls,function(a){a.$rollbackViewValue()})},$commitViewValue:function(){I(this.$$controls,
function(a){a.$commitViewValue()})},$addControl:function(a){Ob(a.$name,"input");this.$$controls.push(a);a.$name&&(this[a.$name]=a);a.$$parentForm=this},$$renameControl:function(a,b){var d=a.$name;this[d]===a&&delete this[d];this[b]=a;a.$name=b},$removeControl:function(a){a.$name&&this[a.$name]===a&&delete this[a.$name];I(this.$pending,function(b,d){this.$setValidity(d,null,a)},this);I(this.$error,function(b,d){this.$setValidity(d,null,a)},this);I(this.$$success,function(b,d){this.$setValidity(d,null,
a)},this);cc(this.$$controls,a);a.$$parentForm=Zc},$setDirty:function(){this.$$animate.removeClass(this.$$element,$b);this.$$animate.addClass(this.$$element,ed);this.$dirty=!0;this.$pristine=!1;this.$$parentForm.$setDirty()},$setPristine:function(){this.$$animate.setClass(this.$$element,$b,ed+" ng-submitted");this.$dirty=!1;this.$pristine=!0;this.$submitted=!1;I(this.$$controls,function(a){a.$setPristine()})},$setUntouched:function(){I(this.$$controls,function(a){a.$setUntouched()})},$setSubmitted:function(){this.$$animate.addClass(this.$$element,
"ng-submitted");this.$submitted=!0;this.$$parentForm.$setSubmitted()}};wf({clazz:Yc,set:function(a,b,d){var c=a[b];c?-1===c.indexOf(d)&&c.push(d):a[b]=[d]},unset:function(a,b,d){var c=a[b];c&&(cc(c,d),0===c.length&&delete a[b])}});var Ff=function(a){return["$timeout","$parse",function(b,d){function c(e){return""===e?d('this[""]').assign:d(e).assign||ja}return{name:"form",restrict:a?"EAC":"E",require:["form","^^?form"],controller:Yc,compile:function(e,g){e.addClass($b).addClass(pc);var f=g.name?"name":
a&&g.ngForm?"ngForm":!1;return{pre:function(k,h,l,n){var q=n[0];if(!("action"in l)){var t=function(H){k.$apply(function(){q.$commitViewValue();q.$setSubmitted()});H.preventDefault()};h[0].addEventListener("submit",t);h.on("$destroy",function(){b(function(){h[0].removeEventListener("submit",t)},0,!1)})}(n[1]||q.$$parentForm).$addControl(q);var w=f?c(q.$name):ja;f&&(w(k,q),l.$observe(f,function(H){q.$name!==H&&(w(k,void 0),q.$$parentForm.$$renameControl(q,H),w=c(q.$name),w(k,q))}));h.on("$destroy",
function(){q.$$parentForm.$removeControl(q);w(k,void 0);Aa(q,Zc)})}}}}}]},ki=Ff(),li=Ff(!0),Kh=/^\d{4,}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d\.\d+(?:[+-][0-2]\d:[0-5]\d|Z)$/,mi=/^[a-z][a-z\d.+-]*:\/*(?:[^:@]+(?::[^@]+)?@)?(?:[^\s:/?#]+|\[[a-f\d:]+])(?::\d+)?(?:\/[^?#]*)?(?:\?[^#]*)?(?:#.*)?$/i,ni=/^(?=.{1,254}$)(?=.{1,64}@)[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+(\.[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+)*@[A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?(\.[A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*$/,Lh=/^\s*(-|\+)?(\d+|(\d*(\.\d*)))([eE][+-]?\d+)?\s*$/,
Gf=/^(\d{4,})-(\d{2})-(\d{2})$/,Hf=/^(\d{4,})-(\d\d)-(\d\d)T(\d\d):(\d\d)(?::(\d\d)(\.\d{1,3})?)?$/,ce=/^(\d{4,})-W(\d\d)$/,If=/^(\d{4,})-(\d\d)$/,Jf=/^(\d\d):(\d\d)(?::(\d\d)(\.\d{1,3})?)?$/,yf=Ea();I(["date","datetime-local","month","time","week"],function(a){yf[a]=!0});var Kf={text:function(a,b,d,c,e,g){Wb(a,b,d,c,e,g);Wd(c)},date:qc("date",Gf,$c(Gf,["yyyy","MM","dd"]),"yyyy-MM-dd"),"datetime-local":qc("datetimelocal",Hf,$c(Hf,"yyyy MM dd HH mm ss sss".split(" ")),"yyyy-MM-ddTHH:mm:ss.sss"),time:qc("time",
Jf,$c(Jf,["HH","mm","ss","sss"]),"HH:mm:ss.sss"),week:qc("week",ce,function(a,b){if(Xa(a))return a;if(na(a)){ce.lastIndex=0;var d=ce.exec(a);if(d){a=+d[1];var c=+d[2],e=d=0,g=0,f=0,k=sf(a);c=7*(c-1);b&&(d=b.getHours(),e=b.getMinutes(),g=b.getSeconds(),f=b.getMilliseconds());return new Date(a,0,k.getDate()+c,d,e,g,f)}}return NaN},"yyyy-Www"),month:qc("month",If,$c(If,["yyyy","MM"]),"yyyy-MM"),number:function(a,b,d,c,e,g){Xd(a,b,d,c);zf(c);Wb(a,b,d,c,e,g);var f,k;if(R(d.min)||d.ngMin)c.$validators.min=
function(l){return c.$isEmpty(l)||U(f)||l>=f},d.$observe("min",function(l){f=Xb(l);c.$validate()});if(R(d.max)||d.ngMax)c.$validators.max=function(l){return c.$isEmpty(l)||U(k)||l<=k},d.$observe("max",function(l){k=Xb(l);c.$validate()});if(R(d.step)||d.ngStep){var h;c.$validators.step=function(l,n){return c.$isEmpty(n)||U(h)||Af(n,f||0,h)};d.$observe("step",function(l){h=Xb(l);c.$validate()})}},url:function(a,b,d,c,e,g){Wb(a,b,d,c,e,g);Wd(c);c.$$parserName="url";c.$validators.url=function(f,k){f=
f||k;return c.$isEmpty(f)||mi.test(f)}},email:function(a,b,d,c,e,g){Wb(a,b,d,c,e,g);Wd(c);c.$$parserName="email";c.$validators.email=function(f,k){f=f||k;return c.$isEmpty(f)||ni.test(f)}},radio:function(a,b,d,c){var e=!d.ngTrim||"false"!==Ca(d.ngTrim);U(d.name)&&b.attr("name",++sc);b.on("click",function(g){if(b[0].checked){var f=d.value;e&&(f=Ca(f));c.$setViewValue(f,g&&g.type)}});c.$render=function(){var g=d.value;e&&(g=Ca(g));b[0].checked=g===c.$viewValue};d.$observe("value",c.$render)},range:function(a,
b,d,c,e,g){function f(C,D){b.attr(C,d[C]);d.$observe(C,D)}function k(C){q=Xb(C);Ua(c.$modelValue)||(n?(C=b.val(),q>C&&(C=q,b.val(C)),c.$setViewValue(C)):c.$validate())}function h(C){t=Xb(C);Ua(c.$modelValue)||(n?(C=b.val(),t<C&&(b.val(t),C=t<q?q:t),c.$setViewValue(C)):c.$validate())}function l(C){w=Xb(C);Ua(c.$modelValue)||(n&&c.$viewValue!==b.val()?c.$setViewValue(b.val()):c.$validate())}Xd(a,b,d,c);zf(c);Wb(a,b,d,c,e,g);var n=c.$$hasNativeValidators&&"range"===b[0].type,q=n?0:void 0,t=n?100:void 0,
w=n?1:void 0,H=b[0].validity;a=R(d.min);e=R(d.max);g=R(d.step);var F=c.$render;c.$render=n&&R(H.rangeUnderflow)&&R(H.rangeOverflow)?function(){F();c.$setViewValue(b.val())}:F;a&&(c.$validators.min=n?function(){return!0}:function(C,D){return c.$isEmpty(D)||U(q)||D>=q},f("min",k));e&&(c.$validators.max=n?function(){return!0}:function(C,D){return c.$isEmpty(D)||U(t)||D<=t},f("max",h));g&&(c.$validators.step=n?function(){return!H.stepMismatch}:function(C,D){return c.$isEmpty(D)||U(w)||Af(D,q||0,w)},f("step",
l))},checkbox:function(a,b,d,c,e,g,f,k){var h=Bf(k,a,"ngTrueValue",d.ngTrueValue,!0),l=Bf(k,a,"ngFalseValue",d.ngFalseValue,!1);b.on("click",function(n){c.$setViewValue(b[0].checked,n&&n.type)});c.$render=function(){b[0].checked=c.$viewValue};c.$isEmpty=function(n){return!1===n};c.$formatters.push(function(n){return db(n,h)});c.$parsers.push(function(n){return n?h:l})},hidden:ja,button:ja,submit:ja,reset:ja,file:ja},Lf=["$browser","$sniffer","$filter","$parse",function(a,b,d,c){return{restrict:"E",
require:["?ngModel"],link:{pre:function(e,g,f,k){k[0]&&(Kf[xa(f.type)]||Kf.text)(e,g,f,k[0],b,a,d,c)}}}}],oi=function(){var a={configurable:!0,enumerable:!1,get:function(){return this.getAttribute("value")||""},set:function(b){this.setAttribute("value",b)}};return{restrict:"E",priority:200,compile:function(b,d){if("hidden"===xa(d.type))return{pre:function(c,e,g,f){c=e[0];c.parentNode&&c.parentNode.insertBefore(c,c.nextSibling);Object.defineProperty&&Object.defineProperty(c,"value",a)}}}}},pi=/^(true|false|\d+)$/,
qi=function(){function a(b,d,c){var e=R(c)?c:9===qb?"":null;b.prop("value",e);d.$set("value",c)}return{restrict:"A",priority:100,compile:function(b,d){return pi.test(d.ngValue)?function(c,e,g){c=c.$eval(g.ngValue);a(e,g,c)}:function(c,e,g){c.$watch(g.ngValue,function(f){a(e,g,f)})}}}},ri=["$compile",function(a){return{restrict:"AC",compile:function(b){a.$$addBindingClass(b);return function(d,c,e){a.$$addBindingInfo(c,e.ngBind);c=c[0];d.$watch(e.ngBind,function(g){c.textContent=rd(g)})}}}}],si=["$interpolate",
"$compile",function(a,b){return{compile:function(d){b.$$addBindingClass(d);return function(c,e,g){c=a(e.attr(g.$attr.ngBindTemplate));b.$$addBindingInfo(e,c.expressions);e=e[0];g.$observe("ngBindTemplate",function(f){e.textContent=U(f)?"":f})}}}}],ti=["$sce","$parse","$compile",function(a,b,d){return{restrict:"A",compile:function(c,e){var g=b(e.ngBindHtml),f=b(e.ngBindHtml,function(k){return a.valueOf(k)});d.$$addBindingClass(c);return function(k,h,l){d.$$addBindingInfo(h,l.ngBindHtml);k.$watch(f,
function(){var n=g(k);h.html(a.getTrustedHtml(n)||"")})}}}}],ui=cb({restrict:"A",require:"ngModel",link:function(a,b,d,c){c.$viewChangeListeners.push(function(){a.$eval(d.ngChange)})}}),vi=Zd("",!0),wi=Zd("Odd",0),xi=Zd("Even",1),yi=Vb({compile:function(a,b){b.$set("ngCloak",void 0);a.removeClass("ng-cloak")}}),zi=[function(){return{restrict:"A",scope:!0,controller:"@",priority:500}}],Mf={},Ai={blur:!0,focus:!0};I("click dblclick mousedown mouseup mouseover mouseout mousemove mouseenter mouseleave keydown keyup keypress submit focus blur copy cut paste".split(" "),
function(a){var b=lb("ng-"+a);Mf[b]=["$parse","$rootScope",function(d,c){return{restrict:"A",compile:function(e,g){var f=d(g[b]);return function(k,h){h.on(a,function(l){var n=function(){f(k,{$event:l})};Ai[a]&&c.$$phase?k.$evalAsync(n):k.$apply(n)})}}}}]});var Bi=["$animate","$compile",function(a,b){return{multiElement:!0,transclude:"element",priority:600,terminal:!0,restrict:"A",$$tlb:!0,link:function(d,c,e,g,f){var k,h,l;d.$watch(e.ngIf,function(n){n?h||f(function(q,t){h=t;q[q.length++]=b.$$createComment("end ngIf",
e.ngIf);k={clone:q};a.enter(q,c.parent(),c)}):(l&&(l.remove(),l=null),h&&(h.$destroy(),h=null),k&&(l=wc(k.clone),a.leave(l).done(function(q){!1!==q&&(l=null)}),k=null))})}}}],Ci=["$templateRequest","$anchorScroll","$animate",function(a,b,d){return{restrict:"ECA",priority:400,terminal:!0,transclude:"element",controller:Va.noop,compile:function(c,e){var g=e.ngInclude||e.src,f=e.onload||"",k=e.autoscroll;return function(h,l,n,q,t){var w=0,H,F,C,D=function(){F&&(F.remove(),F=null);H&&(H.$destroy(),H=
null);C&&(d.leave(C).done(function(y){!1!==y&&(F=null)}),F=C,C=null)};h.$watch(g,function(y){var v=function(r){!1===r||!R(k)||k&&!h.$eval(k)||b()},p=++w;y?(a(y,!0).then(function(r){if(!h.$$destroyed&&p===w){var m=h.$new();q.template=r;r=t(m,function(x){D();d.enter(x,null,l).done(v)});H=m;C=r;H.$emit("$includeContentLoaded",y);h.$eval(f)}},function(){h.$$destroyed||p!==w||(D(),h.$emit("$includeContentError",y))}),h.$emit("$includeContentRequested",y)):(D(),q.template=null)})}}}}],Di=["$compile",function(a){return{restrict:"ECA",
priority:-400,require:"ngInclude",link:function(b,d,c,e){Ta.call(d[0]).match(/SVG/)?(d.empty(),a(oe(e.template,ia.document).childNodes)(b,function(g){d.append(g)},{futureParentElement:d})):(d.html(e.template),a(d.contents())(b))}}}],Ei=Vb({priority:450,compile:function(){return{pre:function(a,b,d){a.$eval(d.ngInit)}}}}),Fi=function(){return{restrict:"A",priority:100,require:"ngModel",link:function(a,b,d,c){var e=d.ngList||", ",g="false"!==d.ngTrim,f=g?Ca(e):e;c.$parsers.push(function(k){if(!U(k)){var h=
[];k&&I(k.split(f),function(l){l&&h.push(g?Ca(l):l)});return h}});c.$formatters.push(function(k){if(oa(k))return k.join(e)});c.$isEmpty=function(k){return!k||!k.length}}}},pc="ng-valid",vf="ng-invalid",$b="ng-pristine",ed="ng-dirty",rc=va("ngModel");ad.$inject="$scope $exceptionHandler $attrs $element $parse $animate $timeout $q $interpolate".split(" ");ad.prototype={$$initGetterSetters:function(){if(this.$options.getOption("getterSetter")){var a=this.$$parse(this.$$attr.ngModel+"()"),b=this.$$parse(this.$$attr.ngModel+
"($$$p)");this.$$ngModelGet=function(d){var c=this.$$parsedNgModel(d);ca(c)&&(c=a(d));return c};this.$$ngModelSet=function(d,c){ca(this.$$parsedNgModel(d))?b(d,{$$$p:c}):this.$$parsedNgModelAssign(d,c)}}else if(!this.$$parsedNgModel.assign)throw rc("nonassign",this.$$attr.ngModel,jb(this.$$element));},$render:ja,$isEmpty:function(a){return U(a)||""===a||null===a||a!==a},$$updateEmptyClasses:function(a){this.$isEmpty(a)?(this.$$animate.removeClass(this.$$element,"ng-not-empty"),this.$$animate.addClass(this.$$element,
"ng-empty")):(this.$$animate.removeClass(this.$$element,"ng-empty"),this.$$animate.addClass(this.$$element,"ng-not-empty"))},$setPristine:function(){this.$dirty=!1;this.$pristine=!0;this.$$animate.removeClass(this.$$element,ed);this.$$animate.addClass(this.$$element,$b)},$setDirty:function(){this.$dirty=!0;this.$pristine=!1;this.$$animate.removeClass(this.$$element,$b);this.$$animate.addClass(this.$$element,ed);this.$$parentForm.$setDirty()},$setUntouched:function(){this.$touched=!1;this.$untouched=
!0;this.$$animate.setClass(this.$$element,"ng-untouched","ng-touched")},$setTouched:function(){this.$touched=!0;this.$untouched=!1;this.$$animate.setClass(this.$$element,"ng-touched","ng-untouched")},$rollbackViewValue:function(){this.$$timeout.cancel(this.$$pendingDebounce);this.$viewValue=this.$$lastCommittedViewValue;this.$render()},$validate:function(){if(!Ua(this.$modelValue)){var a=this.$$lastCommittedViewValue,b=this.$$rawModelValue,d=this.$valid,c=this.$modelValue,e=this.$options.getOption("allowInvalid"),
g=this;this.$$runValidators(b,a,function(f){e||d===f||(g.$modelValue=f?b:void 0,g.$modelValue!==c&&g.$$writeModelToScope())})}},$$runValidators:function(a,b,d){function c(k,h){g===f.$$currentValidationRunId&&f.$setValidity(k,h)}function e(k){g===f.$$currentValidationRunId&&d(k)}this.$$currentValidationRunId++;var g=this.$$currentValidationRunId,f=this;(function(){var k=f.$$parserName||"parse";if(U(f.$$parserValid))c(k,null);else return f.$$parserValid||(I(f.$validators,function(h,l){c(l,null)}),I(f.$asyncValidators,
function(h,l){c(l,null)})),c(k,f.$$parserValid),f.$$parserValid;return!0})()?function(){var k=!0;I(f.$validators,function(h,l){h=!!h(a,b);k=k&&h;c(l,h)});return k?!0:(I(f.$asyncValidators,function(h,l){c(l,null)}),!1)}()?function(){var k=[],h=!0;I(f.$asyncValidators,function(l,n){l=l(a,b);if(!l||!ca(l.then))throw rc("nopromise",l);c(n,void 0);k.push(l.then(function(){c(n,!0)},function(){h=!1;c(n,!1)}))});k.length?f.$$q.all(k).then(function(){e(h)},ja):e(!0)}():e(!1):e(!1)},$commitViewValue:function(){var a=
this.$viewValue;this.$$timeout.cancel(this.$$pendingDebounce);if(this.$$lastCommittedViewValue!==a||""===a&&this.$$hasNativeValidators)this.$$updateEmptyClasses(a),this.$$lastCommittedViewValue=a,this.$pristine&&this.$setDirty(),this.$$parseAndValidate()},$$parseAndValidate:function(){var a=this.$$lastCommittedViewValue,b=this;if(this.$$parserValid=U(a)?void 0:!0)for(var d=0;d<this.$parsers.length;d++)if(a=this.$parsers[d](a),U(a)){this.$$parserValid=!1;break}Ua(this.$modelValue)&&(this.$modelValue=
this.$$ngModelGet(this.$$scope));var c=this.$modelValue,e=this.$options.getOption("allowInvalid");this.$$rawModelValue=a;e&&(this.$modelValue=a,b.$modelValue!==c&&b.$$writeModelToScope());this.$$runValidators(a,this.$$lastCommittedViewValue,function(g){e||(b.$modelValue=g?a:void 0,b.$modelValue!==c&&b.$$writeModelToScope())})},$$writeModelToScope:function(){this.$$ngModelSet(this.$$scope,this.$modelValue);I(this.$viewChangeListeners,function(a){try{a()}catch(b){this.$$exceptionHandler(b)}},this)},
$setViewValue:function(a,b){this.$viewValue=a;this.$options.getOption("updateOnDefault")&&this.$$debounceViewValueCommit(b)},$$debounceViewValueCommit:function(a){var b=this.$options.getOption("debounce");Pa(b[a])?b=b[a]:Pa(b["default"])&&(b=b["default"]);this.$$timeout.cancel(this.$$pendingDebounce);var d=this;0<b?this.$$pendingDebounce=this.$$timeout(function(){d.$commitViewValue()},b):this.$$scope.$root.$$phase?this.$commitViewValue():this.$$scope.$apply(function(){d.$commitViewValue()})},$overrideModelOptions:function(a){this.$options=
this.$options.createChild(a);this.$$setUpdateOnEvents()},$processModelValue:function(){var a=this.$$format();this.$viewValue!==a&&(this.$$updateEmptyClasses(a),this.$viewValue=this.$$lastCommittedViewValue=a,this.$render(),this.$$runValidators(this.$modelValue,this.$viewValue,ja))},$$format:function(){for(var a=this.$formatters,b=a.length,d=this.$modelValue;b--;)d=a[b](d);return d},$$setModelValue:function(a){this.$modelValue=this.$$rawModelValue=a;this.$$parserValid=void 0;this.$processModelValue()},
$$setUpdateOnEvents:function(){this.$$updateEvents&&this.$$element.off(this.$$updateEvents,this.$$updateEventHandler);if(this.$$updateEvents=this.$options.getOption("updateOn"))this.$$element.on(this.$$updateEvents,this.$$updateEventHandler)},$$updateEventHandler:function(a){this.$$debounceViewValueCommit(a&&a.type)}};wf({clazz:ad,set:function(a,b){a[b]=!0},unset:function(a,b){delete a[b]}});var Gi=["$rootScope",function(a){return{restrict:"A",require:["ngModel","^?form","^?ngModelOptions"],controller:ad,
priority:1,compile:function(b){b.addClass($b).addClass("ng-untouched").addClass(pc);return{pre:function(d,c,e,g){var f=g[0];c=g[1]||f.$$parentForm;if(g=g[2])f.$options=g.$options;f.$$initGetterSetters();c.$addControl(f);e.$observe("name",function(k){f.$name!==k&&f.$$parentForm.$$renameControl(f,k)});d.$on("$destroy",function(){f.$$parentForm.$removeControl(f)})},post:function(d,c,e,g){function f(){k.$setTouched()}var k=g[0];k.$$setUpdateOnEvents();c.on("blur",function(){k.$touched||(a.$$phase?d.$evalAsync(f):
d.$apply(f))})}}}}}],Hi=/(\s+|^)default(\s+|$)/;ae.prototype={getOption:function(a){return this.$$options[a]},createChild:function(a){var b=!1;a=Aa({},a);I(a,function(d,c){"$inherit"===d?"*"===c?b=!0:(a[c]=this.$$options[c],"updateOn"===c&&(a.updateOnDefault=this.$$options.updateOnDefault)):"updateOn"===c&&(a.updateOnDefault=!1,a[c]=Ca(d.replace(Hi,function(){a.updateOnDefault=!0;return" "})))},this);b&&(delete a["*"],Cf(a,this.$$options));Cf(a,$d.$$options);return new ae(a)}};var $d=new ae({updateOn:"",
updateOnDefault:!0,debounce:0,getterSetter:!1,allowInvalid:!1,timezone:null});var Ii=function(){function a(b,d){this.$$attrs=b;this.$$scope=d}a.$inject=["$attrs","$scope"];a.prototype={$onInit:function(){var b=this.parentCtrl?this.parentCtrl.$options:$d,d=this.$$scope.$eval(this.$$attrs.ngModelOptions);this.$options=b.createChild(d)}};return{restrict:"A",priority:10,require:{parentCtrl:"?^^ngModelOptions"},bindToController:!0,controller:a}},Ji=Vb({terminal:!0,priority:1E3}),Ki=va("ngOptions"),Li=
/^\s*([\s\S]+?)(?:\s+as\s+([\s\S]+?))?(?:\s+group\s+by\s+([\s\S]+?))?(?:\s+disable\s+when\s+([\s\S]+?))?\s+for\s+(?:([$\w][$\w]*)|(?:\(\s*([$\w][$\w]*)\s*,\s*([$\w][$\w]*)\s*\)))\s+in\s+([\s\S]+?)(?:\s+track\s+by\s+([\s\S]+?))?$/,Mi=["$compile","$document","$parse",function(a,b,d){function c(f,k,h){function l(B,A,E,L,Q){this.selectValue=B;this.viewValue=A;this.label=E;this.group=L;this.disabled=Q}function n(B){if(!w&&ub(B))var A=B;else{A=[];for(var E in B)B.hasOwnProperty(E)&&"$"!==E.charAt(0)&&A.push(E)}return A}
var q=f.match(Li);if(!q)throw Ki("iexp",f,jb(k));var t=q[5]||q[7],w=q[6];f=/ as /.test(q[0])&&q[1];var H=q[9];k=d(q[2]?q[1]:t);var F=f&&d(f)||k,C=H&&d(H),D=H?function(B,A){return C(h,A)}:function(B){return Pb(B)},y=function(B,A){return D(B,G(B,A))},v=d(q[2]||q[1]),p=d(q[3]||""),r=d(q[4]||""),m=d(q[8]),x={},G=w?function(B,A){x[w]=A;x[t]=B;return x}:function(B){x[t]=B;return x};return{trackBy:H,getTrackByValue:y,getWatchables:d(m,function(B){var A=[];B=B||[];for(var E=n(B),L=E.length,Q=0;Q<L;Q++){var S=
B===E?Q:E[Q],X=B[S];S=G(X,S);X=D(X,S);A.push(X);if(q[2]||q[1])X=v(h,S),A.push(X);q[4]&&(S=r(h,S),A.push(S))}return A}),getOptions:function(){for(var B=[],A={},E=m(h)||[],L=n(E),Q=L.length,S=0;S<Q;S++){var X=E===L?S:L[S],ha=G(E[X],X),ka=F(h,ha);X=D(ka,ha);var ea=v(h,ha),ma=p(h,ha);ha=r(h,ha);ka=new l(X,ka,ea,ma,ha);B.push(ka);A[X]=ka}return{items:B,selectValueMap:A,getOptionFromViewValue:function(la){return A[y(la)]},getViewValueFromOption:function(la){return H?Bb(la.viewValue):la.viewValue}}}}}var e=
ia.document.createElement("option"),g=ia.document.createElement("optgroup");return{restrict:"A",terminal:!0,require:["select","ngModel"],link:{pre:function(f,k,h,l){l[0].registerOption=ja},post:function(f,k,h,l){function n(p){var r=(p=D.getOptionFromViewValue(p))&&p.element;r&&!r.selected&&(r.selected=!0);return p}function q(p,r){p.element=r;r.disabled=p.disabled;p.label!==r.label&&(r.label=p.label,r.textContent=p.label);r.value=p.selectValue}var t=l[0],w=l[1],H=h.multiple;l=0;for(var F=k.children(),
C=F.length;l<C;l++)if(""===F[l].value){t.hasEmptyOption=!0;t.emptyOption=F.eq(l);break}k.empty();l=!!t.emptyOption;da(e.cloneNode(!1)).val("?");var D,y=c(h.ngOptions,k,f),v=b[0].createDocumentFragment();t.generateUnknownOptionValue=function(p){return"?"};H?(t.writeValue=function(p){if(D){var r=p&&p.map(n)||[];D.items.forEach(function(m){m.element.selected&&-1===Array.prototype.indexOf.call(r,m)&&(m.element.selected=!1)})}},t.readValue=function(){var p=k.val()||[],r=[];I(p,function(m){(m=D.selectValueMap[m])&&
!m.disabled&&r.push(D.getViewValueFromOption(m))});return r},y.trackBy&&f.$watchCollection(function(){if(oa(w.$viewValue))return w.$viewValue.map(function(p){return y.getTrackByValue(p)})},function(){w.$render()})):(t.writeValue=function(p){if(D){var r=k[0].options[k[0].selectedIndex],m=D.getOptionFromViewValue(p);r&&r.removeAttribute("selected");m?(k[0].value!==m.selectValue&&(t.removeUnknownOption(),k[0].value=m.selectValue,m.element.selected=!0),m.element.setAttribute("selected","selected")):t.selectUnknownOrEmptyOption(p)}},
t.readValue=function(){var p=D.selectValueMap[k.val()];return p&&!p.disabled?(t.unselectEmptyOption(),t.removeUnknownOption(),D.getViewValueFromOption(p)):null},y.trackBy&&f.$watch(function(){return y.getTrackByValue(w.$viewValue)},function(){w.$render()}));l&&(a(t.emptyOption)(f),k.prepend(t.emptyOption),8===t.emptyOption[0].nodeType?(t.hasEmptyOption=!1,t.registerOption=function(p,r){""===r.val()&&(t.hasEmptyOption=!0,t.emptyOption=r,t.emptyOption.removeClass("ng-scope"),w.$render(),r.on("$destroy",
function(){var m=t.$isEmptyOptionSelected();t.hasEmptyOption=!1;t.emptyOption=void 0;m&&w.$render()}))}):t.emptyOption.removeClass("ng-scope"));f.$watchCollection(y.getWatchables,function(){var p=D&&t.readValue();if(D)for(var r=D.items.length-1;0<=r;r--){var m=D.items[r];R(m.group)?Fc(m.element.parentNode):Fc(m.element)}D=y.getOptions();var x={};D.items.forEach(function(G){if(R(G.group)){var B=x[G.group];B||(B=g.cloneNode(!1),v.appendChild(B),B.label=null===G.group?"null":G.group,x[G.group]=B);var A=
e.cloneNode(!1);B.appendChild(A);q(G,A)}else B=e.cloneNode(!1),v.appendChild(B),q(G,B)});k[0].appendChild(v);w.$render();w.$isEmpty(p)||(r=t.readValue(),(y.trackBy||H?db(p,r):p===r)||(w.$setViewValue(r),w.$render()))})}}}}],Ni=["$locale","$interpolate","$log",function(a,b,d){var c=/{}/g,e=/^when(Minus)?(.+)$/;return{link:function(g,f,k){function h(v){f.text(v||"")}var l=k.count,n=k.$attr.when&&f.attr(k.$attr.when),q=k.offset||0,t=g.$eval(n)||{},w={},H=b.startSymbol(),F=b.endSymbol(),C=H+l+"-"+q+F,
D=Va.noop,y;I(k,function(v,p){if(v=e.exec(p))v=(v[1]?"-":"")+xa(v[2]),t[v]=f.attr(k.$attr[p])});I(t,function(v,p){w[p]=b(v.replace(c,C))});g.$watch(l,function(v){var p=parseFloat(v),r=Ua(p);r||p in t||(p=a.pluralCat(p-q));p===y||r&&Ua(y)||(D(),r=w[p],U(r)?(null!=v&&d.debug("ngPluralize: no rule defined for '"+p+"' in "+n),D=ja,h()):D=g.$watch(r,h),y=p)})}}}],Oi=["$parse","$animate","$compile",function(a,b,d){var c=va("ngRepeat"),e=function(g,f,k,h,l,n,q){g[k]=h;l&&(g[l]=n);g.$index=f;g.$first=0===
f;g.$last=f===q-1;g.$middle=!(g.$first||g.$last);g.$odd=!(g.$even=0===(f&1))};return{restrict:"A",multiElement:!0,transclude:"element",priority:1E3,terminal:!0,$$tlb:!0,compile:function(g,f){var k=f.ngRepeat,h=d.$$createComment("end ngRepeat",k);g=k.match(/^\s*([\s\S]+?)\s+in\s+([\s\S]+?)(?:\s+as\s+([\s\S]+?))?(?:\s+track\s+by\s+([\s\S]+?))?\s*$/);if(!g)throw c("iexp",k);f=g[1];var l=g[2],n=g[3],q=g[4];g=f.match(/^(?:(\s*[$\w]+)|\(\s*([$\w]+)\s*,\s*([$\w]+)\s*\))$/);if(!g)throw c("iidexp",f);var t=
g[3]||g[1],w=g[2];if(n&&(!/^[$a-zA-Z_][$a-zA-Z0-9_]*$/.test(n)||/^(null|undefined|this|\$index|\$first|\$middle|\$last|\$even|\$odd|\$parent|\$root|\$id)$/.test(n)))throw c("badident",n);var H,F={$id:Pb};if(q)var C=a(q);else{var D=function(v,p){return Pb(p)};var y=function(v){return v}}return function(v,p,r,m,x){C&&(H=function(B,A,E){w&&(F[w]=B);F[t]=A;F.$index=E;return C(v,F)});var G=Ea();v.$watchCollection(l,function(B){var A,E=p[0],L=Ea();n&&(v[n]=B);if(ub(B)){var Q=B;var S=H||D}else for(ha in S=
H||y,Q=[],B)bb.call(B,ha)&&"$"!==ha.charAt(0)&&Q.push(ha);var X=Q.length;var ha=Array(X);for(A=0;A<X;A++){var ka=B===Q?A:Q[A];var ea=B[ka];var ma=S(ka,ea,A);if(G[ma]){var la=G[ma];delete G[ma];L[ma]=la;ha[A]=la}else{if(L[ma])throw I(ha,function(ua){ua&&ua.scope&&(G[ua.id]=ua)}),c("dupes",k,ma,ea);ha[A]={id:ma,scope:void 0,clone:void 0};L[ma]=!0}}for(ya in G){la=G[ya];ma=wc(la.clone);b.leave(ma);if(ma[0].parentNode)for(A=0,S=ma.length;A<S;A++)ma[A].$$NG_REMOVED=!0;la.scope.$destroy()}for(A=0;A<X;A++)if(ka=
B===Q?A:Q[A],ea=B[ka],la=ha[A],la.scope){var ya=E;do ya=ya.nextSibling;while(ya&&ya.$$NG_REMOVED);la.clone[0]!==ya&&b.move(wc(la.clone),null,E);E=la.clone[la.clone.length-1];e(la.scope,A,t,ea,w,ka,X)}else x(function(ua,mb){la.scope=mb;mb=h.cloneNode(!1);ua[ua.length++]=mb;b.enter(ua,null,E);E=mb;la.clone=ua;L[la.id]=la;e(la.scope,A,t,ea,w,ka,X)});G=L})}}}}],Pi=["$animate",function(a){return{restrict:"A",multiElement:!0,link:function(b,d,c){b.$watch(c.ngShow,function(e){a[e?"removeClass":"addClass"](d,
"ng-hide",{tempClasses:"ng-hide-animate"})})}}}],Qi=["$animate",function(a){return{restrict:"A",multiElement:!0,link:function(b,d,c){b.$watch(c.ngHide,function(e){a[e?"addClass":"removeClass"](d,"ng-hide",{tempClasses:"ng-hide-animate"})})}}}],Ri=Vb(function(a,b,d){a.$watch(d.ngStyle,function(c,e){e&&c!==e&&I(e,function(g,f){b.css(f,"")});c&&b.css(c)},!0)}),Si=["$animate","$compile",function(a,b){return{require:"ngSwitch",controller:["$scope",function(){this.cases={}}],link:function(d,c,e,g){var f=
[],k=[],h=[],l=[],n=function(q,t){return function(w){!1!==w&&q.splice(t,1)}};d.$watch(e.ngSwitch||e.on,function(q){for(var t,w;h.length;)a.cancel(h.pop());t=0;for(w=l.length;t<w;++t){var H=wc(k[t].clone);l[t].$destroy();(h[t]=a.leave(H)).done(n(h,t))}k.length=0;l.length=0;(f=g.cases["!"+q]||g.cases["?"])&&I(f,function(F){F.transclude(function(C,D){l.push(D);D=F.element;C[C.length++]=b.$$createComment("end ngSwitchWhen");k.push({clone:C});a.enter(C,D.parent(),D)})})})}}}],Ti=Vb({transclude:"element",
priority:1200,require:"^ngSwitch",multiElement:!0,link:function(a,b,d,c,e){a=d.ngSwitchWhen.split(d.ngSwitchWhenSeparator).sort().filter(function(g,f,k){return k[f-1]!==g});I(a,function(g){c.cases["!"+g]=c.cases["!"+g]||[];c.cases["!"+g].push({transclude:e,element:b})})}}),Ui=Vb({transclude:"element",priority:1200,require:"^ngSwitch",multiElement:!0,link:function(a,b,d,c,e){c.cases["?"]=c.cases["?"]||[];c.cases["?"].push({transclude:e,element:b})}}),Vi=va("ngTransclude"),Wi=["$compile",function(a){return{restrict:"EAC",
compile:function(b){var d=a(b.contents());b.empty();return function(c,e,g,f,k){function h(){d(c,function(l){e.append(l)})}if(!k)throw Vi("orphan",jb(e));g.ngTransclude===g.$attr.ngTransclude&&(g.ngTransclude="");g=g.ngTransclude||g.ngTranscludeSlot;k(function(l,n){var q;if(q=l.length)a:{q=0;for(var t=l.length;q<t;q++){var w=l[q];if(w.nodeType!==wb||w.nodeValue.trim()){q=!0;break a}}q=void 0}q?e.append(l):(h(),n.$destroy())},null,g);g&&!k.isSlotFilled(g)&&h()}}}}],Xi=["$templateCache",function(a){return{restrict:"E",
terminal:!0,compile:function(b,d){"text/ng-template"===d.type&&a.put(d.id,b[0].text)}}}],Yi={$setViewValue:ja,$render:ja},Zi=["$element","$scope",function(a,b){function d(){f||(f=!0,b.$$postDigest(function(){f=!1;e.ngModelCtrl.$render()}))}function c(h){k||(k=!0,b.$$postDigest(function(){b.$$destroyed||(k=!1,e.ngModelCtrl.$setViewValue(e.readValue()),h&&e.ngModelCtrl.$render())}))}var e=this,g=new Hc;e.selectValueMap={};e.ngModelCtrl=Yi;e.multiple=!1;e.unknownOption=da(ia.document.createElement("option"));
e.hasEmptyOption=!1;e.emptyOption=void 0;e.renderUnknownOption=function(h){h=e.generateUnknownOptionValue(h);e.unknownOption.val(h);a.prepend(e.unknownOption);Lb(e.unknownOption,!0);a.val(h)};e.updateUnknownOption=function(h){h=e.generateUnknownOptionValue(h);e.unknownOption.val(h);Lb(e.unknownOption,!0);a.val(h)};e.generateUnknownOptionValue=function(h){return"? "+Pb(h)+" ?"};e.removeUnknownOption=function(){e.unknownOption.parent()&&e.unknownOption.remove()};e.selectEmptyOption=function(){e.emptyOption&&
(a.val(""),Lb(e.emptyOption,!0))};e.unselectEmptyOption=function(){e.hasEmptyOption&&Lb(e.emptyOption,!1)};b.$on("$destroy",function(){e.renderUnknownOption=ja});e.readValue=function(){var h=a.val();h=h in e.selectValueMap?e.selectValueMap[h]:h;return e.hasOption(h)?h:null};e.writeValue=function(h){var l=a[0].options[a[0].selectedIndex];l&&Lb(da(l),!1);e.hasOption(h)?(e.removeUnknownOption(),l=Pb(h),a.val(l in e.selectValueMap?l:h),Lb(da(a[0].options[a[0].selectedIndex]),!0)):e.selectUnknownOrEmptyOption(h)};
e.addOption=function(h,l){8!==l[0].nodeType&&(Ob(h,'"option value"'),""===h&&(e.hasEmptyOption=!0,e.emptyOption=l),l=g.get(h)||0,g.set(h,l+1),d())};e.removeOption=function(h){var l=g.get(h);l&&(1===l?(g.delete(h),""===h&&(e.hasEmptyOption=!1,e.emptyOption=void 0)):g.set(h,l-1))};e.hasOption=function(h){return!!g.get(h)};e.$hasEmptyOption=function(){return e.hasEmptyOption};e.$isUnknownOptionSelected=function(){return a[0].options[0]===e.unknownOption[0]};e.$isEmptyOptionSelected=function(){return e.hasEmptyOption&&
a[0].options[a[0].selectedIndex]===e.emptyOption[0]};e.selectUnknownOrEmptyOption=function(h){null==h&&e.emptyOption?(e.removeUnknownOption(),e.selectEmptyOption()):e.unknownOption.parent().length?e.updateUnknownOption(h):e.renderUnknownOption(h)};var f=!1,k=!1;e.registerOption=function(h,l,n,q,t){if(n.$attr.ngValue){var w,H=NaN;n.$observe("value",function(F){var C=l.prop("selected");if(R(H)){e.removeOption(w);delete e.selectValueMap[H];var D=!0}H=Pb(F);w=F;e.selectValueMap[H]=F;e.addOption(F,l);
l.attr("value",H);D&&C&&c()})}else q?n.$observe("value",function(F){e.readValue();var C=l.prop("selected");if(R(w)){e.removeOption(w);var D=!0}w=F;e.addOption(F,l);D&&C&&c()}):t?h.$watch(t,function(F,C){n.$set("value",F);var D=l.prop("selected");C!==F&&e.removeOption(C);e.addOption(F,l);C&&D&&c()}):e.addOption(n.value,l);n.$observe("disabled",function(F){if("true"===F||F&&l.prop("selected"))e.multiple?c(!0):(e.ngModelCtrl.$setViewValue(null),e.ngModelCtrl.$render())});l.on("$destroy",function(){var F=
e.readValue(),C=n.value;e.removeOption(C);d();(e.multiple&&F&&-1!==F.indexOf(C)||F===C)&&c(!0)})}}],$i=function(){return{restrict:"E",require:["select","?ngModel"],controller:Zi,priority:1,link:{pre:function(a,b,d,c){var e=c[0],g=c[1];if(g){if(e.ngModelCtrl=g,b.on("change",function(){e.removeUnknownOption();a.$apply(function(){g.$setViewValue(e.readValue())})}),d.multiple){e.multiple=!0;e.readValue=function(){var h=[];I(b.find("option"),function(l){l.selected&&!l.disabled&&(l=l.value,h.push(l in e.selectValueMap?
e.selectValueMap[l]:l))});return h};e.writeValue=function(h){I(b.find("option"),function(l){var n=!!h&&(-1!==Array.prototype.indexOf.call(h,l.value)||-1!==Array.prototype.indexOf.call(h,e.selectValueMap[l.value]));n!==l.selected&&Lb(da(l),n)})};var f,k=NaN;a.$watch(function(){k!==g.$viewValue||db(f,g.$viewValue)||(f=kb(g.$viewValue),g.$render());k=g.$viewValue});g.$isEmpty=function(h){return!h||0===h.length}}}else e.registerOption=ja},post:function(a,b,d,c){var e=c[1];if(e){var g=c[0];e.$render=function(){g.writeValue(e.$viewValue)}}}}}},
aj=["$interpolate",function(a){return{restrict:"E",priority:100,compile:function(b,d){var c;if(!R(d.ngValue))if(R(d.value))var e=a(d.value,!0);else(c=a(b.text(),!0))||d.$set("value",b.text());return function(g,f,k){var h=f.parent();(h=h.data("$selectController")||h.parent().data("$selectController"))&&h.registerOption(g,f,k,e,c)}}}}],Nf=function(){return{restrict:"A",require:"?ngModel",link:function(a,b,d,c){c&&(d.required=!0,c.$validators.required=function(e,g){return!d.required||!c.$isEmpty(g)},
d.$observe("required",function(){c.$validate()}))}}},Of=function(){return{restrict:"A",require:"?ngModel",link:function(a,b,d,c){if(c){var e,g=d.ngPattern||d.pattern;d.$observe("pattern",function(f){na(f)&&0<f.length&&(f=new RegExp("^"+f+"$"));if(f&&!f.test)throw va("ngPattern")("noregexp",g,f,jb(b));e=f||void 0;c.$validate()});c.$validators.pattern=function(f,k){return c.$isEmpty(k)||U(e)||e.test(k)}}}}},Pf=function(){return{restrict:"A",require:"?ngModel",link:function(a,b,d,c){if(c){var e=-1;d.$observe("maxlength",
function(g){g=parseInt(g,10);e=Ua(g)?-1:g;c.$validate()});c.$validators.maxlength=function(g,f){return 0>e||c.$isEmpty(f)||f.length<=e}}}}},Qf=function(){return{restrict:"A",require:"?ngModel",link:function(a,b,d,c){if(c){var e=0;d.$observe("minlength",function(g){e=parseInt(g,10)||0;c.$validate()});c.$validators.minlength=function(g,f){return c.$isEmpty(f)||f.length>=e}}}}};if(ia.angular.bootstrap)ia.console&&console.log("WARNING: Tried to load AngularJS more than once.");else{(function(){if(!Df){var a=
bd();if((Ab=U(a)?ia.jQuery:a?ia[a]:void 0)&&Ab.fn.on){da=Ab;Aa(Ab.fn,{scope:Qb.scope,isolateScope:Qb.isolateScope,controller:Qb.controller,injector:Qb.injector,inheritedData:Qb.inheritedData});var b=Ab.cleanData;Ab.cleanData=function(d){for(var c,e=0,g;null!=(g=d[e]);e++)(c=Ab._data(g,"events"))&&c.$destroy&&Ab(g).triggerHandler("$destroy");b(d)}}else da=Ha;Va.element=da;Df=!0}})();(function(a){Aa(a,{errorHandlingConfig:Rf,bootstrap:le,copy:Bb,extend:Aa,merge:Tf,equals:db,element:da,forEach:I,injector:gc,
noop:ja,bind:Mb,toJson:ec,fromJson:ie,identity:uc,isUndefined:U,isDefined:R,isString:na,isFunction:ca,isObject:fa,isNumber:Pa,isElement:id,isArray:oa,version:Th,isDate:Xa,lowercase:xa,uppercase:Tc,callbacks:{$$counter:0},getTestability:bg,reloadWithDebugInfo:ag,$$minErr:va,$$csp:Jb,$$encodeUriSegment:fc,$$encodeUriQuery:Za,$$stringify:rd});zd=dg(ia);zd("ng",["ngLocale"],["$provide",function(b){b.provider({$$sanitizeUri:th});b.provider("$compile",xe).directive({a:ji,input:Lf,textarea:Lf,form:ki,script:Xi,
select:$i,option:aj,ngBind:ri,ngBindHtml:ti,ngBindTemplate:si,ngClass:vi,ngClassEven:xi,ngClassOdd:wi,ngCloak:yi,ngController:zi,ngForm:li,ngHide:Qi,ngIf:Bi,ngInclude:Ci,ngInit:Ei,ngNonBindable:Ji,ngPluralize:Ni,ngRepeat:Oi,ngShow:Pi,ngStyle:Ri,ngSwitch:Si,ngSwitchWhen:Ti,ngSwitchDefault:Ui,ngOptions:Mi,ngTransclude:Wi,ngModel:Gi,ngList:Fi,ngChange:ui,pattern:Of,ngPattern:Of,required:Nf,ngRequired:Nf,minlength:Qf,ngMinlength:Qf,maxlength:Pf,ngMaxlength:Pf,ngValue:qi,ngModelOptions:Ii}).directive({ngInclude:Di,
input:oi}).directive(dd).directive(Mf);b.provider({$anchorScroll:ug,$animate:ai,$animateCss:di,$$animateJs:Zh,$$animateQueue:$h,$$AnimateRunner:ci,$$animateAsyncRun:bi,$browser:xg,$cacheFactory:yg,$controller:Rg,$document:Sg,$$isDocumentHidden:Tg,$exceptionHandler:Ug,$filter:kf,$$forceReflow:ei,$interpolate:eh,$interval:fh,$http:$g,$httpParamSerializer:Vg,$httpParamSerializerJQLike:Wg,$httpBackend:ch,$xhrFactory:bh,$jsonpCallbacks:fi,$location:ih,$log:jh,$parse:oh,$rootScope:sh,$q:ph,$$q:qh,$sce:Oh,
$sceDelegate:Nh,$sniffer:uh,$templateCache:zg,$templateRequest:Ph,$$testability:vh,$timeout:wh,$window:xh,$$rAF:rh,$$jqLite:pg,$$Map:Wh,$$cookieReader:yh})}]).info({angularVersion:"1.6.4-local+sha.617b36117"})})(Va);Va.module("ngLocale",[],["$provide",function(a){a.value("$locale",{DATETIME_FORMATS:{AMPMS:["AM","PM"],DAY:"Sunday Monday Tuesday Wednesday Thursday Friday Saturday".split(" "),ERANAMES:["Before Christ","Anno Domini"],ERAS:["BC","AD"],FIRSTDAYOFWEEK:6,MONTH:"January February March April May June July August September October November December".split(" "),
SHORTDAY:"Sun Mon Tue Wed Thu Fri Sat".split(" "),SHORTMONTH:"Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(" "),STANDALONEMONTH:"January February March April May June July August September October November December".split(" "),WEEKENDRANGE:[5,6],fullDate:"EEEE, MMMM d, y",longDate:"MMMM d, y",medium:"MMM d, y h:mm:ss a",mediumDate:"MMM d, y",mediumTime:"h:mm:ss a","short":"M/d/yy h:mm a",shortDate:"M/d/yy",shortTime:"h:mm a"},NUMBER_FORMATS:{CURRENCY_SYM:"$",DECIMAL_SEP:".",GROUP_SEP:",",
PATTERNS:[{gSize:3,lgSize:3,maxFrac:3,minFrac:0,minInt:1,negPre:"-",negSuf:"",posPre:"",posSuf:""},{gSize:3,lgSize:3,maxFrac:2,minFrac:2,minInt:1,negPre:"-\u00a4",negSuf:"",posPre:"\u00a4",posSuf:""}]},id:"en-us",localeID:"en_US",pluralCat:function(b,d){var c=b|0;if(void 0===d){d=Math;var e=d.min;b+="";var g=b.indexOf(".");d=e.call(d,-1==g?0:b.length-g-1,3)}return 1==c&&0==d?"one":"other"}})}]);var Ya=va("$sce"),Yb={HTML:"html",CSS:"css",URL:"url",RESOURCE_URL:"resourceUrl",TEMPLATE_URL:"templateUrl",
JS:"js"},be=/_([a-z])/g,Qh=va("$compile");da(function(){Zf(ia.document,le)})}})(window);angular.element(document).find("head").append(angular.element("<style>").text('@charset "UTF-8";\n\n[ng\\:cloak], [ng-cloak], [data-ng-cloak], [x-ng-cloak],\n.ng-cloak, .x-ng-cloak,\n.ng-hide:not(.ng-hide-animate) {\n  display: none !important;\n}\n\nng\\:form {\n  display: block;\n}\n\n.ng-animate-shim {\n  visibility:hidden;\n}\n\n.ng-anchor {\n  position:absolute;\n}\n'));

//third_party/javascript/angular/v1_6/angular-route.min.js
/*
 AngularJS v1.6.4-local+sha.617b36117
 (c) 2010-2018 Google, Inc. http://angularjs.org
 License: MIT
*/
'use strict';(function(B,e){'use strict';function J(r){C&&r.get("$route")}function K(r,y,q){return{restrict:"ECA",terminal:!0,priority:400,transclude:"element",link:function(c,d,h,k,l){function p(){t&&(q.cancel(t),t=null);m&&(m.$destroy(),m=null);v&&(t=q.leave(v),t.done(function(u){!1!==u&&(t=null)}),v=null)}function z(){var u=r.current&&r.current.locals;if(e.isDefined(u&&u.$template)){u=c.$new();var G=r.current;v=l(u,function(H){q.enter(H,null,v||d).done(function(D){!1===D||!e.isDefined(A)||A&&!c.$eval(A)||y()});
p()});m=G.scope=u;m.$emit("$viewContentLoaded");m.$eval(I)}else p()}var m,v,t,A=h.autoscroll,I=h.onload||"";c.$on("$routeChangeSuccess",z);z()}}}function L(r,y,q){return{restrict:"ECA",priority:-400,link:function(c,d){var h=q.current,k=h.locals;d.html(k.$template);var l=r(d.contents());if(h.controller){k.$scope=c;var p=y(h.controller,k);h.controllerAs&&(c[h.controllerAs]=p);d.data("$ngControllerController",p);d.children().data("$ngControllerController",p)}c[h.resolveAs||"$resolve"]=k;l(c)}}}"use strict";
var M,N,O,P;B=e.module("ngRoute",[]).info({angularVersion:"1.6.4-local+sha.617b36117"}).provider("$route",function(){function r(c,d){return e.extend(Object.create(c),d)}function y(c,d){d=d.caseInsensitiveMatch;var h={originalPath:c,regexp:c},k=h.keys=[];c=c.replace(/([().])/g,"\\$1").replace(/(\/)?:(\w+)(\*\?|[?*])?/g,function(l,p,z,m){l="?"===m||"*?"===m?"?":null;m="*"===m||"*?"===m?"*":null;k.push({name:z,optional:!!l});p=p||"";return""+(l?"":p)+"(?:"+(l?p:"")+(m&&"(.+?)"||"([^/]+)")+(l||"")+")"+
(l||"")}).replace(/([/$*])/g,"\\$1");h.regexp=new RegExp("^"+c+"$",d?"i":"");return h}M=e.isArray;N=e.isObject;O=e.isDefined;P=e.noop;var q={};this.when=function(c,d){var h=void 0;if(M(d)){h=h||[];for(var k=0,l=d.length;k<l;k++)h[k]=d[k]}else if(N(d))for(k in h=h||{},d)if("$"!==k.charAt(0)||"$"!==k.charAt(1))h[k]=d[k];d=h||d;e.isUndefined(d.reloadOnSearch)&&(d.reloadOnSearch=!0);e.isUndefined(d.caseInsensitiveMatch)&&(d.caseInsensitiveMatch=this.caseInsensitiveMatch);q[c]=e.extend(d,c&&y(c,d));c&&
(h="/"===c[c.length-1]?c.substr(0,c.length-1):c+"/",q[h]=e.extend({redirectTo:c},y(h,d)));return this};this.caseInsensitiveMatch=!1;this.otherwise=function(c){"string"===typeof c&&(c={redirectTo:c});this.when(null,c);return this};C=!0;this.eagerInstantiationEnabled=function(c){return O(c)?(C=c,this):C};this.$get=["$rootScope","$location","$routeParams","$q","$injector","$templateRequest","$sce","$browser",function(c,d,h,k,l,p,z,m){function v(a){var b=w.current;(Q=(x=H())&&b&&x.$$route===b.$$route&&
e.equals(x.pathParams,b.pathParams)&&!x.reloadOnSearch&&!E)||!b&&!x||c.$broadcast("$routeChangeStart",x,b).defaultPrevented&&a&&a.preventDefault()}function t(){var a=w.current,b=x;if(Q)a.params=b.params,e.copy(a.params,h),c.$broadcast("$routeUpdate",a);else if(b||a){E=!1;w.current=b;var f=k.resolve(b);m.$$incOutstandingRequestCount();f.then(A).then(I).then(function(g){return g&&f.then(u).then(function(n){b===w.current&&(b&&(b.locals=n,e.copy(b.params,h)),c.$broadcast("$routeChangeSuccess",b,a))})}).catch(function(g){b===
w.current&&c.$broadcast("$routeChangeError",b,a,g)}).finally(function(){m.$$completeOutstandingRequest(P)})}}function A(a){var b={route:a,hasRedirection:!1};if(a)if(a.redirectTo)if(e.isString(a.redirectTo))b.path=D(a.redirectTo,a.params),b.search=a.params,b.hasRedirection=!0;else{var f=d.path(),g=d.search();a=a.redirectTo(a.pathParams,f,g);e.isDefined(a)&&(b.url=a,b.hasRedirection=!0)}else if(a.resolveRedirectTo)return k.resolve(l.invoke(a.resolveRedirectTo)).then(function(n){e.isDefined(n)&&(b.url=
n,b.hasRedirection=!0);return b});return b}function I(a){var b=!0;if(a.route!==w.current)b=!1;else if(a.hasRedirection){var f=d.url(),g=a.url;g?d.url(g).replace():g=d.path(a.path).search(a.search).replace().url();g!==f&&(b=!1)}return b}function u(a){if(a){var b=e.extend({},a.resolve);e.forEach(b,function(f,g){b[g]=e.isString(f)?l.get(f):l.invoke(f,null,null,g)});a=G(a);e.isDefined(a)&&(b.$template=a);return k.all(b)}}function G(a){var b,f;e.isDefined(b=a.template)?e.isFunction(b)&&(b=b(a.params)):
e.isDefined(f=a.templateUrl)&&(e.isFunction(f)&&(f=f(a.params)),e.isDefined(f)&&(a.loadedTemplateUrl=z.valueOf(f),b=p(f)));return b}function H(){var a,b;e.forEach(q,function(f,g){if(g=!b){var n=d.path();g=f.keys;var R={};if(f.regexp)if(n=f.regexp.exec(n)){for(var F=1,U=n.length;F<U;++F){var S=g[F-1],T=n[F];S&&T&&(R[S.name]=T)}g=R}else g=null;else g=null;g=a=g}g&&(b=r(f,{params:e.extend({},d.search(),a),pathParams:a}),b.$$route=f)});return b||q[null]&&r(q[null],{params:{},pathParams:{}})}function D(a,
b){var f=[];e.forEach((a||"").split(":"),function(g,n){0===n?f.push(g):(g=g.match(/(\w+)(?:[?*])?(.*)/),n=g[1],f.push(b[n]),f.push(g[2]||""),delete b[n])});return f.join("")}var E=!1,x,Q,w={routes:q,reload:function(){E=!0;var a={defaultPrevented:!1,preventDefault:function(){this.defaultPrevented=!0;E=!1}};c.$evalAsync(function(){v(a);a.defaultPrevented||t()})},updateParams:function(a){if(this.current&&this.current.$$route)a=e.extend({},this.current.params,a),d.path(D(this.current.$$route.originalPath,
a)),d.search(a);else throw V("norout");}};c.$on("$locationChangeStart",v);c.$on("$locationChangeSuccess",t);return w}]}).run(J);var V=e.$$minErr("ngRoute"),C;J.$inject=["$injector"];"use strict";B.provider("$routeParams",function(){this.$get=function(){return{}}});"use strict";B.directive("ngView",K);B.directive("ngView",L);K.$inject=["$route","$anchorScroll","$animate"];L.$inject=["$compile","$controller","$route"]})(window,window.angular);

//third_party/javascript/angular/v1_6/angular-sanitize.min.js
/*
 AngularJS v1.6.4-local+sha.617b36117
 (c) 2010-2018 Google, Inc. http://angularjs.org
 License: MIT
*/
'use strict';(function(H,h){'use strict';var L=h.$$minErr("$sanitize"),O,r,P,Q,R,C,S,T,U,M;h.module("ngSanitize",[]).provider("$sanitize",function(){function m(a,b){return D(a.split(","),b)}function D(a,b){var d={},c;for(c=0;c<a.length;c++)d[b?C(a[c]):a[c]]=!0;return d}function z(a,b){b&&b.length&&r(a,D(b))}function I(a){return a.replace(/&/g,"&amp;").replace(g,function(b){var d=b.charCodeAt(0);b=b.charCodeAt(1);return"&#"+(1024*(d-55296)+(b-56320)+65536)+";"}).replace(J,function(b){return"&#"+b.charCodeAt(0)+
";"}).replace(/</g,"&lt;").replace(/>/g,"&gt;")}function K(a){for(;a;){if(a.nodeType===H.Node.ELEMENT_NODE)for(var b=a.attributes,d=0,c=b.length;d<c;d++){var e=b[d],k=e.name.toLowerCase();if("xmlns:ns1"===k||0===k.lastIndexOf("ns1:",0))a.removeAttributeNode(e),d--,c--}(b=a.firstChild)&&K(b);a=A("nextSibling",a)}}function A(a,b){if((a=b[a])&&T.call(b,a))throw L("elclob",b.outerHTML||b.outerText);return a}var E=!1,F=!1;this.$get=["$$sanitizeUri",function(a){E=!0;F&&r(n,u);return function(b){var d=[];
U(b,M(d,function(c,e){return!/^unsafe:/.test(a(c,e))}));return d.join("")}}];this.enableSvg=function(a){return R(a)?(F=a,this):F};this.addValidElements=function(a){E||(Q(a)&&(a={htmlElements:a}),z(u,a.svgElements),z(v,a.htmlVoidElements),z(n,a.htmlVoidElements),z(n,a.htmlElements));return this};this.addValidAttrs=function(a){E||r(p,D(a,!0));return this};O=h.bind;r=h.extend;P=h.forEach;Q=h.isArray;R=h.isDefined;C=h.lowercase;S=h.noop;U=function(a,b){null===a||void 0===a?a="":"string"!==typeof a&&(a=
""+a);var d=y(a);if(!d)return"";var c=5;do{if(0===c)throw L("uinput");c--;a=d.innerHTML;d=y(a)}while(a!==d.innerHTML);for(a=d.firstChild;a;){switch(a.nodeType){case 1:c=b;for(var e=c.start,k=a.nodeName.toLowerCase(),f=a.attributes,l={},q=0,N=f.length;q<N;q++){var V=f[q];l[V.name]=V.value}e.call(c,k,l);break;case 3:b.chars(a.textContent)}if(!(c=a.firstChild)&&(1===a.nodeType&&b.end(a.nodeName.toLowerCase()),c=A("nextSibling",a),!c))for(;null==c;){a=A("parentNode",a);if(a===d)break;c=A("nextSibling",
a);1===a.nodeType&&b.end(a.nodeName.toLowerCase())}a=c}for(;a=d.firstChild;)d.removeChild(a)};M=function(a,b){var d=!1,c=O(a,a.push);return{start:function(e,k){e=C(e);!d&&t[e]&&(d=e);d||!0!==n[e]||(c("<"),c(e),P(k,function(f,l){var q=C(l),N="img"===e&&"src"===q||"background"===q;!0!==p[q]||!0===B[q]&&!b(f,N)||(c(" "),c(l),c('="'),c(I(f)),c('"'))}),c(">"))},end:function(e){e=C(e);d||!0!==n[e]||!0===v[e]||(c("</"),c(e),c(">"));e==d&&(d=!1)},chars:function(e){d||c(I(e))}}};T=H.Node.prototype.contains||
function(a){return!!(this.compareDocumentPosition(a)&16)};var g=/[\uD800-\uDBFF][\uDC00-\uDFFF]/g,J=/([^#-~ |!])/g,v=m("area,br,col,hr,img,wbr"),w=m("colgroup,dd,dt,li,p,tbody,td,tfoot,th,thead,tr"),x=m("rp,rt"),G=r({},x,w);w=r({},w,m("address,article,aside,blockquote,caption,center,del,dir,div,dl,figure,figcaption,footer,h1,h2,h3,h4,h5,h6,header,hgroup,hr,ins,map,menu,nav,ol,pre,section,table,ul"));x=r({},x,m("a,abbr,acronym,b,bdi,bdo,big,br,cite,code,del,dfn,em,font,i,img,ins,kbd,label,map,mark,q,ruby,rp,rt,s,samp,small,span,strike,strong,sub,sup,time,tt,u,var"));
var u=m("circle,defs,desc,ellipse,font-face,font-face-name,font-face-src,g,glyph,hkern,image,linearGradient,line,marker,metadata,missing-glyph,mpath,path,polygon,polyline,radialGradient,rect,stop,svg,switch,text,title,tspan"),t=m("script,style"),n=r({},v,w,x,G),B=m("background,cite,href,longdesc,src,xlink:href,xml:base");G=m("abbr,align,alt,axis,bgcolor,border,cellpadding,cellspacing,class,clear,color,cols,colspan,compact,coords,dir,face,headers,height,hreflang,hspace,ismap,lang,language,nohref,nowrap,rel,rev,rows,rowspan,rules,scope,scrolling,shape,size,span,start,summary,tabindex,target,title,type,valign,value,vspace,width");
x=m("accent-height,accumulate,additive,alphabetic,arabic-form,ascent,baseProfile,bbox,begin,by,calcMode,cap-height,class,color,color-rendering,content,cx,cy,d,dx,dy,descent,display,dur,end,fill,fill-rule,font-family,font-size,font-stretch,font-style,font-variant,font-weight,from,fx,fy,g1,g2,glyph-name,gradientUnits,hanging,height,horiz-adv-x,horiz-origin-x,ideographic,k,keyPoints,keySplines,keyTimes,lang,marker-end,marker-mid,marker-start,markerHeight,markerUnits,markerWidth,mathematical,max,min,offset,opacity,orient,origin,overline-position,overline-thickness,panose-1,path,pathLength,points,preserveAspectRatio,r,refX,refY,repeatCount,repeatDur,requiredExtensions,requiredFeatures,restart,rotate,rx,ry,slope,stemh,stemv,stop-color,stop-opacity,strikethrough-position,strikethrough-thickness,stroke,stroke-dasharray,stroke-dashoffset,stroke-linecap,stroke-linejoin,stroke-miterlimit,stroke-opacity,stroke-width,systemLanguage,target,text-anchor,to,transform,type,u1,u2,underline-position,underline-thickness,unicode,unicode-range,units-per-em,values,version,viewBox,visibility,width,widths,x,x-height,x1,x2,xlink:actuate,xlink:arcrole,xlink:role,xlink:show,xlink:title,xlink:type,xml:base,xml:lang,xml:space,xmlns,xmlns:xlink,y,y1,y2,zoomAndPan",
!0);var p=r({},B,x,G),y=function(a,b){function d(f){f="<remove></remove>"+f;try{var l=(new a.DOMParser).parseFromString(f,"text/html").body;l.firstChild.remove();return l}catch(q){}}function c(f){k.innerHTML=f;b.documentMode&&K(k);return k}if(b&&b.implementation)var e=b.implementation.createHTMLDocument("inert");else throw L("noinert");var k=(e.documentElement||e.getDocumentElement()).querySelector("body");k.innerHTML='<svg><g onload="this.parentNode.remove()"></g></svg>';return k.querySelector("svg")?
(k.innerHTML='<svg><p><style><img src="</style><img src=x onerror=alert(1)//">',k.querySelector("svg img")?d:c):function(f){f="<remove></remove>"+f;try{f=encodeURI(f)}catch(q){return}var l=new a.XMLHttpRequest;l.responseType="document";l.open("GET","data:text/html;charset=utf-8,"+f,!1);l.send(null);f=l.response.body;f.firstChild.remove();return f}}(H,H.document)}).info({angularVersion:"1.6.4-local+sha.617b36117"});h.module("ngSanitize").filter("linky",["$sanitize",function(m){var D=/((s?ftp|https?):\/\/|(www\.)|(mailto:)?[A-Za-z0-9._%+-]+@)\S*[^\s.;,(){}<>"\u201d\u2019]/i,
z=/^mailto:/i,I=h.$$minErr("linky"),K=h.isDefined,A=h.isFunction,E=h.isObject,F=h.isString;return function(g,J,v){function w(p){if(p){var y=t,a=y.push,b=[];M(b,S).chars(p);p=b.join("");a.call(y,p)}}function x(p,y){var a,b=G(p);t.push("<a ");for(a in b)t.push(a+'="'+b[a]+'" ');!K(J)||"target"in b||t.push('target="',J,'" ');t.push('href="',p.replace(/"/g,"&quot;"),'">');w(y);t.push("</a>")}if(null==g||""===g)return g;if(!F(g))throw I("notstring",g);for(var G=A(v)?v:E(v)?function(){return v}:function(){return{}},
u=g,t=[],n,B;g=u.match(D);)n=g[0],g[2]||g[4]||(n=(g[3]?"http://":"mailto:")+n),B=g.index,w(u.substr(0,B)),x(n,g[0].replace(z,"")),u=u.substring(B+g[0].length);w(u);return m(t.join(""))}}])})(window,window.angular);

//third_party/javascript/angular/v1_6/angular-animate.min.js
/*
 AngularJS v1.6.4-local+sha.617b36117
 (c) 2010-2018 Google, Inc. http://angularjs.org
 License: MIT
*/
'use strict';(function(Ba,ha){'use strict';function Va(a,b,d){if(!a)throw jb("areq",b||"?",d||"required");return a}function Wa(a,b){if(!a&&!b)return"";if(!a)return b;if(!b)return a;sa(a)&&(a=a.join(" "));sa(b)&&(b=b.join(" "));return a+" "+b}function kb(a){var b={};a&&(a.to||a.from)&&(b.to=a.to,b.from=a.from);return b}function ta(a,b,d){var k="";a=sa(a)?a:a&&pa(a)&&a.length?a.split(/\s+/):[];L(a,function(r,x){r&&0<r.length&&(k+=0<x?" ":"",k+=d?b+r:r+b)});return k}function Xa(a){if(a instanceof ja)switch(a.length){case 0:return a;
case 1:if(1===a[0].nodeType)return a;break;default:return ja(Na(a))}if(1===a.nodeType)return ja(a)}function Na(a){if(!a[0])return a;for(var b=0;b<a.length;b++){var d=a[b];if(1===d.nodeType)return d}}function lb(a,b,d){L(b,function(k){a.addClass(k,d)})}function mb(a,b,d){L(b,function(k){a.removeClass(k,d)})}function Ga(a){return function(b,d){d.addClass&&(lb(a,b,d.addClass),d.addClass=null);d.removeClass&&(mb(a,b,d.removeClass),d.removeClass=null)}}function Ha(a){a=a||{};if(!a.$$prepared){var b=a.domOperation||
ka;a.domOperation=function(){a.$$domOperationFired=!0;b();b=ka};a.$$prepared=!0}return a}function ya(a,b){Ya(a,b);Za(a,b)}function Ya(a,b){b.from&&(a.css(b.from),b.from=null)}function Za(a,b){b.to&&(a.css(b.to),b.to=null)}function Ca(a,b,d){var k=b.options||{};d=d.options||{};var r=(k.addClass||"")+" "+(d.addClass||""),x=(k.removeClass||"")+" "+(d.removeClass||"");a=nb(a.attr("class"),r,x);d.preparationClasses&&(k.preparationClasses=Ia(d.preparationClasses,k.preparationClasses),delete d.preparationClasses);
r=k.domOperation!==ka?k.domOperation:null;Oa(k,d);r&&(k.domOperation=r);k.addClass=a.addClass?a.addClass:null;k.removeClass=a.removeClass?a.removeClass:null;b.addClass=k.addClass;b.removeClass=k.removeClass;return k}function nb(a,b,d){function k(e){pa(e)&&(e=e.split(" "));var g={};L(e,function(y){y.length&&(g[y]=!0)});return g}var r={};a=k(a);b=k(b);L(b,function(e,g){r[g]=1});d=k(d);L(d,function(e,g){r[g]=1===r[g]?null:-1});var x={addClass:"",removeClass:""};L(r,function(e,g){if(1===e){var y="addClass";
var C=!a[g]||a[g+"-remove"]}else-1===e&&(y="removeClass",C=a[g]||a[g+"-add"]);C&&(x[y].length&&(x[y]+=" "),x[y]+=g)});return x}function ma(a){return a instanceof ja?a[0]:a}function ob(a,b,d){var k="";b&&(k=ta(b,"ng-",!0));d.addClass&&(k=Ia(k,ta(d.addClass,"-add")));d.removeClass&&(k=Ia(k,ta(d.removeClass,"-remove")));k.length&&(d.preparationClasses=k,a.addClass(k))}function Ja(a,b){b=b?"-"+b+"s":"";Da(a,[Ea,b]);return[Ea,b]}function Pa(a,b){b=b?"paused":"";var d=va+"PlayState";Da(a,[d,b]);return[d,
b]}function Da(a,b){a.style[b[0]]=b[1]}function Ia(a,b){return a?b?a+" "+b:a:b}function $a(a,b,d){var k=Object.create(null),r=a.getComputedStyle(b)||{};L(d,function(x,e){if(x=r[x]){var g=x.charAt(0);if("-"===g||"+"===g||0<=g)x=pb(x);0===x&&(x=null);k[e]=x}});return k}function pb(a){var b=0;a=a.split(/\s*,\s*/);L(a,function(d){"s"===d.charAt(d.length-1)&&(d=d.substring(0,d.length-1));d=parseFloat(d)||0;b=b?Math.max(d,b):d});return b}function Qa(a){return 0===a||null!=a}function ab(a,b){var d=qa;a+=
"s";b?d+="Duration":a+=" linear all";return[d,a]}function bb(){var a=Object.create(null);return{flush:function(){a=Object.create(null)},count:function(b){return(b=a[b])?b.total:0},get:function(b){return(b=a[b])&&b.value},put:function(b,d){a[b]?a[b].total++:a[b]={total:1,value:d}}}}function cb(a,b,d){L(d,function(k){a[k]=Ra(a[k])?a[k]:b.style.getPropertyValue(k)})}if(void 0===Ba.ontransitionend&&void 0!==Ba.onwebkittransitionend){var qa="WebkitTransition";var db="webkitTransitionEnd transitionend"}else qa=
"transition",db="transitionend";if(void 0===Ba.onanimationend&&void 0!==Ba.onwebkitanimationend){var va="WebkitAnimation";var eb="webkitAnimationEnd animationend"}else va="animation",eb="animationend";var Ka=va+"Delay",Sa=va+"Duration",Ea=qa+"Delay",fb=qa+"Duration",jb=ha.$$minErr("ng");"use strict";"use strict";"use strict";var qb={transitionDuration:fb,transitionDelay:Ea,transitionProperty:qa+"Property",animationDuration:Sa,animationDelay:Ka,animationIterationCount:va+"IterationCount"},rb={transitionDuration:fb,
transitionDelay:Ea,animationDuration:Sa,animationDelay:Ka};"use strict";"use strict";"use strict";"use strict";"use strict";"use strict";"use strict";var Ta,Oa,L,sa,Ra,La,Ua,Ma,pa,za,ja,ka;ha.module("ngAnimate",[],function(){ka=ha.noop;Ta=ha.copy;Oa=ha.extend;ja=ha.element;L=ha.forEach;sa=ha.isArray;pa=ha.isString;Ma=ha.isObject;za=ha.isUndefined;Ra=ha.isDefined;Ua=ha.isFunction;La=ha.isElement}).info({angularVersion:"1.6.4-local+sha.617b36117"}).directive("ngAnimateSwap",["$animate","$rootScope",
function(a,b){return{restrict:"A",transclude:"element",terminal:!0,priority:600,link:function(d,k,r,x,e){var g,y;d.$watchCollection(r.ngAnimateSwap||r["for"],function(C){g&&a.leave(g);y&&(y.$destroy(),y=null);if(C||0===C)y=d.$new(),e(y,function(T){g=T;a.enter(T,null,k)})})}}}]).directive("ngAnimateChildren",["$interpolate",function(a){return{link:function(b,d,k){function r(e){d.data("$$ngAnimateChildren","on"===e||"true"===e)}var x=k.ngAnimateChildren;pa(x)&&0===x.length?d.data("$$ngAnimateChildren",
!0):(r(a(x)(b)),k.$observe("ngAnimateChildren",r))}}}]).factory("$$rAFScheduler",["$$rAF",function(a){function b(x){r=r.concat(x);d()}function d(){if(r.length){for(var x=r.shift(),e=0;e<x.length;e++)x[e]();k||a(function(){k||d()})}}var k;var r=b.queue=[];b.waitUntilQuiet=function(x){k&&k();k=a(function(){k=null;x();d()})};return b}]).provider("$$animateQueue",["$animateProvider",function(a){function b(e){if(!e)return null;e=e.split(" ");var g=Object.create(null);L(e,function(y){g[y]=!0});return g}
function d(e,g){if(e&&g){var y=b(g);return e.split(" ").some(function(C){return y[C]})}}function k(e,g,y){return x[e].some(function(C){return C(g,y)})}function r(e,g){var y=0<(e.addClass||"").length;e=0<(e.removeClass||"").length;return g?y&&e:y||e}var x=this.rules={skip:[],cancel:[],join:[]};x.join.push(function(e,g){return!e.structural&&r(e)});x.skip.push(function(e,g){return!e.structural&&!r(e)});x.skip.push(function(e,g){return"leave"===g.event&&e.structural});x.skip.push(function(e,g){return g.structural&&
2===g.state&&!e.structural});x.cancel.push(function(e,g){return g.structural&&e.structural});x.cancel.push(function(e,g){return 2===g.state&&e.structural});x.cancel.push(function(e,g){if(g.structural)return!1;var y=e.addClass;e=e.removeClass;var C=g.addClass;g=g.removeClass;return za(y)&&za(e)||za(C)&&za(g)?!1:d(y,g)||d(e,C)});this.$get=["$$rAF","$rootScope","$rootElement","$document","$$Map","$$animation","$$AnimateRunner","$templateRequest","$$jqLite","$$forceReflow","$$isDocumentHidden",function(e,
g,y,C,T,I,Y,V,z,P,M){function N(){var h=!1;return function(l){h?l():g.$$postDigest(function(){h=!0;l()})}}function n(h,l,q){var G=[],W=f[q];W&&L(W,function(A){X.call(A.node,l)?G.push(A.callback):"leave"===q&&X.call(A.node,h)&&G.push(A.callback)});return G}function t(h,l,q){var G=Na(l);return h.filter(function(W){return!(W.node===G&&(!q||W.callback===q))})}function u(h,l,q){function G(p,ca,ba,ra){wa(function(){var ea=n(na,O,ca);ea.length?e(function(){L(ea,function(la){la(Q,ba,ra)});"close"!==ba||O.parentNode||
aa.off(O)}):"close"!==ba||O.parentNode||aa.off(O)});p.progress(ca,ba,ra)}function W(p){var ca=Q,ba=A;ba.preparationClasses&&(ca.removeClass(ba.preparationClasses),ba.preparationClasses=null);ba.activeClasses&&(ca.removeClass(ba.activeClasses),ba.activeClasses=null);R(Q,A);ya(Q,A);A.domOperation();U.complete(!p)}var A=Ta(q),Q=Xa(h),O=ma(Q),na=O&&O.parentNode;A=Ha(A);var U=new Y,wa=N();sa(A.addClass)&&(A.addClass=A.addClass.join(" "));A.addClass&&!pa(A.addClass)&&(A.addClass=null);sa(A.removeClass)&&
(A.removeClass=A.removeClass.join(" "));A.removeClass&&!pa(A.removeClass)&&(A.removeClass=null);A.from&&!Ma(A.from)&&(A.from=null);A.to&&!Ma(A.to)&&(A.to=null);if(!(c&&O&&J(O,l,q)&&B(O,A)))return W(),U;var ua=0<=["enter","move","leave"].indexOf(l),F=M(),ia=F||m.get(O);q=!ia&&D.get(O)||{};var oa=!!q.state;ia||oa&&1===q.state||(ia=!H(O,na,l));if(ia)return F&&G(U,l,"start"),W(),F&&G(U,l,"close"),U;ua&&S(O);F={structural:ua,element:Q,event:l,addClass:A.addClass,removeClass:A.removeClass,close:W,options:A,
runner:U};if(oa){if(k("skip",F,q)){if(2===q.state)return W(),U;Ca(Q,q,F);return q.runner}if(k("cancel",F,q))if(2===q.state)q.runner.end();else if(q.structural)q.close();else return Ca(Q,q,F),q.runner;else if(k("join",F,q))if(2===q.state)Ca(Q,F,{});else return ob(Q,ua?l:null,A),l=F.event=q.event,A=Ca(Q,q,F),q.runner}else Ca(Q,F,{});(oa=F.structural)||(oa="animate"===F.event&&0<Object.keys(F.options.to||{}).length||r(F));if(!oa)return W(),v(O),U;var da=(q.counter||0)+1;F.counter=da;w(O,1,F);g.$$postDigest(function(){Q=
Xa(h);var p=D.get(O),ca=!p;p=p||{};var ba=0<(Q.parent()||[]).length&&("animate"===p.event||p.structural||r(p));if(ca||p.counter!==da||!ba){ca&&(R(Q,A),ya(Q,A));if(ca||ua&&p.event!==l)A.domOperation(),U.end();ba||v(O)}else l=!p.structural&&r(p,!0)?"setClass":p.event,w(O,2),p=I(Q,l,p.options),U.setHost(p),G(U,l,"start",{}),p.done(function(ra){W(!ra);(ra=D.get(O))&&ra.counter===da&&v(O);G(U,l,"close",{})})});return U}function S(h){h=h.querySelectorAll("[data-ng-animate]");L(h,function(l){var q=parseInt(l.getAttribute("data-ng-animate"),
10),G=D.get(l);if(G)switch(q){case 2:G.runner.end();case 1:D.delete(l)}})}function v(h){h.removeAttribute("data-ng-animate");D.delete(h)}function H(h,l,q){q=C[0].body;var G=ma(y),W=h===q||"HTML"===h.nodeName,A=h===G,Q=!1,O=m.get(h),na;for((h=ja.data(h,"$ngAnimatePin"))&&(l=ma(h));l;){A||(A=l===G);if(1!==l.nodeType)break;h=D.get(l)||{};if(!Q){var U=m.get(l);if(!0===U&&!1!==O){O=!0;break}else!1===U&&(O=!1);Q=h.structural}if(za(na)||!0===na)h=ja.data(l,"$$ngAnimateChildren"),Ra(h)&&(na=h);if(Q&&!1===
na)break;W||(W=l===q);if(W&&A)break;if(!A&&(h=ja.data(l,"$ngAnimatePin"))){l=ma(h);continue}l=l.parentNode}return(!Q||na)&&!0!==O&&A&&W}function w(h,l,q){q=q||{};q.state=l;h.setAttribute("data-ng-animate",l);q=(l=D.get(h))?Oa(l,q):q;D.set(h,q)}var D=new T,m=new T,c=null,E=g.$watch(function(){return 0===V.totalPendingRequests},function(h){h&&(E(),g.$$postDigest(function(){g.$$postDigest(function(){null===c&&(c=!0)})}))}),f=Object.create(null);T=a.customFilter();var K=a.classNameFilter();P=function(){return!0};
var J=T||P,B=K?function(h,l){h=[h.getAttribute("class"),l.addClass,l.removeClass].join(" ");return K.test(h)}:P,R=Ga(z),X=Ba.Node.prototype.contains||function(h){return this===h||!!(this.compareDocumentPosition(h)&16)},aa={on:function(h,l,q){var G=Na(l);f[h]=f[h]||[];f[h].push({node:G,callback:q});ja(l).on("$destroy",function(){D.get(G)||aa.off(h,l,q)})},off:function(h,l,q){if(1!==arguments.length||pa(arguments[0])){var G=f[h];G&&(f[h]=1===arguments.length?null:t(G,l,q))}else for(G in l=arguments[0],
f)f[G]=t(f[G],l)},pin:function(h,l){Va(La(h),"element","not an element");Va(La(l),"parentElement","not an element");h.data("$ngAnimatePin",l)},push:function(h,l,q,G){q=q||{};q.domOperation=G;return u(h,l,q)},enabled:function(h,l){var q=arguments.length;if(0===q)l=!!c;else if(La(h)){var G=ma(h);1===q?l=!m.get(G):m.set(G,!l)}else l=c=!!h;return l}};return aa}]}]).provider("$$animation",["$animateProvider",function(a){var b=this.drivers=[];this.$get=["$$jqLite","$rootScope","$injector","$$AnimateRunner",
"$$Map","$$rAFScheduler",function(d,k,r,x,e,g){function y(I){function Y(N){if(N.processed)return N;N.processed=!0;var n=N.domNode,t=n.parentNode;P.set(n,N);for(var u;t;){if(u=P.get(t)){u.processed||(u=Y(u));break}t=t.parentNode}(u||V).children.push(N);return N}var V={children:[]},z,P=new e;for(z=0;z<I.length;z++){var M=I[z];P.set(M.domNode,I[z]={domNode:M.domNode,fn:M.fn,children:[]})}for(z=0;z<I.length;z++)Y(I[z]);return function(N){var n=[],t=[],u;for(u=0;u<N.children.length;u++)t.push(N.children[u]);
N=t.length;var S=0,v=[];for(u=0;u<t.length;u++){var H=t[u];0>=N&&(N=S,S=0,n.push(v),v=[]);v.push(H.fn);H.children.forEach(function(w){S++;t.push(w)});N--}v.length&&n.push(v);return n}(V)}var C=[],T=Ga(d);return function(I,Y,V){function z(m){m=m.hasAttribute("ng-animate-ref")?[m]:m.querySelectorAll("[ng-animate-ref]");var c=[];L(m,function(E){var f=E.getAttribute("ng-animate-ref");f&&f.length&&c.push(E)});return c}function P(m){var c=[],E={};L(m,function(J,B){var R=ma(J.element),X=0<=["enter","move"].indexOf(J.event);
R=J.structural?z(R):[];if(R.length){var aa=X?"to":"from";L(R,function(h){var l=h.getAttribute("ng-animate-ref");E[l]=E[l]||{};E[l][aa]={animationID:B,element:ja(h)}})}else c.push(J)});var f={},K={};L(E,function(J,B){B=J.from;J=J.to;if(B&&J){var R=m[B.animationID],X=m[J.animationID],aa=B.animationID.toString();if(!K[aa]){var h=K[aa]={structural:!0,beforeStart:function(){R.beforeStart();X.beforeStart()},close:function(){R.close();X.close()},classes:M(R.classes,X.classes),from:R,to:X,anchors:[]};h.classes.length?
c.push(h):(c.push(R),c.push(X))}K[aa].anchors.push({out:B.element,"in":J.element})}else B=B?B.animationID:J.animationID,J=B.toString(),f[J]||(f[J]=!0,c.push(m[B]))});return c}function M(m,c){m=m.split(" ");c=c.split(" ");for(var E=[],f=0;f<m.length;f++){var K=m[f];if("ng-"!==K.substring(0,3))for(var J=0;J<c.length;J++)if(K===c[J]){E.push(K);break}}return E.join(" ")}function N(m){for(var c=b.length-1;0<=c;c--){var E=r.get(b[c])(m);if(E)return E}}function n(m,c){function E(f){(f=f.data("$$animationRunner"))&&
f.setHost(c)}m.from&&m.to?(E(m.from.element),E(m.to.element)):E(m.element)}function t(){var m=I.data("$$animationRunner");!m||"leave"===Y&&V.$$domOperationFired||m.end()}function u(m){I.off("$destroy",t);I.removeData("$$animationRunner");T(I,V);ya(I,V);V.domOperation();w&&d.removeClass(I,w);I.removeClass("ng-animate");v.complete(!m)}V=Ha(V);var S=0<=["enter","move","leave"].indexOf(Y),v=new x({end:function(){u()},cancel:function(){u(!0)}});if(!b.length)return u(),v;I.data("$$animationRunner",v);var H=
Wa(I.attr("class"),Wa(V.addClass,V.removeClass)),w=V.tempClasses;w&&(H+=" "+w,V.tempClasses=null);if(S){var D="ng-"+Y+"-prepare";d.addClass(I,D)}C.push({element:I,classes:H,event:Y,structural:S,options:V,beforeStart:function(){I.addClass("ng-animate");w&&d.addClass(I,w);D&&(d.removeClass(I,D),D=null)},close:u});I.on("$destroy",t);if(1<C.length)return v;k.$$postDigest(function(){var m=[];L(C,function(f){f.element.data("$$animationRunner")?m.push(f):f.close()});C.length=0;var c=P(m),E=[];L(c,function(f){E.push({domNode:ma(f.from?
f.from.element:f.element),fn:function(){f.beforeStart();var K=f.close;if((f.anchors?f.from.element||f.to.element:f.element).data("$$animationRunner")){var J=N(f);if(J)var B=J.start}B?(B=B(),B.done(function(R){K(!R)}),n(f,B)):K()}})});g(y(E))});return v}}]}]).provider("$animateCss",["$animateProvider",function(a){var b=bb(),d=bb();this.$get=["$window","$$jqLite","$$AnimateRunner","$timeout","$$forceReflow","$sniffer","$$rAFScheduler","$$animateQueue",function(k,r,x,e,g,y,C,T){function I(n,t){var u=
n.parentNode;return(u.$$ngAnimateParentKey||(u.$$ngAnimateParentKey=++M))+"-"+n.getAttribute("class")+"-"+t}function Y(n,t,u,S){if(0<b.count(u)){var v=d.get(u);v||(t=ta(t,"-stagger"),r.addClass(n,t),v=$a(k,n,S),v.animationDuration=Math.max(v.animationDuration,0),v.transitionDuration=Math.max(v.transitionDuration,0),r.removeClass(n,t),d.put(u,v))}return v||{}}function V(n){N.push(n);C.waitUntilQuiet(function(){b.flush();d.flush();for(var t=g(),u=0;u<N.length;u++)N[u](t);N.length=0})}function z(n,t,
u){t=b.get(u);t||(t=$a(k,n,qb),"infinite"===t.animationIterationCount&&(t.animationIterationCount=1));b.put(u,t);n=t;u=n.animationDelay;t=n.transitionDelay;n.maxDelay=u&&t?Math.max(u,t):u||t;n.maxDuration=Math.max(n.animationDuration*n.animationIterationCount,n.transitionDuration);return n}var P=Ga(r),M=0,N=[];return function(n,t){function u(){v()}function S(){v(!0)}function v(ea){if(!(R||aa&&X)){R=!0;X=!1;c.$$skipPreparationClasses||r.removeClass(n,Q);r.removeClass(n,na);Pa(f,!1);Ja(f,!1);L(K,function(xa){f.style[xa[0]]=
""});P(n,c);ya(n,c);Object.keys(E).length&&L(E,function(xa,Fa){xa?f.style.setProperty(Fa,xa):f.style.removeProperty(Fa)});if(c.onDone)c.onDone();G&&G.length&&n.off(G.join(" "),D);var la=n.data("$$animateCss");la&&(e.cancel(la[0].timer),n.removeData("$$animateCss"));h&&h.complete(!ea)}}function H(ea){p.blockTransition&&Ja(f,ea);p.blockKeyframeAnimation&&Pa(f,!!ea)}function w(){h=new x({end:u,cancel:S});V(ka);v();return{$$willAnimate:!1,start:function(){return h},end:u}}function D(ea){ea.stopPropagation();
var la=ea.originalEvent||ea;la.target===f&&(ea=la.$manualTimeStamp||Date.now(),la=parseFloat(la.elapsedTime.toFixed(3)),Math.max(ea-q,0)>=ba&&la>=da&&(aa=!0,v()))}function m(){function ea(){if(!R){H(!1);L(K,function(gb){f.style[gb[0]]=gb[1]});P(n,c);r.addClass(n,na);if(p.recalculateTimingStyles){O=f.getAttribute("class")+" "+Q;wa=I(f,O);F=z(f,O,wa);ia=F.maxDelay;oa=Math.max(ia,0);da=F.maxDuration;if(0===da){v();return}p.hasTransitions=0<F.transitionDuration;p.hasAnimations=0<F.animationDuration}p.applyAnimationDelay&&
(ia="boolean"!==typeof c.delay&&Qa(c.delay)?parseFloat(c.delay):ia,oa=Math.max(ia,0),F.animationDelay=ia,ca=[Ka,ia+"s"],K.push(ca),f.style[ca[0]]=ca[1]);ba=1E3*oa;ra=1E3*da;if(c.easing){var Z=c.easing;if(p.hasTransitions){var fa=qa+"TimingFunction";K.push([fa,Z]);f.style[fa]=Z}p.hasAnimations&&(fa=va+"TimingFunction",K.push([fa,Z]),f.style[fa]=Z)}F.transitionDuration&&G.push(db);F.animationDuration&&G.push(eb);q=Date.now();var Aa=ba+1.5*ra;fa=q+Aa;Z=n.data("$$animateCss")||[];var hb=!0;if(Z.length){var ib=
Z[0];(hb=fa>ib.expectedEndTime)?e.cancel(ib.timer):Z.push(v)}hb&&(Aa=e(la,Aa,!1),Z[0]={timer:Aa,expectedEndTime:fa},Z.push(v),n.data("$$animateCss",Z));if(G.length)n.on(G.join(" "),D);c.to&&(c.cleanupStyles&&cb(E,f,Object.keys(c.to)),Za(n,c))}}function la(){var Z=n.data("$$animateCss");if(Z){for(var fa=1;fa<Z.length;fa++)Z[fa]();n.removeData("$$animateCss")}}if(!R)if(f.parentNode){var xa=function(Z){if(aa)X&&Z&&(X=!1,v());else if(X=!Z,F.animationDuration)if(Z=Pa(f,X),X)K.push(Z);else{var fa=K,Aa=
fa.indexOf(Z);0<=Z&&fa.splice(Aa,1)}},Fa=0<ua&&(F.transitionDuration&&0===U.transitionDuration||F.animationDuration&&0===U.animationDuration)&&Math.max(U.animationDelay,U.transitionDelay);Fa?e(ea,Math.floor(Fa*ua*1E3),!1):ea();l.resume=function(){xa(!0)};l.pause=function(){xa(!1)}}else v()}var c=t||{};c.$$prepared||(c=Ha(Ta(c)));var E={},f=ma(n);if(!f||!f.parentNode||!T.enabled())return w();var K=[],J=n.attr("class"),B=kb(c),R,X,aa,h,l,q,G=[];if(0===c.duration||!y.animations&&!y.transitions)return w();
var W=c.event&&sa(c.event)?c.event.join(" "):c.event,A="";t="";W&&c.structural?A=ta(W,"ng-",!0):W&&(A=W);c.addClass&&(t+=ta(c.addClass,"-add"));c.removeClass&&(t.length&&(t+=" "),t+=ta(c.removeClass,"-remove"));c.applyClassesEarly&&t.length&&P(n,c);var Q=[A,t].join(" ").trim(),O=J+" "+Q,na=ta(Q,"-active");J=B.to&&0<Object.keys(B.to).length;if(!(0<(c.keyframeStyle||"").length||J||Q))return w();if(0<c.stagger){B=parseFloat(c.stagger);var U={transitionDelay:B,animationDelay:B,transitionDuration:0,animationDuration:0}}else{var wa=
I(f,O);U=Y(f,Q,wa,rb)}c.$$skipPreparationClasses||r.addClass(n,Q);c.transitionStyle&&(B=[qa,c.transitionStyle],Da(f,B),K.push(B));0<=c.duration&&(B=0<f.style[qa].length,B=ab(c.duration,B),Da(f,B),K.push(B));c.keyframeStyle&&(B=[va,c.keyframeStyle],Da(f,B),K.push(B));var ua=U?0<=c.staggerIndex?c.staggerIndex:b.count(wa):0;(W=0===ua)&&!c.skipBlocking&&Ja(f,9999);var F=z(f,O,wa),ia=F.maxDelay;var oa=Math.max(ia,0);var da=F.maxDuration;var p={};p.hasTransitions=0<F.transitionDuration;p.hasAnimations=
0<F.animationDuration;p.hasTransitionAll=p.hasTransitions&&"all"===F.transitionProperty;p.applyTransitionDuration=J&&(p.hasTransitions&&!p.hasTransitionAll||p.hasAnimations&&!p.hasTransitions);p.applyAnimationDuration=c.duration&&p.hasAnimations;p.applyTransitionDelay=Qa(c.delay)&&(p.applyTransitionDuration||p.hasTransitions);p.applyAnimationDelay=Qa(c.delay)&&p.hasAnimations;p.recalculateTimingStyles=0<t.length;if(p.applyTransitionDuration||p.applyAnimationDuration)da=c.duration?parseFloat(c.duration):
da,p.applyTransitionDuration&&(p.hasTransitions=!0,F.transitionDuration=da,B=0<f.style[qa+"Property"].length,K.push(ab(da,B))),p.applyAnimationDuration&&(p.hasAnimations=!0,F.animationDuration=da,K.push([Sa,da+"s"]));if(0===da&&!p.recalculateTimingStyles)return w();if(null!=c.delay){if("boolean"!==typeof c.delay){var ca=parseFloat(c.delay);oa=Math.max(ca,0)}p.applyTransitionDelay&&K.push([Ea,ca+"s"]);p.applyAnimationDelay&&K.push([Ka,ca+"s"])}null==c.duration&&0<F.transitionDuration&&(p.recalculateTimingStyles=
p.recalculateTimingStyles||W);var ba=1E3*oa;var ra=1E3*da;c.skipBlocking||(p.blockTransition=0<F.transitionDuration,p.blockKeyframeAnimation=0<F.animationDuration&&0<U.animationDelay&&0===U.animationDuration);c.from&&(c.cleanupStyles&&cb(E,f,Object.keys(c.from)),Ya(n,c));p.blockTransition||p.blockKeyframeAnimation?H(da):c.skipBlocking||Ja(f,!1);return{$$willAnimate:!0,end:u,start:function(){if(!R)return l={end:u,cancel:S,resume:null,pause:null},h=new x(l),V(m),h}}}}]}]).provider("$$animateCssDriver",
["$$animationProvider",function(a){a.drivers.push("$$animateCssDriver");this.$get=["$animateCss","$rootScope","$$AnimateRunner","$rootElement","$sniffer","$$jqLite","$document",function(b,d,k,r,x,e,g){function y(z,P){pa(z)&&(z=z.split(" "));pa(P)&&(P=P.split(" "));return z.filter(function(M){return-1===P.indexOf(M)}).join(" ")}function C(z,P,M){function N(w){var D={},m=ma(w).getBoundingClientRect();L(["width","height","top","left"],function(c){var E=m[c];switch(c){case "top":E+=Y.scrollTop;break;
case "left":E+=Y.scrollLeft}D[c]=Math.floor(E)+"px"});return D}function n(){var w=(M.attr("class")||"").replace(/\bng-\S+\b/g,""),D=y(w,S);w=y(S,w);D=b(u,{to:N(M),addClass:"ng-anchor-in "+D,removeClass:"ng-anchor-out "+w,delay:!0});return D.$$willAnimate?D:null}function t(){u.remove();P.removeClass("ng-animate-shim");M.removeClass("ng-animate-shim")}var u=ja(ma(P).cloneNode(!0)),S=(u.attr("class")||"").replace(/\bng-\S+\b/g,"");P.addClass("ng-animate-shim");M.addClass("ng-animate-shim");u.addClass("ng-anchor");
V.append(u);z=function(){var w=b(u,{addClass:"ng-anchor-out",delay:!0,from:N(P)});return w.$$willAnimate?w:null}();if(!z){var v=n();if(!v)return t()}var H=z||v;return{start:function(){function w(){m&&m.end()}var D,m=H.start();m.done(function(){m=null;if(!v&&(v=n()))return m=v.start(),m.done(function(){m=null;t();D.complete()}),m;t();D.complete()});return D=new k({end:w,cancel:w})}}}function T(z,P,M,N){var n=I(z,ka),t=I(P,ka),u=[];L(N,function(S){(S=C(M,S.out,S["in"]))&&u.push(S)});if(n||t||0!==u.length)return{start:function(){function S(){L(v,
function(w){w.end()})}var v=[];n&&v.push(n.start());t&&v.push(t.start());L(u,function(w){v.push(w.start())});var H=new k({end:S,cancel:S});k.all(v,function(w){H.complete(w)});return H}}}function I(z){var P=z.element,M=z.options||{};z.structural&&(M.event=z.event,M.structural=!0,M.applyClassesEarly=!0,"leave"===z.event&&(M.onDone=M.domOperation));M.preparationClasses&&(M.event=Ia(M.event,M.preparationClasses));z=b(P,M);return z.$$willAnimate?z:null}if(!x.animations&&!x.transitions)return ka;var Y=
g[0].body;d=ma(r);var V=ja(d.parentNode&&11===d.parentNode.nodeType||Y.contains(d)?d:Y);return function(z){return z.from&&z.to?T(z.from,z.to,z.classes,z.anchors):I(z)}}]}]).provider("$$animateJs",["$animateProvider",function(a){this.$get=["$injector","$$AnimateRunner","$$jqLite",function(b,d,k){function r(e){e=sa(e)?e:e.split(" ");for(var g=[],y={},C=0;C<e.length;C++){var T=e[C],I=a.$$registeredAnimations[T];I&&!y[T]&&(g.push(b.get(I)),y[T]=!0)}return g}var x=Ga(k);return function(e,g,y,C){function T(){C.domOperation();
x(e,C)}function I(H,w,D,m,c){switch(D){case "animate":w=[w,m.from,m.to,c];break;case "setClass":w=[w,P,M,c];break;case "addClass":w=[w,P,c];break;case "removeClass":w=[w,M,c];break;default:w=[w,c]}w.push(m);if(H=H.apply(H,w))if(Ua(H.start)&&(H=H.start()),H instanceof d)H.done(c);else if(Ua(H))return H;return ka}function Y(H,w,D,m,c){var E=[];L(m,function(f){var K=f[c];K&&E.push(function(){var J=!1,B=function(aa){J||(J=!0,(X||ka)(aa),R.complete(!aa))};var R=new d({end:function(){B()},cancel:function(){B(!0)}});
var X=I(K,H,w,D,function(aa){B(!1===aa)});return R})});return E}function V(H,w,D,m,c){var E=Y(H,w,D,m,c);if(0===E.length){if("beforeSetClass"===c){var f=Y(H,"removeClass",D,m,"beforeRemoveClass");var K=Y(H,"addClass",D,m,"beforeAddClass")}else"setClass"===c&&(f=Y(H,"removeClass",D,m,"removeClass"),K=Y(H,"addClass",D,m,"addClass"));f&&(E=E.concat(f));K&&(E=E.concat(K))}if(0!==E.length)return function(J){var B=[];E.length&&L(E,function(R){B.push(R())});B.length?d.all(B,J):J();return function(R){L(B,
function(X){R?X.cancel():X.end()})}}}var z=!1;3===arguments.length&&Ma(y)&&(C=y,y=null);C=Ha(C);y||(y=e.attr("class")||"",C.addClass&&(y+=" "+C.addClass),C.removeClass&&(y+=" "+C.removeClass));var P=C.addClass,M=C.removeClass,N=r(y),n;if(N.length){if("leave"===g){var t="leave";var u="afterLeave"}else t="before"+g.charAt(0).toUpperCase()+g.substr(1),u=g;"enter"!==g&&"move"!==g&&(n=V(e,g,C,N,t));var S=V(e,g,C,N,u)}if(n||S){var v;return{$$willAnimate:!0,end:function(){v?v.end():(z=!0,T(),ya(e,C),v=new d,
v.complete(!0));return v},start:function(){function H(m){z=!0;T();ya(e,C);v.complete(m)}if(v)return v;v=new d;var w,D=[];n&&D.push(function(m){w=n(m)});D.length?D.push(function(m){T();m(!0)}):T();S&&D.push(function(m){w=S(m)});v.setHost({end:function(){z||((w||ka)(void 0),H(void 0))},cancel:function(){z||((w||ka)(!0),H(!0))}});d.chain(D,H);return v}}}}}]}]).provider("$$animateJsDriver",["$$animationProvider",function(a){a.drivers.push("$$animateJsDriver");this.$get=["$$animateJs","$$AnimateRunner",
function(b,d){function k(r){return b(r.element,r.event,r.classes,r.options)}return function(r){if(r.from&&r.to){var x=k(r.from),e=k(r.to);return x||e?{start:function(){function g(){return function(){L(y,function(T){T.end()})}}var y=[];x&&y.push(x.start());e&&y.push(e.start());d.all(y,function(T){C.complete(T)});var C=new d({end:g(),cancel:g()});return C}}:void 0}return k(r)}}]}])})(window,window.angular);

//third_party/javascript/angular/v1_6/angular-aria.min.js
/*
 AngularJS v1.6.4-local+sha.617b36117
 (c) 2010-2018 Google, Inc. http://angularjs.org
 License: MIT
*/
'use strict';(function(A,r){'use strict';var m="BUTTON A INPUT TEXTAREA SELECT DETAILS SUMMARY".split(" "),q=function(b,d){if(-1!==d.indexOf(b[0].nodeName))return!0};r.module("ngAria",["ng"]).info({angularVersion:"1.6.4-local+sha.617b36117"}).provider("$aria",function(){function b(h,n,c,e){return function(f,l,a){var g=a.$normalize(n);!d[g]||q(l,c)||a[g]||f.$watch(a[h],function(k){k=e?!k:!!k;l.attr(n,k)})}}var d={ariaHidden:!0,ariaChecked:!0,ariaReadonly:!0,ariaDisabled:!0,ariaRequired:!0,ariaInvalid:!0,ariaValue:!0,
tabindex:!0,bindKeydown:!0,bindRoleForClick:!0};this.config=function(h){d=r.extend(d,h)};this.$get=function(){return{config:function(h){return d[h]},$$watchExpr:b}}}).directive("ngShow",["$aria",function(b){return b.$$watchExpr("ngShow","aria-hidden",[],!0)}]).directive("ngHide",["$aria",function(b){return b.$$watchExpr("ngHide","aria-hidden",[],!1)}]).directive("ngValue",["$aria",function(b){return b.$$watchExpr("ngValue","aria-checked",m,!1)}]).directive("ngChecked",["$aria",function(b){return b.$$watchExpr("ngChecked",
"aria-checked",m,!1)}]).directive("ngReadonly",["$aria",function(b){return b.$$watchExpr("ngReadonly","aria-readonly",m,!1)}]).directive("ngRequired",["$aria",function(b){return b.$$watchExpr("ngRequired","aria-required",m,!1)}]).directive("ngModel",["$aria",function(b){function d(c,e,f,l){return b.config(e)&&!f.attr(c)&&(l||!q(f,m))}function h(c,e){return!e.attr("role")&&e.attr("type")===c&&!q(e,m)}function n(c,e){e=c.type;c=c.role;return"checkbox"===(e||c)||"menuitemcheckbox"===c?"checkbox":"radio"===
(e||c)||"menuitemradio"===c?"radio":"range"===e||"progressbar"===c||"slider"===c?"range":""}return{restrict:"A",require:"ngModel",priority:200,compile:function(c,e){var f=n(e,c);return{post:function(l,a,g,k){function t(){return k.$modelValue}function v(p){a.attr("aria-checked",g.value==k.$viewValue)}function w(){a.attr("aria-checked",!k.$isEmpty(k.$viewValue))}var u=d("tabindex","tabindex",a,!1);switch(f){case "radio":case "checkbox":h(f,a)&&a.attr("role",f);d("aria-checked","ariaChecked",a,!1)&&
l.$watch(t,"radio"===f?v:w);u&&a.attr("tabindex",0);break;case "range":h(f,a)&&a.attr("role","slider");if(b.config("ariaValue")){var x=!a.attr("aria-valuemin")&&(g.hasOwnProperty("min")||g.hasOwnProperty("ngMin")),y=!a.attr("aria-valuemax")&&(g.hasOwnProperty("max")||g.hasOwnProperty("ngMax")),z=!a.attr("aria-valuenow");x&&g.$observe("min",function(p){a.attr("aria-valuemin",p)});y&&g.$observe("max",function(p){a.attr("aria-valuemax",p)});z&&l.$watch(t,function(p){a.attr("aria-valuenow",p)})}u&&a.attr("tabindex",
0)}!g.hasOwnProperty("ngRequired")&&k.$validators.required&&d("aria-required","ariaRequired",a,!1)&&g.$observe("required",function(){a.attr("aria-required",!!g.required)});d("aria-invalid","ariaInvalid",a,!0)&&l.$watch(function(){return k.$invalid},function(p){a.attr("aria-invalid",!!p)})}}}}}]).directive("ngDisabled",["$aria",function(b){return b.$$watchExpr("ngDisabled","aria-disabled",m,!1)}]).directive("ngMessages",function(){return{restrict:"A",require:"?ngMessages",link:function(b,d,h,n){d.attr("aria-live")||
d.attr("aria-live","assertive")}}}).directive("ngClick",["$aria","$parse",function(b,d){return{restrict:"A",compile:function(h,n){var c=d(n.ngClick);return function(e,f,l){if(!q(f,m)&&(b.config("bindRoleForClick")&&!f.attr("role")&&f.attr("role","button"),b.config("tabindex")&&!f.attr("tabindex")&&f.attr("tabindex",0),b.config("bindKeydown")&&!l.ngKeydown&&!l.ngKeypress&&!l.ngKeyup))f.on("keydown",function(a){function g(){c(e,{$event:a})}var k=a.which||a.keyCode;32!==k&&13!==k||e.$apply(g)})}}}}]).directive("ngDblclick",
["$aria",function(b){return function(d,h,n){!b.config("tabindex")||h.attr("tabindex")||q(h,m)||h.attr("tabindex",0)}}])})(window,window.angular);

//third_party/javascript/closure/debug/error.js
goog.loadModule(function(exports) {'use strict';/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Provides a base class for custom Error objects such that the
 * stack is correctly maintained.
 *
 * You should never need to throw DebugError(msg) directly, Error(msg) is
 * sufficient.
 */

goog.module('goog.debug.Error');
goog.module.declareLegacyNamespace();



/**
 * Base class for custom error objects.
 * @param {*=} msg The message associated with the error.
 * @param {{
 *    message: (?|undefined),
 *    name: (?|undefined),
 *    lineNumber: (?|undefined),
 *    fileName: (?|undefined),
 *    stack: (?|undefined),
 *    cause: (?|undefined),
 * }=} cause The original error object to chain with.
 * @constructor
 * @extends {Error}
 */
function DebugError(msg = undefined, cause = undefined) {
  // Attempt to ensure there is a stack trace.
  if (Error.captureStackTrace) {
    Error.captureStackTrace(this, DebugError);
  } else {
    const stack = new Error().stack;
    if (stack) {
      /** @override */
      this.stack = stack;
    }
  }

  if (msg) {
    /** @override */
    this.message = String(msg);
  }

  if (cause !== undefined) {
    /** @type {?} */
    this.cause = cause;
  }

  /**
   * Whether to report this error to the server. Setting this to false will
   * cause the error reporter to not report the error back to the server,
   * which can be useful if the client knows that the error has already been
   * logged on the server.
   * @type {boolean}
   */
  this.reportErrorToServer = true;
}
goog.inherits(DebugError, Error);


/** @override @type {string} */
DebugError.prototype.name = 'CustomError';


exports = DebugError;

;return exports;});

//third_party/javascript/closure/dom/nodetype.js
/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Definition of goog.dom.NodeType.
 */

goog.provide('goog.dom.NodeType');


/**
 * Constants for the nodeType attribute in the Node interface.
 *
 * These constants match those specified in the Node interface. These are
 * usually present on the Node object in recent browsers, but not in older
 * browsers (specifically, early IEs) and thus are given here.
 *
 * In some browsers (early IEs), these are not defined on the Node object,
 * so they are provided here.
 *
 * See http://www.w3.org/TR/DOM-Level-2-Core/core.html#ID-1950641247
 * @enum {number}
 */
goog.dom.NodeType = {
  ELEMENT: 1,
  ATTRIBUTE: 2,
  TEXT: 3,
  CDATA_SECTION: 4,
  ENTITY_REFERENCE: 5,
  ENTITY: 6,
  PROCESSING_INSTRUCTION: 7,
  COMMENT: 8,
  DOCUMENT: 9,
  DOCUMENT_TYPE: 10,
  DOCUMENT_FRAGMENT: 11,
  NOTATION: 12
};

//third_party/javascript/closure/asserts/asserts.js
/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Utilities to check the preconditions, postconditions and
 * invariants runtime.
 *
 * Methods in this package are given special treatment by the compiler
 * for type-inference. For example, <code>goog.asserts.assert(foo)</code>
 * will make the compiler treat <code>foo</code> as non-nullable. Similarly,
 * <code>goog.asserts.assertNumber(foo)</code> informs the compiler about the
 * type of <code>foo</code>. Where applicable, such assertions are preferable to
 * casts by jsdoc with <code>@type</code>.
 *
 * The compiler has an option to disable asserts. So code like:
 * <code>
 * var x = goog.asserts.assert(foo());
 * goog.asserts.assert(bar());
 * </code>
 * will be transformed into:
 * <code>
 * var x = foo();
 * </code>
 * The compiler will leave in foo() (because its return value is used),
 * but it will remove bar() because it assumes it does not have side-effects.
 *
 * Additionally, note the compiler will consider the type to be "tightened" for
 * all statements <em>after</em> the assertion. For example:
 * <code>
 * const /** ?Object &#ast;/ value = foo();
 * goog.asserts.assert(value);
 * // "value" is of type {!Object} at this point.
 * </code>
 */

goog.provide('goog.asserts');
goog.provide('goog.asserts.AssertionError');

goog.require('goog.debug.Error');
goog.require('goog.dom.NodeType');


/**
 * @define {boolean} Whether to strip out asserts or to leave them in.
 */
goog.asserts.ENABLE_ASSERTS =
    goog.define('goog.asserts.ENABLE_ASSERTS', goog.DEBUG);



/**
 * Error object for failed assertions.
 * @param {string} messagePattern The pattern that was used to form message.
 * @param {!Array<*>} messageArgs The items to substitute into the pattern.
 * @constructor
 * @extends {goog.debug.Error}
 * @final
 */
goog.asserts.AssertionError = function(messagePattern, messageArgs) {
  'use strict';
  goog.debug.Error.call(this, goog.asserts.subs_(messagePattern, messageArgs));

  /**
   * The message pattern used to format the error message. Error handlers can
   * use this to uniquely identify the assertion.
   * @type {string}
   */
  this.messagePattern = messagePattern;
};
goog.inherits(goog.asserts.AssertionError, goog.debug.Error);


/** @override @type {string} */
goog.asserts.AssertionError.prototype.name = 'AssertionError';


/**
 * The default error handler.
 * @param {!goog.asserts.AssertionError} e The exception to be handled.
 * @return {void}
 */
goog.asserts.DEFAULT_ERROR_HANDLER = function(e) {
  'use strict';
  throw e;
};


/**
 * The handler responsible for throwing or logging assertion errors.
 * @private {function(!goog.asserts.AssertionError)}
 */
goog.asserts.errorHandler_ = goog.asserts.DEFAULT_ERROR_HANDLER;


/**
 * Does simple python-style string substitution.
 * subs("foo%s hot%s", "bar", "dog") becomes "foobar hotdog".
 * @param {string} pattern The string containing the pattern.
 * @param {!Array<*>} subs The items to substitute into the pattern.
 * @return {string} A copy of `str` in which each occurrence of
 *     {@code %s} has been replaced an argument from `var_args`.
 * @private
 */
goog.asserts.subs_ = function(pattern, subs) {
  'use strict';
  var splitParts = pattern.split('%s');
  var returnString = '';

  // Replace up to the last split part. We are inserting in the
  // positions between split parts.
  var subLast = splitParts.length - 1;
  for (var i = 0; i < subLast; i++) {
    // keep unsupplied as '%s'
    var sub = (i < subs.length) ? subs[i] : '%s';
    returnString += splitParts[i] + sub;
  }
  return returnString + splitParts[subLast];
};


/**
 * Throws an exception with the given message and "Assertion failed" prefixed
 * onto it.
 * @param {string} defaultMessage The message to use if givenMessage is empty.
 * @param {Array<*>} defaultArgs The substitution arguments for defaultMessage.
 * @param {string|undefined} givenMessage Message supplied by the caller.
 * @param {Array<*>} givenArgs The substitution arguments for givenMessage.
 * @throws {goog.asserts.AssertionError} When the value is not a number.
 * @private
 */
goog.asserts.doAssertFailure_ = function(
    defaultMessage, defaultArgs, givenMessage, givenArgs) {
  'use strict';
  var message = 'Assertion failed';
  if (givenMessage) {
    message += ': ' + givenMessage;
    var args = givenArgs;
  } else if (defaultMessage) {
    message += ': ' + defaultMessage;
    args = defaultArgs;
  }
  // The '' + works around an Opera 10 bug in the unit tests. Without it,
  // a stack trace is added to var message above. With this, a stack trace is
  // not added until this line (it causes the extra garbage to be added after
  // the assertion message instead of in the middle of it).
  var e = new goog.asserts.AssertionError('' + message, args || []);
  goog.asserts.errorHandler_(e);
};


/**
 * Sets a custom error handler that can be used to customize the behavior of
 * assertion failures, for example by turning all assertion failures into log
 * messages.
 * @param {function(!goog.asserts.AssertionError)} errorHandler
 * @return {void}
 */
goog.asserts.setErrorHandler = function(errorHandler) {
  'use strict';
  if (goog.asserts.ENABLE_ASSERTS) {
    goog.asserts.errorHandler_ = errorHandler;
  }
};


/**
 * Checks if the condition evaluates to true if goog.asserts.ENABLE_ASSERTS is
 * true.
 * @template T
 * @param {T} condition The condition to check.
 * @param {string=} opt_message Error message in case of failure.
 * @param {...*} var_args The items to substitute into the failure message.
 * @return {T} The value of the condition.
 * @throws {goog.asserts.AssertionError} When the condition evaluates to false.
 * @closurePrimitive {asserts.truthy}
 */
goog.asserts.assert = function(condition, opt_message, var_args) {
  'use strict';
  if (goog.asserts.ENABLE_ASSERTS && !condition) {
    goog.asserts.doAssertFailure_(
        '', null, opt_message, Array.prototype.slice.call(arguments, 2));
  }
  return condition;
};


/**
 * Checks if `value` is `null` or `undefined` if goog.asserts.ENABLE_ASSERTS is
 * true.
 *
 * @param {T} value The value to check.
 * @param {string=} opt_message Error message in case of failure.
 * @param {...*} var_args The items to substitute into the failure message.
 * @return {R} `value` with its type narrowed to exclude `null` and `undefined`.
 *
 * @template T
 * @template R :=
 *     mapunion(T, (V) =>
 *         cond(eq(V, 'null'),
 *             none(),
 *             cond(eq(V, 'undefined'),
 *                 none(),
 *                 V)))
 *  =:
 *
 * @throws {!goog.asserts.AssertionError} When `value` is `null` or `undefined`.
 * @closurePrimitive {asserts.matchesReturn}
 */
goog.asserts.assertExists = function(value, opt_message, var_args) {
  'use strict';
  if (goog.asserts.ENABLE_ASSERTS && value == null) {
    goog.asserts.doAssertFailure_(
        'Expected to exist: %s.', [value], opt_message,
        Array.prototype.slice.call(arguments, 2));
  }
  return value;
};


/**
 * Fails if goog.asserts.ENABLE_ASSERTS is true. This function is useful in case
 * when we want to add a check in the unreachable area like switch-case
 * statement:
 *
 * <pre>
 *  switch(type) {
 *    case FOO: doSomething(); break;
 *    case BAR: doSomethingElse(); break;
 *    default: goog.asserts.fail('Unrecognized type: ' + type);
 *      // We have only 2 types - "default:" section is unreachable code.
 *  }
 * </pre>
 *
 * @param {string=} opt_message Error message in case of failure.
 * @param {...*} var_args The items to substitute into the failure message.
 * @return {void}
 * @throws {goog.asserts.AssertionError} Failure.
 * @closurePrimitive {asserts.fail}
 */
goog.asserts.fail = function(opt_message, var_args) {
  'use strict';
  if (goog.asserts.ENABLE_ASSERTS) {
    goog.asserts.errorHandler_(new goog.asserts.AssertionError(
        'Failure' + (opt_message ? ': ' + opt_message : ''),
        Array.prototype.slice.call(arguments, 1)));
  }
};


/**
 * Checks if the value is a number if goog.asserts.ENABLE_ASSERTS is true.
 * @param {*} value The value to check.
 * @param {string=} opt_message Error message in case of failure.
 * @param {...*} var_args The items to substitute into the failure message.
 * @return {number} The value, guaranteed to be a number when asserts enabled.
 * @throws {goog.asserts.AssertionError} When the value is not a number.
 * @closurePrimitive {asserts.matchesReturn}
 */
goog.asserts.assertNumber = function(value, opt_message, var_args) {
  'use strict';
  if (goog.asserts.ENABLE_ASSERTS && typeof value !== 'number') {
    goog.asserts.doAssertFailure_(
        'Expected number but got %s: %s.', [goog.typeOf(value), value],
        opt_message, Array.prototype.slice.call(arguments, 2));
  }
  return /** @type {number} */ (value);
};


/**
 * Checks if the value is a string if goog.asserts.ENABLE_ASSERTS is true.
 * @param {*} value The value to check.
 * @param {string=} opt_message Error message in case of failure.
 * @param {...*} var_args The items to substitute into the failure message.
 * @return {string} The value, guaranteed to be a string when asserts enabled.
 * @throws {goog.asserts.AssertionError} When the value is not a string.
 * @closurePrimitive {asserts.matchesReturn}
 */
goog.asserts.assertString = function(value, opt_message, var_args) {
  'use strict';
  if (goog.asserts.ENABLE_ASSERTS && typeof value !== 'string') {
    goog.asserts.doAssertFailure_(
        'Expected string but got %s: %s.', [goog.typeOf(value), value],
        opt_message, Array.prototype.slice.call(arguments, 2));
  }
  return /** @type {string} */ (value);
};


/**
 * Checks if the value is a function if goog.asserts.ENABLE_ASSERTS is true.
 * @param {*} value The value to check.
 * @param {string=} opt_message Error message in case of failure.
 * @param {...*} var_args The items to substitute into the failure message.
 * @return {!Function} The value, guaranteed to be a function when asserts
 *     enabled.
 * @throws {goog.asserts.AssertionError} When the value is not a function.
 * @closurePrimitive {asserts.matchesReturn}
 */
goog.asserts.assertFunction = function(value, opt_message, var_args) {
  'use strict';
  if (goog.asserts.ENABLE_ASSERTS && typeof value !== 'function') {
    goog.asserts.doAssertFailure_(
        'Expected function but got %s: %s.', [goog.typeOf(value), value],
        opt_message, Array.prototype.slice.call(arguments, 2));
  }
  return /** @type {!Function} */ (value);
};


/**
 * Checks if the value is an Object if goog.asserts.ENABLE_ASSERTS is true.
 * @param {*} value The value to check.
 * @param {string=} opt_message Error message in case of failure.
 * @param {...*} var_args The items to substitute into the failure message.
 * @return {!Object} The value, guaranteed to be a non-null object.
 * @throws {goog.asserts.AssertionError} When the value is not an object.
 * @closurePrimitive {asserts.matchesReturn}
 */
goog.asserts.assertObject = function(value, opt_message, var_args) {
  'use strict';
  if (goog.asserts.ENABLE_ASSERTS && !goog.isObject(value)) {
    goog.asserts.doAssertFailure_(
        'Expected object but got %s: %s.', [goog.typeOf(value), value],
        opt_message, Array.prototype.slice.call(arguments, 2));
  }
  return /** @type {!Object} */ (value);
};


/**
 * Checks if the value is an Array if goog.asserts.ENABLE_ASSERTS is true.
 * @param {*} value The value to check.
 * @param {string=} opt_message Error message in case of failure.
 * @param {...*} var_args The items to substitute into the failure message.
 * @return {!Array<?>} The value, guaranteed to be a non-null array.
 * @throws {goog.asserts.AssertionError} When the value is not an array.
 * @closurePrimitive {asserts.matchesReturn}
 */
goog.asserts.assertArray = function(value, opt_message, var_args) {
  'use strict';
  if (goog.asserts.ENABLE_ASSERTS && !Array.isArray(value)) {
    goog.asserts.doAssertFailure_(
        'Expected array but got %s: %s.', [goog.typeOf(value), value],
        opt_message, Array.prototype.slice.call(arguments, 2));
  }
  return /** @type {!Array<?>} */ (value);
};


/**
 * Checks if the value is a boolean if goog.asserts.ENABLE_ASSERTS is true.
 * @param {*} value The value to check.
 * @param {string=} opt_message Error message in case of failure.
 * @param {...*} var_args The items to substitute into the failure message.
 * @return {boolean} The value, guaranteed to be a boolean when asserts are
 *     enabled.
 * @throws {goog.asserts.AssertionError} When the value is not a boolean.
 * @closurePrimitive {asserts.matchesReturn}
 */
goog.asserts.assertBoolean = function(value, opt_message, var_args) {
  'use strict';
  if (goog.asserts.ENABLE_ASSERTS && typeof value !== 'boolean') {
    goog.asserts.doAssertFailure_(
        'Expected boolean but got %s: %s.', [goog.typeOf(value), value],
        opt_message, Array.prototype.slice.call(arguments, 2));
  }
  return /** @type {boolean} */ (value);
};


/**
 * Checks if the value is a DOM Element if goog.asserts.ENABLE_ASSERTS is true.
 * @param {*} value The value to check.
 * @param {string=} opt_message Error message in case of failure.
 * @param {...*} var_args The items to substitute into the failure message.
 * @return {!Element} The value, likely to be a DOM Element when asserts are
 *     enabled.
 * @throws {goog.asserts.AssertionError} When the value is not an Element.
 * @closurePrimitive {asserts.matchesReturn}
 * @deprecated Use goog.asserts.dom.assertIsElement instead.
 */
goog.asserts.assertElement = function(value, opt_message, var_args) {
  'use strict';
  if (goog.asserts.ENABLE_ASSERTS &&
      (!goog.isObject(value) ||
       /** @type {!Node} */ (value).nodeType != goog.dom.NodeType.ELEMENT)) {
    goog.asserts.doAssertFailure_(
        'Expected Element but got %s: %s.', [goog.typeOf(value), value],
        opt_message, Array.prototype.slice.call(arguments, 2));
  }
  return /** @type {!Element} */ (value);
};


/**
 * Checks if the value is an instance of the user-defined type if
 * goog.asserts.ENABLE_ASSERTS is true.
 *
 * The compiler may tighten the type returned by this function.
 *
 * Do not use this to ensure a value is an HTMLElement or a subclass! Cross-
 * document DOM inherits from separate - though identical - browser classes, and
 * such a check will unexpectedly fail. Please use the methods in
 * goog.asserts.dom for these purposes.
 *
 * @param {?} value The value to check.
 * @param {function(new: T, ...)} type A user-defined constructor.
 * @param {string=} opt_message Error message in case of failure.
 * @param {...*} var_args The items to substitute into the failure message.
 * @throws {goog.asserts.AssertionError} When the value is not an instance of
 *     type.
 * @return {T}
 * @template T
 * @closurePrimitive {asserts.matchesReturn}
 */
goog.asserts.assertInstanceof = function(value, type, opt_message, var_args) {
  'use strict';
  if (goog.asserts.ENABLE_ASSERTS && !(value instanceof type)) {
    goog.asserts.doAssertFailure_(
        'Expected instanceof %s but got %s.',
        [goog.asserts.getType_(type), goog.asserts.getType_(value)],
        opt_message, Array.prototype.slice.call(arguments, 3));
  }
  return value;
};


/**
 * Checks whether the value is a finite number, if goog.asserts.ENABLE_ASSERTS
 * is true.
 *
 * @param {*} value The value to check.
 * @param {string=} opt_message Error message in case of failure.
 * @param {...*} var_args The items to substitute into the failure message.
 * @throws {goog.asserts.AssertionError} When the value is not a number, or is
 *     a non-finite number such as NaN, Infinity or -Infinity.
 * @return {number} The value initially passed in.
 */
goog.asserts.assertFinite = function(value, opt_message, var_args) {
  'use strict';
  if (goog.asserts.ENABLE_ASSERTS &&
      (typeof value != 'number' || !isFinite(value))) {
    goog.asserts.doAssertFailure_(
        'Expected %s to be a finite number but it is not.', [value],
        opt_message, Array.prototype.slice.call(arguments, 2));
  }
  return /** @type {number} */ (value);
};

/**
 * Returns the type of a value. If a constructor is passed, and a suitable
 * string cannot be found, 'unknown type name' will be returned.
 * @param {*} value A constructor, object, or primitive.
 * @return {string} The best display name for the value, or 'unknown type name'.
 * @private
 */
goog.asserts.getType_ = function(value) {
  'use strict';
  if (value instanceof Function) {
    return value.displayName || value.name || 'unknown type name';
  } else if (value instanceof Object) {
    return /** @type {string} */ (value.constructor.displayName) ||
        value.constructor.name || Object.prototype.toString.call(value);
  } else {
    return value === null ? 'null' : typeof value;
  }
};

//third_party/javascript/closure/array/array.js
goog.loadModule(function(exports) {'use strict';/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Utilities for manipulating arrays.
 */


goog.module('goog.array');
goog.module.declareLegacyNamespace();

const asserts = goog.require('goog.asserts');


/**
 * @define {boolean} NATIVE_ARRAY_PROTOTYPES indicates whether the code should
 * rely on Array.prototype functions, if available.
 *
 * The Array.prototype functions can be defined by external libraries like
 * Prototype and setting this flag to false forces closure to use its own
 * goog.array implementation.
 *
 * If your javascript can be loaded by a third party site and you are wary about
 * relying on the prototype functions, specify
 * "--define goog.NATIVE_ARRAY_PROTOTYPES=false" to the JSCompiler.
 *
 * Setting goog.TRUSTED_SITE to false will automatically set
 * NATIVE_ARRAY_PROTOTYPES to false.
 */
goog.NATIVE_ARRAY_PROTOTYPES =
    goog.define('goog.NATIVE_ARRAY_PROTOTYPES', goog.TRUSTED_SITE);


/**
 * @define {boolean} If true, JSCompiler will use the native implementation of
 * array functions where appropriate (e.g., `Array#filter`) and remove the
 * unused pure JS implementation.
 */
const ASSUME_NATIVE_FUNCTIONS = goog.define(
    'goog.array.ASSUME_NATIVE_FUNCTIONS', goog.FEATURESET_YEAR > 2012);
exports.ASSUME_NATIVE_FUNCTIONS = ASSUME_NATIVE_FUNCTIONS;


/**
 * Returns the last element in an array without removing it.
 * Same as {@link goog.array.last}.
 * @param {IArrayLike<T>|string} array The array.
 * @return {T} Last item in array.
 * @template T
 */
function peek(array) {
  return array[array.length - 1];
}
exports.peek = peek;


/**
 * Returns the last element in an array without removing it.
 * Same as {@link goog.array.peek}.
 * @param {IArrayLike<T>|string} array The array.
 * @return {T} Last item in array.
 * @template T
 */
exports.last = peek;

// NOTE(arv): Since most of the array functions are generic it allows you to
// pass an array-like object. Strings have a length and are considered array-
// like. However, the 'in' operator does not work on strings so we cannot just
// use the array path even if the browser supports indexing into strings. We
// therefore end up splitting the string.


/**
 * Returns the index of the first element of an array with a specified value, or
 * -1 if the element is not present in the array.
 *
 * See {@link http://tinyurl.com/developer-mozilla-org-array-indexof}
 *
 * @param {IArrayLike<T>|string} arr The array to be searched.
 * @param {T} obj The object for which we are searching.
 * @param {number=} opt_fromIndex The index at which to start the search. If
 *     omitted the search starts at index 0.
 * @return {number} The index of the first matching array element.
 * @template T
 */
const indexOf = goog.NATIVE_ARRAY_PROTOTYPES &&
        (ASSUME_NATIVE_FUNCTIONS || Array.prototype.indexOf) ?
    function(arr, obj, opt_fromIndex) {
      asserts.assert(arr.length != null);

      return Array.prototype.indexOf.call(arr, obj, opt_fromIndex);
    } :
    function(arr, obj, opt_fromIndex) {
      const fromIndex = opt_fromIndex == null ?
          0 :
          (opt_fromIndex < 0 ? Math.max(0, arr.length + opt_fromIndex) :
                               opt_fromIndex);

      if (typeof arr === 'string') {
        // Array.prototype.indexOf uses === so only strings should be found.
        if (typeof obj !== 'string' || obj.length != 1) {
          return -1;
        }
        return arr.indexOf(obj, fromIndex);
      }

      for (let i = fromIndex; i < arr.length; i++) {
        if (i in arr && arr[i] === obj) return i;
      }
      return -1;
    };
exports.indexOf = indexOf;


/**
 * Returns the index of the last element of an array with a specified value, or
 * -1 if the element is not present in the array.
 *
 * See {@link http://tinyurl.com/developer-mozilla-org-array-lastindexof}
 *
 * @param {!IArrayLike<T>|string} arr The array to be searched.
 * @param {T} obj The object for which we are searching.
 * @param {?number=} opt_fromIndex The index at which to start the search. If
 *     omitted the search starts at the end of the array.
 * @return {number} The index of the last matching array element.
 * @template T
 */
const lastIndexOf = goog.NATIVE_ARRAY_PROTOTYPES &&
        (ASSUME_NATIVE_FUNCTIONS || Array.prototype.lastIndexOf) ?
    function(arr, obj, opt_fromIndex) {
      asserts.assert(arr.length != null);

      // Firefox treats undefined and null as 0 in the fromIndex argument which
      // leads it to always return -1
      const fromIndex = opt_fromIndex == null ? arr.length - 1 : opt_fromIndex;
      return Array.prototype.lastIndexOf.call(arr, obj, fromIndex);
    } :
    function(arr, obj, opt_fromIndex) {
      let fromIndex = opt_fromIndex == null ? arr.length - 1 : opt_fromIndex;

      if (fromIndex < 0) {
        fromIndex = Math.max(0, arr.length + fromIndex);
      }

      if (typeof arr === 'string') {
        // Array.prototype.lastIndexOf uses === so only strings should be found.
        if (typeof obj !== 'string' || obj.length != 1) {
          return -1;
        }
        return arr.lastIndexOf(obj, fromIndex);
      }

      for (let i = fromIndex; i >= 0; i--) {
        if (i in arr && arr[i] === obj) return i;
      }
      return -1;
    };
exports.lastIndexOf = lastIndexOf;


/**
 * Calls a function for each element in an array. Skips holes in the array.
 * See {@link http://tinyurl.com/developer-mozilla-org-array-foreach}
 *
 * @param {IArrayLike<T>|string} arr Array or array like object over
 *     which to iterate.
 * @param {?function(this: S, T, number, ?): ?} f The function to call for every
 *     element. This function takes 3 arguments (the element, the index and the
 *     array). The return value is ignored.
 * @param {S=} opt_obj The object to be used as the value of 'this' within f.
 * @template T,S
 */
const forEach = goog.NATIVE_ARRAY_PROTOTYPES &&
        (ASSUME_NATIVE_FUNCTIONS || Array.prototype.forEach) ?
    function(arr, f, opt_obj) {
      asserts.assert(arr.length != null);

      Array.prototype.forEach.call(arr, f, opt_obj);
    } :
    function(arr, f, opt_obj) {
      const l = arr.length;  // must be fixed during loop... see docs
      const arr2 = (typeof arr === 'string') ? arr.split('') : arr;
      for (let i = 0; i < l; i++) {
        if (i in arr2) {
          f.call(/** @type {?} */ (opt_obj), arr2[i], i, arr);
        }
      }
    };
exports.forEach = forEach;


/**
 * Calls a function for each element in an array, starting from the last
 * element rather than the first.
 *
 * @param {IArrayLike<T>|string} arr Array or array
 *     like object over which to iterate.
 * @param {?function(this: S, T, number, ?): ?} f The function to call for every
 *     element. This function
 *     takes 3 arguments (the element, the index and the array). The return
 *     value is ignored.
 * @param {S=} opt_obj The object to be used as the value of 'this'
 *     within f.
 * @template T,S
 */
function forEachRight(arr, f, opt_obj) {
  const l = arr.length;  // must be fixed during loop... see docs
  const arr2 = (typeof arr === 'string') ? arr.split('') : arr;
  for (let i = l - 1; i >= 0; --i) {
    if (i in arr2) {
      f.call(/** @type {?} */ (opt_obj), arr2[i], i, arr);
    }
  }
}
exports.forEachRight = forEachRight;


/**
 * Calls a function for each element in an array, and if the function returns
 * true adds the element to a new array.
 *
 * See {@link http://tinyurl.com/developer-mozilla-org-array-filter}
 *
 * @param {IArrayLike<T>|string} arr Array or array
 *     like object over which to iterate.
 * @param {?function(this:S, T, number, ?):boolean} f The function to call for
 *     every element. This function
 *     takes 3 arguments (the element, the index and the array) and must
 *     return a Boolean. If the return value is true the element is added to the
 *     result array. If it is false the element is not included.
 * @param {S=} opt_obj The object to be used as the value of 'this'
 *     within f.
 * @return {!Array<T>} a new array in which only elements that passed the test
 *     are present.
 * @template T,S
 */
const filter = goog.NATIVE_ARRAY_PROTOTYPES &&
        (ASSUME_NATIVE_FUNCTIONS || Array.prototype.filter) ?
    function(arr, f, opt_obj) {
      asserts.assert(arr.length != null);

      return Array.prototype.filter.call(arr, f, opt_obj);
    } :
    function(arr, f, opt_obj) {
      const l = arr.length;  // must be fixed during loop... see docs
      const res = [];
      let resLength = 0;
      const arr2 = (typeof arr === 'string') ? arr.split('') : arr;
      for (let i = 0; i < l; i++) {
        if (i in arr2) {
          const val = arr2[i];  // in case f mutates arr2
          if (f.call(/** @type {?} */ (opt_obj), val, i, arr)) {
            res[resLength++] = val;
          }
        }
      }
      return res;
    };
exports.filter = filter;


/**
 * Calls a function for each element in an array and inserts the result into a
 * new array.
 *
 * See {@link http://tinyurl.com/developer-mozilla-org-array-map}
 *
 * @param {IArrayLike<VALUE>|string} arr Array or array like object
 *     over which to iterate.
 * @param {function(this:THIS, VALUE, number, ?): RESULT} f The function to call
 *     for every element. This function takes 3 arguments (the element,
 *     the index and the array) and should return something. The result will be
 *     inserted into a new array.
 * @param {THIS=} opt_obj The object to be used as the value of 'this' within f.
 * @return {!Array<RESULT>} a new array with the results from f.
 * @template THIS, VALUE, RESULT
 */
const map = goog.NATIVE_ARRAY_PROTOTYPES &&
        (ASSUME_NATIVE_FUNCTIONS || Array.prototype.map) ?
    function(arr, f, opt_obj) {
      asserts.assert(arr.length != null);

      return Array.prototype.map.call(arr, f, opt_obj);
    } :
    function(arr, f, opt_obj) {
      const l = arr.length;  // must be fixed during loop... see docs
      const res = new Array(l);
      const arr2 = (typeof arr === 'string') ? arr.split('') : arr;
      for (let i = 0; i < l; i++) {
        if (i in arr2) {
          res[i] = f.call(/** @type {?} */ (opt_obj), arr2[i], i, arr);
        }
      }
      return res;
    };
exports.map = map;


/**
 * Passes every element of an array into a function and accumulates the result.
 *
 * See {@link http://tinyurl.com/developer-mozilla-org-array-reduce}
 * Note that this implementation differs from the native Array.prototype.reduce
 * in that the initial value is assumed to be defined (the MDN docs linked above
 * recommend not omitting this parameter, although it is technically optional).
 *
 * For example:
 * var a = [1, 2, 3, 4];
 * reduce(a, function(r, v, i, arr) {return r + v;}, 0);
 * returns 10
 *
 * @param {IArrayLike<T>|string} arr Array or array
 *     like object over which to iterate.
 * @param {function(this:S, R, T, number, ?) : R} f The function to call for
 *     every element. This function
 *     takes 4 arguments (the function's previous result or the initial value,
 *     the value of the current array element, the current array index, and the
 *     array itself)
 *     function(previousValue, currentValue, index, array).
 * @param {?} val The initial value to pass into the function on the first call.
 * @param {S=} opt_obj  The object to be used as the value of 'this'
 *     within f.
 * @return {R} Result of evaluating f repeatedly across the values of the array.
 * @template T,S,R
 */
const reduce = goog.NATIVE_ARRAY_PROTOTYPES &&
        (ASSUME_NATIVE_FUNCTIONS || Array.prototype.reduce) ?
    function(arr, f, val, opt_obj) {
      asserts.assert(arr.length != null);
      if (opt_obj) {
        f = goog.bind(f, opt_obj);
      }
      return Array.prototype.reduce.call(arr, f, val);
    } :
    function(arr, f, val, opt_obj) {
      let rval = val;
      forEach(arr, function(val, index) {
        rval = f.call(/** @type {?} */ (opt_obj), rval, val, index, arr);
      });
      return rval;
    };
exports.reduce = reduce;


/**
 * Passes every element of an array into a function and accumulates the result,
 * starting from the last element and working towards the first.
 *
 * See {@link http://tinyurl.com/developer-mozilla-org-array-reduceright}
 *
 * For example:
 * var a = ['a', 'b', 'c'];
 * reduceRight(a, function(r, v, i, arr) {return r + v;}, '');
 * returns 'cba'
 *
 * @param {IArrayLike<T>|string} arr Array or array
 *     like object over which to iterate.
 * @param {?function(this:S, R, T, number, ?) : R} f The function to call for
 *     every element. This function
 *     takes 4 arguments (the function's previous result or the initial value,
 *     the value of the current array element, the current array index, and the
 *     array itself)
 *     function(previousValue, currentValue, index, array).
 * @param {?} val The initial value to pass into the function on the first call.
 * @param {S=} opt_obj The object to be used as the value of 'this'
 *     within f.
 * @return {R} Object returned as a result of evaluating f repeatedly across the
 *     values of the array.
 * @template T,S,R
 */
const reduceRight = goog.NATIVE_ARRAY_PROTOTYPES &&
        (ASSUME_NATIVE_FUNCTIONS || Array.prototype.reduceRight) ?
    function(arr, f, val, opt_obj) {
      asserts.assert(arr.length != null);
      asserts.assert(f != null);
      if (opt_obj) {
        f = goog.bind(f, opt_obj);
      }
      return Array.prototype.reduceRight.call(arr, f, val);
    } :
    function(arr, f, val, opt_obj) {
      let rval = val;
      forEachRight(arr, function(val, index) {
        rval = f.call(/** @type {?} */ (opt_obj), rval, val, index, arr);
      });
      return rval;
    };
exports.reduceRight = reduceRight;


/**
 * Calls f for each element of an array. If any call returns true, some()
 * returns true (without checking the remaining elements). If all calls
 * return false, some() returns false.
 *
 * See {@link http://tinyurl.com/developer-mozilla-org-array-some}
 *
 * @param {IArrayLike<T>|string} arr Array or array
 *     like object over which to iterate.
 * @param {?function(this:S, T, number, ?) : boolean} f The function to call for
 *     for every element. This function takes 3 arguments (the element, the
 *     index and the array) and should return a boolean.
 * @param {S=} opt_obj  The object to be used as the value of 'this'
 *     within f.
 * @return {boolean} true if any element passes the test.
 * @template T,S
 */
const some = goog.NATIVE_ARRAY_PROTOTYPES &&
        (ASSUME_NATIVE_FUNCTIONS || Array.prototype.some) ?
    function(arr, f, opt_obj) {
      asserts.assert(arr.length != null);

      return Array.prototype.some.call(arr, f, opt_obj);
    } :
    function(arr, f, opt_obj) {
      const l = arr.length;  // must be fixed during loop... see docs
      const arr2 = (typeof arr === 'string') ? arr.split('') : arr;
      for (let i = 0; i < l; i++) {
        if (i in arr2 && f.call(/** @type {?} */ (opt_obj), arr2[i], i, arr)) {
          return true;
        }
      }
      return false;
    };
exports.some = some;


/**
 * Call f for each element of an array. If all calls return true, every()
 * returns true. If any call returns false, every() returns false and
 * does not continue to check the remaining elements.
 *
 * See {@link http://tinyurl.com/developer-mozilla-org-array-every}
 *
 * @param {IArrayLike<T>|string} arr Array or array
 *     like object over which to iterate.
 * @param {?function(this:S, T, number, ?) : boolean} f The function to call for
 *     for every element. This function takes 3 arguments (the element, the
 *     index and the array) and should return a boolean.
 * @param {S=} opt_obj The object to be used as the value of 'this'
 *     within f.
 * @return {boolean} false if any element fails the test.
 * @template T,S
 */
const every = goog.NATIVE_ARRAY_PROTOTYPES &&
        (ASSUME_NATIVE_FUNCTIONS || Array.prototype.every) ?
    function(arr, f, opt_obj) {
      asserts.assert(arr.length != null);

      return Array.prototype.every.call(arr, f, opt_obj);
    } :
    function(arr, f, opt_obj) {
      const l = arr.length;  // must be fixed during loop... see docs
      const arr2 = (typeof arr === 'string') ? arr.split('') : arr;
      for (let i = 0; i < l; i++) {
        if (i in arr2 && !f.call(/** @type {?} */ (opt_obj), arr2[i], i, arr)) {
          return false;
        }
      }
      return true;
    };
exports.every = every;


/**
 * Counts the array elements that fulfill the predicate, i.e. for which the
 * callback function returns true. Skips holes in the array.
 *
 * @param {!IArrayLike<T>|string} arr Array or array like object
 *     over which to iterate.
 * @param {function(this: S, T, number, ?): boolean} f The function to call for
 *     every element. Takes 3 arguments (the element, the index and the array).
 * @param {S=} opt_obj The object to be used as the value of 'this' within f.
 * @return {number} The number of the matching elements.
 * @template T,S
 */
function count(arr, f, opt_obj) {
  let count = 0;
  forEach(arr, function(element, index, arr) {
    if (f.call(/** @type {?} */ (opt_obj), element, index, arr)) {
      ++count;
    }
  }, opt_obj);
  return count;
}
exports.count = count;


/**
 * Search an array for the first element that satisfies a given condition and
 * return that element.
 * @param {IArrayLike<T>|string} arr Array or array
 *     like object over which to iterate.
 * @param {?function(this:S, T, number, ?) : boolean} f The function to call
 *     for every element. This function takes 3 arguments (the element, the
 *     index and the array) and should return a boolean.
 * @param {S=} opt_obj An optional "this" context for the function.
 * @return {T|null} The first array element that passes the test, or null if no
 *     element is found.
 * @template T,S
 */
function find(arr, f, opt_obj) {
  const i = findIndex(arr, f, opt_obj);
  return i < 0 ? null : typeof arr === 'string' ? arr.charAt(i) : arr[i];
}
exports.find = find;


/**
 * Search an array for the first element that satisfies a given condition and
 * return its index.
 * @param {IArrayLike<T>|string} arr Array or array
 *     like object over which to iterate.
 * @param {?function(this:S, T, number, ?) : boolean} f The function to call for
 *     every element. This function
 *     takes 3 arguments (the element, the index and the array) and should
 *     return a boolean.
 * @param {S=} opt_obj An optional "this" context for the function.
 * @return {number} The index of the first array element that passes the test,
 *     or -1 if no element is found.
 * @template T,S
 */
function findIndex(arr, f, opt_obj) {
  const l = arr.length;  // must be fixed during loop... see docs
  const arr2 = (typeof arr === 'string') ? arr.split('') : arr;
  for (let i = 0; i < l; i++) {
    if (i in arr2 && f.call(/** @type {?} */ (opt_obj), arr2[i], i, arr)) {
      return i;
    }
  }
  return -1;
}
exports.findIndex = findIndex;


/**
 * Search an array (in reverse order) for the last element that satisfies a
 * given condition and return that element.
 * @param {IArrayLike<T>|string} arr Array or array
 *     like object over which to iterate.
 * @param {?function(this:S, T, number, ?) : boolean} f The function to call
 *     for every element. This function
 *     takes 3 arguments (the element, the index and the array) and should
 *     return a boolean.
 * @param {S=} opt_obj An optional "this" context for the function.
 * @return {T|null} The last array element that passes the test, or null if no
 *     element is found.
 * @template T,S
 */
function findRight(arr, f, opt_obj) {
  const i = findIndexRight(arr, f, opt_obj);
  return i < 0 ? null : typeof arr === 'string' ? arr.charAt(i) : arr[i];
}
exports.findRight = findRight;


/**
 * Search an array (in reverse order) for the last element that satisfies a
 * given condition and return its index.
 * @param {IArrayLike<T>|string} arr Array or array
 *     like object over which to iterate.
 * @param {?function(this:S, T, number, ?) : boolean} f The function to call
 *     for every element. This function
 *     takes 3 arguments (the element, the index and the array) and should
 *     return a boolean.
 * @param {S=} opt_obj An optional "this" context for the function.
 * @return {number} The index of the last array element that passes the test,
 *     or -1 if no element is found.
 * @template T,S
 */
function findIndexRight(arr, f, opt_obj) {
  const l = arr.length;  // must be fixed during loop... see docs
  const arr2 = (typeof arr === 'string') ? arr.split('') : arr;
  for (let i = l - 1; i >= 0; i--) {
    if (i in arr2 && f.call(/** @type {?} */ (opt_obj), arr2[i], i, arr)) {
      return i;
    }
  }
  return -1;
}
exports.findIndexRight = findIndexRight;


/**
 * Whether the array contains the given object.
 * @param {IArrayLike<?>|string} arr The array to test for the presence of the
 *     element.
 * @param {*} obj The object for which to test.
 * @return {boolean} true if obj is present.
 */
function contains(arr, obj) {
  return indexOf(arr, obj) >= 0;
}
exports.contains = contains;


/**
 * Whether the array is empty.
 * @param {IArrayLike<?>|string} arr The array to test.
 * @return {boolean} true if empty.
 */
function isEmpty(arr) {
  return arr.length == 0;
}
exports.isEmpty = isEmpty;


/**
 * Clears the array.
 * @param {IArrayLike<?>} arr Array or array like object to clear.
 */
function clear(arr) {
  // For non real arrays we don't have the magic length so we delete the
  // indices.
  if (!Array.isArray(arr)) {
    for (let i = arr.length - 1; i >= 0; i--) {
      delete arr[i];
    }
  }
  arr.length = 0;
}
exports.clear = clear;


/**
 * Pushes an item into an array, if it's not already in the array.
 * @param {Array<T>} arr Array into which to insert the item.
 * @param {T} obj Value to add.
 * @template T
 */
function insert(arr, obj) {
  if (!contains(arr, obj)) {
    arr.push(obj);
  }
}
exports.insert = insert;


/**
 * Inserts an object at the given index of the array.
 * @param {IArrayLike<?>} arr The array to modify.
 * @param {*} obj The object to insert.
 * @param {number=} opt_i The index at which to insert the object. If omitted,
 *      treated as 0. A negative index is counted from the end of the array.
 */
function insertAt(arr, obj, opt_i) {
  splice(arr, opt_i, 0, obj);
}
exports.insertAt = insertAt;


/**
 * Inserts at the given index of the array, all elements of another array.
 * @param {IArrayLike<?>} arr The array to modify.
 * @param {IArrayLike<?>} elementsToAdd The array of elements to add.
 * @param {number=} opt_i The index at which to insert the object. If omitted,
 *      treated as 0. A negative index is counted from the end of the array.
 */
function insertArrayAt(arr, elementsToAdd, opt_i) {
  goog.partial(splice, arr, opt_i, 0).apply(null, elementsToAdd);
}
exports.insertArrayAt = insertArrayAt;


/**
 * Inserts an object into an array before a specified object.
 * @param {Array<T>} arr The array to modify.
 * @param {T} obj The object to insert.
 * @param {T=} opt_obj2 The object before which obj should be inserted. If obj2
 *     is omitted or not found, obj is inserted at the end of the array.
 * @template T
 */
function insertBefore(arr, obj, opt_obj2) {
  let i;
  if (arguments.length == 2 || (i = indexOf(arr, opt_obj2)) < 0) {
    arr.push(obj);
  } else {
    insertAt(arr, obj, i);
  }
}
exports.insertBefore = insertBefore;


/**
 * Removes the first occurrence of a particular value from an array.
 * @param {IArrayLike<T>} arr Array from which to remove
 *     value.
 * @param {T} obj Object to remove.
 * @return {boolean} True if an element was removed.
 * @template T
 */
function remove(arr, obj) {
  const i = indexOf(arr, obj);
  let rv;
  if ((rv = i >= 0)) {
    removeAt(arr, i);
  }
  return rv;
}
exports.remove = remove;


/**
 * Removes the last occurrence of a particular value from an array.
 * @param {!IArrayLike<T>} arr Array from which to remove value.
 * @param {T} obj Object to remove.
 * @return {boolean} True if an element was removed.
 * @template T
 */
function removeLast(arr, obj) {
  const i = lastIndexOf(arr, obj);
  if (i >= 0) {
    removeAt(arr, i);
    return true;
  }
  return false;
}
exports.removeLast = removeLast;


/**
 * Removes from an array the element at index i
 * @param {IArrayLike<?>} arr Array or array like object from which to
 *     remove value.
 * @param {number} i The index to remove.
 * @return {boolean} True if an element was removed.
 */
function removeAt(arr, i) {
  asserts.assert(arr.length != null);

  // use generic form of splice
  // splice returns the removed items and if successful the length of that
  // will be 1
  return Array.prototype.splice.call(arr, i, 1).length == 1;
}
exports.removeAt = removeAt;


/**
 * Removes the first value that satisfies the given condition.
 * @param {IArrayLike<T>} arr Array or array
 *     like object over which to iterate.
 * @param {?function(this:S, T, number, ?) : boolean} f The function to call
 *     for every element. This function
 *     takes 3 arguments (the element, the index and the array) and should
 *     return a boolean.
 * @param {S=} opt_obj An optional "this" context for the function.
 * @return {boolean} True if an element was removed.
 * @template T,S
 */
function removeIf(arr, f, opt_obj) {
  const i = findIndex(arr, f, opt_obj);
  if (i >= 0) {
    removeAt(arr, i);
    return true;
  }
  return false;
}
exports.removeIf = removeIf;


/**
 * Removes all values that satisfy the given condition.
 * @param {IArrayLike<T>} arr Array or array
 *     like object over which to iterate.
 * @param {?function(this:S, T, number, ?) : boolean} f The function to call
 *     for every element. This function
 *     takes 3 arguments (the element, the index and the array) and should
 *     return a boolean.
 * @param {S=} opt_obj An optional "this" context for the function.
 * @return {number} The number of items removed
 * @template T,S
 */
function removeAllIf(arr, f, opt_obj) {
  let removedCount = 0;
  forEachRight(arr, function(val, index) {
    if (f.call(/** @type {?} */ (opt_obj), val, index, arr)) {
      if (removeAt(arr, index)) {
        removedCount++;
      }
    }
  });
  return removedCount;
}
exports.removeAllIf = removeAllIf;


/**
 * Returns a new array that is the result of joining the arguments.  If arrays
 * are passed then their items are added, however, if non-arrays are passed they
 * will be added to the return array as is.
 *
 * Note that ArrayLike objects will be added as is, rather than having their
 * items added.
 *
 * concat([1, 2], [3, 4]) -> [1, 2, 3, 4]
 * concat(0, [1, 2]) -> [0, 1, 2]
 * concat([1, 2], null) -> [1, 2, null]
 *
 * There is bug in all current versions of IE (6, 7 and 8) where arrays created
 * in an iframe become corrupted soon (not immediately) after the iframe is
 * destroyed. This is common if loading data via goog.net.IframeIo, for example.
 * This corruption only affects the concat method which will start throwing
 * Catastrophic Errors (#-2147418113).
 *
 * See http://endoflow.com/scratch/corrupted-arrays.html for a test case.
 *
 * Internally goog.array should use this, so that all methods will continue to
 * work on these broken array objects.
 *
 * @param {...*} var_args Items to concatenate.  Arrays will have each item
 *     added, while primitives and objects will be added as is.
 * @return {!Array<?>} The new resultant array.
 */
function concat(var_args) {
  return Array.prototype.concat.apply([], arguments);
}
exports.concat = concat;


/**
 * Returns a new array that contains the contents of all the arrays passed.
 * @param {...!Array<T>} var_args
 * @return {!Array<T>}
 * @template T
 */
function join(var_args) {
  return Array.prototype.concat.apply([], arguments);
}
exports.join = join;


/**
 * Converts an object to an array.
 * @param {IArrayLike<T>|string} object  The object to convert to an
 *     array.
 * @return {!Array<T>} The object converted into an array. If object has a
 *     length property, every property indexed with a non-negative number
 *     less than length will be included in the result. If object does not
 *     have a length property, an empty array will be returned.
 * @template T
 */
function toArray(object) {
  const length = object.length;

  // If length is not a number the following is false. This case is kept for
  // backwards compatibility since there are callers that pass objects that are
  // not array like.
  if (length > 0) {
    const rv = new Array(length);
    for (let i = 0; i < length; i++) {
      rv[i] = object[i];
    }
    return rv;
  }
  return [];
}
exports.toArray = toArray;


/**
 * Does a shallow copy of an array.
 * @param {IArrayLike<T>|string} arr  Array or array-like object to
 *     clone.
 * @return {!Array<T>} Clone of the input array.
 * @template T
 */
const clone = toArray;
exports.clone = clone;


/**
 * Extends an array with another array, element, or "array like" object.
 * This function operates 'in-place', it does not create a new Array.
 *
 * Example:
 * var a = [];
 * extend(a, [0, 1]);
 * a; // [0, 1]
 * extend(a, 2);
 * a; // [0, 1, 2]
 *
 * @param {Array<VALUE>} arr1  The array to modify.
 * @param {...(IArrayLike<VALUE>|VALUE)} var_args The elements or arrays of
 *     elements to add to arr1.
 * @template VALUE
 */
function extend(arr1, var_args) {
  for (let i = 1; i < arguments.length; i++) {
    const arr2 = arguments[i];
    if (goog.isArrayLike(arr2)) {
      const len1 = arr1.length || 0;
      const len2 = arr2.length || 0;
      arr1.length = len1 + len2;
      for (let j = 0; j < len2; j++) {
        arr1[len1 + j] = arr2[j];
      }
    } else {
      arr1.push(arr2);
    }
  }
}
exports.extend = extend;


/**
 * Adds or removes elements from an array. This is a generic version of Array
 * splice. This means that it might work on other objects similar to arrays,
 * such as the arguments object.
 *
 * @param {IArrayLike<T>} arr The array to modify.
 * @param {number|undefined} index The index at which to start changing the
 *     array. If not defined, treated as 0.
 * @param {number} howMany How many elements to remove (0 means no removal. A
 *     value below 0 is treated as zero and so is any other non number. Numbers
 *     are floored).
 * @param {...T} var_args Optional, additional elements to insert into the
 *     array.
 * @return {!Array<T>} the removed elements.
 * @template T
 */
function splice(arr, index, howMany, var_args) {
  asserts.assert(arr.length != null);

  return Array.prototype.splice.apply(arr, slice(arguments, 1));
}
exports.splice = splice;


/**
 * Returns a new array from a segment of an array. This is a generic version of
 * Array slice. This means that it might work on other objects similar to
 * arrays, such as the arguments object.
 *
 * @param {IArrayLike<T>|string} arr The array from
 * which to copy a segment.
 * @param {number} start The index of the first element to copy.
 * @param {number=} opt_end The index after the last element to copy.
 * @return {!Array<T>} A new array containing the specified segment of the
 *     original array.
 * @template T
 */
function slice(arr, start, opt_end) {
  asserts.assert(arr.length != null);

  // passing 1 arg to slice is not the same as passing 2 where the second is
  // null or undefined (in that case the second argument is treated as 0).
  // we could use slice on the arguments object and then use apply instead of
  // testing the length
  if (arguments.length <= 2) {
    return Array.prototype.slice.call(arr, start);
  } else {
    return Array.prototype.slice.call(arr, start, opt_end);
  }
}
exports.slice = slice;


/**
 * Removes all duplicates from an array (retaining only the first
 * occurrence of each array element).  This function modifies the
 * array in place and doesn't change the order of the non-duplicate items.
 *
 * For objects, duplicates are identified as having the same unique ID as
 * defined by {@link goog.getUid}.
 *
 * Alternatively you can specify a custom hash function that returns a unique
 * value for each item in the array it should consider unique.
 *
 * Runtime: N,
 * Worstcase space: 2N (no dupes)
 *
 * @param {IArrayLike<T>} arr The array from which to remove
 *     duplicates.
 * @param {Array=} opt_rv An optional array in which to return the results,
 *     instead of performing the removal inplace.  If specified, the original
 *     array will remain unchanged.
 * @param {function(T):string=} opt_hashFn An optional function to use to
 *     apply to every item in the array. This function should return a unique
 *     value for each item in the array it should consider unique.
 * @template T
 */
function removeDuplicates(arr, opt_rv, opt_hashFn) {
  const returnArray = opt_rv || arr;
  const defaultHashFn = function(item) {
    // Prefix each type with a single character representing the type to
    // prevent conflicting keys (e.g. true and 'true').
    return goog.isObject(item) ? 'o' + goog.getUid(item) :
                                 (typeof item).charAt(0) + item;
  };
  const hashFn = opt_hashFn || defaultHashFn;

  let cursorInsert = 0;
  let cursorRead = 0;
  const seen = {};

  while (cursorRead < arr.length) {
    const current = arr[cursorRead++];
    const key = hashFn(current);
    if (!Object.prototype.hasOwnProperty.call(seen, key)) {
      seen[key] = true;
      returnArray[cursorInsert++] = current;
    }
  }
  returnArray.length = cursorInsert;
}
exports.removeDuplicates = removeDuplicates;


/**
 * Searches the specified array for the specified target using the binary
 * search algorithm.  If no opt_compareFn is specified, elements are compared
 * using <code>defaultCompare</code>, which compares the elements
 * using the built in < and > operators.  This will produce the expected
 * behavior for homogeneous arrays of String(s) and Number(s). The array
 * specified <b>must</b> be sorted in ascending order (as defined by the
 * comparison function).  If the array is not sorted, results are undefined.
 * If the array contains multiple instances of the specified target value, the
 * left-most instance will be found.
 *
 * Runtime: O(log n)
 *
 * @param {IArrayLike<VALUE>} arr The array to be searched.
 * @param {TARGET} target The sought value.
 * @param {function(TARGET, VALUE): number=} opt_compareFn Optional comparison
 *     function by which the array is ordered. Should take 2 arguments to
 *     compare, the target value and an element from your array, and return a
 *     negative number, zero, or a positive number depending on whether the
 *     first argument is less than, equal to, or greater than the second.
 * @return {number} Lowest index of the target value if found, otherwise
 *     (-(insertion point) - 1). The insertion point is where the value should
 *     be inserted into arr to preserve the sorted property.  Return value >= 0
 *     iff target is found.
 * @template TARGET, VALUE
 */
function binarySearch(arr, target, opt_compareFn) {
  return binarySearch_(
      arr, opt_compareFn || defaultCompare, false /* isEvaluator */, target);
}
exports.binarySearch = binarySearch;


/**
 * Selects an index in the specified array using the binary search algorithm.
 * The evaluator receives an element and determines whether the desired index
 * is before, at, or after it.  The evaluator must be consistent (formally,
 * map(map(arr, evaluator, opt_obj), goog.math.sign)
 * must be monotonically non-increasing).
 *
 * Runtime: O(log n)
 *
 * @param {IArrayLike<VALUE>} arr The array to be searched.
 * @param {function(this:THIS, VALUE, number, ?): number} evaluator
 *     Evaluator function that receives 3 arguments (the element, the index and
 *     the array). Should return a negative number, zero, or a positive number
 *     depending on whether the desired index is before, at, or after the
 *     element passed to it.
 * @param {THIS=} opt_obj The object to be used as the value of 'this'
 *     within evaluator.
 * @return {number} Index of the leftmost element matched by the evaluator, if
 *     such exists; otherwise (-(insertion point) - 1). The insertion point is
 *     the index of the first element for which the evaluator returns negative,
 *     or arr.length if no such element exists. The return value is non-negative
 *     iff a match is found.
 * @template THIS, VALUE
 */
function binarySelect(arr, evaluator, opt_obj) {
  return binarySearch_(
      arr, evaluator, true /* isEvaluator */, undefined /* opt_target */,
      opt_obj);
}
exports.binarySelect = binarySelect;


/**
 * Implementation of a binary search algorithm which knows how to use both
 * comparison functions and evaluators. If an evaluator is provided, will call
 * the evaluator with the given optional data object, conforming to the
 * interface defined in binarySelect. Otherwise, if a comparison function is
 * provided, will call the comparison function against the given data object.
 *
 * This implementation purposefully does not use goog.bind or goog.partial for
 * performance reasons.
 *
 * Runtime: O(log n)
 *
 * @param {IArrayLike<?>} arr The array to be searched.
 * @param {function(?, ?, ?): number | function(?, ?): number} compareFn
 *     Either an evaluator or a comparison function, as defined by binarySearch
 *     and binarySelect above.
 * @param {boolean} isEvaluator Whether the function is an evaluator or a
 *     comparison function.
 * @param {?=} opt_target If the function is a comparison function, then
 *     this is the target to binary search for.
 * @param {Object=} opt_selfObj If the function is an evaluator, this is an
 *     optional this object for the evaluator.
 * @return {number} Lowest index of the target value if found, otherwise
 *     (-(insertion point) - 1). The insertion point is where the value should
 *     be inserted into arr to preserve the sorted property.  Return value >= 0
 *     iff target is found.
 * @private
 */
function binarySearch_(arr, compareFn, isEvaluator, opt_target, opt_selfObj) {
  let left = 0;            // inclusive
  let right = arr.length;  // exclusive
  let found;
  while (left < right) {
    const middle = left + ((right - left) >>> 1);
    let compareResult;
    if (isEvaluator) {
      compareResult = compareFn.call(opt_selfObj, arr[middle], middle, arr);
    } else {
      // NOTE(dimvar): To avoid this cast, we'd have to use function overloading
      // for the type of binarySearch_, which the type system can't express yet.
      compareResult = /** @type {function(?, ?): number} */ (compareFn)(
          opt_target, arr[middle]);
    }
    if (compareResult > 0) {
      left = middle + 1;
    } else {
      right = middle;
      // We are looking for the lowest index so we can't return immediately.
      found = !compareResult;
    }
  }
  // left is the index if found, or the insertion point otherwise.
  // Avoiding bitwise not operator, as that causes a loss in precision for array
  // indexes outside the bounds of a 32-bit signed integer.  Array indexes have
  // a maximum value of 2^32-2 https://tc39.es/ecma262/#array-index
  return found ? left : -left - 1;
}


/**
 * Sorts the specified array into ascending order.  If no opt_compareFn is
 * specified, elements are compared using
 * <code>defaultCompare</code>, which compares the elements using
 * the built in < and > operators.  This will produce the expected behavior
 * for homogeneous arrays of String(s) and Number(s), unlike the native sort,
 * but will give unpredictable results for heterogeneous lists of strings and
 * numbers with different numbers of digits.
 *
 * This sort is not guaranteed to be stable.
 *
 * Runtime: Same as `Array.prototype.sort`
 *
 * @param {Array<T>} arr The array to be sorted.
 * @param {?function(T,T):number=} opt_compareFn Optional comparison
 *     function by which the
 *     array is to be ordered. Should take 2 arguments to compare, and return a
 *     negative number, zero, or a positive number depending on whether the
 *     first argument is less than, equal to, or greater than the second.
 * @template T
 */
function sort(arr, opt_compareFn) {
  // TODO(arv): Update type annotation since null is not accepted.
  arr.sort(opt_compareFn || defaultCompare);
}
exports.sort = sort;


/**
 * Sorts the specified array into ascending order in a stable way.  If no
 * opt_compareFn is specified, elements are compared using
 * <code>defaultCompare</code>, which compares the elements using
 * the built in < and > operators.  This will produce the expected behavior
 * for homogeneous arrays of String(s) and Number(s).
 *
 * Runtime: Same as `Array.prototype.sort`, plus an additional
 * O(n) overhead of copying the array twice.
 *
 * @param {Array<T>} arr The array to be sorted.
 * @param {?function(T, T): number=} opt_compareFn Optional comparison function
 *     by which the array is to be ordered. Should take 2 arguments to compare,
 *     and return a negative number, zero, or a positive number depending on
 *     whether the first argument is less than, equal to, or greater than the
 *     second.
 * @template T
 */
function stableSort(arr, opt_compareFn) {
  const compArr = new Array(arr.length);
  for (let i = 0; i < arr.length; i++) {
    compArr[i] = {index: i, value: arr[i]};
  }
  const valueCompareFn = opt_compareFn || defaultCompare;
  function stableCompareFn(obj1, obj2) {
    return valueCompareFn(obj1.value, obj2.value) || obj1.index - obj2.index;
  }
  sort(compArr, stableCompareFn);
  for (let i = 0; i < arr.length; i++) {
    arr[i] = compArr[i].value;
  }
}
exports.stableSort = stableSort;


/**
 * Sort the specified array into ascending order based on item keys
 * returned by the specified key function.
 * If no opt_compareFn is specified, the keys are compared in ascending order
 * using <code>defaultCompare</code>.
 *
 * Runtime: O(S(f(n)), where S is runtime of <code>sort</code>
 * and f(n) is runtime of the key function.
 *
 * @param {Array<T>} arr The array to be sorted.
 * @param {function(T): K} keyFn Function taking array element and returning
 *     a key used for sorting this element.
 * @param {?function(K, K): number=} opt_compareFn Optional comparison function
 *     by which the keys are to be ordered. Should take 2 arguments to compare,
 *     and return a negative number, zero, or a positive number depending on
 *     whether the first argument is less than, equal to, or greater than the
 *     second.
 * @template T,K
 */
function sortByKey(arr, keyFn, opt_compareFn) {
  const keyCompareFn = opt_compareFn || defaultCompare;
  sort(arr, function(a, b) {
    return keyCompareFn(keyFn(a), keyFn(b));
  });
}
exports.sortByKey = sortByKey;


/**
 * Sorts an array of objects by the specified object key and compare
 * function. If no compare function is provided, the key values are
 * compared in ascending order using <code>defaultCompare</code>.
 * This won't work for keys that get renamed by the compiler. So use
 * {'foo': 1, 'bar': 2} rather than {foo: 1, bar: 2}.
 * @param {Array<Object>} arr An array of objects to sort.
 * @param {string} key The object key to sort by.
 * @param {Function=} opt_compareFn The function to use to compare key
 *     values.
 */
function sortObjectsByKey(arr, key, opt_compareFn) {
  sortByKey(arr, function(obj) {
    return obj[key];
  }, opt_compareFn);
}
exports.sortObjectsByKey = sortObjectsByKey;


/**
 * Tells if the array is sorted.
 * @param {!IArrayLike<T>} arr The array.
 * @param {?function(T,T):number=} opt_compareFn Function to compare the
 *     array elements.
 *     Should take 2 arguments to compare, and return a negative number, zero,
 *     or a positive number depending on whether the first argument is less
 *     than, equal to, or greater than the second.
 * @param {boolean=} opt_strict If true no equal elements are allowed.
 * @return {boolean} Whether the array is sorted.
 * @template T
 */
function isSorted(arr, opt_compareFn, opt_strict) {
  const compare = opt_compareFn || defaultCompare;
  for (let i = 1; i < arr.length; i++) {
    const compareResult = compare(arr[i - 1], arr[i]);
    if (compareResult > 0 || compareResult == 0 && opt_strict) {
      return false;
    }
  }
  return true;
}
exports.isSorted = isSorted;


/**
 * Compares two arrays for equality. Two arrays are considered equal if they
 * have the same length and their corresponding elements are equal according to
 * the comparison function.
 *
 * @param {IArrayLike<A>} arr1 The first array to compare.
 * @param {IArrayLike<B>} arr2 The second array to compare.
 * @param {?function(A,B):boolean=} opt_equalsFn Optional comparison function.
 *     Should take 2 arguments to compare, and return true if the arguments
 *     are equal. Defaults to {@link goog.array.defaultCompareEquality} which
 *     compares the elements using the built-in '===' operator.
 * @return {boolean} Whether the two arrays are equal.
 * @template A
 * @template B
 */
function equals(arr1, arr2, opt_equalsFn) {
  if (!goog.isArrayLike(arr1) || !goog.isArrayLike(arr2) ||
      arr1.length != arr2.length) {
    return false;
  }
  const l = arr1.length;
  const equalsFn = opt_equalsFn || defaultCompareEquality;
  for (let i = 0; i < l; i++) {
    if (!equalsFn(arr1[i], arr2[i])) {
      return false;
    }
  }
  return true;
}
exports.equals = equals;


/**
 * 3-way array compare function.
 * @param {!IArrayLike<VALUE>} arr1 The first array to
 *     compare.
 * @param {!IArrayLike<VALUE>} arr2 The second array to
 *     compare.
 * @param {function(VALUE, VALUE): number=} opt_compareFn Optional comparison
 *     function by which the array is to be ordered. Should take 2 arguments to
 *     compare, and return a negative number, zero, or a positive number
 *     depending on whether the first argument is less than, equal to, or
 *     greater than the second.
 * @return {number} Negative number, zero, or a positive number depending on
 *     whether the first argument is less than, equal to, or greater than the
 *     second.
 * @template VALUE
 */
function compare3(arr1, arr2, opt_compareFn) {
  const compare = opt_compareFn || defaultCompare;
  const l = Math.min(arr1.length, arr2.length);
  for (let i = 0; i < l; i++) {
    const result = compare(arr1[i], arr2[i]);
    if (result != 0) {
      return result;
    }
  }
  return defaultCompare(arr1.length, arr2.length);
}
exports.compare3 = compare3;


/**
 * Compares its two arguments for order, using the built in < and >
 * operators.
 * @param {VALUE} a The first object to be compared.
 * @param {VALUE} b The second object to be compared.
 * @return {number} A negative number, zero, or a positive number as the first
 *     argument is less than, equal to, or greater than the second,
 *     respectively.
 * @template VALUE
 */
function defaultCompare(a, b) {
  return a > b ? 1 : a < b ? -1 : 0;
}
exports.defaultCompare = defaultCompare;


/**
 * Compares its two arguments for inverse order, using the built in < and >
 * operators.
 * @param {VALUE} a The first object to be compared.
 * @param {VALUE} b The second object to be compared.
 * @return {number} A negative number, zero, or a positive number as the first
 *     argument is greater than, equal to, or less than the second,
 *     respectively.
 * @template VALUE
 */
function inverseDefaultCompare(a, b) {
  return -defaultCompare(a, b);
}
exports.inverseDefaultCompare = inverseDefaultCompare;


/**
 * Compares its two arguments for equality, using the built in === operator.
 * @param {*} a The first object to compare.
 * @param {*} b The second object to compare.
 * @return {boolean} True if the two arguments are equal, false otherwise.
 */
function defaultCompareEquality(a, b) {
  return a === b;
}
exports.defaultCompareEquality = defaultCompareEquality;


/**
 * Inserts a value into a sorted array. The array is not modified if the
 * value is already present.
 * @param {IArrayLike<VALUE>} array The array to modify.
 * @param {VALUE} value The object to insert.
 * @param {function(VALUE, VALUE): number=} opt_compareFn Optional comparison
 *     function by which the array is ordered. Should take 2 arguments to
 *     compare, and return a negative number, zero, or a positive number
 *     depending on whether the first argument is less than, equal to, or
 *     greater than the second.
 * @return {boolean} True if an element was inserted.
 * @template VALUE
 */
function binaryInsert(array, value, opt_compareFn) {
  const index = binarySearch(array, value, opt_compareFn);
  if (index < 0) {
    insertAt(array, value, -(index + 1));
    return true;
  }
  return false;
}
exports.binaryInsert = binaryInsert;


/**
 * Removes a value from a sorted array.
 * @param {!IArrayLike<VALUE>} array The array to modify.
 * @param {VALUE} value The object to remove.
 * @param {function(VALUE, VALUE): number=} opt_compareFn Optional comparison
 *     function by which the array is ordered. Should take 2 arguments to
 *     compare, and return a negative number, zero, or a positive number
 *     depending on whether the first argument is less than, equal to, or
 *     greater than the second.
 * @return {boolean} True if an element was removed.
 * @template VALUE
 */
function binaryRemove(array, value, opt_compareFn) {
  const index = binarySearch(array, value, opt_compareFn);
  return (index >= 0) ? removeAt(array, index) : false;
}
exports.binaryRemove = binaryRemove;


/**
 * Splits an array into disjoint buckets according to a splitting function.
 * @param {IArrayLike<T>} array The array.
 * @param {function(this:S, T, number, !IArrayLike<T>):?} sorter Function to
 *     call for every element.  This takes 3 arguments (the element, the index
 *     and the array) and must return a valid object key (a string, number,
 *     etc), or undefined, if that object should not be placed in a bucket.
 * @param {S=} opt_obj The object to be used as the value of 'this' within
 *     sorter.
 * @return {!Object<!Array<T>>} An object, with keys being all of the unique
 *     return values of sorter, and values being arrays containing the items for
 *     which the splitter returned that key.
 * @template T,S
 */
function bucket(array, sorter, opt_obj) {
  const buckets = {};

  for (let i = 0; i < array.length; i++) {
    const value = array[i];
    const key = sorter.call(/** @type {?} */ (opt_obj), value, i, array);
    if (key !== undefined) {
      // Push the value to the right bucket, creating it if necessary.
      const bucket = buckets[key] || (buckets[key] = []);
      bucket.push(value);
    }
  }

  return buckets;
}
exports.bucket = bucket;


/**
 * Splits an array into disjoint buckets according to a splitting function.
 * @param {!IArrayLike<V>} array The array.
 * @param {function(V, number, !IArrayLike<V>):(K|undefined)} sorter Function to
 *     call for every element.  This takes 3 arguments (the element, the index,
 *     and the array) and must return a value to use as a key, or undefined, if
 *     that object should not be placed in a bucket.
 * @return {!Map<K, !Array<V>>} A map, with keys being all of the unique
 *     return values of sorter, and values being arrays containing the items for
 *     which the splitter returned that key.
 * @template K,V
 */
function bucketToMap(array, sorter) {
  const /** !Map<K, !Array<V>> */ buckets = new Map();

  for (let i = 0; i < array.length; i++) {
    const value = array[i];
    const key = sorter(value, i, array);
    if (key !== undefined) {
      // Push the value to the right bucket, creating it if necessary.
      let bucket = buckets.get(key);
      if (!bucket) {
        bucket = [];
        buckets.set(key, bucket);
      }
      bucket.push(value);
    }
  }

  return buckets;
}
exports.bucketToMap = bucketToMap;


/**
 * Creates a new object built from the provided array and the key-generation
 * function.
 * @param {IArrayLike<T>} arr Array or array like object over
 *     which to iterate whose elements will be the values in the new object.
 * @param {?function(this:S, T, number, ?) : string} keyFunc The function to
 *     call for every element. This function takes 3 arguments (the element, the
 *     index and the array) and should return a string that will be used as the
 *     key for the element in the new object. If the function returns the same
 *     key for more than one element, the value for that key is
 *     implementation-defined.
 * @param {S=} opt_obj The object to be used as the value of 'this'
 *     within keyFunc.
 * @return {!Object<T>} The new object.
 * @template T,S
 */
function toObject(arr, keyFunc, opt_obj) {
  const ret = {};
  forEach(arr, function(element, index) {
    ret[keyFunc.call(/** @type {?} */ (opt_obj), element, index, arr)] =
        element;
  });
  return ret;
}
exports.toObject = toObject;


/**
 * Creates a new ES6 Map built from the provided array and the key-generation
 * function.
 * @param {!IArrayLike<V>} arr Array or array like object over which to iterate
 *     whose elements will be the values in the new object.
 * @param {?function(V, number, ?) : K} keyFunc The function to call for every
 *     element. This function takes 3 arguments (the element, the index, and the
 *     array) and should return a value that will be used as the key for the
 *     element in the new object. If the function returns the same key for more
 *     than one element, the value for that key is implementation-defined.
 * @return {!Map<K, V>} The new map.
 * @template K,V
 */
function toMap(arr, keyFunc) {
  const /** !Map<K, V> */ map = new Map();

  for (let i = 0; i < arr.length; i++) {
    const element = arr[i];
    map.set(keyFunc(element, i, arr), element);
  }

  return map;
}
exports.toMap = toMap;


/**
 * Creates a range of numbers in an arithmetic progression.
 *
 * Range takes 1, 2, or 3 arguments:
 * <pre>
 * range(5) is the same as range(0, 5, 1) and produces [0, 1, 2, 3, 4]
 * range(2, 5) is the same as range(2, 5, 1) and produces [2, 3, 4]
 * range(-2, -5, -1) produces [-2, -3, -4]
 * range(-2, -5, 1) produces [], since stepping by 1 wouldn't ever reach -5.
 * </pre>
 *
 * @param {number} startOrEnd The starting value of the range if an end argument
 *     is provided. Otherwise, the start value is 0, and this is the end value.
 * @param {number=} opt_end The optional end value of the range.
 * @param {number=} opt_step The step size between range values. Defaults to 1
 *     if opt_step is undefined or 0.
 * @return {!Array<number>} An array of numbers for the requested range. May be
 *     an empty array if adding the step would not converge toward the end
 *     value.
 */
function range(startOrEnd, opt_end, opt_step) {
  const array = [];
  let start = 0;
  let end = startOrEnd;
  const step = opt_step || 1;
  if (opt_end !== undefined) {
    start = startOrEnd;
    end = opt_end;
  }

  if (step * (end - start) < 0) {
    // Sign mismatch: start + step will never reach the end value.
    return [];
  }

  if (step > 0) {
    for (let i = start; i < end; i += step) {
      array.push(i);
    }
  } else {
    for (let i = start; i > end; i += step) {
      array.push(i);
    }
  }
  return array;
}
exports.range = range;


/**
 * Returns an array consisting of the given value repeated N times.
 *
 * @param {VALUE} value The value to repeat.
 * @param {number} n The repeat count.
 * @return {!Array<VALUE>} An array with the repeated value.
 * @template VALUE
 */
function repeat(value, n) {
  const array = [];
  for (let i = 0; i < n; i++) {
    array[i] = value;
  }
  return array;
}
exports.repeat = repeat;


/**
 * Returns an array consisting of every argument with all arrays
 * expanded in-place recursively.
 *
 * @param {...*} var_args The values to flatten.
 * @return {!Array<?>} An array containing the flattened values.
 */
function flatten(var_args) {
  const CHUNK_SIZE = 8192;

  const result = [];
  for (let i = 0; i < arguments.length; i++) {
    const element = arguments[i];
    if (Array.isArray(element)) {
      for (let c = 0; c < element.length; c += CHUNK_SIZE) {
        const chunk = slice(element, c, c + CHUNK_SIZE);
        const recurseResult = flatten.apply(null, chunk);
        for (let r = 0; r < recurseResult.length; r++) {
          result.push(recurseResult[r]);
        }
      }
    } else {
      result.push(element);
    }
  }
  return result;
}
exports.flatten = flatten;


/**
 * Rotates an array in-place. After calling this method, the element at
 * index i will be the element previously at index (i - n) %
 * array.length, for all values of i between 0 and array.length - 1,
 * inclusive.
 *
 * For example, suppose list comprises [t, a, n, k, s]. After invoking
 * rotate(array, 1) (or rotate(array, -4)), array will comprise [s, t, a, n, k].
 *
 * @param {!Array<T>} array The array to rotate.
 * @param {number} n The amount to rotate.
 * @return {!Array<T>} The array.
 * @template T
 */
function rotate(array, n) {
  asserts.assert(array.length != null);

  if (array.length) {
    n %= array.length;
    if (n > 0) {
      Array.prototype.unshift.apply(array, array.splice(-n, n));
    } else if (n < 0) {
      Array.prototype.push.apply(array, array.splice(0, -n));
    }
  }
  return array;
}
exports.rotate = rotate;


/**
 * Moves one item of an array to a new position keeping the order of the rest
 * of the items. Example use case: keeping a list of JavaScript objects
 * synchronized with the corresponding list of DOM elements after one of the
 * elements has been dragged to a new position.
 * @param {!IArrayLike<?>} arr The array to modify.
 * @param {number} fromIndex Index of the item to move between 0 and
 *     `arr.length - 1`.
 * @param {number} toIndex Target index between 0 and `arr.length - 1`.
 */
function moveItem(arr, fromIndex, toIndex) {
  asserts.assert(fromIndex >= 0 && fromIndex < arr.length);
  asserts.assert(toIndex >= 0 && toIndex < arr.length);
  // Remove 1 item at fromIndex.
  const removedItems = Array.prototype.splice.call(arr, fromIndex, 1);
  // Insert the removed item at toIndex.
  Array.prototype.splice.call(arr, toIndex, 0, removedItems[0]);
  // We don't use goog.array.insertAt and goog.array.removeAt, because they're
  // significantly slower than splice.
}
exports.moveItem = moveItem;


/**
 * Creates a new array for which the element at position i is an array of the
 * ith element of the provided arrays.  The returned array will only be as long
 * as the shortest array provided; additional values are ignored.  For example,
 * the result of zipping [1, 2] and [3, 4, 5] is [[1,3], [2, 4]].
 *
 * This is similar to the zip() function in Python.  See {@link
 * http://docs.python.org/library/functions.html#zip}
 *
 * @param {...!IArrayLike<?>} var_args Arrays to be combined.
 * @return {!Array<!Array<?>>} A new array of arrays created from
 *     provided arrays.
 */
function zip(var_args) {
  if (!arguments.length) {
    return [];
  }
  const result = [];
  let minLen = arguments[0].length;
  for (let i = 1; i < arguments.length; i++) {
    if (arguments[i].length < minLen) {
      minLen = arguments[i].length;
    }
  }
  for (let i = 0; i < minLen; i++) {
    const value = [];
    for (let j = 0; j < arguments.length; j++) {
      value.push(arguments[j][i]);
    }
    result.push(value);
  }
  return result;
}
exports.zip = zip;


/**
 * Shuffles the values in the specified array using the Fisher-Yates in-place
 * shuffle (also known as the Knuth Shuffle). By default, calls Math.random()
 * and so resets the state of that random number generator. Similarly, may reset
 * the state of any other specified random number generator.
 *
 * Runtime: O(n)
 *
 * @param {!Array<?>} arr The array to be shuffled.
 * @param {function():number=} opt_randFn Optional random function to use for
 *     shuffling.
 *     Takes no arguments, and returns a random number on the interval [0, 1).
 *     Defaults to Math.random() using JavaScript's built-in Math library.
 */
function shuffle(arr, opt_randFn) {
  const randFn = opt_randFn || Math.random;

  for (let i = arr.length - 1; i > 0; i--) {
    // Choose a random array index in [0, i] (inclusive with i).
    const j = Math.floor(randFn() * (i + 1));

    const tmp = arr[i];
    arr[i] = arr[j];
    arr[j] = tmp;
  }
}
exports.shuffle = shuffle;


/**
 * Returns a new array of elements from arr, based on the indexes of elements
 * provided by index_arr. For example, the result of index copying
 * ['a', 'b', 'c'] with index_arr [1,0,0,2] is ['b', 'a', 'a', 'c'].
 *
 * @param {!IArrayLike<T>} arr The array to get a indexed copy from.
 * @param {!IArrayLike<number>} index_arr An array of indexes to get from arr.
 * @return {!Array<T>} A new array of elements from arr in index_arr order.
 * @template T
 */
function copyByIndex(arr, index_arr) {
  const result = [];
  forEach(index_arr, function(index) {
    result.push(arr[index]);
  });
  return result;
}
exports.copyByIndex = copyByIndex;


/**
 * Maps each element of the input array into zero or more elements of the output
 * array.
 *
 * @param {!IArrayLike<VALUE>|string} arr Array or array like object
 *     over which to iterate.
 * @param {function(this:THIS, VALUE, number, ?): !Array<RESULT>} f The function
 *     to call for every element. This function takes 3 arguments (the element,
 *     the index and the array) and should return an array. The result will be
 *     used to extend a new array.
 * @param {THIS=} opt_obj The object to be used as the value of 'this' within f.
 * @return {!Array<RESULT>} a new array with the concatenation of all arrays
 *     returned from f.
 * @template THIS, VALUE, RESULT
 */
function concatMap(arr, f, opt_obj) {
  return concat.apply([], map(arr, f, opt_obj));
}
exports.concatMap = concatMap;

;return exports;});

//third_party/javascript/closure/dom/htmlelement.js
/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

goog.provide('goog.dom.HtmlElement');



/**
 * This subclass of HTMLElement is used when only a HTMLElement is possible and
 * not any of its subclasses. Normally, a type can refer to an instance of
 * itself or an instance of any subtype. More concretely, if HTMLElement is used
 * then the compiler must assume that it might still be e.g. HTMLScriptElement.
 * With this, the type check knows that it couldn't be any special element.
 *
 * @constructor
 * @extends {HTMLElement}
 */
goog.dom.HtmlElement = function() {};

//third_party/javascript/closure/dom/tagname.js
/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Defines the goog.dom.TagName class. Its constants enumerate
 * all HTML tag names specified in either the W3C HTML 4.01 index of elements
 * or the HTML5.1 specification.
 *
 * References:
 * https://www.w3.org/TR/html401/index/elements.html
 * https://www.w3.org/TR/html51/dom.html#elements
 */
goog.provide('goog.dom.TagName');

goog.require('goog.dom.HtmlElement');

/**
 * A tag name for an HTML element.
 *
 * This type is a lie. All instances are actually strings. Do not implement it.
 *
 * It exists because we need an object type to host the template type parameter,
 * and that's not possible with literal or enum types. It is a record type so
 * that runtime type checks don't try to validate the lie.
 *
 * @template T
 * @record
 */
goog.dom.TagName = class {
  /**
   * Cast a string into the tagname for the associated constructor.
   *
   * @template T
   * @param {string} name
   * @param {function(new:T, ...?)} type
   * @return {!goog.dom.TagName<T>}
   */
  static cast(name, type) {
    return /** @type {?} */ (name);
  }

  /** @suppress {unusedPrivateMembers} */
  constructor() {
    /** @private {null} */
    this.googDomTagName_doNotImplementThisTypeOrElse_;

    /** @private {T} */
    this.ensureTypeScriptRemembersTypeT_;
  }

  /**
   * Appease the compiler that instances are stringafiable for the
   * purpose of being a dictionary key.
   *
   * Never implemented; always backed by `String::toString`.
   *
   * @override
   * @return {string}
   */
  toString() {}
};



/** @const {!goog.dom.TagName<!HTMLAnchorElement>} */
goog.dom.TagName.A = /** @type {?} */ ('A');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.ABBR = /** @type {?} */ ('ABBR');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.ACRONYM = /** @type {?} */ ('ACRONYM');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.ADDRESS = /** @type {?} */ ('ADDRESS');

/** @const {!goog.dom.TagName<!HTMLAppletElement>} */
goog.dom.TagName.APPLET = /** @type {?} */ ('APPLET');

/** @const {!goog.dom.TagName<!HTMLAreaElement>} */
goog.dom.TagName.AREA = /** @type {?} */ ('AREA');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.ARTICLE = /** @type {?} */ ('ARTICLE');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.ASIDE = /** @type {?} */ ('ASIDE');

/** @const {!goog.dom.TagName<!HTMLAudioElement>} */
goog.dom.TagName.AUDIO = /** @type {?} */ ('AUDIO');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.B = /** @type {?} */ ('B');

/** @const {!goog.dom.TagName<!HTMLBaseElement>} */
goog.dom.TagName.BASE = /** @type {?} */ ('BASE');

/** @const {!goog.dom.TagName<!HTMLBaseFontElement>} */
goog.dom.TagName.BASEFONT = /** @type {?} */ ('BASEFONT');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.BDI = /** @type {?} */ ('BDI');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.BDO = /** @type {?} */ ('BDO');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.BIG = /** @type {?} */ ('BIG');

/** @const {!goog.dom.TagName<!HTMLQuoteElement>} */
goog.dom.TagName.BLOCKQUOTE = /** @type {?} */ ('BLOCKQUOTE');

/** @const {!goog.dom.TagName<!HTMLBodyElement>} */
goog.dom.TagName.BODY = /** @type {?} */ ('BODY');

/** @const {!goog.dom.TagName<!HTMLBRElement>} */
goog.dom.TagName.BR = /** @type {?} */ ('BR');

/** @const {!goog.dom.TagName<!HTMLButtonElement>} */
goog.dom.TagName.BUTTON = /** @type {?} */ ('BUTTON');

/** @const {!goog.dom.TagName<!HTMLCanvasElement>} */
goog.dom.TagName.CANVAS = /** @type {?} */ ('CANVAS');

/** @const {!goog.dom.TagName<!HTMLTableCaptionElement>} */
goog.dom.TagName.CAPTION = /** @type {?} */ ('CAPTION');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.CENTER = /** @type {?} */ ('CENTER');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.CITE = /** @type {?} */ ('CITE');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.CODE = /** @type {?} */ ('CODE');

/** @const {!goog.dom.TagName<!HTMLTableColElement>} */
goog.dom.TagName.COL = /** @type {?} */ ('COL');

/** @const {!goog.dom.TagName<!HTMLTableColElement>} */
goog.dom.TagName.COLGROUP = /** @type {?} */ ('COLGROUP');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.COMMAND = /** @type {?} */ ('COMMAND');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.DATA = /** @type {?} */ ('DATA');

/** @const {!goog.dom.TagName<!HTMLDataListElement>} */
goog.dom.TagName.DATALIST = /** @type {?} */ ('DATALIST');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.DD = /** @type {?} */ ('DD');

/** @const {!goog.dom.TagName<!HTMLModElement>} */
goog.dom.TagName.DEL = /** @type {?} */ ('DEL');

/** @const {!goog.dom.TagName<!HTMLDetailsElement>} */
goog.dom.TagName.DETAILS = /** @type {?} */ ('DETAILS');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.DFN = /** @type {?} */ ('DFN');

/** @const {!goog.dom.TagName<!HTMLDialogElement>} */
goog.dom.TagName.DIALOG = /** @type {?} */ ('DIALOG');

/** @const {!goog.dom.TagName<!HTMLDirectoryElement>} */
goog.dom.TagName.DIR = /** @type {?} */ ('DIR');

/** @const {!goog.dom.TagName<!HTMLDivElement>} */
goog.dom.TagName.DIV = /** @type {?} */ ('DIV');

/** @const {!goog.dom.TagName<!HTMLDListElement>} */
goog.dom.TagName.DL = /** @type {?} */ ('DL');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.DT = /** @type {?} */ ('DT');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.EM = /** @type {?} */ ('EM');

/** @const {!goog.dom.TagName<!HTMLEmbedElement>} */
goog.dom.TagName.EMBED = /** @type {?} */ ('EMBED');

/** @const {!goog.dom.TagName<!HTMLFieldSetElement>} */
goog.dom.TagName.FIELDSET = /** @type {?} */ ('FIELDSET');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.FIGCAPTION = /** @type {?} */ ('FIGCAPTION');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.FIGURE = /** @type {?} */ ('FIGURE');

/** @const {!goog.dom.TagName<!HTMLFontElement>} */
goog.dom.TagName.FONT = /** @type {?} */ ('FONT');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.FOOTER = /** @type {?} */ ('FOOTER');

/** @const {!goog.dom.TagName<!HTMLFormElement>} */
goog.dom.TagName.FORM = /** @type {?} */ ('FORM');

/** @const {!goog.dom.TagName<!HTMLFrameElement>} */
goog.dom.TagName.FRAME = /** @type {?} */ ('FRAME');

/** @const {!goog.dom.TagName<!HTMLFrameSetElement>} */
goog.dom.TagName.FRAMESET = /** @type {?} */ ('FRAMESET');

/** @const {!goog.dom.TagName<!HTMLHeadingElement>} */
goog.dom.TagName.H1 = /** @type {?} */ ('H1');

/** @const {!goog.dom.TagName<!HTMLHeadingElement>} */
goog.dom.TagName.H2 = /** @type {?} */ ('H2');

/** @const {!goog.dom.TagName<!HTMLHeadingElement>} */
goog.dom.TagName.H3 = /** @type {?} */ ('H3');

/** @const {!goog.dom.TagName<!HTMLHeadingElement>} */
goog.dom.TagName.H4 = /** @type {?} */ ('H4');

/** @const {!goog.dom.TagName<!HTMLHeadingElement>} */
goog.dom.TagName.H5 = /** @type {?} */ ('H5');

/** @const {!goog.dom.TagName<!HTMLHeadingElement>} */
goog.dom.TagName.H6 = /** @type {?} */ ('H6');

/** @const {!goog.dom.TagName<!HTMLHeadElement>} */
goog.dom.TagName.HEAD = /** @type {?} */ ('HEAD');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.HEADER = /** @type {?} */ ('HEADER');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.HGROUP = /** @type {?} */ ('HGROUP');

/** @const {!goog.dom.TagName<!HTMLHRElement>} */
goog.dom.TagName.HR = /** @type {?} */ ('HR');

/** @const {!goog.dom.TagName<!HTMLHtmlElement>} */
goog.dom.TagName.HTML = /** @type {?} */ ('HTML');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.I = /** @type {?} */ ('I');

/** @const {!goog.dom.TagName<!HTMLIFrameElement>} */
goog.dom.TagName.IFRAME = /** @type {?} */ ('IFRAME');

/** @const {!goog.dom.TagName<!HTMLImageElement>} */
goog.dom.TagName.IMG = /** @type {?} */ ('IMG');

/** @const {!goog.dom.TagName<!HTMLInputElement>} */
goog.dom.TagName.INPUT = /** @type {?} */ ('INPUT');

/** @const {!goog.dom.TagName<!HTMLModElement>} */
goog.dom.TagName.INS = /** @type {?} */ ('INS');

/** @const {!goog.dom.TagName<!HTMLIsIndexElement>} */
goog.dom.TagName.ISINDEX = /** @type {?} */ ('ISINDEX');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.KBD = /** @type {?} */ ('KBD');

// HTMLKeygenElement is deprecated.
/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.KEYGEN = /** @type {?} */ ('KEYGEN');

/** @const {!goog.dom.TagName<!HTMLLabelElement>} */
goog.dom.TagName.LABEL = /** @type {?} */ ('LABEL');

/** @const {!goog.dom.TagName<!HTMLLegendElement>} */
goog.dom.TagName.LEGEND = /** @type {?} */ ('LEGEND');

/** @const {!goog.dom.TagName<!HTMLLIElement>} */
goog.dom.TagName.LI = /** @type {?} */ ('LI');

/** @const {!goog.dom.TagName<!HTMLLinkElement>} */
goog.dom.TagName.LINK = /** @type {?} */ ('LINK');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.MAIN = /** @type {?} */ ('MAIN');

/** @const {!goog.dom.TagName<!HTMLMapElement>} */
goog.dom.TagName.MAP = /** @type {?} */ ('MAP');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.MARK = /** @type {?} */ ('MARK');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.MATH = /** @type {?} */ ('MATH');

/** @const {!goog.dom.TagName<!HTMLMenuElement>} */
goog.dom.TagName.MENU = /** @type {?} */ ('MENU');

/** @const {!goog.dom.TagName<!HTMLMenuItemElement>} */
goog.dom.TagName.MENUITEM = /** @type {?} */ ('MENUITEM');

/** @const {!goog.dom.TagName<!HTMLMetaElement>} */
goog.dom.TagName.META = /** @type {?} */ ('META');

/** @const {!goog.dom.TagName<!HTMLMeterElement>} */
goog.dom.TagName.METER = /** @type {?} */ ('METER');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.NAV = /** @type {?} */ ('NAV');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.NOFRAMES = /** @type {?} */ ('NOFRAMES');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.NOSCRIPT = /** @type {?} */ ('NOSCRIPT');

/** @const {!goog.dom.TagName<!HTMLObjectElement>} */
goog.dom.TagName.OBJECT = /** @type {?} */ ('OBJECT');

/** @const {!goog.dom.TagName<!HTMLOListElement>} */
goog.dom.TagName.OL = /** @type {?} */ ('OL');

/** @const {!goog.dom.TagName<!HTMLOptGroupElement>} */
goog.dom.TagName.OPTGROUP = /** @type {?} */ ('OPTGROUP');

/** @const {!goog.dom.TagName<!HTMLOptionElement>} */
goog.dom.TagName.OPTION = /** @type {?} */ ('OPTION');

/** @const {!goog.dom.TagName<!HTMLOutputElement>} */
goog.dom.TagName.OUTPUT = /** @type {?} */ ('OUTPUT');

/** @const {!goog.dom.TagName<!HTMLParagraphElement>} */
goog.dom.TagName.P = /** @type {?} */ ('P');

/** @const {!goog.dom.TagName<!HTMLParamElement>} */
goog.dom.TagName.PARAM = /** @type {?} */ ('PARAM');

/** @const {!goog.dom.TagName<!HTMLPictureElement>} */
goog.dom.TagName.PICTURE = /** @type {?} */ ('PICTURE');

/** @const {!goog.dom.TagName<!HTMLPreElement>} */
goog.dom.TagName.PRE = /** @type {?} */ ('PRE');

/** @const {!goog.dom.TagName<!HTMLProgressElement>} */
goog.dom.TagName.PROGRESS = /** @type {?} */ ('PROGRESS');

/** @const {!goog.dom.TagName<!HTMLQuoteElement>} */
goog.dom.TagName.Q = /** @type {?} */ ('Q');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.RP = /** @type {?} */ ('RP');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.RT = /** @type {?} */ ('RT');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.RTC = /** @type {?} */ ('RTC');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.RUBY = /** @type {?} */ ('RUBY');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.S = /** @type {?} */ ('S');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.SAMP = /** @type {?} */ ('SAMP');

/** @const {!goog.dom.TagName<!HTMLScriptElement>} */
goog.dom.TagName.SCRIPT = /** @type {?} */ ('SCRIPT');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.SECTION = /** @type {?} */ ('SECTION');

/** @const {!goog.dom.TagName<!HTMLSelectElement>} */
goog.dom.TagName.SELECT = /** @type {?} */ ('SELECT');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.SMALL = /** @type {?} */ ('SMALL');

/** @const {!goog.dom.TagName<!HTMLSourceElement>} */
goog.dom.TagName.SOURCE = /** @type {?} */ ('SOURCE');

/** @const {!goog.dom.TagName<!HTMLSpanElement>} */
goog.dom.TagName.SPAN = /** @type {?} */ ('SPAN');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.STRIKE = /** @type {?} */ ('STRIKE');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.STRONG = /** @type {?} */ ('STRONG');

/** @const {!goog.dom.TagName<!HTMLStyleElement>} */
goog.dom.TagName.STYLE = /** @type {?} */ ('STYLE');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.SUB = /** @type {?} */ ('SUB');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.SUMMARY = /** @type {?} */ ('SUMMARY');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.SUP = /** @type {?} */ ('SUP');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.SVG = /** @type {?} */ ('SVG');

/** @const {!goog.dom.TagName<!HTMLTableElement>} */
goog.dom.TagName.TABLE = /** @type {?} */ ('TABLE');

/** @const {!goog.dom.TagName<!HTMLTableSectionElement>} */
goog.dom.TagName.TBODY = /** @type {?} */ ('TBODY');

/** @const {!goog.dom.TagName<!HTMLTableCellElement>} */
goog.dom.TagName.TD = /** @type {?} */ ('TD');

/** @const {!goog.dom.TagName<!HTMLTemplateElement>} */
goog.dom.TagName.TEMPLATE = /** @type {?} */ ('TEMPLATE');

/** @const {!goog.dom.TagName<!HTMLTextAreaElement>} */
goog.dom.TagName.TEXTAREA = /** @type {?} */ ('TEXTAREA');

/** @const {!goog.dom.TagName<!HTMLTableSectionElement>} */
goog.dom.TagName.TFOOT = /** @type {?} */ ('TFOOT');

/** @const {!goog.dom.TagName<!HTMLTableCellElement>} */
goog.dom.TagName.TH = /** @type {?} */ ('TH');

/** @const {!goog.dom.TagName<!HTMLTableSectionElement>} */
goog.dom.TagName.THEAD = /** @type {?} */ ('THEAD');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.TIME = /** @type {?} */ ('TIME');

/** @const {!goog.dom.TagName<!HTMLTitleElement>} */
goog.dom.TagName.TITLE = /** @type {?} */ ('TITLE');

/** @const {!goog.dom.TagName<!HTMLTableRowElement>} */
goog.dom.TagName.TR = /** @type {?} */ ('TR');

/** @const {!goog.dom.TagName<!HTMLTrackElement>} */
goog.dom.TagName.TRACK = /** @type {?} */ ('TRACK');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.TT = /** @type {?} */ ('TT');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.U = /** @type {?} */ ('U');

/** @const {!goog.dom.TagName<!HTMLUListElement>} */
goog.dom.TagName.UL = /** @type {?} */ ('UL');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.VAR = /** @type {?} */ ('VAR');

/** @const {!goog.dom.TagName<!HTMLVideoElement>} */
goog.dom.TagName.VIDEO = /** @type {?} */ ('VIDEO');

/** @const {!goog.dom.TagName<!goog.dom.HtmlElement>} */
goog.dom.TagName.WBR = /** @type {?} */ ('WBR');

//third_party/javascript/closure/object/object.js
goog.loadModule(function(exports) {'use strict';/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Utilities for manipulating objects/maps/hashes.
 */
goog.module('goog.object');
goog.module.declareLegacyNamespace();

/**
 * Calls a function for each element in an object/map/hash.
 * @param {?Object<K,V>} obj The object over which to iterate.
 * @param {function(this:T,V,?,?Object<K,V>):?} f The function to call for every
 *     element. This function takes 3 arguments (the value, the key and the
 *     object) and the return value is ignored.
 * @param {T=} opt_obj This is used as the 'this' object within f.
 * @return {void}
 * @template T,K,V
 */
function forEach(obj, f, opt_obj) {
  for (const key in obj) {
    f.call(/** @type {?} */ (opt_obj), obj[key], key, obj);
  }
}

/**
 * Calls a function for each element in an object/map/hash. If that call returns
 * true, adds the element to a new object.
 * @param {?Object<K,V>} obj The object over which to iterate.
 * @param {function(this:T,V,?,?Object<K,V>):boolean} f The function to call for
 *     every element. This function takes 3 arguments (the value, the key and
 *     the object) and should return a boolean. If the return value is true the
 *     element is added to the result object. If it is false the element is not
 *     included.
 * @param {T=} opt_obj This is used as the 'this' object within f.
 * @return {!Object<K,V>} a new object in which only elements that passed the
 *     test are present.
 * @template T,K,V
 */
function filter(obj, f, opt_obj) {
  const res = {};
  for (const key in obj) {
    if (f.call(/** @type {?} */ (opt_obj), obj[key], key, obj)) {
      res[key] = obj[key];
    }
  }
  return res;
}

/**
 * For every element in an object/map/hash calls a function and inserts the
 * result into a new object.
 * @param {?Object<K,V>} obj The object over which to iterate.
 * @param {function(this:T,V,?,?Object<K,V>):R} f The function to call for every
 *     element. This function takes 3 arguments (the value, the key and the
 *     object) and should return something. The result will be inserted into a
 *     new object.
 * @param {T=} opt_obj This is used as the 'this' object within f.
 * @return {!Object<K,R>} a new object with the results from f.
 * @template T,K,V,R
 */
function map(obj, f, opt_obj) {
  const res = {};
  for (const key in obj) {
    res[key] = f.call(/** @type {?} */ (opt_obj), obj[key], key, obj);
  }
  return res;
}

/**
 * Calls a function for each element in an object/map/hash. If any
 * call returns true, returns true (without checking the rest). If
 * all calls return false, returns false.
 * @param {?Object<K,V>} obj The object to check.
 * @param {function(this:T,V,?,?Object<K,V>):boolean} f The function to call for
 *     every element. This function takes 3 arguments (the value, the key and
 *     the object) and should return a boolean.
 * @param {T=} opt_obj This is used as the 'this' object within f.
 * @return {boolean} true if any element passes the test.
 * @template T,K,V
 */
function some(obj, f, opt_obj) {
  for (const key in obj) {
    if (f.call(/** @type {?} */ (opt_obj), obj[key], key, obj)) {
      return true;
    }
  }
  return false;
}

/**
 * Calls a function for each element in an object/map/hash. If
 * all calls return true, returns true. If any call returns false, returns
 * false at this point and does not continue to check the remaining elements.
 * @param {?Object<K,V>} obj The object to check.
 * @param {?function(this:T,V,?,?Object<K,V>):boolean} f The function to call
 *     for every element. This function takes 3 arguments (the value, the key
 *     and the object) and should return a boolean.
 * @param {T=} opt_obj This is used as the 'this' object within f.
 * @return {boolean} false if any element fails the test.
 * @template T,K,V
 */
function every(obj, f, opt_obj) {
  for (const key in obj) {
    if (!f.call(/** @type {?} */ (opt_obj), obj[key], key, obj)) {
      return false;
    }
  }
  return true;
}

/**
 * Returns the number of key-value pairs in the object map.
 * @param {?Object} obj The object for which to get the number of key-value
 *     pairs.
 * @return {number} The number of key-value pairs in the object map.
 */
function getCount(obj) {
  let rv = 0;
  for (const key in obj) {
    rv++;
  }
  return rv;
}

/**
 * Returns one key from the object map, if any exists.
 * For map literals the returned key will be the first one in most of the
 * browsers (a know exception is Konqueror).
 * @param {?Object} obj The object to pick a key from.
 * @return {string|undefined} The key or undefined if the object is empty.
 */
function getAnyKey(obj) {
  for (const key in obj) {
    return key;
  }
}

/**
 * Returns one value from the object map, if any exists.
 * For map literals the returned value will be the first one in most of the
 * browsers (a know exception is Konqueror).
 * @param {?Object<K,V>} obj The object to pick a value from.
 * @return {V|undefined} The value or undefined if the object is empty.
 * @template K,V
 */
function getAnyValue(obj) {
  for (const key in obj) {
    return obj[key];
  }
}

/**
 * Whether the object/hash/map contains the given object as a value.
 * An alias for containsValue(obj, val).
 * @param {?Object<K,V>} obj The object in which to look for val.
 * @param {V} val The object for which to check.
 * @return {boolean} true if val is present.
 * @template K,V
 */
function contains(obj, val) {
  return containsValue(obj, val);
}

/**
 * Returns the values of the object/map/hash.
 * @param {?Object<K,V>} obj The object from which to get the values.
 * @return {!Array<V>} The values in the object/map/hash.
 * @template K,V
 */
function getValues(obj) {
  const res = [];
  let i = 0;
  for (const key in obj) {
    res[i++] = obj[key];
  }
  return res;
}

/**
 * Returns the keys of the object/map/hash.
 * @param {?Object} obj The object from which to get the keys.
 * @return {!Array<string>} Array of property keys.
 */
function getKeys(obj) {
  const res = [];
  let i = 0;
  for (const key in obj) {
    res[i++] = key;
  }
  return res;
}

/**
 * Get a value from an object multiple levels deep.  This is useful for
 * pulling values from deeply nested objects, such as JSON responses.
 * Example usage: getValueByKeys(jsonObj, 'foo', 'entries', 3)
 * @param {?Object} obj An object to get the value from. Can be array-like.
 * @param {...(string|number|!IArrayLike<number|string>)} var_args A number of
 *     keys (as strings, or numbers, for array-like objects). Can also be
 *     specified as a single array of keys.
 * @return {*} The resulting value. If, at any point, the value for a key in the
 *     current object is null or undefined, returns undefined.
 */
function getValueByKeys(obj, var_args) {
  const isArrayLike = goog.isArrayLike(var_args);
  const keys = isArrayLike ?
      /** @type {!IArrayLike<number|string>} */ (var_args) :
      arguments;

  // Start with the 2nd parameter for the variable parameters syntax.
  for (let i = isArrayLike ? 0 : 1; i < keys.length; i++) {
    if (obj == null) return undefined;
    obj = obj[keys[i]];
  }

  return obj;
}

/**
 * Whether the object/map/hash contains the given key.
 * @param {?Object} obj The object in which to look for key.
 * @param {?} key The key for which to check.
 * @return {boolean} true If the map contains the key.
 */
function containsKey(obj, key) {
  return obj !== null && key in obj;
}

/**
 * Whether the object/map/hash contains the given value. This is O(n).
 * @param {?Object<K,V>} obj The object in which to look for val.
 * @param {V} val The value for which to check.
 * @return {boolean} true If the map contains the value.
 * @template K,V
 */
function containsValue(obj, val) {
  for (const key in obj) {
    if (obj[key] == val) {
      return true;
    }
  }
  return false;
}

/**
 * Searches an object for an element that satisfies the given condition and
 * returns its key.
 * @param {?Object<K,V>} obj The object to search in.
 * @param {function(this:T,V,string,?Object<K,V>):boolean} f The function to
 *     call for every element. Takes 3 arguments (the value, the key and the
 *     object) and should return a boolean.
 * @param {T=} thisObj An optional "this" context for the function.
 * @return {string|undefined} The key of an element for which the function
 *     returns true or undefined if no such element is found.
 * @template T,K,V
 */
function findKey(obj, f, thisObj = undefined) {
  for (const key in obj) {
    if (f.call(/** @type {?} */ (thisObj), obj[key], key, obj)) {
      return key;
    }
  }
  return undefined;
}

/**
 * Searches an object for an element that satisfies the given condition and
 * returns its value.
 * @param {?Object<K,V>} obj The object to search in.
 * @param {function(this:T,V,string,?Object<K,V>):boolean} f The function to
 *     call for every element. Takes 3 arguments (the value, the key and the
 *     object) and should return a boolean.
 * @param {T=} thisObj An optional "this" context for the function.
 * @return {V} The value of an element for which the function returns true or
 *     undefined if no such element is found.
 * @template T,K,V
 */
function findValue(obj, f, thisObj = undefined) {
  const key = findKey(obj, f, thisObj);
  return key && obj[key];
}

/**
 * Whether the object/map/hash is empty.
 * @param {?Object} obj The object to test.
 * @return {boolean} true if obj is empty.
 */
function isEmpty(obj) {
  for (const key in obj) {
    return false;
  }
  return true;
}

/**
 * Removes all key value pairs from the object/map/hash.
 * @param {?Object} obj The object to clear.
 * @return {void}
 */
function clear(obj) {
  for (const i in obj) {
    delete obj[i];
  }
}

/**
 * Removes a key-value pair based on the key.
 * @param {?Object} obj The object from which to remove the key.
 * @param {?} key The key to remove.
 * @return {boolean} Whether an element was removed.
 */
function remove(obj, key) {
  let rv;
  if (rv = key in /** @type {!Object} */ (obj)) {
    delete obj[key];
  }
  return rv;
}

/**
 * Adds a key-value pair to the object. Throws an exception if the key is
 * already in use. Use set if you want to change an existing pair.
 * @param {?Object<K,V>} obj The object to which to add the key-value pair.
 * @param {string} key The key to add.
 * @param {V} val The value to add.
 * @return {void}
 * @template K,V
 */
function add(obj, key, val) {
  if (obj !== null && key in obj) {
    throw new Error(`The object already contains the key "${key}"`);
  }
  set(obj, key, val);
}

/**
 * Returns the value for the given key.
 * @param {?Object<K,V>} obj The object from which to get the value.
 * @param {string} key The key for which to get the value.
 * @param {R=} val The value to return if no item is found for the given key
 *     (default is undefined).
 * @return {V|R|undefined} The value for the given key.
 * @template K,V,R
 */
function get(obj, key, val = undefined) {
  if (obj !== null && key in obj) {
    return obj[key];
  }
  return val;
}

/**
 * Adds a key-value pair to the object/map/hash.
 * @param {?Object<K,V>} obj The object to which to add the key-value pair.
 * @param {string} key The key to add.
 * @param {V} value The value to add.
 * @template K,V
 * @return {void}
 */
function set(obj, key, value) {
  obj[key] = value;
}

/**
 * Adds a key-value pair to the object/map/hash if it doesn't exist yet.
 * @param {?Object<K,V>} obj The object to which to add the key-value pair.
 * @param {string} key The key to add.
 * @param {V} value The value to add if the key wasn't present.
 * @return {V} The value of the entry at the end of the function.
 * @template K,V
 */
function setIfUndefined(obj, key, value) {
  return key in /** @type {!Object} */ (obj) ? obj[key] : (obj[key] = value);
}

/**
 * Sets a key and value to an object if the key is not set. The value will be
 * the return value of the given function. If the key already exists, the
 * object will not be changed and the function will not be called (the function
 * will be lazily evaluated -- only called if necessary).
 * This function is particularly useful when used with an `Object` which is
 * acting as a cache.
 * @param {?Object<K,V>} obj The object to which to add the key-value pair.
 * @param {string} key The key to add.
 * @param {function():V} f The value to add if the key wasn't present.
 * @return {V} The value of the entry at the end of the function.
 * @template K,V
 */
function setWithReturnValueIfNotSet(obj, key, f) {
  if (key in obj) {
    return obj[key];
  }

  const val = f();
  obj[key] = val;
  return val;
}

/**
 * Compares two objects for equality using === on the values.
 * @param {!Object<K,V>} a
 * @param {!Object<K,V>} b
 * @return {boolean}
 * @template K,V
 */
function equals(a, b) {
  for (const k in a) {
    if (!(k in b) || a[k] !== b[k]) {
      return false;
    }
  }
  for (const k in b) {
    if (!(k in a)) {
      return false;
    }
  }
  return true;
}

/**
 * Returns a shallow clone of the object.
 * @param {?Object<K,V>} obj Object to clone.
 * @return {!Object<K,V>} Clone of the input object.
 * @template K,V
 */
function clone(obj) {
  const res = {};
  for (const key in obj) {
    res[key] = obj[key];
  }
  return res;
}

/**
 * Clones a value. The input may be an Object, Array, or basic type. Objects and
 * arrays will be cloned recursively.
 * WARNINGS:
 * <code>unsafeClone</code> does not detect reference loops. Objects
 * that refer to themselves will cause infinite recursion.
 * <code>unsafeClone</code> is unaware of unique identifiers, and
 * copies UIDs created by <code>getUid</code> into cloned results.
 * @param {T} obj The value to clone.
 * @return {T} A clone of the input value.
 * @template T
 */
function unsafeClone(obj) {
  if (!obj || typeof obj !== 'object') return obj;
  if (typeof obj.clone === 'function') return obj.clone();
  if (typeof Map !== 'undefined' && obj instanceof Map) {
    return new Map(obj);
  } else if (typeof Set !== 'undefined' && obj instanceof Set) {
    return new Set(obj);
  }
  const clone = Array.isArray(obj) ? [] :
      typeof ArrayBuffer === 'function' &&
          typeof ArrayBuffer.isView === 'function' && ArrayBuffer.isView(obj) &&
          !(obj instanceof DataView) ?
                                     new obj.constructor(obj.length) :
                                     {};
  for (const key in obj) {
    clone[key] = unsafeClone(obj[key]);
  }
  return clone;
}

/**
 * Returns a new object in which all the keys and values are interchanged
 * (keys become values and values become keys). If multiple keys map to the
 * same value, the chosen transposed value is implementation-dependent.
 * @param {?Object} obj The object to transpose.
 * @return {!Object} The transposed object.
 */
function transpose(obj) {
  const transposed = {};
  for (const key in obj) {
    transposed[obj[key]] = key;
  }
  return transposed;
}

/**
 * The names of the fields that are defined on Object.prototype.
 * @type {!Array<string>}
 */
const PROTOTYPE_FIELDS = [
  'constructor',
  'hasOwnProperty',
  'isPrototypeOf',
  'propertyIsEnumerable',
  'toLocaleString',
  'toString',
  'valueOf',
];

/**
 * Extends an object with another object.
 * This operates 'in-place'; it does not create a new Object.
 * Example:
 * var o = {};
 * extend(o, {a: 0, b: 1});
 * o; // {a: 0, b: 1}
 * extend(o, {b: 2, c: 3});
 * o; // {a: 0, b: 2, c: 3}
 * @param {?Object} target The object to modify. Existing properties will be
 *     overwritten if they are also present in one of the objects in `var_args`.
 * @param {...(?Object|undefined)} var_args The objects from which values
 *     will be copied.
 * @return {void}
 * @deprecated Prefer Object.assign
 */
function extend(target, var_args) {
  let key;
  let source;
  for (let i = 1; i < arguments.length; i++) {
    source = arguments[i];
    for (key in source) {
      target[key] = source[key];
    }

    // For IE the for-in-loop does not contain any properties that are not
    // enumerable on the prototype object (for example isPrototypeOf from
    // Object.prototype) and it will also not include 'replace' on objects that
    // extend String and change 'replace' (not that it is common for anyone to
    // extend anything except Object).

    for (let j = 0; j < PROTOTYPE_FIELDS.length; j++) {
      key = PROTOTYPE_FIELDS[j];
      if (Object.prototype.hasOwnProperty.call(source, key)) {
        target[key] = source[key];
      }
    }
  }
}

/**
 * Creates a new object built from the key-value pairs provided as arguments.
 * @param {...*} var_args If only one argument is provided and it is an array
 *     then this is used as the arguments, otherwise even arguments are used as
 *     the property names and odd arguments are used as the property values.
 * @return {!Object} The new object.
 * @throws {!Error} If there are uneven number of arguments or there is only one
 *     non array argument.
 */
function create(var_args) {
  const argLength = arguments.length;
  if (argLength == 1 && Array.isArray(arguments[0])) {
    return create.apply(null, arguments[0]);
  }

  if (argLength % 2) {
    throw new Error('Uneven number of arguments');
  }

  const rv = {};
  for (let i = 0; i < argLength; i += 2) {
    rv[arguments[i]] = arguments[i + 1];
  }
  return rv;
}

/**
 * Creates a new object where the property names come from the arguments but
 * the value is always set to true
 * @param {...*} var_args If only one argument is provided and it is an array
 *     then this is used as the arguments, otherwise the arguments are used as
 *     the property names.
 * @return {!Object} The new object.
 */
function createSet(var_args) {
  const argLength = arguments.length;
  if (argLength == 1 && Array.isArray(arguments[0])) {
    return createSet.apply(null, arguments[0]);
  }

  const rv = {};
  for (let i = 0; i < argLength; i++) {
    rv[arguments[i]] = true;
  }
  return rv;
}

/**
 * Creates an immutable view of the underlying object, if the browser
 * supports immutable objects.
 * In default mode, writes to this view will fail silently. In strict mode,
 * they will throw an error.
 * @param {!Object<K,V>} obj An object.
 * @return {!Object<K,V>} An immutable view of that object, or the original
 *     object if this browser does not support immutables.
 * @template K,V
 */
function createImmutableView(obj) {
  let result = obj;
  if (Object.isFrozen && !Object.isFrozen(obj)) {
    result = Object.create(obj);
    Object.freeze(result);
  }
  return result;
}

/**
 * @param {!Object} obj An object.
 * @return {boolean} Whether this is an immutable view of the object.
 */
function isImmutableView(obj) {
  return !!Object.isFrozen && Object.isFrozen(obj);
}

/**
 * Get all properties names on a given Object regardless of enumerability.
 * <p> If the browser does not support `Object.getOwnPropertyNames` nor
 * `Object.getPrototypeOf` then this is equivalent to using
 * `getKeys`
 * @param {?Object} obj The object to get the properties of.
 * @param {boolean=} includeObjectPrototype Whether properties defined on
 *     `Object.prototype` should be included in the result.
 * @param {boolean=} includeFunctionPrototype Whether properties defined on
 *     `Function.prototype` should be included in the result.
 * @return {!Array<string>}
 * @public
 */
function getAllPropertyNames(
    obj, includeObjectPrototype = undefined,
    includeFunctionPrototype = undefined) {
  if (!obj) {
    return [];
  }

  // Naively use a for..in loop to get the property names if the browser doesn't
  // support any other APIs for getting it.
  if (!Object.getOwnPropertyNames || !Object.getPrototypeOf) {
    return getKeys(obj);
  }

  const visitedSet = {};

  // Traverse the prototype chain and add all properties to the visited set.
  let proto = obj;
  while (proto && (proto !== Object.prototype || !!includeObjectPrototype) &&
         (proto !== Function.prototype || !!includeFunctionPrototype)) {
    const names = Object.getOwnPropertyNames(proto);
    for (let i = 0; i < names.length; i++) {
      visitedSet[names[i]] = true;
    }
    proto = Object.getPrototypeOf(proto);
  }

  return getKeys(visitedSet);
}

/**
 * Given a ES5 or ES6 class reference, return its super class / super
 * constructor.
 * This should be used in rare cases where you need to walk up the inheritance
 * tree (this is generally a bad idea). But this work with ES5 and ES6 classes,
 * unlike relying on the superClass_ property.
 * Note: To start walking up the hierarchy from an instance call this with its
 * `constructor` property; e.g. `getSuperClass(instance.constructor)`.
 * @param {function(new: ?)} constructor
 * @return {?Object}
 */
function getSuperClass(constructor) {
  const proto = Object.getPrototypeOf(constructor.prototype);
  return proto && proto.constructor;
}

exports = {
  add,
  clear,
  clone,
  contains,
  containsKey,
  containsValue,
  create,
  createImmutableView,
  createSet,
  equals,
  every,
  extend,
  filter,
  findKey,
  findValue,
  forEach,
  get,
  getAllPropertyNames,
  getAnyKey,
  getAnyValue,
  getCount,
  getKeys,
  getSuperClass,
  getValueByKeys,
  getValues,
  isEmpty,
  isImmutableView,
  map,
  remove,
  set,
  setIfUndefined,
  setWithReturnValueIfNotSet,
  some,
  transpose,
  unsafeClone,
};

;return exports;});

//third_party/javascript/closure/dom/tags.js
/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Utilities for HTML element tag names.
 */
goog.provide('goog.dom.tags');

goog.require('goog.object');


/**
 * The void elements specified by
 * http://www.w3.org/TR/html-markup/syntax.html#void-elements.
 * @const @private {!Object<string, boolean>}
 */
goog.dom.tags.VOID_TAGS_ = goog.object.createSet(
    'area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input',
    'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr');


/**
 * Checks whether the tag is void (with no contents allowed and no legal end
 * tag), for example 'br'.
 * @param {string} tagName The tag name in lower case.
 * @return {boolean}
 */
goog.dom.tags.isVoidTag = function(tagName) {
  'use strict';
  return goog.dom.tags.VOID_TAGS_[tagName] === true;
};

//third_party/javascript/closure/html/trustedtypes.js
/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Policy to convert strings to Trusted Types. See
 * https://github.com/WICG/trusted-types for details.
 */

goog.provide('goog.html.trustedtypes');


/**
 * Cached result of goog.createTrustedTypesPolicy.
 * @type {?TrustedTypePolicy|undefined}
 * @private
 */
goog.html.trustedtypes.cachedPolicy_;


/**
 * Creates a (singleton) Trusted Type Policy for Safe HTML Types.
 * @return {?TrustedTypePolicy}
 * @package
 */
goog.html.trustedtypes.getPolicyPrivateDoNotAccessOrElse = function() {
  'use strict';
  if (!goog.TRUSTED_TYPES_POLICY_NAME) {
    // Binary not configured for Trusted Types.
    return null;
  }

  if (goog.html.trustedtypes.cachedPolicy_ === undefined) {
    goog.html.trustedtypes.cachedPolicy_ =
        goog.createTrustedTypesPolicy(goog.TRUSTED_TYPES_POLICY_NAME + '#html');
  }

  return goog.html.trustedtypes.cachedPolicy_;
};

//third_party/javascript/closure/string/typedstring.js
/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

goog.provide('goog.string.TypedString');



/**
 * Wrapper for strings that conform to a data type or language.
 *
 * Implementations of this interface are wrappers for strings, and typically
 * associate a type contract with the wrapped string.  Concrete implementations
 * of this interface may choose to implement additional run-time type checking,
 * see for example `goog.html.SafeHtml`. If available, client code that
 * needs to ensure type membership of an object should use the type's function
 * to assert type membership, such as `goog.html.SafeHtml.unwrap`.
 * @interface
 */
goog.string.TypedString = function() {};


/**
 * Interface marker of the TypedString interface.
 *
 * This property can be used to determine at runtime whether or not an object
 * implements this interface.  All implementations of this interface set this
 * property to `true`.
 * @type {boolean}
 */
goog.string.TypedString.prototype.implementsGoogStringTypedString;


/**
 * Retrieves this wrapped string's value.
 * @return {string} The wrapped string's value.
 */
goog.string.TypedString.prototype.getTypedStringValue;

//third_party/javascript/closure/string/const.js
/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

goog.provide('goog.string.Const');

goog.require('goog.asserts');
goog.require('goog.string.TypedString');



/**
 * Wrapper for compile-time-constant strings.
 *
 * Const is a wrapper for strings that can only be created from program
 * constants (i.e., string literals).  This property relies on a custom Closure
 * compiler check that `goog.string.Const.from` is only invoked on
 * compile-time-constant expressions.
 *
 * Const is useful in APIs whose correct and secure use requires that certain
 * arguments are not attacker controlled: Compile-time constants are inherently
 * under the control of the application and not under control of external
 * attackers, and hence are safe to use in such contexts.
 *
 * Instances of this type must be created via its factory method
 * `goog.string.Const.from` and not by invoking its constructor.  The
 * constructor intentionally takes no parameters and the type is immutable;
 * hence only a default instance corresponding to the empty string can be
 * obtained via constructor invocation.  Use goog.string.Const.EMPTY
 * instead of using this constructor to get an empty Const string.
 *
 * @see goog.string.Const#from
 * @constructor
 * @final
 * @struct
 * @implements {goog.string.TypedString}
 * @param {Object=} opt_token package-internal implementation detail.
 * @param {string=} opt_content package-internal implementation detail.
 */
goog.string.Const = function(opt_token, opt_content) {
  'use strict';
  /**
   * The wrapped value of this Const object.  The field has a purposely ugly
   * name to make (non-compiled) code that attempts to directly access this
   * field stand out.
   * @private {string}
   */
  this.stringConstValueWithSecurityContract__googStringSecurityPrivate_ =
      ((opt_token ===
        goog.string.Const.GOOG_STRING_CONSTRUCTOR_TOKEN_PRIVATE_) &&
       opt_content) ||
      '';

  /**
   * A type marker used to implement additional run-time type checking.
   * @see goog.string.Const#unwrap
   * @const {!Object}
   * @private
   */
  this.STRING_CONST_TYPE_MARKER__GOOG_STRING_SECURITY_PRIVATE_ =
      goog.string.Const.TYPE_MARKER_;
};


/**
 * @override
 * @const
 */
goog.string.Const.prototype.implementsGoogStringTypedString = true;


/**
 * Returns this Const's value as a string.
 *
 * IMPORTANT: In code where it is security-relevant that an object's type is
 * indeed `goog.string.Const`, use `goog.string.Const.unwrap`
 * instead of this method.
 *
 * @see goog.string.Const#unwrap
 * @override
 * @return {string}
 */
goog.string.Const.prototype.getTypedStringValue = function() {
  'use strict';
  return this.stringConstValueWithSecurityContract__googStringSecurityPrivate_;
};


if (goog.DEBUG) {
  /**
   * Returns a debug-string representation of this value.
   *
   * To obtain the actual string value wrapped inside an object of this type,
   * use `goog.string.Const.unwrap`.
   *
   * @see goog.string.Const#unwrap
   * @override
   * @return {string}
   */
  goog.string.Const.prototype.toString = function() {
    'use strict';
    return 'Const{' +
        this.stringConstValueWithSecurityContract__googStringSecurityPrivate_ +
        '}';
  };
}


/**
 * Performs a runtime check that the provided object is indeed an instance
 * of `goog.string.Const`, and returns its value.
 * @param {!goog.string.Const} stringConst The object to extract from.
 * @return {string} The Const object's contained string, unless the run-time
 *     type check fails. In that case, `unwrap` returns an innocuous
 *     string, or, if assertions are enabled, throws
 *     `goog.asserts.AssertionError`.
 */
goog.string.Const.unwrap = function(stringConst) {
  'use strict';
  // Perform additional run-time type-checking to ensure that stringConst is
  // indeed an instance of the expected type.  This provides some additional
  // protection against security bugs due to application code that disables type
  // checks.
  if (stringConst instanceof goog.string.Const &&
      stringConst.constructor === goog.string.Const &&
      stringConst.STRING_CONST_TYPE_MARKER__GOOG_STRING_SECURITY_PRIVATE_ ===
          goog.string.Const.TYPE_MARKER_) {
    return stringConst
        .stringConstValueWithSecurityContract__googStringSecurityPrivate_;
  } else {
    goog.asserts.fail(
        'expected object of type Const, got \'' + stringConst + '\'');
    return 'type_error:Const';
  }
};


/**
 * Creates a Const object from a compile-time constant string.
 *
 * It is illegal to invoke this function on an expression whose
 * compile-time-constant value cannot be determined by the Closure compiler.
 *
 * Correct invocations include,
 * <pre>
 *   var s = goog.string.Const.from('hello');
 *   var t = goog.string.Const.from('hello' + 'world');
 * </pre>
 *
 * In contrast, the following are illegal:
 * <pre>
 *   var s = goog.string.Const.from(getHello());
 *   var t = goog.string.Const.from('hello' + world);
 * </pre>
 *
 * @param {string} s A constant string from which to create a Const.
 * @return {!goog.string.Const} A Const object initialized to stringConst.
 */
goog.string.Const.from = function(s) {
  'use strict';
  return new goog.string.Const(
      goog.string.Const.GOOG_STRING_CONSTRUCTOR_TOKEN_PRIVATE_, s);
};

/**
 * Type marker for the Const type, used to implement additional run-time
 * type checking.
 * @const {!Object}
 * @private
 */
goog.string.Const.TYPE_MARKER_ = {};

/**
 * @type {!Object}
 * @private
 * @const
 */
goog.string.Const.GOOG_STRING_CONSTRUCTOR_TOKEN_PRIVATE_ = {};

/**
 * A Const instance wrapping the empty string.
 * @const {!goog.string.Const}
 */
goog.string.Const.EMPTY = goog.string.Const.from('');

//third_party/javascript/closure/html/safescript.js
goog.loadModule(function(exports) {'use strict';/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview The SafeScript type and its builders.
 *
 * TODO(xtof): Link to document stating type contract.
 */

goog.module('goog.html.SafeScript');
goog.module.declareLegacyNamespace();

const Const = goog.require('goog.string.Const');
const TypedString = goog.require('goog.string.TypedString');
const trustedtypes = goog.require('goog.html.trustedtypes');
const {fail} = goog.require('goog.asserts');

/**
 * Token used to ensure that object is created only from this file. No code
 * outside of this file can access this token.
 * @const {!Object}
 */
const CONSTRUCTOR_TOKEN_PRIVATE = {};

/**
 * A string-like object which represents JavaScript code and that carries the
 * security type contract that its value, as a string, will not cause execution
 * of unconstrained attacker controlled code (XSS) when evaluated as JavaScript
 * in a browser.
 *
 * Instances of this type must be created via the factory method
 * `SafeScript.fromConstant` and not by invoking its constructor. The
 * constructor intentionally takes an extra parameter that cannot be constructed
 * outside of this file and the type is immutable; hence only a default instance
 * corresponding to the empty string can be obtained via constructor invocation.
 *
 * A SafeScript's string representation can safely be interpolated as the
 * content of a script element within HTML. The SafeScript string should not be
 * escaped before interpolation.
 *
 * Note that the SafeScript might contain text that is attacker-controlled but
 * that text should have been interpolated with appropriate escaping,
 * sanitization and/or validation into the right location in the script, such
 * that it is highly constrained in its effect (for example, it had to match a
 * set of whitelisted words).
 *
 * A SafeScript can be constructed via security-reviewed unchecked
 * conversions. In this case producers of SafeScript must ensure themselves that
 * the SafeScript does not contain unsafe script. Note in particular that
 * `&lt;` is dangerous, even when inside JavaScript strings, and so should
 * always be forbidden or JavaScript escaped in user controlled input. For
 * example, if `&lt;/script&gt;&lt;script&gt;evil&lt;/script&gt;"` were
 * interpolated inside a JavaScript string, it would break out of the context
 * of the original script element and `evil` would execute. Also note
 * that within an HTML script (raw text) element, HTML character references,
 * such as "&lt;" are not allowed. See
 * http://www.w3.org/TR/html5/scripting-1.html#restrictions-for-contents-of-script-elements.
 * Creating SafeScript objects HAS SIDE-EFFECTS due to calling Trusted Types Web
 * API.
 *
 * @see SafeScript#fromConstant
 * @final
 * @implements {TypedString}
 */
class SafeScript {
  /**
   * @param {!TrustedScript|string} value
   * @param {!Object} token package-internal implementation detail.
   */
  constructor(value, token) {
    /**
     * The contained value of this SafeScript.  The field has a purposely ugly
     * name to make (non-compiled) code that attempts to directly access this
     * field stand out.
     * @private {!TrustedScript|string}
     */
    this.privateDoNotAccessOrElseSafeScriptWrappedValue_ =
        (token === CONSTRUCTOR_TOKEN_PRIVATE) ? value : '';

    /**
     * @override
     * @const
     */
    this.implementsGoogStringTypedString = true;
  }

  /**
   * Creates a SafeScript object from a compile-time constant string.
   *
   * @param {!Const} script A compile-time-constant string from which to create
   *     a SafeScript.
   * @return {!SafeScript} A SafeScript object initialized to `script`.
   */
  static fromConstant(script) {
    const scriptString = Const.unwrap(script);
    if (scriptString.length === 0) {
      return SafeScript.EMPTY;
    }
    return SafeScript.createSafeScriptSecurityPrivateDoNotAccessOrElse(
        scriptString);
  }

  /**
   * Creates a SafeScript JSON representation from anything that could be passed
   * to JSON.stringify.
   * @param {*} val
   * @return {!SafeScript}
   */
  static fromJson(val) {
    return SafeScript.createSafeScriptSecurityPrivateDoNotAccessOrElse(
        SafeScript.stringify_(val));
  }

  /**
   * Returns this SafeScript's value as a string.
   *
   * IMPORTANT: In code where it is security relevant that an object's type is
   * indeed `SafeScript`, use `SafeScript.unwrap` instead of
   * this method. If in doubt, assume that it's security relevant. In
   * particular, note that goog.html functions which return a goog.html type do
   * not guarantee the returned instance is of the right type. For example:
   *
   * <pre>
   * var fakeSafeHtml = new String('fake');
   * fakeSafeHtml.__proto__ = goog.html.SafeHtml.prototype;
   * var newSafeHtml = goog.html.SafeHtml.htmlEscape(fakeSafeHtml);
   * // newSafeHtml is just an alias for fakeSafeHtml, it's passed through by
   * // goog.html.SafeHtml.htmlEscape() as fakeSafeHtml
   * // instanceof goog.html.SafeHtml.
   * </pre>
   *
   * @see SafeScript#unwrap
   * @override
   */
  getTypedStringValue() {
    return this.privateDoNotAccessOrElseSafeScriptWrappedValue_.toString();
  }

  /**
   * Performs a runtime check that the provided object is indeed a
   * SafeScript object, and returns its value.
   *
   * @param {!SafeScript} safeScript The object to extract from.
   * @return {string} The safeScript object's contained string, unless
   *     the run-time type check fails. In that case, `unwrap` returns an
   *     innocuous string, or, if assertions are enabled, throws
   *     `asserts.AssertionError`.
   */
  static unwrap(safeScript) {
    return SafeScript.unwrapTrustedScript(safeScript).toString();
  }

  /**
   * Unwraps value as TrustedScript if supported or as a string if not.
   * @param {!SafeScript} safeScript
   * @return {!TrustedScript|string}
   * @see SafeScript.unwrap
   */
  static unwrapTrustedScript(safeScript) {
    // Perform additional Run-time type-checking to ensure that
    // safeScript is indeed an instance of the expected type.  This
    // provides some additional protection against security bugs due to
    // application code that disables type checks.
    // Specifically, the following checks are performed:
    // 1. The object is an instance of the expected type.
    // 2. The object is not an instance of a subclass.
    if (safeScript instanceof SafeScript &&
        safeScript.constructor === SafeScript) {
      return safeScript.privateDoNotAccessOrElseSafeScriptWrappedValue_;
    } else {
      fail(
          'expected object of type SafeScript, got \'' + safeScript +
          '\' of type ' + goog.typeOf(safeScript));
      return 'type_error:SafeScript';
    }
  }

  /**
   * Converts the given value to an embeddable JSON string and returns it. The
   * resulting string can be embedded in HTML because the '<' character is
   * encoded.
   *
   * @param {*} val
   * @return {string}
   * @private
   */
  static stringify_(val) {
    const json = JSON.stringify(val);
    return json.replace(/</g, '\\x3c');
  }

  /**
   * Package-internal utility method to create SafeScript instances.
   *
   * @param {string} script The string to initialize the SafeScript object with.
   * @return {!SafeScript} The initialized SafeScript object.
   * @package
   */
  static createSafeScriptSecurityPrivateDoNotAccessOrElse(script) {
    const policy = trustedtypes.getPolicyPrivateDoNotAccessOrElse();
    const trustedScript = policy ? policy.createScript(script) : script;
    return new SafeScript(trustedScript, CONSTRUCTOR_TOKEN_PRIVATE);
  }
}

/**
 * Returns a string-representation of this value.
 *
 * To obtain the actual string value wrapped in a SafeScript, use
 * `SafeScript.unwrap`.
 *
 * @return {string}
 * @see SafeScript#unwrap
 * @override
 */
SafeScript.prototype.toString = function() {
  return this.privateDoNotAccessOrElseSafeScriptWrappedValue_.toString();
};


/**
 * A SafeScript instance corresponding to the empty string.
 * @const {!SafeScript}
 */
SafeScript.EMPTY = /** @type {!SafeScript} */ ({
  // NOTE: this compiles to nothing, but hides the possible side effect of
  // SafeScript creation (due to calling trustedTypes.createPolicy) from the
  // compiler so that the entire call can be removed if the result is not used.
  // MOE:begin_strip
  // TODO(b/155299094): Refactor after adding compiler support.
  // MOE:end_strip
  valueOf: function() {
    return SafeScript.createSafeScriptSecurityPrivateDoNotAccessOrElse('');
  },
}.valueOf());


exports = SafeScript;

;return exports;});

//third_party/javascript/closure/fs/url.js
/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Wrapper for URL and its createObjectUrl and revokeObjectUrl
 * methods that are part of the HTML5 File API.
 */

goog.provide('goog.fs.url');


/**
 * Creates a blob URL for a blob object.
 * Throws an error if the browser does not support Object Urls.
 *
 * @param {!File|!Blob|!MediaSource|!MediaStream} obj The object for which
 *   to create the URL.
 * @return {string} The URL for the object.
 */
goog.fs.url.createObjectUrl = function(obj) {
  'use strict';
  return goog.fs.url.getUrlObject_().createObjectURL(obj);
};


/**
 * Revokes a URL created by {@link goog.fs.url.createObjectUrl}.
 * Throws an error if the browser does not support Object Urls.
 *
 * @param {string} url The URL to revoke.
 * @return {void}
 */
goog.fs.url.revokeObjectUrl = function(url) {
  'use strict';
  goog.fs.url.getUrlObject_().revokeObjectURL(url);
};


/**
 * @record
 * @private
 */
goog.fs.url.UrlObject_ = function() {};

/**
 * @param {!File|!Blob|!MediaSource|!MediaStream} arg
 * @return {string}
 */
goog.fs.url.UrlObject_.prototype.createObjectURL = function(arg) {};

/**
 * @param {string} s
 * @return {void}
 */
goog.fs.url.UrlObject_.prototype.revokeObjectURL = function(s) {};


/**
 * Get the object that has the createObjectURL and revokeObjectURL functions for
 * this browser.
 *
 * @return {!goog.fs.url.UrlObject_} The object for this browser.
 * @private
 */
goog.fs.url.getUrlObject_ = function() {
  'use strict';
  const urlObject = goog.fs.url.findUrlObject_();
  if (urlObject != null) {
    return urlObject;
  } else {
    throw new Error('This browser doesn\'t seem to support blob URLs');
  }
};


/**
 * Finds the object that has the createObjectURL and revokeObjectURL functions
 * for this browser.
 *
 * @return {?goog.fs.url.UrlObject_} The object for this browser or null if the
 *     browser does not support Object Urls.
 * @private
 */
goog.fs.url.findUrlObject_ = function() {
  'use strict';
  // This is what the spec says to do
  // http://dev.w3.org/2006/webapi/FileAPI/#dfn-createObjectURL
  if (goog.global.URL !== undefined &&
      goog.global.URL.createObjectURL !== undefined) {
    return /** @type {!goog.fs.url.UrlObject_} */ (goog.global.URL);
    // This is what the spec used to say to do
  } else if (goog.global.createObjectURL !== undefined) {
    return /** @type {!goog.fs.url.UrlObject_} */ (goog.global);
  } else {
    return null;
  }
};


/**
 * Checks whether this browser supports Object Urls. If not, calls to
 * createObjectUrl and revokeObjectUrl will result in an error.
 *
 * @return {boolean} True if this browser supports Object Urls.
 */
goog.fs.url.browserSupportsObjectUrls = function() {
  'use strict';
  return goog.fs.url.findUrlObject_() != null;
};

//third_party/javascript/closure/fs/blob.js
/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Wrappers for the HTML5 File API. These wrappers closely mirror
 * the underlying APIs, but use Closure-style events and Deferred return values.
 * Their existence also makes it possible to mock the FileSystem API for testing
 * in browsers that don't support it natively.
 *
 * When adding public functions to anything under this namespace, be sure to add
 * its mock counterpart to goog.testing.fs.
 */

goog.provide('goog.fs.blob');



/**
 * Concatenates one or more values together and converts them to a Blob.
 *
 * @param {...(string|!Blob|!ArrayBuffer)} var_args The values that will make up
 *     the resulting blob.
 * @return {!Blob} The blob.
 */
goog.fs.blob.getBlob = function(var_args) {
  'use strict';
  const BlobBuilder = goog.global.BlobBuilder || goog.global.WebKitBlobBuilder;

  if (BlobBuilder !== undefined) {
    const bb = new BlobBuilder();
    for (let i = 0; i < arguments.length; i++) {
      bb.append(arguments[i]);
    }
    return bb.getBlob();
  } else {
    return goog.fs.blob.getBlobWithProperties(
        Array.prototype.slice.call(arguments));
  }
};


/**
 * Creates a blob with the given properties.
 * See https://developer.mozilla.org/en-US/docs/Web/API/Blob for more details.
 *
 * @param {!Array<string|!Blob|!ArrayBuffer>} parts The values that will make up
 *     the resulting blob (subset supported by both BlobBuilder.append() and
 *     Blob constructor).
 * @param {string=} opt_type The MIME type of the Blob.
 * @param {string=} opt_endings Specifies how strings containing newlines are to
 *     be written out.
 * @return {!Blob} The blob.
 */
goog.fs.blob.getBlobWithProperties = function(parts, opt_type, opt_endings) {
  'use strict';
  const BlobBuilder = goog.global.BlobBuilder || goog.global.WebKitBlobBuilder;

  if (BlobBuilder !== undefined) {
    const bb = new BlobBuilder();
    for (let i = 0; i < parts.length; i++) {
      bb.append(parts[i], opt_endings);
    }
    return bb.getBlob(opt_type);
  } else if (goog.global.Blob !== undefined) {
    const properties = {};
    if (opt_type) {
      properties['type'] = opt_type;
    }
    if (opt_endings) {
      properties['endings'] = opt_endings;
    }
    return new Blob(parts, properties);
  } else {
    throw new Error('This browser doesn\'t seem to support creating Blobs');
  }
};

//third_party/javascript/closure/i18n/bidi.js
/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Utility functions for supporting Bidi issues.
 */


/**
 * Namespace for bidi supporting functions.
 */
goog.provide('goog.i18n.bidi');
goog.provide('goog.i18n.bidi.Dir');
goog.provide('goog.i18n.bidi.DirectionalString');
goog.provide('goog.i18n.bidi.Format');


/**
 * @define {boolean} FORCE_RTL forces the {@link goog.i18n.bidi.IS_RTL} constant
 * to say that the current locale is a RTL locale.  This should only be used
 * if you want to override the default behavior for deciding whether the
 * current locale is RTL or not.
 *
 * {@see goog.i18n.bidi.IS_RTL}
 */
goog.i18n.bidi.FORCE_RTL = goog.define('goog.i18n.bidi.FORCE_RTL', false);


/**
 * Constant that defines whether or not the current locale is a RTL locale.
 * If {@link goog.i18n.bidi.FORCE_RTL} is not true, this constant will default
 * to check that {@link goog.LOCALE} is one of a few major RTL locales.
 *
 * <p>This is designed to be a maximally efficient compile-time constant. For
 * example, for the default goog.LOCALE, compiling
 * "if (goog.i18n.bidi.IS_RTL) alert('rtl') else {}" should produce no code. It
 * is this design consideration that limits the implementation to only
 * supporting a few major RTL locales, as opposed to the broader repertoire of
 * something like goog.i18n.bidi.isRtlLanguage.
 *
 * <p>Since this constant refers to the directionality of the locale, it is up
 * to the caller to determine if this constant should also be used for the
 * direction of the UI.
 *
 * {@see goog.LOCALE}
 *
 * @type {boolean}
 *
 * TODO(aharon): write a test that checks that this is a compile-time constant.
 */
// LINT.IfChange
goog.i18n.bidi.IS_RTL =
    goog.i18n.bidi.FORCE_RTL ||
    ((goog.LOCALE.substring(0, 2).toLowerCase() == 'ar' ||
      goog.LOCALE.substring(0, 2).toLowerCase() == 'fa' ||
      goog.LOCALE.substring(0, 2).toLowerCase() == 'he' ||
      goog.LOCALE.substring(0, 2).toLowerCase() == 'iw' ||
      goog.LOCALE.substring(0, 2).toLowerCase() == 'ps' ||
      goog.LOCALE.substring(0, 2).toLowerCase() == 'sd' ||
      goog.LOCALE.substring(0, 2).toLowerCase() == 'ug' ||
      goog.LOCALE.substring(0, 2).toLowerCase() == 'ur' ||
      goog.LOCALE.substring(0, 2).toLowerCase() == 'yi') &&
     (goog.LOCALE.length == 2 || goog.LOCALE.substring(2, 3) == '-' ||
      goog.LOCALE.substring(2, 3) == '_')) ||
    (  // Specific to CKB (Central Kurdish)
        goog.LOCALE.length >= 3 &&
        goog.LOCALE.substring(0, 3).toLowerCase() == 'ckb' &&
        (goog.LOCALE.length == 3 || goog.LOCALE.substring(3, 4) == '-' ||
         goog.LOCALE.substring(3, 4) == '_')) ||
    (  // 2 letter language codes with RTL scripts
        goog.LOCALE.length >= 7 &&
        ((goog.LOCALE.substring(2, 3) == '-' ||
          goog.LOCALE.substring(2, 3) == '_') &&
         (goog.LOCALE.substring(3, 7).toLowerCase() == 'adlm' ||
          goog.LOCALE.substring(3, 7).toLowerCase() == 'arab' ||
          goog.LOCALE.substring(3, 7).toLowerCase() == 'hebr' ||
          goog.LOCALE.substring(3, 7).toLowerCase() == 'nkoo' ||
          goog.LOCALE.substring(3, 7).toLowerCase() == 'rohg' ||
          goog.LOCALE.substring(3, 7).toLowerCase() == 'thaa'))) ||
    (  // 3 letter languages codes with RTL scripts
        goog.LOCALE.length >= 8 &&
        ((goog.LOCALE.substring(3, 4) == '-' ||
          goog.LOCALE.substring(3, 4) == '_') &&
         (goog.LOCALE.substring(4, 8).toLowerCase() == 'adlm' ||
          goog.LOCALE.substring(4, 8).toLowerCase() == 'arab' ||
          goog.LOCALE.substring(4, 8).toLowerCase() == 'hebr' ||
          goog.LOCALE.substring(4, 8).toLowerCase() == 'nkoo' ||
          goog.LOCALE.substring(4, 8).toLowerCase() == 'rohg' ||
          goog.LOCALE.substring(4, 8).toLowerCase() == 'thaa')));
//    closure/RtlLocalesTest.java)

// TODO(b/77919903): Add additional scripts and languages that are RTL,
// e.g., mende, samaritan, etc.


/**
 * Unicode formatting characters and directionality string constants.
 * @enum {string}
 */
goog.i18n.bidi.Format = {
  /** Unicode "Left-To-Right Embedding" (LRE) character. */
  LRE: '\u202A',
  /** Unicode "Right-To-Left Embedding" (RLE) character. */
  RLE: '\u202B',
  /** Unicode "Pop Directional Formatting" (PDF) character. */
  PDF: '\u202C',
  /** Unicode "Left-To-Right Mark" (LRM) character. */
  LRM: '\u200E',
  /** Unicode "Right-To-Left Mark" (RLM) character. */
  RLM: '\u200F'
};


/**
 * Directionality enum.
 * @enum {number}
 */
goog.i18n.bidi.Dir = {
  /**
   * Left-to-right.
   */
  LTR: 1,

  /**
   * Right-to-left.
   */
  RTL: -1,

  /**
   * Neither left-to-right nor right-to-left.
   */
  NEUTRAL: 0
};


/**
 * 'right' string constant.
 * @type {string}
 */
goog.i18n.bidi.RIGHT = 'right';


/**
 * 'left' string constant.
 * @type {string}
 */
goog.i18n.bidi.LEFT = 'left';


/**
 * 'left' if locale is RTL, 'right' if not.
 * @type {string}
 */
goog.i18n.bidi.I18N_RIGHT =
    goog.i18n.bidi.IS_RTL ? goog.i18n.bidi.LEFT : goog.i18n.bidi.RIGHT;


/**
 * 'right' if locale is RTL, 'left' if not.
 * @type {string}
 */
goog.i18n.bidi.I18N_LEFT =
    goog.i18n.bidi.IS_RTL ? goog.i18n.bidi.RIGHT : goog.i18n.bidi.LEFT;


/**
 * Convert a directionality given in various formats to a goog.i18n.bidi.Dir
 * constant. Useful for interaction with different standards of directionality
 * representation.
 *
 * @param {goog.i18n.bidi.Dir|number|boolean|null} givenDir Directionality given
 *     in one of the following formats:
 *     1. A goog.i18n.bidi.Dir constant.
 *     2. A number (positive = LTR, negative = RTL, 0 = neutral).
 *     3. A boolean (true = RTL, false = LTR).
 *     4. A null for unknown directionality.
 * @param {boolean=} opt_noNeutral Whether a givenDir of zero or
 *     goog.i18n.bidi.Dir.NEUTRAL should be treated as null, i.e. unknown, in
 *     order to preserve legacy behavior.
 * @return {?goog.i18n.bidi.Dir} A goog.i18n.bidi.Dir constant matching the
 *     given directionality. If given null, returns null (i.e. unknown).
 */
goog.i18n.bidi.toDir = function(givenDir, opt_noNeutral) {
  'use strict';
  if (typeof givenDir == 'number') {
    // This includes the non-null goog.i18n.bidi.Dir case.
    return givenDir > 0 ?
        goog.i18n.bidi.Dir.LTR :
        givenDir < 0 ? goog.i18n.bidi.Dir.RTL :
                       opt_noNeutral ? null : goog.i18n.bidi.Dir.NEUTRAL;
  } else if (givenDir == null) {
    return null;
  } else {
    // Must be typeof givenDir == 'boolean'.
    return givenDir ? goog.i18n.bidi.Dir.RTL : goog.i18n.bidi.Dir.LTR;
  }
};


/**
 * A practical pattern to identify strong LTR character in the BMP.
 * This pattern is not theoretically correct according to the Unicode
 * standard. It is simplified for performance and small code size.
 * It also partially supports LTR scripts beyond U+FFFF by including
 * UTF-16 high surrogate values corresponding to mostly L-class code
 * point ranges.
 * However, low surrogate values and private-use regions are not included
 * in this RegEx.
 * @type {string}
 * @private
 */
goog.i18n.bidi.ltrChars_ =
    'A-Za-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02B8\u0300-\u0590\u0900-\u1FFF' +
    '\u200E\u2C00-\uD801\uD804-\uD839\uD83C-\uDBFF' +
    '\uF900-\uFB1C\uFE00-\uFE6F\uFEFD-\uFFFF';

/**
 * A practical pattern to identify strong RTL character. This pattern is not
 * theoretically correct according to the Unicode standard. It is simplified
 * for performance and small code size.
 * It also partially supports RTL scripts beyond U+FFFF by including
 * UTF-16 high surrogate values corresponding to mostly R- or AL-class
 * code point ranges.
 * However, low surrogate values and private-use regions are not included
 * in this RegEx.
 * @type {string}
 * @private
 */
goog.i18n.bidi.rtlChars_ =
    '\u0591-\u06EF\u06FA-\u08FF\u200F\uD802-\uD803\uD83A-\uD83B' +
    '\uFB1D-\uFDFF\uFE70-\uFEFC';

/**
 * Simplified regular expression for an HTML tag (opening or closing) or an HTML
 * escape. We might want to skip over such expressions when estimating the text
 * directionality.
 * @type {RegExp}
 * @private
 */
goog.i18n.bidi.htmlSkipReg_ = /<[^>]*>|&[^;]+;/g;


/**
 * Returns the input text with spaces instead of HTML tags or HTML escapes, if
 * opt_isStripNeeded is true. Else returns the input as is.
 * Useful for text directionality estimation.
 * Note: the function should not be used in other contexts; it is not 100%
 * correct, but rather a good-enough implementation for directionality
 * estimation purposes.
 * @param {string} str The given string.
 * @param {boolean=} opt_isStripNeeded Whether to perform the stripping.
 *     Default: false (to retain consistency with calling functions).
 * @return {string} The given string cleaned of HTML tags / escapes.
 * @private
 */
goog.i18n.bidi.stripHtmlIfNeeded_ = function(str, opt_isStripNeeded) {
  'use strict';
  return opt_isStripNeeded ? str.replace(goog.i18n.bidi.htmlSkipReg_, '') : str;
};


/**
 * Regular expression to check for RTL characters, BMP and high surrogate.
 * @type {RegExp}
 * @private
 */
goog.i18n.bidi.rtlCharReg_ = new RegExp('[' + goog.i18n.bidi.rtlChars_ + ']');


/**
 * Regular expression to check for LTR characters.
 * @type {RegExp}
 * @private
 */
goog.i18n.bidi.ltrCharReg_ = new RegExp('[' + goog.i18n.bidi.ltrChars_ + ']');


/**
 * Test whether the given string has any RTL characters in it.
 * @param {string} str The given string that need to be tested.
 * @param {boolean=} opt_isHtml Whether str is HTML / HTML-escaped.
 *     Default: false.
 * @return {boolean} Whether the string contains RTL characters.
 */
goog.i18n.bidi.hasAnyRtl = function(str, opt_isHtml) {
  'use strict';
  return goog.i18n.bidi.rtlCharReg_.test(
      goog.i18n.bidi.stripHtmlIfNeeded_(str, opt_isHtml));
};


/**
 * Test whether the given string has any RTL characters in it.
 * @param {string} str The given string that need to be tested.
 * @return {boolean} Whether the string contains RTL characters.
 * @deprecated Use hasAnyRtl.
 */
goog.i18n.bidi.hasRtlChar = goog.i18n.bidi.hasAnyRtl;


/**
 * Test whether the given string has any LTR characters in it.
 * @param {string} str The given string that need to be tested.
 * @param {boolean=} opt_isHtml Whether str is HTML / HTML-escaped.
 *     Default: false.
 * @return {boolean} Whether the string contains LTR characters.
 */
goog.i18n.bidi.hasAnyLtr = function(str, opt_isHtml) {
  'use strict';
  return goog.i18n.bidi.ltrCharReg_.test(
      goog.i18n.bidi.stripHtmlIfNeeded_(str, opt_isHtml));
};


/**
 * Regular expression pattern to check if the first character in the string
 * is LTR.
 * @type {RegExp}
 * @private
 */
goog.i18n.bidi.ltrRe_ = new RegExp('^[' + goog.i18n.bidi.ltrChars_ + ']');


/**
 * Regular expression pattern to check if the first character in the string
 * is RTL.
 * @type {RegExp}
 * @private
 */
goog.i18n.bidi.rtlRe_ = new RegExp('^[' + goog.i18n.bidi.rtlChars_ + ']');


/**
 * Check if the first character in the string is RTL or not.
 * @param {string} str The given string that need to be tested.
 * @return {boolean} Whether the first character in str is an RTL char.
 */
goog.i18n.bidi.isRtlChar = function(str) {
  'use strict';
  return goog.i18n.bidi.rtlRe_.test(str);
};


/**
 * Check if the first character in the string is LTR or not.
 * @param {string} str The given string that need to be tested.
 * @return {boolean} Whether the first character in str is an LTR char.
 */
goog.i18n.bidi.isLtrChar = function(str) {
  'use strict';
  return goog.i18n.bidi.ltrRe_.test(str);
};


/**
 * Check if the first character in the string is neutral or not.
 * @param {string} str The given string that need to be tested.
 * @return {boolean} Whether the first character in str is a neutral char.
 */
goog.i18n.bidi.isNeutralChar = function(str) {
  'use strict';
  return !goog.i18n.bidi.isLtrChar(str) && !goog.i18n.bidi.isRtlChar(str);
};


/**
 * Regular expressions to check if a piece of text is of LTR directionality
 * on first character with strong directionality.
 * @type {RegExp}
 * @private
 */
goog.i18n.bidi.ltrDirCheckRe_ = new RegExp(
    '^[^' + goog.i18n.bidi.rtlChars_ + ']*[' + goog.i18n.bidi.ltrChars_ + ']');


/**
 * Regular expressions to check if a piece of text is of RTL directionality
 * on first character with strong directionality.
 * @type {RegExp}
 * @private
 */
goog.i18n.bidi.rtlDirCheckRe_ = new RegExp(
    '^[^' + goog.i18n.bidi.ltrChars_ + ']*[' + goog.i18n.bidi.rtlChars_ + ']');


/**
 * Check whether the first strongly directional character (if any) is RTL.
 * @param {string} str String being checked.
 * @param {boolean=} opt_isHtml Whether str is HTML / HTML-escaped.
 *     Default: false.
 * @return {boolean} Whether RTL directionality is detected using the first
 *     strongly-directional character method.
 */
goog.i18n.bidi.startsWithRtl = function(str, opt_isHtml) {
  'use strict';
  return goog.i18n.bidi.rtlDirCheckRe_.test(
      goog.i18n.bidi.stripHtmlIfNeeded_(str, opt_isHtml));
};


/**
 * Check whether the first strongly directional character (if any) is RTL.
 * @param {string} str String being checked.
 * @param {boolean=} opt_isHtml Whether str is HTML / HTML-escaped.
 *     Default: false.
 * @return {boolean} Whether RTL directionality is detected using the first
 *     strongly-directional character method.
 * @deprecated Use startsWithRtl.
 */
goog.i18n.bidi.isRtlText = goog.i18n.bidi.startsWithRtl;


/**
 * Check whether the first strongly directional character (if any) is LTR.
 * @param {string} str String being checked.
 * @param {boolean=} opt_isHtml Whether str is HTML / HTML-escaped.
 *     Default: false.
 * @return {boolean} Whether LTR directionality is detected using the first
 *     strongly-directional character method.
 */
goog.i18n.bidi.startsWithLtr = function(str, opt_isHtml) {
  'use strict';
  return goog.i18n.bidi.ltrDirCheckRe_.test(
      goog.i18n.bidi.stripHtmlIfNeeded_(str, opt_isHtml));
};


/**
 * Check whether the first strongly directional character (if any) is LTR.
 * @param {string} str String being checked.
 * @param {boolean=} opt_isHtml Whether str is HTML / HTML-escaped.
 *     Default: false.
 * @return {boolean} Whether LTR directionality is detected using the first
 *     strongly-directional character method.
 * @deprecated Use startsWithLtr.
 */
goog.i18n.bidi.isLtrText = goog.i18n.bidi.startsWithLtr;


/**
 * Regular expression to check if a string looks like something that must
 * always be LTR even in RTL text, e.g. a URL. When estimating the
 * directionality of text containing these, we treat these as weakly LTR,
 * like numbers.
 * @type {RegExp}
 * @private
 */
goog.i18n.bidi.isRequiredLtrRe_ = /^http:\/\/.*/;


/**
 * Check whether the input string either contains no strongly directional
 * characters or looks like a url.
 * @param {string} str String being checked.
 * @param {boolean=} opt_isHtml Whether str is HTML / HTML-escaped.
 *     Default: false.
 * @return {boolean} Whether neutral directionality is detected.
 */
goog.i18n.bidi.isNeutralText = function(str, opt_isHtml) {
  'use strict';
  str = goog.i18n.bidi.stripHtmlIfNeeded_(str, opt_isHtml);
  return goog.i18n.bidi.isRequiredLtrRe_.test(str) ||
      !goog.i18n.bidi.hasAnyLtr(str) && !goog.i18n.bidi.hasAnyRtl(str);
};


/**
 * Regular expressions to check if the last strongly-directional character in a
 * piece of text is LTR.
 * @type {RegExp}
 * @private
 */
goog.i18n.bidi.ltrExitDirCheckRe_ = new RegExp(
    '[' + goog.i18n.bidi.ltrChars_ + ']' +
    '[^' + goog.i18n.bidi.rtlChars_ + ']*$');


/**
 * Regular expressions to check if the last strongly-directional character in a
 * piece of text is RTL.
 * @type {RegExp}
 * @private
 */
goog.i18n.bidi.rtlExitDirCheckRe_ = new RegExp(
    '[' + goog.i18n.bidi.rtlChars_ + ']' +
    '[^' + goog.i18n.bidi.ltrChars_ + ']*$');


/**
 * Check if the exit directionality a piece of text is LTR, i.e. if the last
 * strongly-directional character in the string is LTR.
 * @param {string} str String being checked.
 * @param {boolean=} opt_isHtml Whether str is HTML / HTML-escaped.
 *     Default: false.
 * @return {boolean} Whether LTR exit directionality was detected.
 */
goog.i18n.bidi.endsWithLtr = function(str, opt_isHtml) {
  'use strict';
  return goog.i18n.bidi.ltrExitDirCheckRe_.test(
      goog.i18n.bidi.stripHtmlIfNeeded_(str, opt_isHtml));
};


/**
 * Check if the exit directionality a piece of text is LTR, i.e. if the last
 * strongly-directional character in the string is LTR.
 * @param {string} str String being checked.
 * @param {boolean=} opt_isHtml Whether str is HTML / HTML-escaped.
 *     Default: false.
 * @return {boolean} Whether LTR exit directionality was detected.
 * @deprecated Use endsWithLtr.
 */
goog.i18n.bidi.isLtrExitText = goog.i18n.bidi.endsWithLtr;


/**
 * Check if the exit directionality a piece of text is RTL, i.e. if the last
 * strongly-directional character in the string is RTL.
 * @param {string} str String being checked.
 * @param {boolean=} opt_isHtml Whether str is HTML / HTML-escaped.
 *     Default: false.
 * @return {boolean} Whether RTL exit directionality was detected.
 */
goog.i18n.bidi.endsWithRtl = function(str, opt_isHtml) {
  'use strict';
  return goog.i18n.bidi.rtlExitDirCheckRe_.test(
      goog.i18n.bidi.stripHtmlIfNeeded_(str, opt_isHtml));
};


/**
 * Check if the exit directionality a piece of text is RTL, i.e. if the last
 * strongly-directional character in the string is RTL.
 * @param {string} str String being checked.
 * @param {boolean=} opt_isHtml Whether str is HTML / HTML-escaped.
 *     Default: false.
 * @return {boolean} Whether RTL exit directionality was detected.
 * @deprecated Use endsWithRtl.
 */
goog.i18n.bidi.isRtlExitText = goog.i18n.bidi.endsWithRtl;


/**
 * A regular expression for matching right-to-left language codes.
 * See {@link #isRtlLanguage} for the design.
 * Note that not all RTL scripts are included.
 * @type {!RegExp}
 * @private
 */
goog.i18n.bidi.rtlLocalesRe_ = new RegExp(
    '^(ar|ckb|dv|he|iw|fa|nqo|ps|sd|ug|ur|yi|' +
        '.*[-_](Adlm|Arab|Hebr|Nkoo|Rohg|Thaa))' +
        '(?!.*[-_](Latn|Cyrl)($|-|_))($|-|_)',
    'i');


/**
 * Check if a BCP 47 / III language code indicates an RTL language, i.e. either:
 * - a language code explicitly specifying one of the right-to-left scripts,
 *   e.g. "az-Arab", or<p>
 * - a language code specifying one of the languages normally written in a
 *   right-to-left script, e.g. "fa" (Farsi), except ones explicitly specifying
 *   Latin or Cyrillic script (which are the usual LTR alternatives).<p>
 * The list of right-to-left scripts appears in the 100-199 range in
 * http://www.unicode.org/iso15924/iso15924-num.html, of which Arabic and
 * Hebrew are by far the most widely used. We also recognize Thaana, and N'Ko,
 * which also have significant modern usage. Adlam and Rohingya
 * scripts are now included since they can be expected to be used in the
 * future. The rest (Syriac, Samaritan, Mandaic, etc.) seem to have extremely
 * limited or no modern usage and are not recognized to save on code size. The
 * languages usually written in a right-to-left script are taken as those with
 * Suppress-Script: Hebr|Arab|Thaa|Nkoo|Adlm|Rohg in
 * http://www.iana.org/assignments/language-subtag-registry,
 * as well as Central (or Sorani) Kurdish (ckb), Sindhi (sd) and Uyghur (ug).
 * Other subtags of the language code, e.g. regions like EG (Egypt), are
 * ignored.
 * @param {string} lang BCP 47 (a.k.a III) language code.
 * @return {boolean} Whether the language code is an RTL language.
 */
goog.i18n.bidi.isRtlLanguage = function(lang) {
  'use strict';
  return goog.i18n.bidi.rtlLocalesRe_.test(lang);
};


/**
 * Regular expression for bracket guard replacement in text.
 * @type {RegExp}
 * @private
 */
goog.i18n.bidi.bracketGuardTextRe_ =
    /(\(.*?\)+)|(\[.*?\]+)|(\{.*?\}+)|(<.*?>+)/g;


/**
 * Apply bracket guard using LRM and RLM. This is to address the problem of
 * messy bracket display frequently happens in RTL layout.
 * This function works for plain text, not for HTML. In HTML, the opening
 * bracket might be in a different context than the closing bracket (such as
 * an attribute value).
 * @param {string} s The string that need to be processed.
 * @param {boolean=} opt_isRtlContext specifies default direction (usually
 *     direction of the UI).
 * @return {string} The processed string, with all bracket guarded.
 */
goog.i18n.bidi.guardBracketInText = function(s, opt_isRtlContext) {
  'use strict';
  const useRtl = opt_isRtlContext === undefined ? goog.i18n.bidi.hasAnyRtl(s) :
                                                  opt_isRtlContext;
  const mark = useRtl ? goog.i18n.bidi.Format.RLM : goog.i18n.bidi.Format.LRM;
  return s.replace(goog.i18n.bidi.bracketGuardTextRe_, mark + '$&' + mark);
};


/**
 * Enforce the html snippet in RTL directionality regardless of overall context.
 * If the html piece was enclosed by tag, dir will be applied to existing
 * tag, otherwise a span tag will be added as wrapper. For this reason, if
 * html snippet starts with a tag, this tag must enclose the whole piece. If
 * the tag already has a dir specified, this new one will override existing
 * one in behavior (tested on FF and IE).
 * @param {string} html The string that need to be processed.
 * @return {string} The processed string, with directionality enforced to RTL.
 */
goog.i18n.bidi.enforceRtlInHtml = function(html) {
  'use strict';
  if (html.charAt(0) == '<') {
    return html.replace(/<\w+/, '$& dir=rtl');
  }
  // '\n' is important for FF so that it won't incorrectly merge span groups
  return '\n<span dir=rtl>' + html + '</span>';
};


/**
 * Enforce RTL on both end of the given text piece using unicode BiDi formatting
 * characters RLE and PDF.
 * @param {string} text The piece of text that need to be wrapped.
 * @return {string} The wrapped string after process.
 */
goog.i18n.bidi.enforceRtlInText = function(text) {
  'use strict';
  return goog.i18n.bidi.Format.RLE + text + goog.i18n.bidi.Format.PDF;
};


/**
 * Enforce the html snippet in RTL directionality regardless or overall context.
 * If the html piece was enclosed by tag, dir will be applied to existing
 * tag, otherwise a span tag will be added as wrapper. For this reason, if
 * html snippet starts with a tag, this tag must enclose the whole piece. If
 * the tag already has a dir specified, this new one will override existing
 * one in behavior (tested on FF and IE).
 * @param {string} html The string that need to be processed.
 * @return {string} The processed string, with directionality enforced to RTL.
 */
goog.i18n.bidi.enforceLtrInHtml = function(html) {
  'use strict';
  if (html.charAt(0) == '<') {
    return html.replace(/<\w+/, '$& dir=ltr');
  }
  // '\n' is important for FF so that it won't incorrectly merge span groups
  return '\n<span dir=ltr>' + html + '</span>';
};


/**
 * Enforce LTR on both end of the given text piece using unicode BiDi formatting
 * characters LRE and PDF.
 * @param {string} text The piece of text that need to be wrapped.
 * @return {string} The wrapped string after process.
 */
goog.i18n.bidi.enforceLtrInText = function(text) {
  'use strict';
  return goog.i18n.bidi.Format.LRE + text + goog.i18n.bidi.Format.PDF;
};


/**
 * Regular expression to find dimensions such as "padding: .3 0.4ex 5px 6;"
 * @type {RegExp}
 * @private
 */
goog.i18n.bidi.dimensionsRe_ =
    /:\s*([.\d][.\w]*)\s+([.\d][.\w]*)\s+([.\d][.\w]*)\s+([.\d][.\w]*)/g;


/**
 * Regular expression for left.
 * @type {RegExp}
 * @private
 */
goog.i18n.bidi.leftRe_ = /left/gi;


/**
 * Regular expression for right.
 * @type {RegExp}
 * @private
 */
goog.i18n.bidi.rightRe_ = /right/gi;


/**
 * Placeholder regular expression for swapping.
 * @type {RegExp}
 * @private
 */
goog.i18n.bidi.tempRe_ = /%%%%/g;


/**
 * Swap location parameters and 'left'/'right' in CSS specification. The
 * processed string will be suited for RTL layout. Though this function can
 * cover most cases, there are always exceptions. It is suggested to put
 * those exceptions in separate group of CSS string.
 * @param {string} cssStr CSS spefication string.
 * @return {string} Processed CSS specification string.
 */
goog.i18n.bidi.mirrorCSS = function(cssStr) {
  'use strict';
  return cssStr
      .
      // reverse dimensions
      replace(goog.i18n.bidi.dimensionsRe_, ':$1 $4 $3 $2')
      .replace(goog.i18n.bidi.leftRe_, '%%%%')
      .  // swap left and right
      replace(goog.i18n.bidi.rightRe_, goog.i18n.bidi.LEFT)
      .replace(goog.i18n.bidi.tempRe_, goog.i18n.bidi.RIGHT);
};


/**
 * Regular expression for hebrew double quote substitution, finding quote
 * directly after hebrew characters.
 * @type {RegExp}
 * @private
 */
goog.i18n.bidi.doubleQuoteSubstituteRe_ = /([\u0591-\u05f2])"/g;


/**
 * Regular expression for hebrew single quote substitution, finding quote
 * directly after hebrew characters.
 * @type {RegExp}
 * @private
 */
goog.i18n.bidi.singleQuoteSubstituteRe_ = /([\u0591-\u05f2])'/g;


/**
 * Replace the double and single quote directly after a Hebrew character with
 * GERESH and GERSHAYIM. In such case, most likely that's user intention.
 * @param {string} str String that need to be processed.
 * @return {string} Processed string with double/single quote replaced.
 */
goog.i18n.bidi.normalizeHebrewQuote = function(str) {
  'use strict';
  return str.replace(goog.i18n.bidi.doubleQuoteSubstituteRe_, '$1\u05f4')
      .replace(goog.i18n.bidi.singleQuoteSubstituteRe_, '$1\u05f3');
};


/**
 * Regular expression to split a string into "words" for directionality
 * estimation based on relative word counts.
 * @type {RegExp}
 * @private
 */
goog.i18n.bidi.wordSeparatorRe_ = /\s+/;


/**
 * Regular expression to check if a string contains any numerals. Used to
 * differentiate between completely neutral strings and those containing
 * numbers, which are weakly LTR.
 *
 * Native Arabic digits (\u0660 - \u0669) are not included because although they
 * do flow left-to-right inside a number, this is the case even if the  overall
 * directionality is RTL, and a mathematical expression using these digits is
 * supposed to flow right-to-left overall, including unary plus and minus
 * appearing to the right of a number, and this does depend on the overall
 * directionality being RTL. The digits used in Farsi (\u06F0 - \u06F9), on the
 * other hand, are included, since Farsi math (including unary plus and minus)
 * does flow left-to-right.
 * TODO: Consider other systems of digits, e.g., Adlam.
 *
 * @type {RegExp}
 * @private
 */
goog.i18n.bidi.hasNumeralsRe_ = /[\d\u06f0-\u06f9]/;


/**
 * This constant controls threshold of RTL directionality.
 * @type {number}
 * @private
 */
goog.i18n.bidi.rtlDetectionThreshold_ = 0.40;


/**
 * Estimates the directionality of a string based on relative word counts.
 * If the number of RTL words is above a certain percentage of the total number
 * of strongly directional words, returns RTL.
 * Otherwise, if any words are strongly or weakly LTR, returns LTR.
 * Otherwise, returns UNKNOWN, which is used to mean "neutral".
 * Numbers are counted as weakly LTR.
 * @param {string} str The string to be checked.
 * @param {boolean=} opt_isHtml Whether str is HTML / HTML-escaped.
 *     Default: false.
 * @return {goog.i18n.bidi.Dir} Estimated overall directionality of `str`.
 */
goog.i18n.bidi.estimateDirection = function(str, opt_isHtml) {
  'use strict';
  let rtlCount = 0;
  let totalCount = 0;
  let hasWeaklyLtr = false;
  const tokens = goog.i18n.bidi.stripHtmlIfNeeded_(str, opt_isHtml)
                     .split(goog.i18n.bidi.wordSeparatorRe_);
  for (let i = 0; i < tokens.length; i++) {
    const token = tokens[i];
    if (goog.i18n.bidi.startsWithRtl(token)) {
      rtlCount++;
      totalCount++;
    } else if (goog.i18n.bidi.isRequiredLtrRe_.test(token)) {
      hasWeaklyLtr = true;
    } else if (goog.i18n.bidi.hasAnyLtr(token)) {
      totalCount++;
    } else if (goog.i18n.bidi.hasNumeralsRe_.test(token)) {
      hasWeaklyLtr = true;
    }
  }

  return totalCount == 0 ?
      (hasWeaklyLtr ? goog.i18n.bidi.Dir.LTR : goog.i18n.bidi.Dir.NEUTRAL) :
      (rtlCount / totalCount > goog.i18n.bidi.rtlDetectionThreshold_ ?
           goog.i18n.bidi.Dir.RTL :
           goog.i18n.bidi.Dir.LTR);
};


/**
 * Check the directionality of a piece of text, return true if the piece of
 * text should be laid out in RTL direction.
 * @param {string} str The piece of text that need to be detected.
 * @param {boolean=} opt_isHtml Whether str is HTML / HTML-escaped.
 *     Default: false.
 * @return {boolean} Whether this piece of text should be laid out in RTL.
 */
goog.i18n.bidi.detectRtlDirectionality = function(str, opt_isHtml) {
  'use strict';
  return goog.i18n.bidi.estimateDirection(str, opt_isHtml) ==
      goog.i18n.bidi.Dir.RTL;
};


/**
 * Sets text input element's directionality and text alignment based on a
 * given directionality. Does nothing if the given directionality is unknown or
 * neutral.
 * @param {Element} element Input field element to set directionality to.
 * @param {goog.i18n.bidi.Dir|number|boolean|null} dir Desired directionality,
 *     given in one of the following formats:
 *     1. A goog.i18n.bidi.Dir constant.
 *     2. A number (positive = LRT, negative = RTL, 0 = neutral).
 *     3. A boolean (true = RTL, false = LTR).
 *     4. A null for unknown directionality.
 * @return {void}
 */
goog.i18n.bidi.setElementDirAndAlign = function(element, dir) {
  'use strict';
  if (element) {
    const htmlElement = /** @type {!HTMLElement} */ (element);
    dir = goog.i18n.bidi.toDir(dir);
    if (dir) {
      htmlElement.style.textAlign = dir == goog.i18n.bidi.Dir.RTL ?
          goog.i18n.bidi.RIGHT :
          goog.i18n.bidi.LEFT;
      htmlElement.dir = dir == goog.i18n.bidi.Dir.RTL ? 'rtl' : 'ltr';
    }
  }
};


/**
 * Sets element dir based on estimated directionality of the given text.
 * @param {!Element} element
 * @param {string} text
 * @return {void}
 */
goog.i18n.bidi.setElementDirByTextDirectionality = function(element, text) {
  'use strict';
  const htmlElement = /** @type {!HTMLElement} */ (element);
  switch (goog.i18n.bidi.estimateDirection(text)) {
    case (goog.i18n.bidi.Dir.LTR):
      if (htmlElement.dir !== 'ltr') {
        htmlElement.dir = 'ltr';
      }
      break;
    case (goog.i18n.bidi.Dir.RTL):
      if (htmlElement.dir !== 'rtl') {
        htmlElement.dir = 'rtl';
      }
      break;
    default:
      // Default for no direction, inherit from document.
      htmlElement.removeAttribute('dir');
  }
};



/**
 * Strings that have an (optional) known direction.
 *
 * Implementations of this interface are string-like objects that carry an
 * attached direction, if known.
 * @interface
 */
goog.i18n.bidi.DirectionalString = function() {};


/**
 * Interface marker of the DirectionalString interface.
 *
 * This property can be used to determine at runtime whether or not an object
 * implements this interface.  All implementations of this interface set this
 * property to `true`.
 * @type {boolean}
 */
goog.i18n.bidi.DirectionalString.prototype
    .implementsGoogI18nBidiDirectionalString;


/**
 * Retrieves this object's known direction (if any).
 * @return {?goog.i18n.bidi.Dir} The known direction. Null if unknown.
 */
goog.i18n.bidi.DirectionalString.prototype.getDirection;

//third_party/javascript/closure/html/trustedresourceurl.js
/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview The TrustedResourceUrl type and its builders.
 *
 * TODO(xtof): Link to document stating type contract.
 */

goog.provide('goog.html.TrustedResourceUrl');

goog.require('goog.asserts');
goog.require('goog.fs.blob');
goog.require('goog.fs.url');
goog.require('goog.html.SafeScript');
goog.require('goog.html.trustedtypes');
goog.require('goog.i18n.bidi.Dir');
goog.require('goog.i18n.bidi.DirectionalString');
goog.require('goog.string.Const');
goog.require('goog.string.TypedString');



/**
 * A URL which is under application control and from which script, CSS, and
 * other resources that represent executable code, can be fetched.
 *
 * Given that the URL can only be constructed from strings under application
 * control and is used to load resources, bugs resulting in a malformed URL
 * should not have a security impact and are likely to be easily detectable
 * during testing. Given the wide number of non-RFC compliant URLs in use,
 * stricter validation could prevent some applications from being able to use
 * this type.
 *
 * Instances of this type must be created via the factory method,
 * (`fromConstant`, `fromConstants`, `format` or `formatWithParams`), and not by
 * invoking its constructor. The constructor intentionally takes an extra
 * parameter that cannot be constructed outside of this file and the type is
 * immutable; hence only a default instance corresponding to the empty string
 * can be obtained via constructor invocation.
 *
 * Creating TrustedResourceUrl objects HAS SIDE-EFFECTS due to calling
 * Trusted Types Web API.
 *
 * @see goog.html.TrustedResourceUrl#fromConstant
 * @final
 * @struct
 * @implements {goog.i18n.bidi.DirectionalString}
 * @implements {goog.string.TypedString}
 */
goog.html.TrustedResourceUrl = class {
  /**
   * @param {!TrustedScriptURL|string} value
   * @param {!Object} token package-internal implementation detail.
   */
  constructor(value, token) {
    /**
     * The contained value of this TrustedResourceUrl.  The field has a
     * purposely ugly name to make (non-compiled) code that attempts to directly
     * access this field stand out.
     * @const
     * @private {!TrustedScriptURL|string}
     */
    this.privateDoNotAccessOrElseTrustedResourceUrlWrappedValue_ =
        (token === goog.html.TrustedResourceUrl.CONSTRUCTOR_TOKEN_PRIVATE_) ?
        value :
        '';
  }
};


/**
 * @override
 * @const
 */
goog.html.TrustedResourceUrl.prototype.implementsGoogStringTypedString = true;


/**
 * Returns this TrustedResourceUrl's value as a string.
 *
 * IMPORTANT: In code where it is security relevant that an object's type is
 * indeed `TrustedResourceUrl`, use
 * `goog.html.TrustedResourceUrl.unwrap` instead of this method. If in
 * doubt, assume that it's security relevant. In particular, note that
 * goog.html functions which return a goog.html type do not guarantee that
 * the returned instance is of the right type. For example:
 *
 * <pre>
 * var fakeSafeHtml = new String('fake');
 * fakeSafeHtml.__proto__ = goog.html.SafeHtml.prototype;
 * var newSafeHtml = goog.html.SafeHtml.htmlEscape(fakeSafeHtml);
 * // newSafeHtml is just an alias for fakeSafeHtml, it's passed through by
 * // goog.html.SafeHtml.htmlEscape() as fakeSafeHtml instanceof
 * // goog.html.SafeHtml.
 * </pre>
 *
 * @see goog.html.TrustedResourceUrl#unwrap
 * @override
 */
goog.html.TrustedResourceUrl.prototype.getTypedStringValue = function() {
  'use strict';
  return this.privateDoNotAccessOrElseTrustedResourceUrlWrappedValue_
      .toString();
};


/**
 * @override
 * @const
 */
goog.html.TrustedResourceUrl.prototype.implementsGoogI18nBidiDirectionalString =
    true;


/**
 * Returns this URLs directionality, which is always `LTR`.
 * @override
 * @return {!goog.i18n.bidi.Dir}
 */
goog.html.TrustedResourceUrl.prototype.getDirection = function() {
  'use strict';
  return goog.i18n.bidi.Dir.LTR;
};


/**
 * Creates a new TrustedResourceUrl with params added to URL. Both search and
 * hash params can be specified.
 *
 * @param {string|?Object<string, *>|undefined} searchParams Search parameters
 *     to add to URL. See goog.html.TrustedResourceUrl.stringifyParams_ for
 *     exact format definition.
 * @param {(string|?Object<string, *>)=} opt_hashParams Hash parameters to add
 *     to URL. See goog.html.TrustedResourceUrl.stringifyParams_ for exact
 *     format definition.
 * @return {!goog.html.TrustedResourceUrl} New TrustedResourceUrl with params.
 */
goog.html.TrustedResourceUrl.prototype.cloneWithParams = function(
    searchParams, opt_hashParams) {
  'use strict';
  var url = goog.html.TrustedResourceUrl.unwrap(this);
  var parts = goog.html.TrustedResourceUrl.URL_PARAM_PARSER_.exec(url);
  var urlBase = parts[1];
  var urlSearch = parts[2] || '';
  var urlHash = parts[3] || '';

  return goog.html.TrustedResourceUrl
      .createTrustedResourceUrlSecurityPrivateDoNotAccessOrElse(
          urlBase +
          goog.html.TrustedResourceUrl.stringifyParams_(
              '?', urlSearch, searchParams) +
          goog.html.TrustedResourceUrl.stringifyParams_(
              '#', urlHash, opt_hashParams));
};


/**
 * Returns a string-representation of this value.
 *
 * To obtain the actual string value wrapped in a TrustedResourceUrl, use
 * `goog.html.TrustedResourceUrl.unwrap`.
 *
 * @return {string}
 * @see goog.html.TrustedResourceUrl#unwrap
 * @override
 */
goog.html.TrustedResourceUrl.prototype.toString = function() {
  'use strict';
  return this.privateDoNotAccessOrElseTrustedResourceUrlWrappedValue_ + '';
};


/**
 * Performs a runtime check that the provided object is indeed a
 * TrustedResourceUrl object, and returns its value.
 *
 * @param {!goog.html.TrustedResourceUrl} trustedResourceUrl The object to
 *     extract from.
 * @return {string} The trustedResourceUrl object's contained string, unless
 *     the run-time type check fails. In that case, `unwrap` returns an
 *     innocuous string, or, if assertions are enabled, throws
 *     `goog.asserts.AssertionError`.
 */
goog.html.TrustedResourceUrl.unwrap = function(trustedResourceUrl) {
  'use strict';
  return goog.html.TrustedResourceUrl.unwrapTrustedScriptURL(trustedResourceUrl)
      .toString();
};


/**
 * Unwraps value as TrustedScriptURL if supported or as a string if not.
 * @param {!goog.html.TrustedResourceUrl} trustedResourceUrl
 * @return {!TrustedScriptURL|string}
 * @see goog.html.TrustedResourceUrl.unwrap
 */
goog.html.TrustedResourceUrl.unwrapTrustedScriptURL = function(
    trustedResourceUrl) {
  'use strict';
  // Perform additional Run-time type-checking to ensure that
  // trustedResourceUrl is indeed an instance of the expected type.  This
  // provides some additional protection against security bugs due to
  // application code that disables type checks.
  // Specifically, the following checks are performed:
  // 1. The object is an instance of the expected type.
  // 2. The object is not an instance of a subclass.
  if (trustedResourceUrl instanceof goog.html.TrustedResourceUrl &&
      trustedResourceUrl.constructor === goog.html.TrustedResourceUrl) {
    return trustedResourceUrl
        .privateDoNotAccessOrElseTrustedResourceUrlWrappedValue_;
  } else {
    goog.asserts.fail('expected object of type TrustedResourceUrl, got \'' +
        trustedResourceUrl + '\' of type ' + goog.typeOf(trustedResourceUrl));
    return 'type_error:TrustedResourceUrl';
  }
};


/**
 * Creates a TrustedResourceUrl from a format string and arguments.
 *
 * The arguments for interpolation into the format string map labels to values.
 * Values of type `goog.string.Const` are interpolated without modifcation.
 * Values of other types are cast to string and encoded with
 * encodeURIComponent.
 *
 * `%{<label>}` markers are used in the format string to indicate locations
 * to be interpolated with the valued mapped to the given label. `<label>`
 * must contain only alphanumeric and `_` characters.
 *
 * The format string must match goog.html.TrustedResourceUrl.BASE_URL_.
 *
 * Example usage:
 *
 *    var url = goog.html.TrustedResourceUrl.format(goog.string.Const.from(
 *        'https://www.google.com/search?q=%{query}'), {'query': searchTerm});
 *
 *    var url = goog.html.TrustedResourceUrl.format(goog.string.Const.from(
 *        '//www.youtube.com/v/%{videoId}?hl=en&fs=1%{autoplay}'), {
 *        'videoId': videoId,
 *        'autoplay': opt_autoplay ?
 *            goog.string.Const.from('&autoplay=1') : goog.string.Const.EMPTY
 *    });
 *
 * While this function can be used to create a TrustedResourceUrl from only
 * constants, fromConstant() and fromConstants() are generally preferable for
 * that purpose.
 *
 * @param {!goog.string.Const} format The format string.
 * @param {!Object<string, (string|number|!goog.string.Const)>} args Mapping
 *     of labels to values to be interpolated into the format string.
 *     goog.string.Const values are interpolated without encoding.
 * @return {!goog.html.TrustedResourceUrl}
 * @throws {!Error} On an invalid format string or if a label used in the
 *     the format string is not present in args.
 */
goog.html.TrustedResourceUrl.format = function(format, args) {
  'use strict';
  var formatStr = goog.string.Const.unwrap(format);
  if (!goog.html.TrustedResourceUrl.BASE_URL_.test(formatStr)) {
    throw new Error('Invalid TrustedResourceUrl format: ' + formatStr);
  }
  var result = formatStr.replace(
      goog.html.TrustedResourceUrl.FORMAT_MARKER_, function(match, id) {
        'use strict';
        if (!Object.prototype.hasOwnProperty.call(args, id)) {
          throw new Error(
              'Found marker, "' + id + '", in format string, "' + formatStr +
              '", but no valid label mapping found ' +
              'in args: ' + JSON.stringify(args));
        }
        var arg = args[id];
        if (arg instanceof goog.string.Const) {
          return goog.string.Const.unwrap(arg);
        } else {
          return encodeURIComponent(String(arg));
        }
      });
  return goog.html.TrustedResourceUrl
      .createTrustedResourceUrlSecurityPrivateDoNotAccessOrElse(result);
};


/**
 * @private @const {!RegExp}
 */
goog.html.TrustedResourceUrl.FORMAT_MARKER_ = /%{(\w+)}/g;


/**
 * The URL must be absolute, scheme-relative or path-absolute. So it must
 * start with:
 * - https:// followed by allowed origin characters.
 * - // followed by allowed origin characters.
 * - Any absolute or relative path.
 *
 * Based on
 * https://url.spec.whatwg.org/commit-snapshots/56b74ce7cca8883eab62e9a12666e2fac665d03d/#url-parsing
 * an initial / which is not followed by another / or \ will end up in the "path
 * state" and from there it can only go to "fragment state" and "query state".
 *
 * We don't enforce a well-formed domain name. So '.' or '1.2' are valid.
 * That's ok because the origin comes from a compile-time constant.
 *
 * A regular expression is used instead of goog.uri for several reasons:
 * - Strictness. E.g. we don't want any userinfo component and we don't
 *   want '/./, nor \' in the first path component.
 * - Small trusted base. goog.uri is generic and might need to change,
 *   reasoning about all the ways it can parse a URL now and in the future
 *   is error-prone.
 * - Code size. We expect many calls to .format(), many of which might
 *   not be using goog.uri.
 * - Simplicity. Using goog.uri would likely not result in simpler nor shorter
 *   code.
 * @private @const {!RegExp}
 */
goog.html.TrustedResourceUrl.BASE_URL_ = new RegExp(
    '^((https:)?//[0-9a-z.:[\\]-]+/'  // Origin.
        + '|/[^/\\\\]'                // Absolute path.
        + '|[^:/\\\\%]+/'             // Relative path.
        + '|[^:/\\\\%]*[?#]'          // Query string or fragment.
        + '|about:blank#'             // about:blank with fragment.
        + ')',
    'i');

/**
 * RegExp for splitting a URL into the base, search field, and hash field.
 *
 * @private @const {!RegExp}
 */
goog.html.TrustedResourceUrl.URL_PARAM_PARSER_ =
    /^([^?#]*)(\?[^#]*)?(#[\s\S]*)?/;


/**
 * Formats the URL same as TrustedResourceUrl.format and then adds extra URL
 * parameters.
 *
 * Example usage:
 *
 *     // Creates '//www.youtube.com/v/abc?autoplay=1' for videoId='abc' and
 *     // opt_autoplay=1. Creates '//www.youtube.com/v/abc' for videoId='abc'
 *     // and opt_autoplay=undefined.
 *     var url = goog.html.TrustedResourceUrl.formatWithParams(
 *         goog.string.Const.from('//www.youtube.com/v/%{videoId}'),
 *         {'videoId': videoId},
 *         {'autoplay': opt_autoplay});
 *
 * @param {!goog.string.Const} format The format string.
 * @param {!Object<string, (string|number|!goog.string.Const)>} args Mapping
 *     of labels to values to be interpolated into the format string.
 *     goog.string.Const values are interpolated without encoding.
 * @param {string|?Object<string, *>|undefined} searchParams Parameters to add
 *     to URL. See goog.html.TrustedResourceUrl.stringifyParams_ for exact
 *     format definition.
 * @param {(string|?Object<string, *>)=} opt_hashParams Hash parameters to add
 *     to URL. See goog.html.TrustedResourceUrl.stringifyParams_ for exact
 *     format definition.
 * @return {!goog.html.TrustedResourceUrl}
 * @throws {!Error} On an invalid format string or if a label used in the
 *     the format string is not present in args.
 */
goog.html.TrustedResourceUrl.formatWithParams = function(
    format, args, searchParams, opt_hashParams) {
  'use strict';
  var url = goog.html.TrustedResourceUrl.format(format, args);
  return url.cloneWithParams(searchParams, opt_hashParams);
};


/**
 * Creates a TrustedResourceUrl object from a compile-time constant string.
 *
 * Compile-time constant strings are inherently program-controlled and hence
 * trusted.
 *
 * @param {!goog.string.Const} url A compile-time-constant string from which to
 *     create a TrustedResourceUrl.
 * @return {!goog.html.TrustedResourceUrl} A TrustedResourceUrl object
 *     initialized to `url`.
 */
goog.html.TrustedResourceUrl.fromConstant = function(url) {
  'use strict';
  return goog.html.TrustedResourceUrl
      .createTrustedResourceUrlSecurityPrivateDoNotAccessOrElse(
          goog.string.Const.unwrap(url));
};


/**
 * Creates a TrustedResourceUrl object from a compile-time constant strings.
 *
 * Compile-time constant strings are inherently program-controlled and hence
 * trusted.
 *
 * @param {!Array<!goog.string.Const>} parts Compile-time-constant strings from
 *     which to create a TrustedResourceUrl.
 * @return {!goog.html.TrustedResourceUrl} A TrustedResourceUrl object
 *     initialized to concatenation of `parts`.
 */
goog.html.TrustedResourceUrl.fromConstants = function(parts) {
  'use strict';
  var unwrapped = '';
  for (var i = 0; i < parts.length; i++) {
    unwrapped += goog.string.Const.unwrap(parts[i]);
  }
  return goog.html.TrustedResourceUrl
      .createTrustedResourceUrlSecurityPrivateDoNotAccessOrElse(unwrapped);
};

/**
 * Creates a TrustedResourceUrl object by generating a Blob from a SafeScript
 * object and then calling createObjectURL with that blob.
 *
 * SafeScript objects are trusted to contain executable JavaScript code.
 *
 * Caller must call goog.fs.url.revokeObjectUrl() on the unwrapped url to
 * release the underlying blob.
 *
 * Throws if browser doesn't support blob construction.
 *
 * @param {!goog.html.SafeScript} safeScript A script from which to create a
 *     TrustedResourceUrl.
 * @return {!goog.html.TrustedResourceUrl} A TrustedResourceUrl object
 *     initialized to a new blob URL.
 */
goog.html.TrustedResourceUrl.fromSafeScript = function(safeScript) {
  'use strict';
  var blob = goog.fs.blob.getBlobWithProperties(
      [goog.html.SafeScript.unwrap(safeScript)], 'text/javascript');
  var url = goog.fs.url.createObjectUrl(blob);
  return goog.html.TrustedResourceUrl
      .createTrustedResourceUrlSecurityPrivateDoNotAccessOrElse(url);
};


/**
 * Token used to ensure that object is created only from this file. No code
 * outside of this file can access this token.
 * @private {!Object}
 * @const
 */
goog.html.TrustedResourceUrl.CONSTRUCTOR_TOKEN_PRIVATE_ = {};


/**
 * Package-internal utility method to create TrustedResourceUrl instances.
 *
 * @param {string} url The string to initialize the TrustedResourceUrl object
 *     with.
 * @return {!goog.html.TrustedResourceUrl} The initialized TrustedResourceUrl
 *     object.
 * @package
 */
goog.html.TrustedResourceUrl
    .createTrustedResourceUrlSecurityPrivateDoNotAccessOrElse = function(url) {
  'use strict';
  const policy = goog.html.trustedtypes.getPolicyPrivateDoNotAccessOrElse();
  var value = policy ? policy.createScriptURL(url) : url;
  return new goog.html.TrustedResourceUrl(
      value, goog.html.TrustedResourceUrl.CONSTRUCTOR_TOKEN_PRIVATE_);
};


/**
 * Stringifies the passed params to be used as either a search or hash field of
 * a URL.
 *
 * @param {string} prefix The prefix character for the given field ('?' or '#').
 * @param {string} currentString The existing field value (including the prefix
 *     character, if the field is present).
 * @param {string|?Object<string, *>|undefined} params The params to set or
 *     append to the field.
 * - If `undefined` or `null`, the field remains unchanged.
 * - If a string, then the string will be escaped and the field will be
 *   overwritten with that value.
 * - If an Object, that object is treated as a set of key-value pairs to be
 *   appended to the current field. Note that JavaScript doesn't guarantee the
 *   order of values in an object which might result in non-deterministic order
 *   of the parameters. However, browsers currently preserve the order. The
 *   rules for each entry:
 *   - If an array, it will be processed as if each entry were an additional
 *     parameter with exactly the same key, following the same logic below.
 *   - If `undefined` or `null`, it will be skipped.
 *   - Otherwise, it will be turned into a string, escaped, and appended.
 * @return {string}
 * @private
 */
goog.html.TrustedResourceUrl.stringifyParams_ = function(
    prefix, currentString, params) {
  'use strict';
  if (params == null) {
    // Do not modify the field.
    return currentString;
  }
  if (typeof params === 'string') {
    // Set field to the passed string.
    return params ? prefix + encodeURIComponent(params) : '';
  }
  // Add on parameters to field from key-value object.
  for (var key in params) {
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/hasOwnProperty#Using_hasOwnProperty_as_a_property_name
    if (Object.prototype.hasOwnProperty.call(params, key)) {
      var value = params[key];
      var outputValues = Array.isArray(value) ? value : [value];
      for (var i = 0; i < outputValues.length; i++) {
        var outputValue = outputValues[i];
        if (outputValue != null) {
          if (!currentString) {
            currentString = prefix;
          }
          currentString += (currentString.length > prefix.length ? '&' : '') +
              encodeURIComponent(key) + '=' +
              encodeURIComponent(String(outputValue));
        }
      }
    }
  }
  return currentString;
};

//third_party/javascript/closure/string/internal.js
/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview String functions called from Closure packages that couldn't
 * depend on each other. Outside Closure, use goog.string function which
 * delegate to these.
 */


goog.provide('goog.string.internal');


/**
 * Fast prefix-checker.
 * @param {string} str The string to check.
 * @param {string} prefix A string to look for at the start of `str`.
 * @return {boolean} True if `str` begins with `prefix`.
 * @see goog.string.startsWith
 */
goog.string.internal.startsWith = function(str, prefix) {
  'use strict';
  return str.lastIndexOf(prefix, 0) == 0;
};


/**
 * Fast suffix-checker.
 * @param {string} str The string to check.
 * @param {string} suffix A string to look for at the end of `str`.
 * @return {boolean} True if `str` ends with `suffix`.
 * @see goog.string.endsWith
 */
goog.string.internal.endsWith = function(str, suffix) {
  'use strict';
  const l = str.length - suffix.length;
  return l >= 0 && str.indexOf(suffix, l) == l;
};


/**
 * Case-insensitive prefix-checker.
 * @param {string} str The string to check.
 * @param {string} prefix  A string to look for at the end of `str`.
 * @return {boolean} True if `str` begins with `prefix` (ignoring
 *     case).
 * @see goog.string.caseInsensitiveStartsWith
 */
goog.string.internal.caseInsensitiveStartsWith = function(str, prefix) {
  'use strict';
  return goog.string.internal.caseInsensitiveCompare(
             prefix, str.substr(0, prefix.length)) == 0;
};


/**
 * Case-insensitive suffix-checker.
 * @param {string} str The string to check.
 * @param {string} suffix A string to look for at the end of `str`.
 * @return {boolean} True if `str` ends with `suffix` (ignoring
 *     case).
 * @see goog.string.caseInsensitiveEndsWith
 */
goog.string.internal.caseInsensitiveEndsWith = function(str, suffix) {
  'use strict';
  return (
      goog.string.internal.caseInsensitiveCompare(
          suffix, str.substr(str.length - suffix.length, suffix.length)) == 0);
};


/**
 * Case-insensitive equality checker.
 * @param {string} str1 First string to check.
 * @param {string} str2 Second string to check.
 * @return {boolean} True if `str1` and `str2` are the same string,
 *     ignoring case.
 * @see goog.string.caseInsensitiveEquals
 */
goog.string.internal.caseInsensitiveEquals = function(str1, str2) {
  'use strict';
  return str1.toLowerCase() == str2.toLowerCase();
};


/**
 * Checks if a string is empty or contains only whitespaces.
 * @param {string} str The string to check.
 * @return {boolean} Whether `str` is empty or whitespace only.
 * @see goog.string.isEmptyOrWhitespace
 */
goog.string.internal.isEmptyOrWhitespace = function(str) {
  'use strict';
  // testing length == 0 first is actually slower in all browsers (about the
  // same in Opera).
  // Since IE doesn't include non-breaking-space (0xa0) in their \s character
  // class (as required by section 7.2 of the ECMAScript spec), we explicitly
  // include it in the regexp to enforce consistent cross-browser behavior.
  return /^[\s\xa0]*$/.test(str);
};


/**
 * Trims white spaces to the left and right of a string.
 * @param {string} str The string to trim.
 * @return {string} A trimmed copy of `str`.
 */
goog.string.internal.trim =
    (goog.TRUSTED_SITE && String.prototype.trim) ? function(str) {
      'use strict';
      return str.trim();
    } : function(str) {
      'use strict';
      // Since IE doesn't include non-breaking-space (0xa0) in their \s
      // character class (as required by section 7.2 of the ECMAScript spec),
      // we explicitly include it in the regexp to enforce consistent
      // cross-browser behavior.
      // NOTE: We don't use String#replace because it might have side effects
      // causing this function to not compile to 0 bytes.
      return /^[\s\xa0]*([\s\S]*?)[\s\xa0]*$/.exec(str)[1];
    };


/**
 * A string comparator that ignores case.
 * -1 = str1 less than str2
 *  0 = str1 equals str2
 *  1 = str1 greater than str2
 *
 * @param {string} str1 The string to compare.
 * @param {string} str2 The string to compare `str1` to.
 * @return {number} The comparator result, as described above.
 * @see goog.string.caseInsensitiveCompare
 */
goog.string.internal.caseInsensitiveCompare = function(str1, str2) {
  'use strict';
  const test1 = String(str1).toLowerCase();
  const test2 = String(str2).toLowerCase();

  if (test1 < test2) {
    return -1;
  } else if (test1 == test2) {
    return 0;
  } else {
    return 1;
  }
};


/**
 * Converts \n to <br>s or <br />s.
 * @param {string} str The string in which to convert newlines.
 * @param {boolean=} opt_xml Whether to use XML compatible tags.
 * @return {string} A copy of `str` with converted newlines.
 * @see goog.string.newLineToBr
 */
goog.string.internal.newLineToBr = function(str, opt_xml) {
  'use strict';
  return str.replace(/(\r\n|\r|\n)/g, opt_xml ? '<br />' : '<br>');
};


/**
 * Escapes double quote '"' and single quote '\'' characters in addition to
 * '&', '<', and '>' so that a string can be included in an HTML tag attribute
 * value within double or single quotes.
 * @param {string} str string to be escaped.
 * @param {boolean=} opt_isLikelyToContainHtmlChars
 * @return {string} An escaped copy of `str`.
 * @see goog.string.htmlEscape
 */
goog.string.internal.htmlEscape = function(
    str, opt_isLikelyToContainHtmlChars) {
  'use strict';
  if (opt_isLikelyToContainHtmlChars) {
    str = str.replace(goog.string.internal.AMP_RE_, '&amp;')
              .replace(goog.string.internal.LT_RE_, '&lt;')
              .replace(goog.string.internal.GT_RE_, '&gt;')
              .replace(goog.string.internal.QUOT_RE_, '&quot;')
              .replace(goog.string.internal.SINGLE_QUOTE_RE_, '&#39;')
              .replace(goog.string.internal.NULL_RE_, '&#0;');
    return str;

  } else {
    // quick test helps in the case when there are no chars to replace, in
    // worst case this makes barely a difference to the time taken
    if (!goog.string.internal.ALL_RE_.test(str)) return str;

    // str.indexOf is faster than regex.test in this case
    if (str.indexOf('&') != -1) {
      str = str.replace(goog.string.internal.AMP_RE_, '&amp;');
    }
    if (str.indexOf('<') != -1) {
      str = str.replace(goog.string.internal.LT_RE_, '&lt;');
    }
    if (str.indexOf('>') != -1) {
      str = str.replace(goog.string.internal.GT_RE_, '&gt;');
    }
    if (str.indexOf('"') != -1) {
      str = str.replace(goog.string.internal.QUOT_RE_, '&quot;');
    }
    if (str.indexOf('\'') != -1) {
      str = str.replace(goog.string.internal.SINGLE_QUOTE_RE_, '&#39;');
    }
    if (str.indexOf('\x00') != -1) {
      str = str.replace(goog.string.internal.NULL_RE_, '&#0;');
    }
    return str;
  }
};


/**
 * Regular expression that matches an ampersand, for use in escaping.
 * @const {!RegExp}
 * @private
 */
goog.string.internal.AMP_RE_ = /&/g;


/**
 * Regular expression that matches a less than sign, for use in escaping.
 * @const {!RegExp}
 * @private
 */
goog.string.internal.LT_RE_ = /</g;


/**
 * Regular expression that matches a greater than sign, for use in escaping.
 * @const {!RegExp}
 * @private
 */
goog.string.internal.GT_RE_ = />/g;


/**
 * Regular expression that matches a double quote, for use in escaping.
 * @const {!RegExp}
 * @private
 */
goog.string.internal.QUOT_RE_ = /"/g;


/**
 * Regular expression that matches a single quote, for use in escaping.
 * @const {!RegExp}
 * @private
 */
goog.string.internal.SINGLE_QUOTE_RE_ = /'/g;


/**
 * Regular expression that matches null character, for use in escaping.
 * @const {!RegExp}
 * @private
 */
goog.string.internal.NULL_RE_ = /\x00/g;


/**
 * Regular expression that matches any character that needs to be escaped.
 * @const {!RegExp}
 * @private
 */
goog.string.internal.ALL_RE_ = /[\x00&<>"']/;


/**
 * Do escaping of whitespace to preserve spatial formatting. We use character
 * entity #160 to make it safer for xml.
 * @param {string} str The string in which to escape whitespace.
 * @param {boolean=} opt_xml Whether to use XML compatible tags.
 * @return {string} An escaped copy of `str`.
 * @see goog.string.whitespaceEscape
 */
goog.string.internal.whitespaceEscape = function(str, opt_xml) {
  'use strict';
  // This doesn't use goog.string.preserveSpaces for backwards compatibility.
  return goog.string.internal.newLineToBr(
      str.replace(/  /g, ' &#160;'), opt_xml);
};


/**
 * Determines whether a string contains a substring.
 * @param {string} str The string to search.
 * @param {string} subString The substring to search for.
 * @return {boolean} Whether `str` contains `subString`.
 * @see goog.string.contains
 */
goog.string.internal.contains = function(str, subString) {
  'use strict';
  return str.indexOf(subString) != -1;
};


/**
 * Determines whether a string contains a substring, ignoring case.
 * @param {string} str The string to search.
 * @param {string} subString The substring to search for.
 * @return {boolean} Whether `str` contains `subString`.
 * @see goog.string.caseInsensitiveContains
 */
goog.string.internal.caseInsensitiveContains = function(str, subString) {
  'use strict';
  return goog.string.internal.contains(
      str.toLowerCase(), subString.toLowerCase());
};


/**
 * Compares two version numbers.
 *
 * @param {string|number} version1 Version of first item.
 * @param {string|number} version2 Version of second item.
 *
 * @return {number}  1 if `version1` is higher.
 *                   0 if arguments are equal.
 *                  -1 if `version2` is higher.
 * @see goog.string.compareVersions
 */
goog.string.internal.compareVersions = function(version1, version2) {
  'use strict';
  let order = 0;
  // Trim leading and trailing whitespace and split the versions into
  // subversions.
  const v1Subs = goog.string.internal.trim(String(version1)).split('.');
  const v2Subs = goog.string.internal.trim(String(version2)).split('.');
  const subCount = Math.max(v1Subs.length, v2Subs.length);

  // Iterate over the subversions, as long as they appear to be equivalent.
  for (let subIdx = 0; order == 0 && subIdx < subCount; subIdx++) {
    let v1Sub = v1Subs[subIdx] || '';
    let v2Sub = v2Subs[subIdx] || '';

    do {
      // Split the subversions into pairs of numbers and qualifiers (like 'b').
      // Two different RegExp objects are use to make it clear the code
      // is side-effect free
      const v1Comp = /(\d*)(\D*)(.*)/.exec(v1Sub) || ['', '', '', ''];
      const v2Comp = /(\d*)(\D*)(.*)/.exec(v2Sub) || ['', '', '', ''];
      // Break if there are no more matches.
      if (v1Comp[0].length == 0 && v2Comp[0].length == 0) {
        break;
      }

      // Parse the numeric part of the subversion. A missing number is
      // equivalent to 0.
      const v1CompNum = v1Comp[1].length == 0 ? 0 : parseInt(v1Comp[1], 10);
      const v2CompNum = v2Comp[1].length == 0 ? 0 : parseInt(v2Comp[1], 10);

      // Compare the subversion components. The number has the highest
      // precedence. Next, if the numbers are equal, a subversion without any
      // qualifier is always higher than a subversion with any qualifier. Next,
      // the qualifiers are compared as strings.
      order = goog.string.internal.compareElements_(v1CompNum, v2CompNum) ||
          goog.string.internal.compareElements_(
              v1Comp[2].length == 0, v2Comp[2].length == 0) ||
          goog.string.internal.compareElements_(v1Comp[2], v2Comp[2]);
      // Stop as soon as an inequality is discovered.

      v1Sub = v1Comp[3];
      v2Sub = v2Comp[3];
    } while (order == 0);
  }

  return order;
};


/**
 * Compares elements of a version number.
 *
 * @param {string|number|boolean} left An element from a version number.
 * @param {string|number|boolean} right An element from a version number.
 *
 * @return {number}  1 if `left` is higher.
 *                   0 if arguments are equal.
 *                  -1 if `right` is higher.
 * @private
 */
goog.string.internal.compareElements_ = function(left, right) {
  'use strict';
  if (left < right) {
    return -1;
  } else if (left > right) {
    return 1;
  }
  return 0;
};

//third_party/javascript/closure/html/safeurl.js
/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview The SafeUrl type and its builders.
 *
 * TODO(xtof): Link to document stating type contract.
 */

goog.provide('goog.html.SafeUrl');

goog.require('goog.asserts');
goog.require('goog.fs.url');
goog.require('goog.html.TrustedResourceUrl');
goog.require('goog.i18n.bidi.Dir');
goog.require('goog.i18n.bidi.DirectionalString');
goog.require('goog.string.Const');
goog.require('goog.string.TypedString');
goog.require('goog.string.internal');



/**
 * A string that is safe to use in URL context in DOM APIs and HTML documents.
 *
 * A SafeUrl is a string-like object that carries the security type contract
 * that its value as a string will not cause untrusted script execution
 * when evaluated as a hyperlink URL in a browser.
 *
 * Values of this type are guaranteed to be safe to use in URL/hyperlink
 * contexts, such as assignment to URL-valued DOM properties, in the sense that
 * the use will not result in a Cross-Site-Scripting vulnerability. Similarly,
 * SafeUrls can be interpolated into the URL context of an HTML template (e.g.,
 * inside a href attribute). However, appropriate HTML-escaping must still be
 * applied.
 *
 * Note that, as documented in `goog.html.SafeUrl.unwrap`, this type's
 * contract does not guarantee that instances are safe to interpolate into HTML
 * without appropriate escaping.
 *
 * Note also that this type's contract does not imply any guarantees regarding
 * the resource the URL refers to.  In particular, SafeUrls are <b>not</b>
 * safe to use in a context where the referred-to resource is interpreted as
 * trusted code, e.g., as the src of a script tag.
 *
 * Instances of this type must be created via the factory methods
 * (`goog.html.SafeUrl.fromConstant`, `goog.html.SafeUrl.sanitize`),
 * etc and not by invoking its constructor. The constructor intentionally takes
 * an extra parameter that cannot be constructed outside of this file and the
 * type is immutable; hence only a default instance corresponding to the empty
 * string can be obtained via constructor invocation.
 *
 * @see goog.html.SafeUrl#fromConstant
 * @see goog.html.SafeUrl#from
 * @see goog.html.SafeUrl#sanitize
 * @final
 * @struct
 * @implements {goog.i18n.bidi.DirectionalString}
 * @implements {goog.string.TypedString}
 */
goog.html.SafeUrl = class {
  /**
   * @param {string} value
   * @param {!Object} token package-internal implementation detail.
   */
  constructor(value, token) {
    /**
     * The contained value of this SafeUrl.  The field has a purposely ugly
     * name to make (non-compiled) code that attempts to directly access this
     * field stand out.
     * @private {string}
     */
    this.privateDoNotAccessOrElseSafeUrlWrappedValue_ =
        (token === goog.html.SafeUrl.CONSTRUCTOR_TOKEN_PRIVATE_) ? value : '';
  };
};


/**
 * The innocuous string generated by goog.html.SafeUrl.sanitize when passed
 * an unsafe URL.
 *
 * about:invalid is registered in
 * http://www.w3.org/TR/css3-values/#about-invalid.
 * http://tools.ietf.org/html/rfc6694#section-2.2.1 permits about URLs to
 * contain a fragment, which is not to be considered when determining if an
 * about URL is well-known.
 *
 * Using about:invalid seems preferable to using a fixed data URL, since
 * browsers might choose to not report CSP violations on it, as legitimate
 * CSS function calls to attr() can result in this URL being produced. It is
 * also a standard URL which matches exactly the semantics we need:
 * "The about:invalid URI references a non-existent document with a generic
 * error condition. It can be used when a URI is necessary, but the default
 * value shouldn't be resolveable as any type of document".
 *
 * @const {string}
 */
goog.html.SafeUrl.INNOCUOUS_STRING = 'about:invalid#zClosurez';


/**
 * @override
 * @const
 */
goog.html.SafeUrl.prototype.implementsGoogStringTypedString = true;


/**
 * Returns this SafeUrl's value as a string.
 *
 * IMPORTANT: In code where it is security relevant that an object's type is
 * indeed `SafeUrl`, use `goog.html.SafeUrl.unwrap` instead of this
 * method. If in doubt, assume that it's security relevant. In particular, note
 * that goog.html functions which return a goog.html type do not guarantee that
 * the returned instance is of the right type.
 *
 * IMPORTANT: The guarantees of the SafeUrl type contract only extend to the
 * behavior of browsers when interpreting URLs. Values of SafeUrl objects MUST
 * be appropriately escaped before embedding in a HTML document. Note that the
 * required escaping is context-sensitive (e.g. a different escaping is
 * required for embedding a URL in a style property within a style
 * attribute, as opposed to embedding in a href attribute).
 *
 * @see goog.html.SafeUrl#unwrap
 * @override
 */
goog.html.SafeUrl.prototype.getTypedStringValue = function() {
  'use strict';
  return this.privateDoNotAccessOrElseSafeUrlWrappedValue_.toString();
};


/**
 * @override
 * @const {boolean}
 */
goog.html.SafeUrl.prototype.implementsGoogI18nBidiDirectionalString = true;


/**
 * Returns this URLs directionality, which is always `LTR`.
 * @override
 * @return {!goog.i18n.bidi.Dir}
 */
goog.html.SafeUrl.prototype.getDirection = function() {
  'use strict';
  return goog.i18n.bidi.Dir.LTR;
};


/**
 * Returns a string-representation of this value.
 *
 * To obtain the actual string value wrapped in a SafeUrl, use
 * `goog.html.SafeUrl.unwrap`.
 *
 * @return {string}
 * @see goog.html.SafeUrl#unwrap
 * @override
 */
goog.html.SafeUrl.prototype.toString = function() {
  'use strict';
  return this.privateDoNotAccessOrElseSafeUrlWrappedValue_.toString();
};



/**
 * Performs a runtime check that the provided object is indeed a SafeUrl
 * object, and returns its value.
 *
 * IMPORTANT: The guarantees of the SafeUrl type contract only extend to the
 * behavior of  browsers when interpreting URLs. Values of SafeUrl objects MUST
 * be appropriately escaped before embedding in a HTML document. Note that the
 * required escaping is context-sensitive (e.g. a different escaping is
 * required for embedding a URL in a style property within a style
 * attribute, as opposed to embedding in a href attribute).
 *
 * @param {!goog.html.SafeUrl} safeUrl The object to extract from.
 * @return {string} The SafeUrl object's contained string, unless the run-time
 *     type check fails. In that case, `unwrap` returns an innocuous
 *     string, or, if assertions are enabled, throws
 *     `goog.asserts.AssertionError`.
 */
goog.html.SafeUrl.unwrap = function(safeUrl) {
  'use strict';
  // Perform additional Run-time type-checking to ensure that safeUrl is indeed
  // an instance of the expected type.  This provides some additional protection
  // against security bugs due to application code that disables type checks.
  // Specifically, the following checks are performed:
  // 1. The object is an instance of the expected type.
  // 2. The object is not an instance of a subclass.
  if (safeUrl instanceof goog.html.SafeUrl &&
      safeUrl.constructor === goog.html.SafeUrl) {
    return safeUrl.privateDoNotAccessOrElseSafeUrlWrappedValue_;
  } else {
    goog.asserts.fail('expected object of type SafeUrl, got \'' +
        safeUrl + '\' of type ' + goog.typeOf(safeUrl));
    return 'type_error:SafeUrl';
  }
};


/**
 * Creates a SafeUrl object from a compile-time constant string.
 *
 * Compile-time constant strings are inherently program-controlled and hence
 * trusted.
 *
 * @param {!goog.string.Const} url A compile-time-constant string from which to
 *         create a SafeUrl.
 * @return {!goog.html.SafeUrl} A SafeUrl object initialized to `url`.
 */
goog.html.SafeUrl.fromConstant = function(url) {
  'use strict';
  return goog.html.SafeUrl.createSafeUrlSecurityPrivateDoNotAccessOrElse(
      goog.string.Const.unwrap(url));
};


/**
 * A pattern that matches Blob or data types that can have SafeUrls created
 * from URL.createObjectURL(blob) or via a data: URI.
 *
 * This has some parameter support (most notably, we haven't implemented the
 * more complex parts like %-encoded characters or non-alphanumerical ones for
 * simplicity's sake). The specs are fairly complex, and they don't
 * always match Chrome's behavior: we settled on a subset where we're confident
 * all parties involved agree.
 *
 * The spec is available at https://mimesniff.spec.whatwg.org/ (and see
 * https://tools.ietf.org/html/rfc2397 for data: urls, which override some of
 * it).
 * @const
 * @private
 */
goog.html.SAFE_MIME_TYPE_PATTERN_ = new RegExp(
    // Note: Due to content-sniffing concerns, only add MIME types for
    // media formats.
    '^(?:audio/(?:3gpp2|3gpp|aac|L16|midi|mp3|mp4|mpeg|oga|ogg|opus|x-m4a|x-matroska|x-wav|wav|webm)|' +
        'font/\\w+|' +
        'image/(?:bmp|gif|jpeg|jpg|png|tiff|webp|x-icon)|' +
        'video/(?:mpeg|mp4|ogg|webm|quicktime|x-matroska))' +
        '(?:;\\w+=(?:\\w+|"[\\w;,= ]+"))*$',  // MIME type parameters
    'i');


/**
 * @param {string} mimeType The MIME type to check if safe.
 * @return {boolean} True if the MIME type is safe and creating a Blob via
 *   `SafeUrl.fromBlob()` with that type will not fail due to the type. False
 *   otherwise.
 */
goog.html.SafeUrl.isSafeMimeType = function(mimeType) {
  'use strict';
  return goog.html.SAFE_MIME_TYPE_PATTERN_.test(mimeType);
};


/**
 * Creates a SafeUrl wrapping a blob URL for the given `blob`.
 *
 * The blob URL is created with `URL.createObjectURL`. If the MIME type
 * for `blob` is not of a known safe audio, image or video MIME type,
 * then the SafeUrl will wrap {@link #INNOCUOUS_STRING}.
 *
 * Note: Call {@link revokeObjectUrl} on the URL after it's used
 * to prevent memory leaks.
 *
 * @see http://www.w3.org/TR/FileAPI/#url
 * @param {!Blob} blob
 * @return {!goog.html.SafeUrl} The blob URL, or an innocuous string wrapped
 *   as a SafeUrl.
 */
goog.html.SafeUrl.fromBlob = function(blob) {
  'use strict';
  var url = goog.html.SafeUrl.isSafeMimeType(blob.type) ?
      goog.fs.url.createObjectUrl(blob) :
      goog.html.SafeUrl.INNOCUOUS_STRING;
  return goog.html.SafeUrl.createSafeUrlSecurityPrivateDoNotAccessOrElse(url);
};


/**
 * Revokes an object URL created for a safe URL created {@link fromBlob()}.
 * @param {!goog.html.SafeUrl} safeUrl SafeUrl wrapping a blob object.
 * @return {void}
 */
goog.html.SafeUrl.revokeObjectUrl = function(safeUrl) {
  'use strict';
  var url = safeUrl.getTypedStringValue();
  if (url !== goog.html.SafeUrl.INNOCUOUS_STRING) {
    goog.fs.url.revokeObjectUrl(url);
  }
};


/**
 * Creates a SafeUrl wrapping a blob URL created for a MediaSource.
 * @param {!MediaSource} mediaSource
 * @return {!goog.html.SafeUrl} The blob URL.
 */
goog.html.SafeUrl.fromMediaSource = function(mediaSource) {
  'use strict';
  goog.asserts.assert(
      'MediaSource' in goog.global, 'No support for MediaSource');
  const url = mediaSource instanceof MediaSource ?
      goog.fs.url.createObjectUrl(mediaSource) :
      goog.html.SafeUrl.INNOCUOUS_STRING;
  return goog.html.SafeUrl.createSafeUrlSecurityPrivateDoNotAccessOrElse(url);
};


/**
 * Matches a base-64 data URL, with the first match group being the MIME type.
 * @const
 * @private
 */
goog.html.DATA_URL_PATTERN_ = /^data:(.*);base64,[a-z0-9+\/]+=*$/i;


/**
 * Attempts to create a SafeUrl wrapping a `data:` URL, after validating it
 * matches a known-safe media MIME type. If it doesn't match, return `null`.
 *
 * @param {string} dataUrl A valid base64 data URL with one of the whitelisted
 *     media MIME types.
 * @return {?goog.html.SafeUrl} A matching safe URL, or `null` if it does not
 *     pass.
 */
goog.html.SafeUrl.tryFromDataUrl = function(dataUrl) {
  'use strict';
  // For defensive purposes, in case users cast around the parameter type.
  dataUrl = String(dataUrl);
  // RFC4648 suggest to ignore CRLF in base64 encoding.
  // See https://tools.ietf.org/html/rfc4648.
  // Remove the CR (%0D) and LF (%0A) from the dataUrl.
  var filteredDataUrl = dataUrl.replace(/(%0A|%0D)/g, '');
  var match = filteredDataUrl.match(goog.html.DATA_URL_PATTERN_);
  // Note: The only risk of XSS here is if the `data:` URL results in a
  // same-origin document. In which case content-sniffing might cause the
  // browser to interpret the contents as html.
  // All modern browsers consider `data:` URL documents to have unique empty
  // origins. Only Firefox for versions prior to v57 behaves differently:
  // https://blog.mozilla.org/security/2017/10/04/treating-data-urls-unique-origins-firefox-57/
  // Older versions of IE don't understand `data:` urls, so it is not an issue.
  var valid = match && goog.html.SafeUrl.isSafeMimeType(match[1]);
  if (valid) {
    return goog.html.SafeUrl.createSafeUrlSecurityPrivateDoNotAccessOrElse(
        filteredDataUrl);
  }
  return null;
};


/**
 * Creates a SafeUrl wrapping a `data:` URL, after validating it matches a
 * known-safe media MIME type. If it doesn't match, return
 * `goog.html.SafeUrl.INNOCUOUS_URL`.
 *
 * @param {string} dataUrl A valid base64 data URL with one of the whitelisted
 *     media MIME types.
 * @return {!goog.html.SafeUrl} A matching safe URL, or
 *     `goog.html.SafeUrl.INNOCUOUS_URL` if it does not pass.
 */
goog.html.SafeUrl.fromDataUrl = function(dataUrl) {
  'use strict';
  return goog.html.SafeUrl.tryFromDataUrl(dataUrl) ||
      goog.html.SafeUrl.INNOCUOUS_URL;
};


/**
 * Creates a SafeUrl wrapping a tel: URL.
 *
 * @param {string} telUrl A tel URL.
 * @return {!goog.html.SafeUrl} A matching safe URL, or {@link INNOCUOUS_STRING}
 *     wrapped as a SafeUrl if it does not pass.
 */
goog.html.SafeUrl.fromTelUrl = function(telUrl) {
  'use strict';
  // There's a risk that a tel: URL could immediately place a call once
  // clicked, without requiring user confirmation. For that reason it is
  // handled in this separate function.
  if (!goog.string.internal.caseInsensitiveStartsWith(telUrl, 'tel:')) {
    telUrl = goog.html.SafeUrl.INNOCUOUS_STRING;
  }
  return goog.html.SafeUrl.createSafeUrlSecurityPrivateDoNotAccessOrElse(
      telUrl);
};


/**
 * Matches a sip/sips URL. We only allow urls that consist of an email address.
 * The characters '?' and '#' are not allowed in the local part of the email
 * address.
 * @const
 * @private
 */
goog.html.SIP_URL_PATTERN_ = new RegExp(
    '^sip[s]?:[+a-z0-9_.!$%&\'*\\/=^`{|}~-]+@([a-z0-9-]+\\.)+[a-z0-9]{2,63}$',
    'i');


/**
 * Creates a SafeUrl wrapping a sip: URL. We only allow urls that consist of an
 * email address. The characters '?' and '#' are not allowed in the local part
 * of the email address.
 *
 * @param {string} sipUrl A sip URL.
 * @return {!goog.html.SafeUrl} A matching safe URL, or {@link INNOCUOUS_STRING}
 *     wrapped as a SafeUrl if it does not pass.
 */
goog.html.SafeUrl.fromSipUrl = function(sipUrl) {
  'use strict';
  if (!goog.html.SIP_URL_PATTERN_.test(decodeURIComponent(sipUrl))) {
    sipUrl = goog.html.SafeUrl.INNOCUOUS_STRING;
  }
  return goog.html.SafeUrl.createSafeUrlSecurityPrivateDoNotAccessOrElse(
      sipUrl);
};


/**
 * Creates a SafeUrl wrapping a fb-messenger://share URL.
 *
 * @param {string} facebookMessengerUrl A facebook messenger URL.
 * @return {!goog.html.SafeUrl} A matching safe URL, or {@link INNOCUOUS_STRING}
 *     wrapped as a SafeUrl if it does not pass.
 */
goog.html.SafeUrl.fromFacebookMessengerUrl = function(facebookMessengerUrl) {
  'use strict';
  if (!goog.string.internal.caseInsensitiveStartsWith(
          facebookMessengerUrl, 'fb-messenger://share')) {
    facebookMessengerUrl = goog.html.SafeUrl.INNOCUOUS_STRING;
  }
  return goog.html.SafeUrl.createSafeUrlSecurityPrivateDoNotAccessOrElse(
      facebookMessengerUrl);
};

/**
 * Creates a SafeUrl wrapping a whatsapp://send URL.
 *
 * @param {string} whatsAppUrl A WhatsApp URL.
 * @return {!goog.html.SafeUrl} A matching safe URL, or {@link INNOCUOUS_STRING}
 *     wrapped as a SafeUrl if it does not pass.
 */
goog.html.SafeUrl.fromWhatsAppUrl = function(whatsAppUrl) {
  'use strict';
  if (!goog.string.internal.caseInsensitiveStartsWith(
          whatsAppUrl, 'whatsapp://send')) {
    whatsAppUrl = goog.html.SafeUrl.INNOCUOUS_STRING;
  }
  return goog.html.SafeUrl.createSafeUrlSecurityPrivateDoNotAccessOrElse(
      whatsAppUrl);
};

/**
 * Creates a SafeUrl wrapping a sms: URL.
 *
 * @param {string} smsUrl A sms URL.
 * @return {!goog.html.SafeUrl} A matching safe URL, or {@link INNOCUOUS_STRING}
 *     wrapped as a SafeUrl if it does not pass.
 */
goog.html.SafeUrl.fromSmsUrl = function(smsUrl) {
  'use strict';
  if (!goog.string.internal.caseInsensitiveStartsWith(smsUrl, 'sms:') ||
      !goog.html.SafeUrl.isSmsUrlBodyValid_(smsUrl)) {
    smsUrl = goog.html.SafeUrl.INNOCUOUS_STRING;
  }
  return goog.html.SafeUrl.createSafeUrlSecurityPrivateDoNotAccessOrElse(
      smsUrl);
};


/**
 * Validates SMS URL `body` parameter, which is optional and should appear at
 * most once and should be percent-encoded if present. Rejects many malformed
 * bodies, but may spuriously reject some URLs and does not reject all malformed
 * sms: URLs.
 *
 * @param {string} smsUrl A sms URL.
 * @return {boolean} Whether SMS URL has a valid `body` parameter if it exists.
 * @private
 */
goog.html.SafeUrl.isSmsUrlBodyValid_ = function(smsUrl) {
  'use strict';
  var hash = smsUrl.indexOf('#');
  if (hash > 0) {
    smsUrl = smsUrl.substring(0, hash);
  }
  var bodyParams = smsUrl.match(/[?&]body=/gi);
  // "body" param is optional
  if (!bodyParams) {
    return true;
  }
  // "body" MUST only appear once
  if (bodyParams.length > 1) {
    return false;
  }
  // Get the encoded `body` parameter value.
  var bodyValue = smsUrl.match(/[?&]body=([^&]*)/)[1];
  if (!bodyValue) {
    return true;
  }
  try {
    decodeURIComponent(bodyValue);
  } catch (error) {
    return false;
  }
  return /^(?:[a-z0-9\-_.~]|%[0-9a-f]{2})+$/i.test(bodyValue);
};


/**
 * Creates a SafeUrl wrapping a ssh: URL.
 *
 * @param {string} sshUrl A ssh URL.
 * @return {!goog.html.SafeUrl} A matching safe URL, or {@link INNOCUOUS_STRING}
 *     wrapped as a SafeUrl if it does not pass.
 */
goog.html.SafeUrl.fromSshUrl = function(sshUrl) {
  'use strict';
  if (!goog.string.internal.caseInsensitiveStartsWith(sshUrl, 'ssh://')) {
    sshUrl = goog.html.SafeUrl.INNOCUOUS_STRING;
  }
  return goog.html.SafeUrl.createSafeUrlSecurityPrivateDoNotAccessOrElse(
      sshUrl);
};

/**
 * Sanitizes a Chrome extension URL to SafeUrl, given a compile-time-constant
 * extension identifier. Can also be restricted to chrome extensions.
 *
 * @param {string} url The url to sanitize. Should start with the extension
 *     scheme and the extension identifier.
 * @param {!goog.string.Const|!Array<!goog.string.Const>} extensionId The
 *     extension id to accept, as a compile-time constant or an array of those.
 *
 * @return {!goog.html.SafeUrl} Either `url` if it's deemed safe, or
 *     `INNOCUOUS_STRING` if it's not.
 */
goog.html.SafeUrl.sanitizeChromeExtensionUrl = function(url, extensionId) {
  'use strict';
  return goog.html.SafeUrl.sanitizeExtensionUrl_(
      /^chrome-extension:\/\/([^\/]+)\//, url, extensionId);
};

/**
 * Sanitizes a Firefox extension URL to SafeUrl, given a compile-time-constant
 * extension identifier. Can also be restricted to chrome extensions.
 *
 * @param {string} url The url to sanitize. Should start with the extension
 *     scheme and the extension identifier.
 * @param {!goog.string.Const|!Array<!goog.string.Const>} extensionId The
 *     extension id to accept, as a compile-time constant or an array of those.
 *
 * @return {!goog.html.SafeUrl} Either `url` if it's deemed safe, or
 *     `INNOCUOUS_STRING` if it's not.
 */
goog.html.SafeUrl.sanitizeFirefoxExtensionUrl = function(url, extensionId) {
  'use strict';
  return goog.html.SafeUrl.sanitizeExtensionUrl_(
      /^moz-extension:\/\/([^\/]+)\//, url, extensionId);
};

/**
 * Sanitizes a Edge extension URL to SafeUrl, given a compile-time-constant
 * extension identifier. Can also be restricted to chrome extensions.
 *
 * @param {string} url The url to sanitize. Should start with the extension
 *     scheme and the extension identifier.
 * @param {!goog.string.Const|!Array<!goog.string.Const>} extensionId The
 *     extension id to accept, as a compile-time constant or an array of those.
 *
 * @return {!goog.html.SafeUrl} Either `url` if it's deemed safe, or
 *     `INNOCUOUS_STRING` if it's not.
 */
goog.html.SafeUrl.sanitizeEdgeExtensionUrl = function(url, extensionId) {
  'use strict';
  return goog.html.SafeUrl.sanitizeExtensionUrl_(
      /^ms-browser-extension:\/\/([^\/]+)\//, url, extensionId);
};

/**
 * Private helper for converting extension URLs to SafeUrl, given the scheme for
 * that particular extension type. Use the sanitizeFirefoxExtensionUrl,
 * sanitizeChromeExtensionUrl or sanitizeEdgeExtensionUrl unless you're building
 * new helpers.
 *
 * @private
 * @param {!RegExp} scheme The scheme to accept as a RegExp extracting the
 *     extension identifier.
 * @param {string} url The url to sanitize. Should start with the extension
 *     scheme and the extension identifier.
 * @param {!goog.string.Const|!Array<!goog.string.Const>} extensionId The
 *     extension id to accept, as a compile-time constant or an array of those.
 *
 * @return {!goog.html.SafeUrl} Either `url` if it's deemed safe, or
 *     `INNOCUOUS_STRING` if it's not.
 */
goog.html.SafeUrl.sanitizeExtensionUrl_ = function(scheme, url, extensionId) {
  'use strict';
  var matches = scheme.exec(url);
  if (!matches) {
    url = goog.html.SafeUrl.INNOCUOUS_STRING;
  } else {
    var extractedExtensionId = matches[1];
    var acceptedExtensionIds;
    if (extensionId instanceof goog.string.Const) {
      acceptedExtensionIds = [goog.string.Const.unwrap(extensionId)];
    } else {
      acceptedExtensionIds = extensionId.map(function unwrap(x) {
        'use strict';
        return goog.string.Const.unwrap(x);
      });
    }
    if (acceptedExtensionIds.indexOf(extractedExtensionId) == -1) {
      url = goog.html.SafeUrl.INNOCUOUS_STRING;
    }
  }
  return goog.html.SafeUrl.createSafeUrlSecurityPrivateDoNotAccessOrElse(url);
};


/**
 * Creates a SafeUrl from TrustedResourceUrl. This is safe because
 * TrustedResourceUrl is more tightly restricted than SafeUrl.
 *
 * @param {!goog.html.TrustedResourceUrl} trustedResourceUrl
 * @return {!goog.html.SafeUrl}
 */
goog.html.SafeUrl.fromTrustedResourceUrl = function(trustedResourceUrl) {
  'use strict';
  return goog.html.SafeUrl.createSafeUrlSecurityPrivateDoNotAccessOrElse(
      goog.html.TrustedResourceUrl.unwrap(trustedResourceUrl));
};


/**
 * A pattern that recognizes a commonly useful subset of URLs that satisfy
 * the SafeUrl contract.
 *
 * This regular expression matches a subset of URLs that will not cause script
 * execution if used in URL context within a HTML document. Specifically, this
 * regular expression matches if (comment from here on and regex copied from
 * Soy's EscapingConventions):
 * (1) Either a protocol in a whitelist (http, https, mailto or ftp).
 * (2) or no protocol.  A protocol must be followed by a colon. The below
 *     allows that by allowing colons only after one of the characters [/?#].
 *     A colon after a hash (#) must be in the fragment.
 *     Otherwise, a colon after a (?) must be in a query.
 *     Otherwise, a colon after a single solidus (/) must be in a path.
 *     Otherwise, a colon after a double solidus (//) must be in the authority
 *     (before port).
 *
 * @private
 * @const {!RegExp}
 */
goog.html.SAFE_URL_PATTERN_ =
    /^(?:(?:https?|mailto|ftp):|[^:/?#]*(?:[/?#]|$))/i;

/**
 * Public version of goog.html.SAFE_URL_PATTERN_. Updating
 * goog.html.SAFE_URL_PATTERN_ doesn't seem to be backward compatible.
 * Namespace is also changed to goog.html.SafeUrl so it can be imported using
 * goog.require('goog.dom.SafeUrl').
 *
 * TODO(bangert): Remove SAFE_URL_PATTERN_
 * @const {!RegExp}
 */
goog.html.SafeUrl.SAFE_URL_PATTERN = goog.html.SAFE_URL_PATTERN_;

/**
 * Attempts to create a SafeUrl object from `url`. The input string is validated
 * to match a pattern of commonly used safe URLs. If validation fails, `null` is
 * returned.
 *
 * `url` may be a URL with the `http:`, `https:`, `mailto:`, `ftp:` or `data`
 * scheme, or a relative URL (i.e., a URL without a scheme; specifically, a
 * scheme-relative, absolute-path-relative, or path-relative URL).
 *
 * @see http://url.spec.whatwg.org/#concept-relative-url
 * @param {string|!goog.string.TypedString} url The URL to validate.
 * @return {?goog.html.SafeUrl} The validated URL, wrapped as a SafeUrl, or null
 *     if validation fails.
 */
goog.html.SafeUrl.trySanitize = function(url) {
  'use strict';
  if (url instanceof goog.html.SafeUrl) {
    return url;
  }
  if (typeof url == 'object' && url.implementsGoogStringTypedString) {
    url = /** @type {!goog.string.TypedString} */ (url).getTypedStringValue();
  } else {
    // For defensive purposes, in case users cast around the parameter type.
    url = String(url);
  }
  if (!goog.html.SAFE_URL_PATTERN_.test(url)) {
    return goog.html.SafeUrl.tryFromDataUrl(url);
  }
  return goog.html.SafeUrl.createSafeUrlSecurityPrivateDoNotAccessOrElse(url);
};

/**
 * Creates a SafeUrl object from `url`. If `url` is a
 * `goog.html.SafeUrl` then it is simply returned. Otherwise the input string is
 * validated to match a pattern of commonly used safe URLs. If validation fails,
 * `goog.html.SafeUrl.INNOCUOUS_URL` is returned.
 *
 * `url` may be a URL with the `http:`, `https:`, `mailto:`, `ftp:` or `data`
 * scheme, or a relative URL (i.e., a URL without a scheme; specifically, a
 * scheme-relative, absolute-path-relative, or path-relative URL).
 *
 * @see http://url.spec.whatwg.org/#concept-relative-url
 * @param {string|!goog.string.TypedString} url The URL to validate.
 * @return {!goog.html.SafeUrl} The validated URL, wrapped as a SafeUrl.
 */
goog.html.SafeUrl.sanitize = function(url) {
  'use strict';
  return goog.html.SafeUrl.trySanitize(url) || goog.html.SafeUrl.INNOCUOUS_URL;
};

/**
 * Creates a SafeUrl object from `url`. If `url` is a
 * `goog.html.SafeUrl` then it is simply returned. Otherwise the input string is
 * validated to match a pattern of commonly used safe URLs.
 *
 * `url` may be a URL with the http, https, mailto or ftp scheme,
 * or a relative URL (i.e., a URL without a scheme; specifically, a
 * scheme-relative, absolute-path-relative, or path-relative URL).
 *
 * This function asserts (using goog.asserts) that the URL matches this pattern.
 * If it does not, in addition to failing the assert, an innocuous URL will be
 * returned.
 *
 * @see http://url.spec.whatwg.org/#concept-relative-url
 * @param {string|!goog.string.TypedString} url The URL to validate.
 * @param {boolean=} opt_allowDataUrl Whether to allow valid data: URLs.
 * @return {!goog.html.SafeUrl} The validated URL, wrapped as a SafeUrl.
 */
goog.html.SafeUrl.sanitizeAssertUnchanged = function(url, opt_allowDataUrl) {
  'use strict';
  if (url instanceof goog.html.SafeUrl) {
    return url;
  } else if (typeof url == 'object' && url.implementsGoogStringTypedString) {
    url = /** @type {!goog.string.TypedString} */ (url).getTypedStringValue();
  } else {
    url = String(url);
  }
  if (opt_allowDataUrl && /^data:/i.test(url)) {
    var safeUrl = goog.html.SafeUrl.fromDataUrl(url);
    if (safeUrl.getTypedStringValue() == url) {
      return safeUrl;
    }
  }
  if (!goog.asserts.assert(
          goog.html.SAFE_URL_PATTERN_.test(url),
          '%s does not match the safe URL pattern', url)) {
    url = goog.html.SafeUrl.INNOCUOUS_STRING;
  }
  return goog.html.SafeUrl.createSafeUrlSecurityPrivateDoNotAccessOrElse(url);
};

/**
 * Token used to ensure that object is created only from this file. No code
 * outside of this file can access this token.
 * @private {!Object}
 * @const
 */
goog.html.SafeUrl.CONSTRUCTOR_TOKEN_PRIVATE_ = {};

/**
 * Package-internal utility method to create SafeUrl instances.
 *
 * @param {string} url The string to initialize the SafeUrl object with.
 * @return {!goog.html.SafeUrl} The initialized SafeUrl object.
 * @package
 */
goog.html.SafeUrl.createSafeUrlSecurityPrivateDoNotAccessOrElse = function(
    url) {
  'use strict';
  return new goog.html.SafeUrl(
      url, goog.html.SafeUrl.CONSTRUCTOR_TOKEN_PRIVATE_);
};


/**
 * `INNOCUOUS_STRING` wrapped in a `SafeUrl`.
 * @const {!goog.html.SafeUrl}
 */
goog.html.SafeUrl.INNOCUOUS_URL =
    goog.html.SafeUrl.createSafeUrlSecurityPrivateDoNotAccessOrElse(
        goog.html.SafeUrl.INNOCUOUS_STRING);


/**
 * A SafeUrl corresponding to the special about:blank url.
 * @const {!goog.html.SafeUrl}
 */
goog.html.SafeUrl.ABOUT_BLANK =
    goog.html.SafeUrl.createSafeUrlSecurityPrivateDoNotAccessOrElse(
        'about:blank');

//third_party/javascript/closure/html/safestyle.js
goog.loadModule(function(exports) {'use strict';/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview The SafeStyle type and its builders.
 *
 * TODO(xtof): Link to document stating type contract.
 */

goog.module('goog.html.SafeStyle');
goog.module.declareLegacyNamespace();

const Const = goog.require('goog.string.Const');
const SafeUrl = goog.require('goog.html.SafeUrl');
const TypedString = goog.require('goog.string.TypedString');
const {AssertionError, assert, fail} = goog.require('goog.asserts');
const {contains, endsWith} = goog.require('goog.string.internal');

/**
 * Token used to ensure that object is created only from this file. No code
 * outside of this file can access this token.
 * @type {!Object}
 * @const
 */
const CONSTRUCTOR_TOKEN_PRIVATE = {};

/**
 * A string-like object which represents a sequence of CSS declarations
 * (`propertyName1: propertyvalue1; propertyName2: propertyValue2; ...`)
 * and that carries the security type contract that its value, as a string,
 * will not cause untrusted script execution (XSS) when evaluated as CSS in a
 * browser.
 *
 * Instances of this type must be created via the factory methods
 * (`SafeStyle.create` or `SafeStyle.fromConstant`)
 * and not by invoking its constructor. The constructor intentionally takes an
 * extra parameter that cannot be constructed outside of this file and the type
 * is immutable; hence only a default instance corresponding to the empty string
 * can be obtained via constructor invocation.
 *
 * SafeStyle's string representation can safely be:
 * <ul>
 *   <li>Interpolated as the content of a *quoted* HTML style attribute.
 *       However, the SafeStyle string *must be HTML-attribute-escaped* before
 *       interpolation.
 *   <li>Interpolated as the content of a {}-wrapped block within a stylesheet.
 *       '<' characters in the SafeStyle string *must be CSS-escaped* before
 *       interpolation. The SafeStyle string is also guaranteed not to be able
 *       to introduce new properties or elide existing ones.
 *   <li>Interpolated as the content of a {}-wrapped block within an HTML
 *       &lt;style&gt; element. '<' characters in the SafeStyle string
 *       *must be CSS-escaped* before interpolation.
 *   <li>Assigned to the style property of a DOM node. The SafeStyle string
 *       should not be escaped before being assigned to the property.
 * </ul>
 *
 * A SafeStyle may never contain literal angle brackets. Otherwise, it could
 * be unsafe to place a SafeStyle into a &lt;style&gt; tag (where it can't
 * be HTML escaped). For example, if the SafeStyle containing
 * `font: 'foo &lt;style/&gt;&lt;script&gt;evil&lt;/script&gt;'` were
 * interpolated within a &lt;style&gt; tag, this would then break out of the
 * style context into HTML.
 *
 * A SafeStyle may contain literal single or double quotes, and as such the
 * entire style string must be escaped when used in a style attribute (if
 * this were not the case, the string could contain a matching quote that
 * would escape from the style attribute).
 *
 * Values of this type must be composable, i.e. for any two values
 * `style1` and `style2` of this type,
 * `SafeStyle.unwrap(style1) +
 * SafeStyle.unwrap(style2)` must itself be a value that satisfies
 * the SafeStyle type constraint. This requirement implies that for any value
 * `style` of this type, `SafeStyle.unwrap(style)` must
 * not end in a "property value" or "property name" context. For example,
 * a value of `background:url("` or `font-` would not satisfy the
 * SafeStyle contract. This is because concatenating such strings with a
 * second value that itself does not contain unsafe CSS can result in an
 * overall string that does. For example, if `javascript:evil())"` is
 * appended to `background:url("}, the resulting string may result in
 * the execution of a malicious script.
 *
 * TODO(mlourenco): Consider whether we should implement UTF-8 interchange
 * validity checks and blacklisting of newlines (including Unicode ones) and
 * other whitespace characters (\t, \f). Document here if so and also update
 * SafeStyle.fromConstant().
 *
 * The following example values comply with this type's contract:
 * <ul>
 *   <li><pre>width: 1em;</pre>
 *   <li><pre>height:1em;</pre>
 *   <li><pre>width: 1em;height: 1em;</pre>
 *   <li><pre>background:url('http://url');</pre>
 * </ul>
 * In addition, the empty string is safe for use in a CSS attribute.
 *
 * The following example values do NOT comply with this type's contract:
 * <ul>
 *   <li><pre>background: red</pre> (missing a trailing semi-colon)
 *   <li><pre>background:</pre> (missing a value and a trailing semi-colon)
 *   <li><pre>1em</pre> (missing an attribute name, which provides context for
 *       the value)
 * </ul>
 *
 * @see SafeStyle#create
 * @see SafeStyle#fromConstant
 * @see http://www.w3.org/TR/css3-syntax/
 * @final
 * @struct
 * @implements {TypedString}
 */
class SafeStyle {
  /**
   * @param {string} value
   * @param {!Object} token package-internal implementation detail.
   */
  constructor(value, token) {
    /**
     * The contained value of this SafeStyle.  The field has a purposely
     * ugly name to make (non-compiled) code that attempts to directly access
     * this field stand out.
     * @private {string}
     */
    this.privateDoNotAccessOrElseSafeStyleWrappedValue_ =
        (token === CONSTRUCTOR_TOKEN_PRIVATE) ? value : '';

    /**
     * @override
     * @const {boolean}
     */
    this.implementsGoogStringTypedString = true;
  }


  /**
   * Creates a SafeStyle object from a compile-time constant string.
   *
   * `style` should be in the format
   * `name: value; [name: value; ...]` and must not have any < or >
   * characters in it. This is so that SafeStyle's contract is preserved,
   * allowing the SafeStyle to correctly be interpreted as a sequence of CSS
   * declarations and without affecting the syntactic structure of any
   * surrounding CSS and HTML.
   *
   * This method performs basic sanity checks on the format of `style`
   * but does not constrain the format of `name` and `value`, except
   * for disallowing tag characters.
   *
   * @param {!Const} style A compile-time-constant string from which
   *     to create a SafeStyle.
   * @return {!SafeStyle} A SafeStyle object initialized to
   *     `style`.
   */
  static fromConstant(style) {
    'use strict';
    const styleString = Const.unwrap(style);
    if (styleString.length === 0) {
      return SafeStyle.EMPTY;
    }
    assert(
        endsWith(styleString, ';'),
        `Last character of style string is not ';': ${styleString}`);
    assert(
        contains(styleString, ':'),
        'Style string must contain at least one \':\', to ' +
            'specify a "name: value" pair: ' + styleString);
    return SafeStyle.createSafeStyleSecurityPrivateDoNotAccessOrElse(
        styleString);
  };


  /**
   * Returns this SafeStyle's value as a string.
   *
   * IMPORTANT: In code where it is security relevant that an object's type is
   * indeed `SafeStyle`, use `SafeStyle.unwrap` instead of
   * this method. If in doubt, assume that it's security relevant. In
   * particular, note that goog.html functions which return a goog.html type do
   * not guarantee the returned instance is of the right type. For example:
   *
   * <pre>
   * var fakeSafeHtml = new String('fake');
   * fakeSafeHtml.__proto__ = goog.html.SafeHtml.prototype;
   * var newSafeHtml = goog.html.SafeHtml.htmlEscape(fakeSafeHtml);
   * // newSafeHtml is just an alias for fakeSafeHtml, it's passed through by
   * // goog.html.SafeHtml.htmlEscape() as fakeSafeHtml
   * // instanceof goog.html.SafeHtml.
   * </pre>
   *
   * @return {string}
   * @see SafeStyle#unwrap
   * @override
   */
  getTypedStringValue() {
    'use strict';
    return this.privateDoNotAccessOrElseSafeStyleWrappedValue_;
  }


  /**
   * Returns a string-representation of this value.
   *
   * To obtain the actual string value wrapped in a SafeStyle, use
   * `SafeStyle.unwrap`.
   *
   * @return {string}
   * @see SafeStyle#unwrap
   * @override
   */
  toString() {
    'use strict';
    return this.privateDoNotAccessOrElseSafeStyleWrappedValue_.toString();
  }


  /**
   * Performs a runtime check that the provided object is indeed a
   * SafeStyle object, and returns its value.
   *
   * @param {!SafeStyle} safeStyle The object to extract from.
   * @return {string} The safeStyle object's contained string, unless
   *     the run-time type check fails. In that case, `unwrap` returns an
   *     innocuous string, or, if assertions are enabled, throws
   *     `AssertionError`.
   */
  static unwrap(safeStyle) {
    'use strict';
    // Perform additional Run-time type-checking to ensure that
    // safeStyle is indeed an instance of the expected type.  This
    // provides some additional protection against security bugs due to
    // application code that disables type checks.
    // Specifically, the following checks are performed:
    // 1. The object is an instance of the expected type.
    // 2. The object is not an instance of a subclass.
    if (safeStyle instanceof SafeStyle && safeStyle.constructor === SafeStyle) {
      return safeStyle.privateDoNotAccessOrElseSafeStyleWrappedValue_;
    } else {
      fail(
          `expected object of type SafeStyle, got '${safeStyle}` +
          '\' of type ' + goog.typeOf(safeStyle));
      return 'type_error:SafeStyle';
    }
  }


  /**
   * Package-internal utility method to create SafeStyle instances.
   *
   * @param {string} style The string to initialize the SafeStyle object with.
   * @return {!SafeStyle} The initialized SafeStyle object.
   * @package
   */
  static createSafeStyleSecurityPrivateDoNotAccessOrElse(style) {
    'use strict';
    return new SafeStyle(style, CONSTRUCTOR_TOKEN_PRIVATE);
  }

  /**
   * Creates a new SafeStyle object from the properties specified in the map.
   * @param {!SafeStyle.PropertyMap} map Mapping of property names to
   *     their values, for example {'margin': '1px'}. Names must consist of
   *     [-_a-zA-Z0-9]. Values might be strings consisting of
   *     [-,.'"%_!# a-zA-Z0-9[\]], where ", ', and [] must be properly balanced.
   *     We also allow simple functions like rgb() and url() which sanitizes its
   *     contents. Other values must be wrapped in Const. URLs might
   *     be passed as SafeUrl which will be wrapped into url(""). We
   *     also support array whose elements are joined with ' '. Null value
   * causes skipping the property.
   * @return {!SafeStyle}
   * @throws {!Error} If invalid name is provided.
   * @throws {!AssertionError} If invalid value is provided. With
   *     disabled assertions, invalid value is replaced by
   *     SafeStyle.INNOCUOUS_STRING.
   */
  static create(map) {
    'use strict';
    let style = '';
    for (let name in map) {
      // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/hasOwnProperty#Using_hasOwnProperty_as_a_property_name
      if (Object.prototype.hasOwnProperty.call(map, name)) {
        if (!/^[-_a-zA-Z0-9]+$/.test(name)) {
          throw new Error(`Name allows only [-_a-zA-Z0-9], got: ${name}`);
        }
        let value = map[name];
        if (value == null) {
          continue;
        }
        if (Array.isArray(value)) {
          value = value.map(sanitizePropertyValue).join(' ');
        } else {
          value = sanitizePropertyValue(value);
        }
        style += `${name}:${value};`;
      }
    }
    if (!style) {
      return SafeStyle.EMPTY;
    }
    return SafeStyle.createSafeStyleSecurityPrivateDoNotAccessOrElse(style);
  };

  /**
   * Creates a new SafeStyle object by concatenating the values.
   * @param {...(!SafeStyle|!Array<!SafeStyle>)} var_args
   *     SafeStyles to concatenate.
   * @return {!SafeStyle}
   */
  static concat(var_args) {
    'use strict';
    let style = '';

    /**
     * @param {!SafeStyle|!Array<!SafeStyle>} argument
     */
    const addArgument = argument => {
      'use strict';
      if (Array.isArray(argument)) {
        argument.forEach(addArgument);
      } else {
        style += SafeStyle.unwrap(argument);
      }
    };

    Array.prototype.forEach.call(arguments, addArgument);
    if (!style) {
      return SafeStyle.EMPTY;
    }
    return SafeStyle.createSafeStyleSecurityPrivateDoNotAccessOrElse(style);
  };
}

/**
 * A SafeStyle instance corresponding to the empty string.
 * @const {!SafeStyle}
 */
SafeStyle.EMPTY = SafeStyle.createSafeStyleSecurityPrivateDoNotAccessOrElse('');


/**
 * The innocuous string generated by SafeStyle.create when passed
 * an unsafe value.
 * @const {string}
 */
SafeStyle.INNOCUOUS_STRING = 'zClosurez';


/**
 * A single property value.
 * @typedef {string|!Const|!SafeUrl}
 */
SafeStyle.PropertyValue;


/**
 * Mapping of property names to their values.
 * We don't support numbers even though some values might be numbers (e.g.
 * line-height or 0 for any length). The reason is that most numeric values need
 * units (e.g. '1px') and allowing numbers could cause users forgetting about
 * them.
 * @typedef {!Object<string, ?SafeStyle.PropertyValue|
 *     ?Array<!SafeStyle.PropertyValue>>}
 */
SafeStyle.PropertyMap;



/**
 * Checks and converts value to string.
 * @param {!SafeStyle.PropertyValue} value
 * @return {string}
 */
function sanitizePropertyValue(value) {
  'use strict';
  if (value instanceof SafeUrl) {
    const url = SafeUrl.unwrap(value);
    return 'url("' + url.replace(/</g, '%3c').replace(/[\\"]/g, '\\$&') + '")';
  }
  const result = value instanceof Const ?
      Const.unwrap(value) :
      sanitizePropertyValueString(String(value));
  // These characters can be used to change context and we don't want that even
  // with const values.
  if (/[{;}]/.test(result)) {
    throw new AssertionError('Value does not allow [{;}], got: %s.', [result]);
  }
  return result;
}


/**
 * Checks string value.
 * @param {string} value
 * @return {string}
 */
function sanitizePropertyValueString(value) {
  'use strict';
  // Some CSS property values permit nested functions. We allow one level of
  // nesting, and all nested functions must also be in the FUNCTIONS_RE_ list.
  const valueWithoutFunctions = value.replace(FUNCTIONS_RE, '$1')
                                    .replace(FUNCTIONS_RE, '$1')
                                    .replace(URL_RE, 'url');
  if (!VALUE_RE.test(valueWithoutFunctions)) {
    fail(
        `String value allows only ${VALUE_ALLOWED_CHARS}` +
        ' and simple functions, got: ' + value);
    return SafeStyle.INNOCUOUS_STRING;
  } else if (COMMENT_RE.test(value)) {
    fail(`String value disallows comments, got: ${value}`);
    return SafeStyle.INNOCUOUS_STRING;
  } else if (!hasBalancedQuotes(value)) {
    fail(`String value requires balanced quotes, got: ${value}`);
    return SafeStyle.INNOCUOUS_STRING;
  } else if (!hasBalancedSquareBrackets(value)) {
    fail(
        'String value requires balanced square brackets and one' +
        ' identifier per pair of brackets, got: ' + value);
    return SafeStyle.INNOCUOUS_STRING;
  }
  return sanitizeUrl(value);
}


/**
 * Checks that quotes (" and ') are properly balanced inside a string. Assumes
 * that neither escape (\) nor any other character that could result in
 * breaking out of a string parsing context are allowed;
 * see http://www.w3.org/TR/css3-syntax/#string-token-diagram.
 * @param {string} value Untrusted CSS property value.
 * @return {boolean} True if property value is safe with respect to quote
 *     balancedness.
 */
function hasBalancedQuotes(value) {
  'use strict';
  let outsideSingle = true;
  let outsideDouble = true;
  for (let i = 0; i < value.length; i++) {
    const c = value.charAt(i);
    if (c == '\'' && outsideDouble) {
      outsideSingle = !outsideSingle;
    } else if (c == '"' && outsideSingle) {
      outsideDouble = !outsideDouble;
    }
  }
  return outsideSingle && outsideDouble;
}


/**
 * Checks that square brackets ([ and ]) are properly balanced inside a string,
 * and that the content in the square brackets is one ident-token;
 * see https://www.w3.org/TR/css-syntax-3/#ident-token-diagram.
 * For practicality, and in line with other restrictions posed on SafeStyle
 * strings, we restrict the character set allowable in the ident-token to
 * [-_a-zA-Z0-9].
 * @param {string} value Untrusted CSS property value.
 * @return {boolean} True if property value is safe with respect to square
 *     bracket balancedness.
 */
function hasBalancedSquareBrackets(value) {
  'use strict';
  let outside = true;
  const tokenRe = /^[-_a-zA-Z0-9]$/;
  for (let i = 0; i < value.length; i++) {
    const c = value.charAt(i);
    if (c == ']') {
      if (outside) return false;  // Unbalanced ].
      outside = true;
    } else if (c == '[') {
      if (!outside) return false;  // No nesting.
      outside = false;
    } else if (!outside && !tokenRe.test(c)) {
      return false;
    }
  }
  return outside;
}


/**
 * Characters allowed in VALUE_RE.
 * @type {string}
 */
const VALUE_ALLOWED_CHARS = '[-,."\'%_!# a-zA-Z0-9\\[\\]]';


/**
 * Regular expression for safe values.
 * Quotes (" and ') are allowed, but a check must be done elsewhere to ensure
 * they're balanced.
 * Square brackets ([ and ]) are allowed, but a check must be done elsewhere
 * to ensure they're balanced. The content inside a pair of square brackets must
 * be one alphanumeric identifier.
 * ',' allows multiple values to be assigned to the same property
 * (e.g. background-attachment or font-family) and hence could allow
 * multiple values to get injected, but that should pose no risk of XSS.
 * The expression checks only for XSS safety, not for CSS validity.
 * @const {!RegExp}
 */
const VALUE_RE = new RegExp(`^${VALUE_ALLOWED_CHARS}+\$`);


/**
 * Regular expression for url(). We support URLs allowed by
 * https://www.w3.org/TR/css-syntax-3/#url-token-diagram without using escape
 * sequences. Use percent-encoding if you need to use special characters like
 * backslash.
 * @const {!RegExp}
 */
const URL_RE = new RegExp(
    '\\b(url\\([ \t\n]*)(' +
        '\'[ -&(-\\[\\]-~]*\'' +  // Printable characters except ' and \.
        '|"[ !#-\\[\\]-~]*"' +    // Printable characters except " and \.
        '|[!#-&*-\\[\\]-~]*' +    // Printable characters except [ "'()\\].
        ')([ \t\n]*\\))',
    'g');

/**
 * Names of functions allowed in FUNCTIONS_RE.
 * @const {!Array<string>}
 */
const ALLOWED_FUNCTIONS = [
  'calc',
  'cubic-bezier',
  'fit-content',
  'hsl',
  'hsla',
  'linear-gradient',
  'matrix',
  'minmax',
  'repeat',
  'rgb',
  'rgba',
  '(rotate|scale|translate)(X|Y|Z|3d)?',
  'var',
];


/**
 * Regular expression for simple functions.
 * @const {!RegExp}
 */
const FUNCTIONS_RE = new RegExp(
    '\\b(' + ALLOWED_FUNCTIONS.join('|') + ')' +
        '\\([-+*/0-9a-z.%\\[\\], ]+\\)',
    'g');


/**
 * Regular expression for comments. These are disallowed in CSS property values.
 * @const {!RegExp}
 */
const COMMENT_RE = /\/\*/;


/**
 * Sanitize URLs inside url().
 * NOTE: We could also consider using CSS.escape once that's available in the
 * browsers. However, loosely matching URL e.g. with url\(.*\) and then escaping
 * the contents would result in a slightly different language than CSS leading
 * to confusion of users. E.g. url(")") is valid in CSS but it would be invalid
 * as seen by our parser. On the other hand, url(\) is invalid in CSS but our
 * parser would be fine with it.
 * @param {string} value Untrusted CSS property value.
 * @return {string}
 */
function sanitizeUrl(value) {
  'use strict';
  return value.replace(URL_RE, (match, before, url, after) => {
    'use strict';
    let quote = '';
    url = url.replace(/^(['"])(.*)\1$/, (match, start, inside) => {
      'use strict';
      quote = start;
      return inside;
    });
    const sanitized = SafeUrl.sanitize(url).getTypedStringValue();
    return before + quote + sanitized + quote + after;
  });
}


exports = SafeStyle;

;return exports;});

//third_party/javascript/closure/html/safestylesheet.js
goog.loadModule(function(exports) {'use strict';/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview The SafeStyleSheet type and its builders.
 *
 * TODO(xtof): Link to document stating type contract.
 */

goog.module('goog.html.SafeStyleSheet');
goog.module.declareLegacyNamespace();

const Const = goog.require('goog.string.Const');
const SafeStyle = goog.require('goog.html.SafeStyle');
const TypedString = goog.require('goog.string.TypedString');
const googObject = goog.require('goog.object');
const {assert, fail} = goog.require('goog.asserts');
const {contains} = goog.require('goog.string.internal');

/**
 * Token used to ensure that object is created only from this file. No code
 * outside of this file can access this token.
 * @const {!Object}
 */
const CONSTRUCTOR_TOKEN_PRIVATE = {};

/**
 * A string-like object which represents a CSS style sheet and that carries the
 * security type contract that its value, as a string, will not cause untrusted
 * script execution (XSS) when evaluated as CSS in a browser.
 *
 * Instances of this type must be created via the factory method
 * `SafeStyleSheet.fromConstant` and not by invoking its constructor. The
 * constructor intentionally takes an extra parameter that cannot be constructed
 * outside of this file and the type is immutable; hence only a default instance
 * corresponding to the empty string can be obtained via constructor invocation.
 *
 * A SafeStyleSheet's string representation can safely be interpolated as the
 * content of a style element within HTML. The SafeStyleSheet string should
 * not be escaped before interpolation.
 *
 * Values of this type must be composable, i.e. for any two values
 * `styleSheet1` and `styleSheet2` of this type,
 * `SafeStyleSheet.unwrap(styleSheet1) + SafeStyleSheet.unwrap(styleSheet2)`
 * must itself be a value that satisfies the SafeStyleSheet type constraint.
 * This requirement implies that for any value `styleSheet` of this type,
 * `SafeStyleSheet.unwrap(styleSheet1)` must end in
 * "beginning of rule" context.
 *
 * A SafeStyleSheet can be constructed via security-reviewed unchecked
 * conversions. In this case producers of SafeStyleSheet must ensure themselves
 * that the SafeStyleSheet does not contain unsafe script. Note in particular
 * that `&lt;` is dangerous, even when inside CSS strings, and so should
 * always be forbidden or CSS-escaped in user controlled input. For example, if
 * `&lt;/style&gt;&lt;script&gt;evil&lt;/script&gt;"` were interpolated
 * inside a CSS string, it would break out of the context of the original
 * style element and `evil` would execute. Also note that within an HTML
 * style (raw text) element, HTML character references, such as
 * `&amp;lt;`, are not allowed. See
 * http://www.w3.org/TR/html5/scripting-1.html#restrictions-for-contents-of-script-elements
 * (similar considerations apply to the style element).
 *
 * @see SafeStyleSheet#fromConstant
 * @final
 * @implements {TypedString}
 */
class SafeStyleSheet {
  /**
   * @param {string} value
   * @param {!Object} token package-internal implementation detail.
   */
  constructor(value, token) {
    /**
     * The contained value of this SafeStyleSheet.  The field has a purposely
     * ugly name to make (non-compiled) code that attempts to directly access
     * this field stand out.
     * @private {string}
     */
    this.privateDoNotAccessOrElseSafeStyleSheetWrappedValue_ =
        (token === CONSTRUCTOR_TOKEN_PRIVATE) ? value : '';

    /**
     * @override
     * @const
     */
    this.implementsGoogStringTypedString = true;
  }

  /**
   * Creates a style sheet consisting of one selector and one style definition.
   * Use {@link SafeStyleSheet.concat} to create longer style sheets.
   * This function doesn't support @import, @media and similar constructs.
   * @param {string} selector CSS selector, e.g. '#id' or 'tag .class, #id'. We
   *     support CSS3 selectors: https://w3.org/TR/css3-selectors/#selectors.
   * @param {!SafeStyle.PropertyMap|!SafeStyle} style Style
   *     definition associated with the selector.
   * @return {!SafeStyleSheet}
   * @throws {!Error} If invalid selector is provided.
   */
  static createRule(selector, style) {
    if (contains(selector, '<')) {
      throw new Error(`Selector does not allow '<', got: ${selector}`);
    }

    // Remove strings.
    const selectorToCheck =
        selector.replace(/('|")((?!\1)[^\r\n\f\\]|\\[\s\S])*\1/g, '');

    // Check characters allowed in CSS3 selectors.
    if (!/^[-_a-zA-Z0-9#.:* ,>+~[\]()=^$|]+$/.test(selectorToCheck)) {
      throw new Error(
          'Selector allows only [-_a-zA-Z0-9#.:* ,>+~[\\]()=^$|] and ' +
          'strings, got: ' + selector);
    }

    // Check balanced () and [].
    if (!SafeStyleSheet.hasBalancedBrackets_(selectorToCheck)) {
      throw new Error(
          '() and [] in selector must be balanced, got: ' + selector);
    }

    if (!(style instanceof SafeStyle)) {
      style = SafeStyle.create(style);
    }
    const styleSheet =
        `${selector}{` + SafeStyle.unwrap(style).replace(/</g, '\\3C ') + '}';
    return SafeStyleSheet.createSafeStyleSheetSecurityPrivateDoNotAccessOrElse(
        styleSheet);
  }

  /**
   * Checks if a string has balanced () and [] brackets.
   * @param {string} s String to check.
   * @return {boolean}
   * @private
   */
  static hasBalancedBrackets_(s) {
    const brackets = {'(': ')', '[': ']'};
    const expectedBrackets = [];
    for (let i = 0; i < s.length; i++) {
      const ch = s[i];
      if (brackets[ch]) {
        expectedBrackets.push(brackets[ch]);
      } else if (googObject.contains(brackets, ch)) {
        if (expectedBrackets.pop() != ch) {
          return false;
        }
      }
    }
    return expectedBrackets.length == 0;
  }

  /**
   * Creates a new SafeStyleSheet object by concatenating values.
   * @param {...(!SafeStyleSheet|!Array<!SafeStyleSheet>)}
   *     var_args Values to concatenate.
   * @return {!SafeStyleSheet}
   */
  static concat(var_args) {
    let result = '';

    /**
     * @param {!SafeStyleSheet|!Array<!SafeStyleSheet>}
     *     argument
     */
    const addArgument = argument => {
      if (Array.isArray(argument)) {
        argument.forEach(addArgument);
      } else {
        result += SafeStyleSheet.unwrap(argument);
      }
    };

    Array.prototype.forEach.call(arguments, addArgument);
    return SafeStyleSheet.createSafeStyleSheetSecurityPrivateDoNotAccessOrElse(
        result);
  }

  /**
   * Creates a SafeStyleSheet object from a compile-time constant string.
   *
   * `styleSheet` must not have any &lt; characters in it, so that
   * the syntactic structure of the surrounding HTML is not affected.
   *
   * @param {!Const} styleSheet A compile-time-constant string from
   *     which to create a SafeStyleSheet.
   * @return {!SafeStyleSheet} A SafeStyleSheet object initialized to
   *     `styleSheet`.
   */
  static fromConstant(styleSheet) {
    const styleSheetString = Const.unwrap(styleSheet);
    if (styleSheetString.length === 0) {
      return SafeStyleSheet.EMPTY;
    }
    // > is a valid character in CSS selectors and there's no strict need to
    // block it if we already block <.
    assert(
        !contains(styleSheetString, '<'),
        `Forbidden '<' character in style sheet string: ${styleSheetString}`);
    return SafeStyleSheet.createSafeStyleSheetSecurityPrivateDoNotAccessOrElse(
        styleSheetString);
  }

  /**
   * Returns this SafeStyleSheet's value as a string.
   *
   * IMPORTANT: In code where it is security relevant that an object's type is
   * indeed `SafeStyleSheet`, use `SafeStyleSheet.unwrap`
   * instead of this method. If in doubt, assume that it's security relevant. In
   * particular, note that goog.html functions which return a goog.html type do
   * not guarantee the returned instance is of the right type. For example:
   *
   * <pre>
   * var fakeSafeHtml = new String('fake');
   * fakeSafeHtml.__proto__ = goog.html.SafeHtml.prototype;
   * var newSafeHtml = goog.html.SafeHtml.htmlEscape(fakeSafeHtml);
   * // newSafeHtml is just an alias for fakeSafeHtml, it's passed through by
   * // goog.html.SafeHtml.htmlEscape() as fakeSafeHtml
   * // instanceof goog.html.SafeHtml.
   * </pre>
   *
   * @see SafeStyleSheet#unwrap
   * @override
   */
  getTypedStringValue() {
    return this.privateDoNotAccessOrElseSafeStyleSheetWrappedValue_;
  }

  /**
   * Performs a runtime check that the provided object is indeed a
   * SafeStyleSheet object, and returns its value.
   *
   * @param {!SafeStyleSheet} safeStyleSheet The object to extract from.
   * @return {string} The safeStyleSheet object's contained string, unless
   *     the run-time type check fails. In that case, `unwrap` returns an
   *     innocuous string, or, if assertions are enabled, throws
   *     `asserts.AssertionError`.
   */
  static unwrap(safeStyleSheet) {
    // Perform additional Run-time type-checking to ensure that
    // safeStyleSheet is indeed an instance of the expected type.  This
    // provides some additional protection against security bugs due to
    // application code that disables type checks.
    // Specifically, the following checks are performed:
    // 1. The object is an instance of the expected type.
    // 2. The object is not an instance of a subclass.
    if (safeStyleSheet instanceof SafeStyleSheet &&
        safeStyleSheet.constructor === SafeStyleSheet) {
      return safeStyleSheet.privateDoNotAccessOrElseSafeStyleSheetWrappedValue_;
    } else {
      fail(
          'expected object of type SafeStyleSheet, got \'' + safeStyleSheet +
          '\' of type ' + goog.typeOf(safeStyleSheet));
      return 'type_error:SafeStyleSheet';
    }
  }

  /**
   * Package-internal utility method to create SafeStyleSheet instances.
   *
   * @param {string} styleSheet The string to initialize the SafeStyleSheet
   *     object with.
   * @return {!SafeStyleSheet} The initialized SafeStyleSheet object.
   * @package
   */
  static createSafeStyleSheetSecurityPrivateDoNotAccessOrElse(styleSheet) {
    return new SafeStyleSheet(styleSheet, CONSTRUCTOR_TOKEN_PRIVATE);
  }
}

/**
 * Returns a string-representation of this value.
 *
 * To obtain the actual string value wrapped in a SafeStyleSheet, use
 * `SafeStyleSheet.unwrap`.
 *
 * @return {string}
 * @see SafeStyleSheet#unwrap
 * @override
 */
SafeStyleSheet.prototype.toString = function() {
  return this.privateDoNotAccessOrElseSafeStyleSheetWrappedValue_.toString();
};


/**
 * A SafeStyleSheet instance corresponding to the empty string.
 * @const {!SafeStyleSheet}
 */
SafeStyleSheet.EMPTY =
    SafeStyleSheet.createSafeStyleSheetSecurityPrivateDoNotAccessOrElse('');


exports = SafeStyleSheet;

;return exports;});

//third_party/javascript/closure/labs/useragent/util.js
/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Utilities used by goog.labs.userAgent tools. These functions
 * should not be used outside of goog.labs.userAgent.*.
 *
 */

goog.provide('goog.labs.userAgent.util');

goog.require('goog.string.internal');


/**
 * Gets the native userAgent string from navigator if it exists.
 * If navigator or navigator.userAgent string is missing, returns an empty
 * string.
 * @return {string}
 * @private
 */
goog.labs.userAgent.util.getNativeUserAgentString_ = function() {
  'use strict';
  var navigator = goog.labs.userAgent.util.getNavigator_();
  if (navigator) {
    var userAgent = navigator.userAgent;
    if (userAgent) {
      return userAgent;
    }
  }
  return '';
};


/**
 * Getter for the native navigator.
 * This is a separate function so it can be stubbed out in testing.
 * @return {!Navigator}
 * @private
 */
goog.labs.userAgent.util.getNavigator_ = function() {
  'use strict';
  return goog.global.navigator;
};


/**
 * A possible override for applications which wish to not check
 * navigator.userAgent but use a specified value for detection instead.
 * @private {string}
 */
goog.labs.userAgent.util.userAgent_ =
    goog.labs.userAgent.util.getNativeUserAgentString_();


/**
 * Applications may override browser detection on the built in
 * navigator.userAgent object by setting this string. Set to null to use the
 * browser object instead.
 * @param {?string=} opt_userAgent The User-Agent override.
 * @return {void}
 */
goog.labs.userAgent.util.setUserAgent = function(opt_userAgent) {
  'use strict';
  goog.labs.userAgent.util.userAgent_ =
      opt_userAgent || goog.labs.userAgent.util.getNativeUserAgentString_();
};


/**
 * @return {string} The user agent string.
 */
goog.labs.userAgent.util.getUserAgent = function() {
  'use strict';
  return goog.labs.userAgent.util.userAgent_;
};


/**
 * @param {string} str
 * @return {boolean} Whether the user agent contains the given string.
 */
goog.labs.userAgent.util.matchUserAgent = function(str) {
  'use strict';
  var userAgent = goog.labs.userAgent.util.getUserAgent();
  return goog.string.internal.contains(userAgent, str);
};


/**
 * @param {string} str
 * @return {boolean} Whether the user agent contains the given string, ignoring
 *     case.
 */
goog.labs.userAgent.util.matchUserAgentIgnoreCase = function(str) {
  'use strict';
  var userAgent = goog.labs.userAgent.util.getUserAgent();
  return goog.string.internal.caseInsensitiveContains(userAgent, str);
};


/**
 * Parses the user agent into tuples for each section.
 * @param {string} userAgent
 * @return {!Array<!Array<string>>} Tuples of key, version, and the contents
 *     of the parenthetical.
 */
goog.labs.userAgent.util.extractVersionTuples = function(userAgent) {
  'use strict';
  // Matches each section of a user agent string.
  // Example UA:
  // Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us)
  // AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405
  // This has three version tuples: Mozilla, AppleWebKit, and Mobile.

  var versionRegExp = new RegExp(
      // Key. Note that a key may have a space.
      // (i.e. 'Mobile Safari' in 'Mobile Safari/5.0')
      '(\\w[\\w ]+)' +

          '/' +                // slash
          '([^\\s]+)' +        // version (i.e. '5.0b')
          '\\s*' +             // whitespace
          '(?:\\((.*?)\\))?',  // parenthetical info. parentheses not matched.
      'g');

  var data = [];
  var match;

  // Iterate and collect the version tuples.  Each iteration will be the
  // next regex match.
  while (match = versionRegExp.exec(userAgent)) {
    data.push([
      match[1],  // key
      match[2],  // value
      // || undefined as this is not undefined in IE7 and IE8
      match[3] || undefined  // info
    ]);
  }

  return data;
};

//third_party/javascript/closure/labs/useragent/browser.js
/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * @fileoverview Closure user agent detection (Browser).
 * @see <a href="http://www.useragentstring.com/">User agent strings</a>
 * For more information on rendering engine, platform, or device see the other
 * sub-namespaces in goog.labs.userAgent, goog.labs.userAgent.platform,
 * goog.labs.userAgent.device respectively.)
 */

goog.provide('goog.labs.userAgent.browser');

goog.require('goog.array');
goog.require('goog.labs.userAgent.util');
goog.require('goog.object');
goog.require('goog.string.internal');


// TODO(nnaze): Refactor to remove excessive exclusion logic in matching
// functions.


/**
 * @return {boolean} Whether the user's browser is Opera.  Note: Chromium
 *     based Opera (Opera 15+) is detected as Chrome to avoid unnecessary
 *     special casing.
 * @private
 */
goog.labs.userAgent.browser.matchOpera_ = function() {
  'use strict';
  return goog.labs.userAgent.util.matchUserAgent('Opera');
};


/**
 * @return {boolean} Whether the user's browser is IE.
 * @private
 */
goog.labs.userAgent.browser.matchIE_ = function() {
  'use strict';
  return goog.labs.userAgent.util.matchUserAgent('Trident') ||
      goog.labs.userAgent.util.matchUserAgent('MSIE');
};


/**
 * @return {boolean} Whether the user's browser is Edge. This refers to EdgeHTML
 * based Edge.
 * @private
 */
goog.labs.userAgent.browser.matchEdgeHtml_ = function() {
  'use strict';
  return goog.labs.userAgent.util.matchUserAgent('Edge');
};


/**
 * @return {boolean} Whether the user's browser is Chromium based Edge.
 * @private
 */
goog.labs.userAgent.browser.matchEdgeChromium_ = function() {
  'use strict';
  return goog.labs.userAgent.util.matchUserAgent('Edg/');
};


/**
 * @return {boolean} Whether the user's browser is Chromium based Opera.
 * @private
 */
goog.labs.userAgent.browser.matchOperaChromium_ = function() {
  'use strict';
  return goog.labs.userAgent.util.matchUserAgent('OPR');
};


/**
 * @return {boolean} Whether the user's browser is Firefox.
 * @private
 */
goog.labs.userAgent.browser.matchFirefox_ = function() {
  'use strict';
  return goog.labs.userAgent.util.matchUserAgent('Firefox') ||
      goog.labs.userAgent.util.matchUserAgent('FxiOS');
};


/**
 * @return {boolean} Whether the user's browser is Safari.
 * @private
 */
goog.labs.userAgent.browser.matchSafari_ = function() {
  'use strict';
  return goog.labs.userAgent.util.matchUserAgent('Safari') &&
      !(goog.labs.userAgent.browser.matchChrome_() ||
        goog.labs.userAgent.browser.matchCoast_() ||
        goog.labs.userAgent.browser.matchOpera_() ||
        goog.labs.userAgent.browser.matchEdgeHtml_() ||
        goog.labs.userAgent.browser.matchEdgeChromium_() ||
        goog.labs.userAgent.browser.matchOperaChromium_() ||
        goog.labs.userAgent.browser.matchFirefox_() ||
        goog.labs.userAgent.browser.isSilk() ||
        goog.labs.userAgent.util.matchUserAgent('Android'));
};


/**
 * @return {boolean} Whether the user's browser is Coast (Opera's Webkit-based
 *     iOS browser).
 * @private
 */
goog.labs.userAgent.browser.matchCoast_ = function() {
  'use strict';
  return goog.labs.userAgent.util.matchUserAgent('Coast');
};


/**
 * @return {boolean} Whether the user's browser is iOS Webview.
 * @private
 */
goog.labs.userAgent.browser.matchIosWebview_ = function() {
  'use strict';
  // iOS Webview does not show up as Chrome or Safari. Also check for Opera's
  // WebKit-based iOS browser, Coast.
  return (goog.labs.userAgent.util.matchUserAgent('iPad') ||
          goog.labs.userAgent.util.matchUserAgent('iPhone')) &&
      !goog.labs.userAgent.browser.matchSafari_() &&
      !goog.labs.userAgent.browser.matchChrome_() &&
      !goog.labs.userAgent.browser.matchCoast_() &&
      !goog.labs.userAgent.browser.matchFirefox_() &&
      goog.labs.userAgent.util.matchUserAgent('AppleWebKit');
};


/**
 * @return {boolean} Whether the user's browser is any Chromium browser. This
 * returns true for Chrome, Opera 15+, and Edge Chromium.
 * @private
 */
goog.labs.userAgent.browser.matchChrome_ = function() {
  'use strict';
  return (goog.labs.userAgent.util.matchUserAgent('Chrome') ||
          goog.labs.userAgent.util.matchUserAgent('CriOS')) &&
      !goog.labs.userAgent.browser.matchEdgeHtml_();
};


/**
 * @return {boolean} Whether the user's browser is the Android browser.
 * @private
 */
goog.labs.userAgent.browser.matchAndroidBrowser_ = function() {
  'use strict';
  // Android can appear in the user agent string for Chrome on Android.
  // This is not the Android standalone browser if it does.
  return goog.labs.userAgent.util.matchUserAgent('Android') &&
      !(goog.labs.userAgent.browser.isChrome() ||
        goog.labs.userAgent.browser.isFirefox() ||
        goog.labs.userAgent.browser.isOpera() ||
        goog.labs.userAgent.browser.isSilk());
};


/**
 * @return {boolean} Whether the user's browser is Opera.
 */
goog.labs.userAgent.browser.isOpera = goog.labs.userAgent.browser.matchOpera_;


/**
 * @return {boolean} Whether the user's browser is IE.
 */
goog.labs.userAgent.browser.isIE = goog.labs.userAgent.browser.matchIE_;


/**
 * @return {boolean} Whether the user's browser is EdgeHTML based Edge.
 */
goog.labs.userAgent.browser.isEdge = goog.labs.userAgent.browser.matchEdgeHtml_;


/**
 * @return {boolean} Whether the user's browser is Chromium based Edge.
 */
goog.labs.userAgent.browser.isEdgeChromium =
    goog.labs.userAgent.browser.matchEdgeChromium_;

/**
 * @return {boolean} Whether the user's browser is Chromium based Opera.
 */
goog.labs.userAgent.browser.isOperaChromium =
    goog.labs.userAgent.browser.matchOperaChromium_;

/**
 * @return {boolean} Whether the user's browser is Firefox.
 */
goog.labs.userAgent.browser.isFirefox =
    goog.labs.userAgent.browser.matchFirefox_;


/**
 * @return {boolean} Whether the user's browser is Safari.
 */
goog.labs.userAgent.browser.isSafari = goog.labs.userAgent.browser.matchSafari_;


/**
 * @return {boolean} Whether the user's browser is Coast (Opera's Webkit-based
 *     iOS browser).
 */
goog.labs.userAgent.browser.isCoast = goog.labs.userAgent.browser.matchCoast_;


/**
 * @return {boolean} Whether the user's browser is iOS Webview.
 */
goog.labs.userAgent.browser.isIosWebview =
    goog.labs.userAgent.browser.matchIosWebview_;


/**
 * @return {boolean} Whether the user's browser is any Chromium based browser (
 * Chrome, Blink-based Opera (15+) and Edge Chromium).
 */
goog.labs.userAgent.browser.isChrome = goog.labs.userAgent.browser.matchChrome_;


/**
 * @return {boolean} Whether the user's browser is the Android browser.
 */
goog.labs.userAgent.browser.isAndroidBrowser =
    goog.labs.userAgent.browser.matchAndroidBrowser_;


/**
 * For more information, see:
 * http://docs.aws.amazon.com/silk/latest/developerguide/user-agent.html
 * @return {boolean} Whether the user's browser is Silk.
 */
goog.labs.userAgent.browser.isSilk = function() {
  'use strict';
  return goog.labs.userAgent.util.matchUserAgent('Silk');
};


/**
 * @return {string} The browser version or empty string if version cannot be
 *     determined. Note that for Internet Explorer, this returns the version of
 *     the browser, not the version of the rendering engine. (IE 8 in
 *     compatibility mode will return 8.0 rather than 7.0. To determine the
 *     rendering engine version, look at document.documentMode instead. See
 *     http://msdn.microsoft.com/en-us/library/cc196988(v=vs.85).aspx for more
 *     details.)
 */
goog.labs.userAgent.browser.getVersion = function() {
  'use strict';
  var userAgentString = goog.labs.userAgent.util.getUserAgent();
  // Special case IE since IE's version is inside the parenthesis and
  // without the '/'.
  if (goog.labs.userAgent.browser.isIE()) {
    return goog.labs.userAgent.browser.getIEVersion_(userAgentString);
  }

  var versionTuples =
      goog.labs.userAgent.util.extractVersionTuples(userAgentString);

  // Construct a map for easy lookup.
  var versionMap = {};
  versionTuples.forEach(function(tuple) {
    'use strict';
    // Note that the tuple is of length three, but we only care about the
    // first two.
    var key = tuple[0];
    var value = tuple[1];
    versionMap[key] = value;
  });

  var versionMapHasKey = goog.partial(goog.object.containsKey, versionMap);

  // Gives the value with the first key it finds, otherwise empty string.
  function lookUpValueWithKeys(keys) {
    var key = goog.array.find(keys, versionMapHasKey);
    return versionMap[key] || '';
  }

  // Check Opera before Chrome since Opera 15+ has "Chrome" in the string.
  // See
  // http://my.opera.com/ODIN/blog/2013/07/15/opera-user-agent-strings-opera-15-and-beyond
  if (goog.labs.userAgent.browser.isOpera()) {
    // Opera 10 has Version/10.0 but Opera/9.8, so look for "Version" first.
    // Opera uses 'OPR' for more recent UAs.
    return lookUpValueWithKeys(['Version', 'Opera']);
  }

  // Check Edge before Chrome since it has Chrome in the string.
  if (goog.labs.userAgent.browser.isEdge()) {
    return lookUpValueWithKeys(['Edge']);
  }

  // Check Chromium Edge before Chrome since it has Chrome in the string.
  if (goog.labs.userAgent.browser.isEdgeChromium()) {
    return lookUpValueWithKeys(['Edg']);
  }

  if (goog.labs.userAgent.browser.isChrome()) {
    return lookUpValueWithKeys(['Chrome', 'CriOS', 'HeadlessChrome']);
  }

  // Usually products browser versions are in the third tuple after "Mozilla"
  // and the engine.
  var tuple = versionTuples[2];
  return tuple && tuple[1] || '';
};


/**
 * @param {string|number} version The version to check.
 * @return {boolean} Whether the browser version is higher or the same as the
 *     given version.
 */
goog.labs.userAgent.browser.isVersionOrHigher = function(version) {
  'use strict';
  return goog.string.internal.compareVersions(
             goog.labs.userAgent.browser.getVersion(), version) >= 0;
};


/**
 * Determines IE version. More information:
 * http://msdn.microsoft.com/en-us/library/ie/bg182625(v=vs.85).aspx#uaString
 * http://msdn.microsoft.com/en-us/library/hh869301(v=vs.85).aspx
 * http://blogs.msdn.com/b/ie/archive/2010/03/23/introducing-ie9-s-user-agent-string.aspx
 * http://blogs.msdn.com/b/ie/archive/2009/01/09/the-internet-explorer-8-user-agent-string-updated-edition.aspx
 *
 * @param {string} userAgent the User-Agent.
 * @return {string}
 * @private
 */
goog.labs.userAgent.browser.getIEVersion_ = function(userAgent) {
  'use strict';
  // IE11 may identify itself as MSIE 9.0 or MSIE 10.0 due to an IE 11 upgrade
  // bug. Example UA:
  // Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; WOW64; Trident/7.0; rv:11.0)
  // like Gecko.
  // See http://www.whatismybrowser.com/developers/unknown-user-agent-fragments.
  var rv = /rv: *([\d\.]*)/.exec(userAgent);
  if (rv && rv[1]) {
    return rv[1];
  }

  var version = '';
  var msie = /MSIE +([\d\.]+)/.exec(userAgent);
  if (msie && msie[1]) {
    // IE in compatibility mode usually identifies itself as MSIE 7.0; in this
    // case, use the Trident version to determine the version of IE. For more
    // details, see the links above.
    var tridentVersion = /Trident\/(\d.\d)/.exec(userAgent);
    if (msie[1] == '7.0') {
      if (tridentVersion && tridentVersion[1]) {
        switch (tridentVersion[1]) {
          case '4.0':
            version = '8.0';
            break;
          case '5.0':
            version = '9.0';
            break;
          case '6.0':
            version = '10.0';
            break;
          case '7.0':
            version = '11.0';
            break;
        }
      } else {
        version = '7.0';
      }
    } else {
      version = msie[1];
    }
  }
  return version;
};

//third_party/javascript/closure/html/safehtml.js
goog.loadModule(function(exports) {'use strict';/**
 * @license
 * Copyright The Closure Library Authors.
 * SPDX-License-Identifier: Apache-2.0
 */


/**
 * @fileoverview The SafeHtml type and its builders.
 *
 * TODO(xtof): Link to document stating type contract.
 */

goog.module('goog.html.SafeHtml');
goog.module.declareLegacyNamespace();

const Const = goog.require('goog.string.Const');
const Dir = goog.require('goog.i18n.bidi.Dir');
const DirectionalString = goog.require('goog.i18n.bidi.DirectionalString');
const SafeScript = goog.require('goog.html.SafeScript');
const SafeStyle = goog.require('goog.html.SafeStyle');
const SafeStyleSheet = goog.require('goog.html.SafeStyleSheet');
const SafeUrl = goog.require('goog.html.SafeUrl');
const TagName = goog.require('goog.dom.TagName');
const TrustedResourceUrl = goog.require('goog.html.TrustedResourceUrl');
const TypedString = goog.require('goog.string.TypedString');
const asserts = goog.require('goog.asserts');
const browser = goog.require('goog.labs.userAgent.browser');
const googArray = goog.require('goog.array');
const googObject = goog.require('goog.object');
const internal = goog.require('goog.string.internal');
const tags = goog.require('goog.dom.tags');
const trustedtypes = goog.require('goog.html.trustedtypes');


/**
 * Token used to ensure that object is created only from this file. No code
 * outside of this file can access this token.
 * @type {!Object}
 * @const
 */
const CONSTRUCTOR_TOKEN_PRIVATE = {};

/**
 * A string that is safe to use in HTML context in DOM APIs and HTML documents.
 *
 * A SafeHtml is a string-like object that carries the security type contract
 * that its value as a string will not cause untrusted script execution when
 * evaluated as HTML in a browser.
 *
 * Values of this type are guaranteed to be safe to use in HTML contexts,
 * such as, assignment to the innerHTML DOM property, or interpolation into
 * a HTML template in HTML PC_DATA context, in the sense that the use will not
 * result in a Cross-Site-Scripting vulnerability.
 *
 * Instances of this type must be created via the factory methods
 * (`SafeHtml.create`, `SafeHtml.htmlEscape`),
 * etc and not by invoking its constructor. The constructor intentionally takes
 * an extra parameter that cannot be constructed outside of this file and the
 * type is immutable; hence only a default instance corresponding to the empty
 * string can be obtained via constructor invocation.
 *
 * Creating SafeHtml objects HAS SIDE-EFFECTS due to calling Trusted Types Web
 * API.
 *
 * Note that there is no `SafeHtml.fromConstant`. The reason is that
 * the following code would create an unsafe HTML:
 *
 * ```
 * SafeHtml.concat(
 *     SafeHtml.fromConstant(Const.from('<script>')),
 *     SafeHtml.htmlEscape(userInput),
 *     SafeHtml.fromConstant(Const.from('<\/script>')));
 * ```
 *
 * There's `goog.dom.constHtmlToNode` to create a node from constant strings
 * only.
 *
 * @see SafeHtml.create
 * @see SafeHtml.htmlEscape
 * @final
 * @struct
 * @implements {DirectionalString}
 * @implements {TypedString}
 */
class SafeHtml {
  /**
   * @param {!TrustedHTML|string} value
   * @param {?Dir} dir
   * @param {!Object} token package-internal implementation detail.
   */
  constructor(value, dir, token) {
    /**
     * The contained value of this SafeHtml.  The field has a purposely ugly
     * name to make (non-compiled) code that attempts to directly access this
     * field stand out.
     * @private {!TrustedHTML|string}
     */
    this.privateDoNotAccessOrElseSafeHtmlWrappedValue_ =
        (token === CONSTRUCTOR_TOKEN_PRIVATE) ? value : '';

    /**
     * This SafeHtml's directionality, or null if unknown.
     * @private {?Dir}
     */
    this.dir_ = dir;

    /**
     * @override
     * @const
     */
    this.implementsGoogI18nBidiDirectionalString = true;

    /**
     * @override
     * @const {boolean}
     */
    this.implementsGoogStringTypedString = true;
  }

  /**
   * @return {?Dir}
   * @override
   */
  getDirection() {
    return this.dir_;
  }


  /**
   * Returns this SafeHtml's value as string.
   *
   * IMPORTANT: In code where it is security relevant that an object's type is
   * indeed `SafeHtml`, use `SafeHtml.unwrap` instead of
   * this method. If in doubt, assume that it's security relevant. In
   * particular, note that goog.html functions which return a goog.html type do
   * not guarantee that the returned instance is of the right type. For example:
   *
   * <pre>
   * var fakeSafeHtml = new String('fake');
   * fakeSafeHtml.__proto__ = SafeHtml.prototype;
   * var newSafeHtml = SafeHtml.htmlEscape(fakeSafeHtml);
   * // newSafeHtml is just an alias for fakeSafeHtml, it's passed through by
   * // SafeHtml.htmlEscape() as fakeSafeHtml
   * // instanceof SafeHtml.
   * </pre>
   *
   * @return {string}
   * @see SafeHtml.unwrap
   * @override
   */
  getTypedStringValue() {
    return this.privateDoNotAccessOrElseSafeHtmlWrappedValue_.toString();
  }


  /**
   * Returns a string-representation of this value.
   *
   * To obtain the actual string value wrapped in a SafeHtml, use
   * `SafeHtml.unwrap`.
   *
   * @return {string}
   * @see SafeHtml.unwrap
   * @override
   */
  toString() {
    return this.privateDoNotAccessOrElseSafeHtmlWrappedValue_.toString();
  }

  /**
   * Performs a runtime check that the provided object is indeed a SafeHtml
   * object, and returns its value.
   * @param {!SafeHtml} safeHtml The object to extract from.
   * @return {string} The SafeHtml object's contained string, unless the
   *     run-time type check fails. In that case, `unwrap` returns an innocuous
   *     string, or, if assertions are enabled, throws
   *     `asserts.AssertionError`.
   */
  static unwrap(safeHtml) {
    return SafeHtml.unwrapTrustedHTML(safeHtml).toString();
  }


  /**
   * Unwraps value as TrustedHTML if supported or as a string if not.
   * @param {!SafeHtml} safeHtml
   * @return {!TrustedHTML|string}
   * @see SafeHtml.unwrap
   */
  static unwrapTrustedHTML(safeHtml) {
    // Perform additional run-time type-checking to ensure that safeHtml is
    // indeed an instance of the expected type.  This provides some additional
    // protection against security bugs due to application code that disables
    // type checks. Specifically, the following checks are performed:
    // 1. The object is an instance of the expected type.
    // 2. The object is not an instance of a subclass.
    if (safeHtml instanceof SafeHtml && safeHtml.constructor === SafeHtml) {
      return safeHtml.privateDoNotAccessOrElseSafeHtmlWrappedValue_;
    } else {
      asserts.fail(
          `expected object of type SafeHtml, got '${safeHtml}' of type ` +
          goog.typeOf(safeHtml));
      return 'type_error:SafeHtml';
    }
  }

  /**
   * Returns HTML-escaped text as a SafeHtml object.
   *
   * If text is of a type that implements
   * `DirectionalString`, the directionality of the new
   * `SafeHtml` object is set to `text`'s directionality, if known.
   * Otherwise, the directionality of the resulting SafeHtml is unknown (i.e.,
   * `null`).
   *
   * @param {!SafeHtml.TextOrHtml_} textOrHtml The text to escape. If
   *     the parameter is of type SafeHtml it is returned directly (no escaping
   *     is done).
   * @return {!SafeHtml} The escaped text, wrapped as a SafeHtml.
   */
  static htmlEscape(textOrHtml) {
    if (textOrHtml instanceof SafeHtml) {
      return textOrHtml;
    }
    const textIsObject = typeof textOrHtml == 'object';
    let dir = null;
    if (textIsObject && textOrHtml.implementsGoogI18nBidiDirectionalString) {
      dir = /** @type {!DirectionalString} */ (textOrHtml).getDirection();
    }
    let textAsString;
    if (textIsObject && textOrHtml.implementsGoogStringTypedString) {
      textAsString =
          /** @type {!TypedString} */ (textOrHtml).getTypedStringValue();
    } else {
      textAsString = String(textOrHtml);
    }
    return SafeHtml.createSafeHtmlSecurityPrivateDoNotAccessOrElse(
        internal.htmlEscape(textAsString), dir);
  }


  /**
   * Returns HTML-escaped text as a SafeHtml object, with newlines changed to
   * &lt;br&gt;.
   * @param {!SafeHtml.TextOrHtml_} textOrHtml The text to escape. If
   *     the parameter is of type SafeHtml it is returned directly (no escaping
   *     is done).
   * @return {!SafeHtml} The escaped text, wrapped as a SafeHtml.
   */
  static htmlEscapePreservingNewlines(textOrHtml) {
    if (textOrHtml instanceof SafeHtml) {
      return textOrHtml;
    }
    const html = SafeHtml.htmlEscape(textOrHtml);
    return SafeHtml.createSafeHtmlSecurityPrivateDoNotAccessOrElse(
        internal.newLineToBr(SafeHtml.unwrap(html)), html.getDirection());
  }


  /**
   * Returns HTML-escaped text as a SafeHtml object, with newlines changed to
   * &lt;br&gt; and escaping whitespace to preserve spatial formatting.
   * Character entity #160 is used to make it safer for XML.
   * @param {!SafeHtml.TextOrHtml_} textOrHtml The text to escape. If
   *     the parameter is of type SafeHtml it is returned directly (no escaping
   *     is done).
   * @return {!SafeHtml} The escaped text, wrapped as a SafeHtml.
   */
  static htmlEscapePreservingNewlinesAndSpaces(textOrHtml) {
    if (textOrHtml instanceof SafeHtml) {
      return textOrHtml;
    }
    const html = SafeHtml.htmlEscape(textOrHtml);
    return SafeHtml.createSafeHtmlSecurityPrivateDoNotAccessOrElse(
        internal.whitespaceEscape(SafeHtml.unwrap(html)), html.getDirection());
  }

  /**
   * Converts an arbitrary string into an HTML comment by HTML-escaping the
   * contents and embedding the result between HTML comment markers.
   *
   * Escaping is needed because Internet Explorer supports conditional comments
   * and so may render HTML markup within comments.
   *
   * @param {string} text
   * @return {!SafeHtml}
   */
  static comment(text) {
    return SafeHtml.createSafeHtmlSecurityPrivateDoNotAccessOrElse(
        '<!--' + internal.htmlEscape(text) + '-->', null);
  }

  /**
   * Creates a SafeHtml content consisting of a tag with optional attributes and
   * optional content.
   *
   * For convenience tag names and attribute names are accepted as regular
   * strings, instead of Const. Nevertheless, you should not pass
   * user-controlled values to these parameters. Note that these parameters are
   * syntactically validated at runtime, and invalid values will result in
   * an exception.
   *
   * Example usage:
   *
   * SafeHtml.create('br');
   * SafeHtml.create('div', {'class': 'a'});
   * SafeHtml.create('p', {}, 'a');
   * SafeHtml.create('p', {}, SafeHtml.create('br'));
   *
   * SafeHtml.create('span', {
   *   'style': {'margin': '0'}
   * });
   *
   * To guarantee SafeHtml's type contract is upheld there are restrictions on
   * attribute values and tag names.
   *
   * - For attributes which contain script code (on*), a Const is
   *   required.
   * - For attributes which contain style (style), a SafeStyle or a
   *   SafeStyle.PropertyMap is required.
   * - For attributes which are interpreted as URLs (e.g. src, href) a
   *   SafeUrl, Const or string is required. If a string
   *   is passed, it will be sanitized with SafeUrl.sanitize().
   * - For tags which can load code or set security relevant page metadata,
   *   more specific SafeHtml.create*() functions must be used. Tags
   *   which are not supported by this function are applet, base, embed, iframe,
   *   link, math, meta, object, script, style, svg, and template.
   *
   * @param {!TagName|string} tagName The name of the tag. Only tag names
   *     consisting of [a-zA-Z0-9-] are allowed. Tag names documented above are
   *     disallowed.
   * @param {?Object<string, ?SafeHtml.AttributeValue>=} attributes  Mapping
   *     from attribute names to their values. Only attribute names consisting
   *     of [a-zA-Z0-9-] are allowed. Value of null or undefined causes the
   *     attribute to be omitted.
   * @param {!SafeHtml.TextOrHtml_|
   *     !Array<!SafeHtml.TextOrHtml_>=} content Content to HTML-escape and put
   * inside the tag. This must be empty for void tags like <br>. Array elements
   * are concatenated.
   * @return {!SafeHtml} The SafeHtml content with the tag.
   * @throws {!Error} If invalid tag name, attribute name, or attribute value is
   *     provided.
   * @throws {!asserts.AssertionError} If content for void tag is provided.
   */
  static create(tagName, attributes = undefined, content = undefined) {
    SafeHtml.verifyTagName(String(tagName));
    return SafeHtml.createSafeHtmlTagSecurityPrivateDoNotAccessOrElse(
        String(tagName), attributes, content);
  }


  /**
   * Verifies if the tag name is valid and if it doesn't change the context.
   * E.g. STRONG is fine but SCRIPT throws because it changes context. See
   * SafeHtml.create for an explanation of allowed tags.
   * @param {string} tagName
   * @return {void}
   * @throws {!Error} If invalid tag name is provided.
   * @package
   */
  static verifyTagName(tagName) {
    if (!VALID_NAMES_IN_TAG.test(tagName)) {
      throw new Error(
          SafeHtml.ENABLE_ERROR_MESSAGES ? `Invalid tag name <${tagName}>.` :
                                           '');
    }
    if (tagName.toUpperCase() in NOT_ALLOWED_TAG_NAMES) {
      throw new Error(
          SafeHtml.ENABLE_ERROR_MESSAGES ?

              `Tag name <${tagName}> is not allowed for SafeHtml.` :
              '');
    }
  }


  /**
   * Creates a SafeHtml representing an iframe tag.
   *
   * This by default restricts the iframe as much as possible by setting the
   * sandbox attribute to the empty string. If the iframe requires less
   * restrictions, set the sandbox attribute as tight as possible, but do not
   * rely on the sandbox as a security feature because it is not supported by
   * older browsers. If a sandbox is essential to security (e.g. for third-party
   * frames), use createSandboxIframe which checks for browser support.
   *
   * @see https://developer.mozilla.org/en/docs/Web/HTML/Element/iframe#attr-sandbox
   *
   * @param {?TrustedResourceUrl=} src The value of the src
   *     attribute. If null or undefined src will not be set.
   * @param {?SafeHtml=} srcdoc The value of the srcdoc attribute.
   *     If null or undefined srcdoc will not be set.
   * @param {?Object<string, ?SafeHtml.AttributeValue>=} attributes  Mapping
   *     from attribute names to their values. Only attribute names consisting
   *     of [a-zA-Z0-9-] are allowed. Value of null or undefined causes the
   *     attribute to be omitted.
   * @param {!SafeHtml.TextOrHtml_|
   *     !Array<!SafeHtml.TextOrHtml_>=} content Content to HTML-escape and put
   * inside the tag. Array elements are concatenated.
   * @return {!SafeHtml} The SafeHtml content with the tag.
   * @throws {!Error} If invalid tag name, attribute name, or attribute value is
   *     provided. If attributes
   * contains the src or srcdoc attributes.
   */
  static createIframe(
      src = undefined, srcdoc = undefined, attributes = undefined,
      content = undefined) {
    if (src) {
      // Check whether this is really TrustedResourceUrl.
      TrustedResourceUrl.unwrap(src);
    }

    const fixedAttributes = {};
    fixedAttributes['src'] = src || null;
    fixedAttributes['srcdoc'] = srcdoc && SafeHtml.unwrap(srcdoc);
    const defaultAttributes = {'sandbox': ''};
    const combinedAttrs = SafeHtml.combineAttributes(
        fixedAttributes, defaultAttributes, attributes);
    return SafeHtml.createSafeHtmlTagSecurityPrivateDoNotAccessOrElse(
        'iframe', combinedAttrs, content);
  }


  /**
   * Creates a SafeHtml representing a sandboxed iframe tag.
   *
   * The sandbox attribute is enforced in its most restrictive mode, an empty
   * string. Consequently, the security requirements for the src and srcdoc
   * attributes are relaxed compared to SafeHtml.createIframe. This function
   * will throw on browsers that do not support the sandbox attribute, as
   * determined by SafeHtml.canUseSandboxIframe.
   *
   * The SafeHtml returned by this function can trigger downloads with no
   * user interaction on Chrome (though only a few, further attempts are
   * blocked). Firefox and IE will block all downloads from the sandbox.
   *
   * @see https://developer.mozilla.org/en/docs/Web/HTML/Element/iframe#attr-sandbox
   * @see https://lists.w3.org/Archives/Public/public-whatwg-archive/2013Feb/0112.html
   *
   * @param {string|!SafeUrl=} src The value of the src
   *     attribute. If null or undefined src will not be set.
   * @param {string=} srcdoc The value of the srcdoc attribute.
   *     If null or undefined srcdoc will not be set. Will not be sanitized.
   * @param {!Object<string, ?SafeHtml.AttributeValue>=} attributes  Mapping
   *     from attribute names to their values. Only attribute names consisting
   *     of [a-zA-Z0-9-] are allowed. Value of null or undefined causes the
   *     attribute to be omitted.
   * @param {!SafeHtml.TextOrHtml_|
   *     !Array<!SafeHtml.TextOrHtml_>=} content Content to HTML-escape and put
   * inside the tag. Array elements are concatenated.
   * @return {!SafeHtml} The SafeHtml content with the tag.
   * @throws {!Error} If invalid tag name, attribute name, or attribute value is
   *     provided. If attributes
   * contains the src, srcdoc or sandbox attributes. If browser does not support
   * the sandbox attribute on iframe.
   */
  static createSandboxIframe(
      src = undefined, srcdoc = undefined, attributes = undefined,
      content = undefined) {
    if (!SafeHtml.canUseSandboxIframe()) {
      throw new Error(
          SafeHtml.ENABLE_ERROR_MESSAGES ?
              'The browser does not support sandboxed iframes.' :
              '');
    }

    const fixedAttributes = {};
    if (src) {
      // Note that sanitize is a no-op on SafeUrl.
      fixedAttributes['src'] = SafeUrl.unwrap(SafeUrl.sanitize(src));
    } else {
      fixedAttributes['src'] = null;
    }
    fixedAttributes['srcdoc'] = srcdoc || null;
    fixedAttributes['sandbox'] = '';
    const combinedAttrs =
        SafeHtml.combineAttributes(fixedAttributes, {}, attributes);
    return SafeHtml.createSafeHtmlTagSecurityPrivateDoNotAccessOrElse(
        'iframe', combinedAttrs, content);
  }


  /**
   * Checks if the user agent supports sandboxed iframes.
   * @return {boolean}
   */
  static canUseSandboxIframe() {
    return goog.global['HTMLIFrameElement'] &&
        ('sandbox' in goog.global['HTMLIFrameElement'].prototype);
  }


  /**
   * Creates a SafeHtml representing a script tag with the src attribute.
   * @param {!TrustedResourceUrl} src The value of the src
   * attribute.
   * @param {?Object<string, ?SafeHtml.AttributeValue>=}
   * attributes
   *     Mapping from attribute names to their values. Only attribute names
   *     consisting of [a-zA-Z0-9-] are allowed. Value of null or undefined
   *     causes the attribute to be omitted.
   * @return {!SafeHtml} The SafeHtml content with the tag.
   * @throws {!Error} If invalid attribute name or value is provided. If
   *     attributes  contains the
   * src attribute.
   */
  static createScriptSrc(src, attributes = undefined) {
    // TODO(mlourenco): The charset attribute should probably be blocked. If
    // its value is attacker controlled, the script contains attacker controlled
    // sub-strings (even if properly escaped) and the server does not set
    // charset then XSS is likely possible.
    // https://html.spec.whatwg.org/multipage/scripting.html#dom-script-charset

    // Check whether this is really TrustedResourceUrl.
    TrustedResourceUrl.unwrap(src);

    const fixedAttributes = {'src': src};
    const defaultAttributes = {};
    const combinedAttrs = SafeHtml.combineAttributes(
        fixedAttributes, defaultAttributes, attributes);
    return SafeHtml.createSafeHtmlTagSecurityPrivateDoNotAccessOrElse(
        'script', combinedAttrs);
  }


  /**
   * Creates a SafeHtml representing a script tag. Does not allow the language,
   * src, text or type attributes to be set.
   * @param {!SafeScript|!Array<!SafeScript>}
   *     script Content to put inside the tag. Array elements are
   *     concatenated.
   * @param {?Object<string, ?SafeHtml.AttributeValue>=} attributes  Mapping
   *     from attribute names to their values. Only attribute names consisting
   *     of [a-zA-Z0-9-] are allowed. Value of null or undefined causes the
   *     attribute to be omitted.
   * @return {!SafeHtml} The SafeHtml content with the tag.
   * @throws {!Error} If invalid attribute name or attribute value is provided.
   *     If attributes  contains the
   *     language, src, text or type attribute.
   */
  static createScript(script, attributes = undefined) {
    for (let attr in attributes) {
      // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/hasOwnProperty#Using_hasOwnProperty_as_a_property_name
      if (Object.prototype.hasOwnProperty.call(attributes, attr)) {
        const attrLower = attr.toLowerCase();
        if (attrLower == 'language' || attrLower == 'src' ||
            attrLower == 'text' || attrLower == 'type') {
          throw new Error(
              SafeHtml.ENABLE_ERROR_MESSAGES ?
                  `Cannot set "${attrLower}" attribute` :
                  '');
        }
      }
    }

    let content = '';
    script = googArray.concat(script);
    for (let i = 0; i < script.length; i++) {
      content += SafeScript.unwrap(script[i]);
    }
    // Convert to SafeHtml so that it's not HTML-escaped. This is safe because
    // as part of its contract, SafeScript should have no dangerous '<'.
    const htmlContent = SafeHtml.createSafeHtmlSecurityPrivateDoNotAccessOrElse(
        content, Dir.NEUTRAL);
    return SafeHtml.createSafeHtmlTagSecurityPrivateDoNotAccessOrElse(
        'script', attributes, htmlContent);
  }


  /**
   * Creates a SafeHtml representing a style tag. The type attribute is set
   * to "text/css".
   * @param {!SafeStyleSheet|!Array<!SafeStyleSheet>}
   *     styleSheet Content to put inside the tag. Array elements are
   *     concatenated.
   * @param {?Object<string, ?SafeHtml.AttributeValue>=} attributes  Mapping
   *     from attribute names to their values. Only attribute names consisting
   *     of [a-zA-Z0-9-] are allowed. Value of null or undefined causes the
   *     attribute to be omitted.
   * @return {!SafeHtml} The SafeHtml content with the tag.
   * @throws {!Error} If invalid attribute name or attribute value is provided.
   *     If attributes  contains the
   *     type attribute.
   */
  static createStyle(styleSheet, attributes = undefined) {
    const fixedAttributes = {'type': 'text/css'};
    const defaultAttributes = {};
    const combinedAttrs = SafeHtml.combineAttributes(
        fixedAttributes, defaultAttributes, attributes);

    let content = '';
    styleSheet = googArray.concat(styleSheet);
    for (let i = 0; i < styleSheet.length; i++) {
      content += SafeStyleSheet.unwrap(styleSheet[i]);
    }
    // Convert to SafeHtml so that it's not HTML-escaped. This is safe because
    // as part of its contract, SafeStyleSheet should have no dangerous '<'.
    const htmlContent = SafeHtml.createSafeHtmlSecurityPrivateDoNotAccessOrElse(
        content, Dir.NEUTRAL);
    return SafeHtml.createSafeHtmlTagSecurityPrivateDoNotAccessOrElse(
        'style', combinedAttrs, htmlContent);
  }


  /**
   * Creates a SafeHtml representing a meta refresh tag.
   * @param {!SafeUrl|string} url Where to redirect. If a string is
   *     passed, it will be sanitized with SafeUrl.sanitize().
   * @param {number=} secs Number of seconds until the page should be
   *     reloaded. Will be set to 0 if unspecified.
   * @return {!SafeHtml} The SafeHtml content with the tag.
   */
  static createMetaRefresh(url, secs = undefined) {
    // Note that sanitize is a no-op on SafeUrl.
    let unwrappedUrl = SafeUrl.unwrap(SafeUrl.sanitize(url));

    if (browser.isIE() || browser.isEdge()) {
      // IE/EDGE can't parse the content attribute if the url contains a
      // semicolon. We can fix this by adding quotes around the url, but then we
      // can't parse quotes in the URL correctly. Also, it seems that IE/EDGE
      // did not unescape semicolons in these URLs at some point in the past. We
      // take a best-effort approach.
      //
      // If the URL has semicolons (which may happen in some cases, see
      // http://www.w3.org/TR/1999/REC-html401-19991224/appendix/notes.html#h-B.2
      // for instance), wrap it in single quotes to protect the semicolons.
      // If the URL has semicolons and single quotes, url-encode the single
      // quotes as well.
      //
      // This is imperfect. Notice that both ' and ; are reserved characters in
      // URIs, so this could do the wrong thing, but at least it will do the
      // wrong thing in only rare cases.
      if (internal.contains(unwrappedUrl, ';')) {
        unwrappedUrl = '\'' + unwrappedUrl.replace(/'/g, '%27') + '\'';
      }
    }
    const attributes = {
      'http-equiv': 'refresh',
      'content': (secs || 0) + '; url=' + unwrappedUrl,
    };

    // This function will handle the HTML escaping for attributes.
    return SafeHtml.createSafeHtmlTagSecurityPrivateDoNotAccessOrElse(
        'meta', attributes);
  }

  /**
   * Creates a SafeHtml content with known directionality consisting of a tag
   * with optional attributes and optional content.
   * @param {!Dir} dir Directionality.
   * @param {string} tagName
   * @param {?Object<string, ?SafeHtml.AttributeValue>=} attributes
   * @param {!SafeHtml.TextOrHtml_|
   *     !Array<!SafeHtml.TextOrHtml_>=} content
   * @return {!SafeHtml} The SafeHtml content with the tag.
   */
  static createWithDir(
      dir, tagName, attributes = undefined, content = undefined) {
    const html = SafeHtml.create(tagName, attributes, content);
    html.dir_ = dir;
    return html;
  }


  /**
   * Creates a new SafeHtml object by joining the parts with separator.
   * @param {!SafeHtml.TextOrHtml_} separator
   * @param {!Array<!SafeHtml.TextOrHtml_|
   *     !Array<!SafeHtml.TextOrHtml_>>} parts Parts to join. If a part
   *     contains an array then each member of this array is also joined with
   * the separator.
   * @return {!SafeHtml}
   */
  static join(separator, parts) {
    const separatorHtml = SafeHtml.htmlEscape(separator);
    let dir = separatorHtml.getDirection();
    const content = [];

    /**
     * @param {!SafeHtml.TextOrHtml_|
     *     !Array<!SafeHtml.TextOrHtml_>} argument
     */
    const addArgument = (argument) => {
      if (Array.isArray(argument)) {
        argument.forEach(addArgument);
      } else {
        const html = SafeHtml.htmlEscape(argument);
        content.push(SafeHtml.unwrap(html));
        const htmlDir = html.getDirection();
        if (dir == Dir.NEUTRAL) {
          dir = htmlDir;
        } else if (htmlDir != Dir.NEUTRAL && dir != htmlDir) {
          dir = null;
        }
      }
    };

    parts.forEach(addArgument);
    return SafeHtml.createSafeHtmlSecurityPrivateDoNotAccessOrElse(
        content.join(SafeHtml.unwrap(separatorHtml)), dir);
  }


  /**
   * Creates a new SafeHtml object by concatenating values.
   * @param {...(!SafeHtml.TextOrHtml_|
   *     !Array<!SafeHtml.TextOrHtml_>)} var_args Values to concatenate.
   * @return {!SafeHtml}
   */
  static concat(var_args) {
    return SafeHtml.join(SafeHtml.EMPTY, Array.prototype.slice.call(arguments));
  }


  /**
   * Creates a new SafeHtml object with known directionality by concatenating
   * the values.
   * @param {!Dir} dir Directionality.
   * @param {...(!SafeHtml.TextOrHtml_|
   *     !Array<!SafeHtml.TextOrHtml_>)} var_args Elements of array
   *     arguments would be processed recursively.
   * @return {!SafeHtml}
   */
  static concatWithDir(dir, var_args) {
    const html = SafeHtml.concat(Array.prototype.slice.call(arguments, 1));
    html.dir_ = dir;
    return html;
  }

  /**
   * Package-internal utility method to create SafeHtml instances.
   *
   * @param {string} html The string to initialize the SafeHtml object with.
   * @param {?Dir} dir The directionality of the SafeHtml to be
   *     constructed, or null if unknown.
   * @return {!SafeHtml} The initialized SafeHtml object.
   * @package
   */
  static createSafeHtmlSecurityPrivateDoNotAccessOrElse(html, dir) {
    const policy = trustedtypes.getPolicyPrivateDoNotAccessOrElse();
    const trustedHtml = policy ? policy.createHTML(html) : html;
    return new SafeHtml(trustedHtml, dir, CONSTRUCTOR_TOKEN_PRIVATE);
  }


  /**
   * Like create() but does not restrict which tags can be constructed.
   *
   * @param {string} tagName Tag name. Set or validated by caller.
   * @param {?Object<string, ?SafeHtml.AttributeValue>=} attributes
   * @param {(!SafeHtml.TextOrHtml_|
   *     !Array<!SafeHtml.TextOrHtml_>)=} content
   * @return {!SafeHtml}
   * @throws {!Error} If invalid or unsafe attribute name or value is provided.
   * @throws {!asserts.AssertionError} If content for void tag is provided.
   * @package
   */
  static createSafeHtmlTagSecurityPrivateDoNotAccessOrElse(
      tagName, attributes = undefined, content = undefined) {
    let dir = null;
    let result = `<${tagName}`;
    result += SafeHtml.stringifyAttributes(tagName, attributes);

    if (content == null) {
      content = [];
    } else if (!Array.isArray(content)) {
      content = [content];
    }

    if (tags.isVoidTag(tagName.toLowerCase())) {
      asserts.assert(
          !content.length, `Void tag <${tagName}> does not allow content.`);
      result += '>';
    } else {
      const html = SafeHtml.concat(content);
      result += '>' + SafeHtml.unwrap(html) + '</' + tagName + '>';
      dir = html.getDirection();
    }

    const dirAttribute = attributes && attributes['dir'];
    if (dirAttribute) {
      if (/^(ltr|rtl|auto)$/i.test(dirAttribute)) {
        // If the tag has the "dir" attribute specified then its direction is
        // neutral because it can be safely used in any context.
        dir = Dir.NEUTRAL;
      } else {
        dir = null;
      }
    }

    return SafeHtml.createSafeHtmlSecurityPrivateDoNotAccessOrElse(result, dir);
  }


  /**
   * Creates a string with attributes to insert after tagName.
   * @param {string} tagName
   * @param {?Object<string, ?SafeHtml.AttributeValue>=} attributes
   * @return {string} Returns an empty string if there are no attributes,
   *     returns a string starting with a space otherwise.
   * @throws {!Error} If attribute value is unsafe for the given tag and
   *     attribute.
   * @package
   */
  static stringifyAttributes(tagName, attributes = undefined) {
    let result = '';
    if (attributes) {
      for (let name in attributes) {
        // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/hasOwnProperty#Using_hasOwnProperty_as_a_property_name
        if (Object.prototype.hasOwnProperty.call(attributes, name)) {
          if (!VALID_NAMES_IN_TAG.test(name)) {
            throw new Error(
                SafeHtml.ENABLE_ERROR_MESSAGES ?
                    `Invalid attribute name "${name}".` :
                    '');
          }
          const value = attributes[name];
          if (value == null) {
            continue;
          }
          result += ' ' + getAttrNameAndValue(tagName, name, value);
        }
      }
    }
    return result;
  }


  /**
   * @param {!Object<string, ?SafeHtml.AttributeValue>} fixedAttributes
   * @param {!Object<string, string>} defaultAttributes
   * @param {?Object<string, ?SafeHtml.AttributeValue>=} attributes  Optional
   *     attributes passed to create*().
   * @return {!Object<string, ?SafeHtml.AttributeValue>}
   * @throws {!Error} If attributes contains an attribute with the same name as
   *     an attribute in fixedAttributes.
   * @package
   */
  static combineAttributes(
      fixedAttributes, defaultAttributes, attributes = undefined) {
    const combinedAttributes = {};

    for (const name in fixedAttributes) {
      // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/hasOwnProperty#Using_hasOwnProperty_as_a_property_name
      if (Object.prototype.hasOwnProperty.call(fixedAttributes, name)) {
        asserts.assert(name.toLowerCase() == name, 'Must be lower case');
        combinedAttributes[name] = fixedAttributes[name];
      }
    }
    for (const name in defaultAttributes) {
      if (Object.prototype.hasOwnProperty.call(defaultAttributes, name)) {
        asserts.assert(name.toLowerCase() == name, 'Must be lower case');
        combinedAttributes[name] = defaultAttributes[name];
      }
    }

    if (attributes) {
      for (const name in attributes) {
        if (Object.prototype.hasOwnProperty.call(attributes, name)) {
          const nameLower = name.toLowerCase();
          if (nameLower in fixedAttributes) {
            throw new Error(
                SafeHtml.ENABLE_ERROR_MESSAGES ?
                    `Cannot override "${nameLower}" attribute, got "` + name +
                        '" with value "' + attributes[name] + '"' :
                    '');
          }
          if (nameLower in defaultAttributes) {
            delete combinedAttributes[nameLower];
          }
          combinedAttributes[name] = attributes[name];
        }
      }
    }

    return combinedAttributes;
  }
}


/**
 * @define {boolean} Whether to strip out error messages or to leave them in.
 */
SafeHtml.ENABLE_ERROR_MESSAGES =
    goog.define('goog.html.SafeHtml.ENABLE_ERROR_MESSAGES', goog.DEBUG);


/**
 * Whether the `style` attribute is supported. Set to false to avoid the byte
 * weight of `SafeStyle` where unneeded. An error will be thrown if
 * the `style` attribute is used.
 * @define {boolean}
 */
SafeHtml.SUPPORT_STYLE_ATTRIBUTE =
    goog.define('goog.html.SafeHtml.SUPPORT_STYLE_ATTRIBUTE', true);


/**
 * Shorthand for union of types that can sensibly be converted to strings
 * or might already be SafeHtml (as SafeHtml is a TypedString).
 * @private
 * @typedef {string|number|boolean|!TypedString|
 *           !DirectionalString}
 */
SafeHtml.TextOrHtml_;


/**
 * Coerces an arbitrary object into a SafeHtml object.
 *
 * If `textOrHtml` is already of type `SafeHtml`, the same
 * object is returned. Otherwise, `textOrHtml` is coerced to string, and
 * HTML-escaped. If `textOrHtml` is of a type that implements
 * `DirectionalString`, its directionality, if known, is
 * preserved.
 *
 * @param {!SafeHtml.TextOrHtml_} textOrHtml The text or SafeHtml to
 *     coerce.
 * @return {!SafeHtml} The resulting SafeHtml object.
 * @deprecated Use SafeHtml.htmlEscape.
 */
SafeHtml.from = SafeHtml.htmlEscape;


/**
 * @const
 */
const VALID_NAMES_IN_TAG = /^[a-zA-Z0-9-]+$/;


/**
 * Set of attributes containing URL as defined at
 * http://www.w3.org/TR/html5/index.html#attributes-1.
 * @const {!Object<string,boolean>}
 */
const URL_ATTRIBUTES = googObject.createSet(
    'action', 'cite', 'data', 'formaction', 'href', 'manifest', 'poster',
    'src');


/**
 * Tags which are unsupported via create(). They might be supported via a
 * tag-specific create method. These are tags which might require a
 * TrustedResourceUrl in one of their attributes or a restricted type for
 * their content.
 * @const {!Object<string,boolean>}
 */
const NOT_ALLOWED_TAG_NAMES = googObject.createSet(
    TagName.APPLET, TagName.BASE, TagName.EMBED, TagName.IFRAME, TagName.LINK,
    TagName.MATH, TagName.META, TagName.OBJECT, TagName.SCRIPT, TagName.STYLE,
    TagName.SVG, TagName.TEMPLATE);


/**
 * @typedef {string|number|!TypedString|
 *     !SafeStyle.PropertyMap|undefined|null}
 */
SafeHtml.AttributeValue;


/**
 * @param {string} tagName The tag name.
 * @param {string} name The attribute name.
 * @param {!SafeHtml.AttributeValue} value The attribute value.
 * @return {string} A "name=value" string.
 * @throws {!Error} If attribute value is unsafe for the given tag and
 *     attribute.
 * @private
 */
function getAttrNameAndValue(tagName, name, value) {
  // If it's goog.string.Const, allow any valid attribute name.
  if (value instanceof Const) {
    value = Const.unwrap(value);
  } else if (name.toLowerCase() == 'style') {
    if (SafeHtml.SUPPORT_STYLE_ATTRIBUTE) {
      value = getStyleValue(value);
    } else {
      throw new Error(
          SafeHtml.ENABLE_ERROR_MESSAGES ? 'Attribute "style" not supported.' :
                                           '');
    }
  } else if (/^on/i.test(name)) {
    // TODO(jakubvrana): Disallow more attributes with a special meaning.
    throw new Error(
        SafeHtml.ENABLE_ERROR_MESSAGES ? `Attribute "${name}` +
                '" requires goog.string.Const value, "' + value + '" given.' :
                                         '');
    // URL attributes handled differently according to tag.
  } else if (name.toLowerCase() in URL_ATTRIBUTES) {
    if (value instanceof TrustedResourceUrl) {
      value = TrustedResourceUrl.unwrap(value);
    } else if (value instanceof SafeUrl) {
      value = SafeUrl.unwrap(value);
    } else if (typeof value === 'string') {
      value = SafeUrl.sanitize(value).getTypedStringValue();
    } else {
      throw new Error(
          SafeHtml.ENABLE_ERROR_MESSAGES ?
              `Attribute "${name}" on tag "${tagName}` +
                  '" requires goog.html.SafeUrl, goog.string.Const, or' +
                  ' string, value "' + value + '" given.' :
              '');
    }
  }

  // Accept SafeUrl, TrustedResourceUrl, etc. for attributes which only require
  // HTML-escaping.
  if (value.implementsGoogStringTypedString) {
    // Ok to call getTypedStringValue() since there's no reliance on the type
    // contract for security here.
    value =
        /** @type {!TypedString} */ (value).getTypedStringValue();
  }

  asserts.assert(
      typeof value === 'string' || typeof value === 'number',
      'String or number value expected, got ' + (typeof value) +
          ' with value: ' + value);
  return `${name}="` + internal.htmlEscape(String(value)) + '"';
}


/**
 * Gets value allowed in "style" attribute.
 * @param {!SafeHtml.AttributeValue} value It could be SafeStyle or a
 *     map which will be passed to SafeStyle.create.
 * @return {string} Unwrapped value.
 * @throws {!Error} If string value is given.
 * @private
 */
function getStyleValue(value) {
  if (!goog.isObject(value)) {
    throw new Error(
        SafeHtml.ENABLE_ERROR_MESSAGES ?
            'The "style" attribute requires goog.html.SafeStyle or map ' +
                'of style properties, ' + (typeof value) + ' given: ' + value :
            '');
  }
  if (!(value instanceof SafeStyle)) {
    // Process the property bag into a style object.
    value = SafeStyle.create(value);
  }
  return SafeStyle.unwrap(value);
}


/**
 * A SafeHtml instance corresponding to the HTML doctype: "<!DOCTYPE html>".
 * @const {!SafeHtml}
 */
SafeHtml.DOCTYPE_HTML = /** @type {!SafeHtml} */ ({
  // NOTE: this compiles to nothing, but hides the possible side effect of
  // SafeHtml creation (due to calling trustedTypes.createPolicy) from the
  // compiler so that the entire call can be removed if the result is not used.
  // MOE:begin_strip
  // TODO(b/155299094): Refactor after adding compiler support.
  // MOE:end_strip
  valueOf: function() {
    return SafeHtml.createSafeHtmlSecurityPrivateDoNotAccessOrElse(
        '<!DOCTYPE html>', Dir.NEUTRAL);
  },
}.valueOf());

/**
 * A SafeHtml instance corresponding to the empty string.
 * @const {!SafeHtml}
 */
SafeHtml.EMPTY = new SafeHtml(
    (goog.global.trustedTypes && goog.global.trustedTypes.emptyHTML) || '',
    Dir.NEUTRAL, CONSTRUCTOR_TOKEN_PRIVATE);

/**
 * A SafeHtml instance corresponding to the <br> tag.
 * @const {!SafeHtml}
 */
SafeHtml.BR = /** @type {!SafeHtml} */ ({
  // NOTE: this compiles to nothing, but hides the possible side effect of
  // SafeHtml creation (due to calling trustedTypes.createPolicy) from the
  // compiler so that the entire call can be removed if the result is not used.
  // MOE:begin_strip
  // TODO(b/155299094): Refactor after adding compiler support.
  // MOE:end_strip
  valueOf: function() {
    return SafeHtml.createSafeHtmlSecurityPrivateDoNotAccessOrElse(
        '<br>', Dir.NEUTRAL);
  },
}.valueOf());


exports = SafeHtml;

;return exports;});

//third_party/javascript/angular/v1_6/goog_hardening/closureSceHelper.js
/**
 * @fileoverview Collection of helpers that link the Angular hardened build to
 *    the Closure goog.html types. This should be compiled alongside Closure,
 *    so that the functions defined here can be called in the hardened Angular
 *    {@code $sce} service.
 *
 * MOE:begin_intracomment_strip
 * @see go/angular-v15-migrate#dependency
 * MOE:end_intracomment_strip
 */

// MOE:begin_strip
// There is no goog.provide to keep JSCompiler from dead-code removing this.
// See http://google3/third_party/java_src/jscomp/java/com/google/javascript/jscomp/JSCompilerRunner.java&l=255&rcl=112285511
// Adding @license_presubmit_check_bypass (this helper is not open source).
// MOE:end_strip

goog.require('goog.html.SafeHtml');
goog.require('goog.html.SafeScript');
goog.require('goog.html.SafeStyle');
goog.require('goog.html.SafeUrl');
goog.require('goog.html.TrustedResourceUrl');


goog.exportSymbol(
    'ng.safehtml.googSceHelper.isGoogHtmlType',

    /**
     * @param {?} value
     * @return {*} true if value is a goog.html type.
     * @public
     */
    function isGoogHtmlType(value) {
      if (value && value.implementsGoogStringTypedString) {
        return true;
      } else {
        return false;
      }
    });

goog.exportSymbol(
    'ng.safehtml.googSceHelper.isCOMPILED',
    /**
     * @return {boolean} the value of COMPILED.
     * @public
     */
    function isCOMPILED() {
      return COMPILED;
    });

goog.exportSymbol(
    'ng.safehtml.googSceHelper.unwrapAny',
    /**
     * Unwraps the value given as a parameter, if it is a goog.html type.
     * Otherwise, returns the parameter. Note that this function will not try to
     * unwrap stock {@code $sce.trustAs} results, and that even though Angular
     * trusts by default  `null`, `undefined` and '', Closure does
     * not, so this function will throw on these values since they are not
     * `goog.html` types.
     * @param {*} value
     * @return {*} An unwrapped version of `value`.
     * @throws {!Error} If the value not of a type among the `goog.html`
     * supported types.
     * @public
     */
    function valueOf(value) {
      if (value instanceof goog.html.TrustedResourceUrl) {
        return goog.html.TrustedResourceUrl.unwrap(value);
      } else if (value instanceof goog.html.SafeHtml) {
        return goog.html.SafeHtml.unwrap(value);
      } else if (value instanceof goog.html.SafeUrl) {
        return goog.html.SafeUrl.unwrap(value);
      } else if (value instanceof goog.html.SafeStyle) {
        return goog.html.SafeStyle.unwrap(value);
      } else if (value instanceof goog.html.SafeScript) {
        return goog.html.SafeScript.unwrap(value);
      } else {
        throw new Error();  // should be caught by Angular
      }
    });

goog.exportSymbol(
    'ng.safehtml.googSceHelper.unwrapGivenContext',
    /**
     * Try to unwrap `maybeTrusted` as a `goog.html` type for {@code
     * type}, then return the value or throw if it failed.
     *
     * @param {string} type Either 'url', 'resourceUrl', 'html', 'js' or 'css'.
     * @param {!goog.html.SafeHtml|!goog.html.SafeUrl|
               !goog.html.TrustedResourceUrl|!goog.html.SafeScript|
               !goog.html.SafeStyle} maybeTrusted Instance of a goog.html type.
     * @return {string} `maybeTrusted` unwrapped to string.
     * @throws {!Error} If maybeTrusted cannot be unwrapped in the given context.
     * @public
     */
    function unwrapGivenContext(type, maybeTrusted) {
      // TODO(rjamet): Is there any good way to get to constants defined
      // in $sce? It seems like we'd need a circular dependency for that.
      if (type == 'html') {  // $sce.HTML
        return goog.html.SafeHtml.unwrap(
            /** @type {!goog.html.SafeHtml} */ (maybeTrusted));
      } else if (type == 'resourceUrl' || type == 'templateUrl') {
        // either $sce.RESOURCE_URL or our new $sce.TEMPLATE_URL
        return goog.html.TrustedResourceUrl.unwrap(
            /** @type {!goog.html.TrustedResourceUrl} */ (maybeTrusted));
      } else if (type == 'url') {  // $sce.URL
        // Angular allows $sce.RESOURCE_URL wherever $sce.URL is allowed.
        if (maybeTrusted instanceof goog.html.TrustedResourceUrl) {
          return goog.html.TrustedResourceUrl.unwrap(maybeTrusted);
        }  // Else assume it's a SafeUrl
        return goog.html.SafeUrl.unwrap(
            /** @type {!goog.html.SafeUrl} */ (maybeTrusted));
      } else if (type == 'css') {  // $sce.CSS
        return goog.html.SafeStyle.unwrap(
            /** @type {!goog.html.SafeStyle} */ (maybeTrusted));
      } else if (type == 'js') {  // $sce.JS
        return goog.html.SafeScript.unwrap(
            /** @type {!goog.html.SafeScript} */ (maybeTrusted));
      }
      throw new Error();  // should be caught by Angular
    });

//third_party/javascript/angular_ui/bootstrap/ui_bootstrap_min_0_13_2.js
/**
 * @license
 * The MIT License
 * 
 * Copyright (c) 2012-2013 the AngularUI Team, https://github.com/organizations/angular-ui/teams/291112
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
/*
 * @license
 * angular-ui-bootstrap
 * http://angular-ui.github.io/bootstrap/

 * Version: 0.13.2 - 2015-08-05
 * License: MIT
 */
angular.module("ui.bootstrap",["ui.bootstrap.collapse","ui.bootstrap.accordion","ui.bootstrap.alert","ui.bootstrap.bindHtml","ui.bootstrap.buttons","ui.bootstrap.carousel","ui.bootstrap.dateparser","ui.bootstrap.position","ui.bootstrap.datepicker","ui.bootstrap.dropdown","ui.bootstrap.modal","ui.bootstrap.pagination","ui.bootstrap.tooltip","ui.bootstrap.popover","ui.bootstrap.progressbar","ui.bootstrap.rating","ui.bootstrap.tabs","ui.bootstrap.timepicker","ui.bootstrap.transition","ui.bootstrap.typeahead"]),angular.module("ui.bootstrap.collapse",[]).directive("collapse",["$animate",function(a){return{link:function(b,c,d){function e(){c.removeClass("collapse").addClass("collapsing").attr("aria-expanded",!0).attr("aria-hidden",!1),a.addClass(c,"in",{to:{height:c[0].scrollHeight+"px"}}).then(f)}function f(){c.removeClass("collapsing"),c.css({height:"auto"})}function g(){return c.hasClass("collapse")||c.hasClass("in")?(c.css({height:c[0].scrollHeight+"px"}).removeClass("collapse").addClass("collapsing").attr("aria-expanded",!1).attr("aria-hidden",!0),void a.removeClass(c,"in",{to:{height:"0"}}).then(h)):h()}function h(){c.css({height:"0"}),c.removeClass("collapsing"),c.addClass("collapse")}b.$watch(d.collapse,function(a){a?g():e()})}}}]),angular.module("ui.bootstrap.accordion",["ui.bootstrap.collapse"]).constant("accordionConfig",{closeOthers:!0}).controller("AccordionController",["$scope","$attrs","accordionConfig",function(a,b,c){this.groups=[],this.closeOthers=function(d){var e=angular.isDefined(b.closeOthers)?a.$eval(b.closeOthers):c.closeOthers;e&&angular.forEach(this.groups,function(a){a!==d&&(a.isOpen=!1)})},this.addGroup=function(a){var b=this;this.groups.push(a),a.$on("$destroy",function(){b.removeGroup(a)})},this.removeGroup=function(a){var b=this.groups.indexOf(a);-1!==b&&this.groups.splice(b,1)}}]).directive("accordion",function(){return{restrict:"EA",controller:"AccordionController",transclude:!0,replace:!1,templateUrl:"template/accordion/accordion.html"}}).directive("accordionGroup",function(){return{require:"^accordion",restrict:"EA",transclude:!0,replace:!0,templateUrl:"template/accordion/accordion-group.html",scope:{heading:"@",isOpen:"=?",isDisabled:"=?"},controller:function(){this.setHeading=function(a){this.heading=a}},link:function(a,b,c,d){d.addGroup(a),a.$watch("isOpen",function(b){b&&d.closeOthers(a)}),a.toggleOpen=function(){a.isDisabled||(a.isOpen=!a.isOpen)}}}}).directive("accordionHeading",function(){return{restrict:"EA",transclude:!0,template:"",replace:!0,require:"^accordionGroup",link:function(a,b,c,d,e){d.setHeading(e(a,angular.noop))}}}).directive("accordionTransclude",function(){return{require:"^accordionGroup",link:function(a,b,c,d){a.$watch(function(){return d[c.accordionTransclude]},function(a){a&&(b.find("span").html(""),b.find("span").append(a))})}}}),angular.module("ui.bootstrap.alert",[]).controller("AlertController",["$scope","$attrs",function(a,b){a.closeable=!!b.close,this.close=a.close}]).directive("alert",function(){return{restrict:"EA",controller:"AlertController",templateUrl:"template/alert/alert.html",transclude:!0,replace:!0,scope:{type:"@",close:"&"}}}).directive("dismissOnTimeout",["$timeout",function(a){return{require:"alert",link:function(b,c,d,e){a(function(){e.close()},parseInt(d.dismissOnTimeout,10))}}}]),angular.module("ui.bootstrap.bindHtml",[]).value("$bindHtmlUnsafeSuppressDeprecated",!1).directive("bindHtmlUnsafe",["$log","$bindHtmlUnsafeSuppressDeprecated",function(a,b){return function(c,d,e){b||a.warn("bindHtmlUnsafe is now deprecated. Use ngBindHtml instead"),d.addClass("ng-binding").data("$binding",e.bindHtmlUnsafe),c.$watch(e.bindHtmlUnsafe,function(a){d.html(a||"")})}}]),angular.module("ui.bootstrap.buttons",[]).constant("buttonConfig",{activeClass:"active",toggleEvent:"click"}).controller("ButtonsController",["buttonConfig",function(a){this.activeClass=a.activeClass||"active",this.toggleEvent=a.toggleEvent||"click"}]).directive("btnRadio",function(){return{require:["btnRadio","ngModel"],controller:"ButtonsController",link:function(a,b,c,d){var e=d[0],f=d[1];f.$render=function(){b.toggleClass(e.activeClass,angular.equals(f.$modelValue,a.$eval(c.btnRadio)))},b.bind(e.toggleEvent,function(){if(!("disabled"in c)){var d=b.hasClass(e.activeClass);(!d||angular.isDefined(c.uncheckable))&&a.$apply(function(){f.$setViewValue(d?null:a.$eval(c.btnRadio)),f.$render()})}})}}}).directive("btnCheckbox",function(){return{require:["btnCheckbox","ngModel"],controller:"ButtonsController",link:function(a,b,c,d){function e(){return g(c.btnCheckboxTrue,!0)}function f(){return g(c.btnCheckboxFalse,!1)}function g(b,c){var d=a.$eval(b);return angular.isDefined(d)?d:c}var h=d[0],i=d[1];i.$render=function(){b.toggleClass(h.activeClass,angular.equals(i.$modelValue,e()))},b.bind(h.toggleEvent,function(){"disabled"in c||a.$apply(function(){i.$setViewValue(b.hasClass(h.activeClass)?f():e()),i.$render()})})}}}),angular.module("ui.bootstrap.carousel",[]).constant("ANIMATE_CSS",angular.version.minor>=4).controller("CarouselController",["$scope","$element","$interval","$animate","ANIMATE_CSS",function(a,b,c,d,e){function f(b,c,f){r||(angular.extend(b,{direction:f,active:!0}),angular.extend(m.currentSlide||{},{direction:f,active:!1}),d.enabled()&&!a.noTransition&&!a.$currentTransition&&b.$element&&(b.$element.data(p,b.direction),a.$currentTransition=!0,e?d.on("addClass",b.$element,function(b){a.$currentTransition=null,a.$currentTransition||d.off("addClass",b)}):b.$element.one("$animate:close",function(){a.$currentTransition=null})),m.currentSlide=b,q=c,h())}function g(a){if(angular.isUndefined(n[a].index))return n[a];{var b;n.length}for(b=0;b<n.length;++b)if(n[b].index==a)return n[b]}function h(){i();var b=+a.interval;!isNaN(b)&&b>0&&(k=c(j,b))}function i(){k&&(c.cancel(k),k=null)}function j(){var b=+a.interval;l&&!isNaN(b)&&b>0&&n.length?a.next():a.pause()}var k,l,m=this,n=m.slides=a.slides=[],o="uib-noTransition",p="uib-slideDirection",q=-1;m.currentSlide=null;var r=!1;m.select=a.select=function(b,c){var d=m.indexOfSlide(b);void 0===c&&(c=d>m.getCurrentIndex()?"next":"prev"),b&&b!==m.currentSlide&&!a.$currentTransition&&f(b,d,c)},a.$on("$destroy",function(){r=!0}),m.getCurrentIndex=function(){return m.currentSlide&&angular.isDefined(m.currentSlide.index)?+m.currentSlide.index:q},m.indexOfSlide=function(a){return angular.isDefined(a.index)?+a.index:n.indexOf(a)},a.next=function(){var b=(m.getCurrentIndex()+1)%n.length;return 0===b&&a.noWrap()?void a.pause():m.select(g(b),"next")},a.prev=function(){var b=m.getCurrentIndex()-1<0?n.length-1:m.getCurrentIndex()-1;return a.noWrap()&&b===n.length-1?void a.pause():m.select(g(b),"prev")},a.isActive=function(a){return m.currentSlide===a},a.$watch("interval",h),a.$on("$destroy",i),a.play=function(){l||(l=!0,h())},a.pause=function(){a.noPause||(l=!1,i())},m.addSlide=function(b,c){!n.length&&c&&c.data(p,"next"),b.$element=c,n.push(b),1===n.length||b.active?(m.select(n[n.length-1]),1==n.length&&a.play()):b.active=!1},m.removeSlide=function(a){angular.isDefined(a.index)&&n.sort(function(a,b){return+a.index>+b.index});var b=n.indexOf(a);n.splice(b,1),n.length>0&&a.active?m.select(b>=n.length?n[b-1]:n[b]):q>b&&q--,0===n.length&&(m.currentSlide=null)},a.$watch("noTransition",function(a){b.data(o,a)})}]).directive("carousel",[function(){return{restrict:"EA",transclude:!0,replace:!0,controller:"CarouselController",require:"carousel",templateUrl:"template/carousel/carousel.html",scope:{interval:"=",noTransition:"=",noPause:"=",noWrap:"&"}}}]).directive("slide",function(){return{require:"^carousel",restrict:"EA",transclude:!0,replace:!0,templateUrl:"template/carousel/slide.html",scope:{active:"=?",index:"=?"},link:function(a,b,c,d){d.addSlide(a,b),a.$on("$destroy",function(){d.removeSlide(a)}),a.$watch("active",function(b){b&&d.select(a)})}}}).animation(".item",["$injector","$animate","ANIMATE_CSS",function(a,b,c){function d(a,b,c){a.removeClass(b),c&&c()}var e="uib-noTransition",f="uib-slideDirection",g=c?a.get("$animateCss"):null;return{beforeAddClass:function(a,c,h){if("active"==c&&a.parent()&&!a.parent().data(e)){var i=!1,j=a.data(f),k="next"==j?"left":"right",l=d.bind(this,a,k+" "+j,h);return a.addClass(j),g?g(a,{addClass:k}).start().done(l):b.addClass(a,k).then(function(){i||l(),h()}),function(){i=!0}}h()},beforeRemoveClass:function(a,c,h){if("active"===c&&a.parent()&&!a.parent().data(e)){var i=!1,j=a.data(f),k="next"==j?"left":"right",l=d.bind(this,a,k,h);return g?g(a,{addClass:k}).start().done(l):b.addClass(a,k).then(function(){i||l(),h()}),function(){i=!0}}h()}}}]),angular.module("ui.bootstrap.dateparser",[]).service("dateParser",["$log","$locale","orderByFilter",function(a,b,c){function d(a){var b=[],d=a.split("");return angular.forEach(g,function(c,e){var f=a.indexOf(e);if(f>-1){a=a.split(""),d[f]="("+c.regex+")",a[f]="$";for(var g=f+1,h=f+e.length;h>g;g++)d[g]="",a[g]="$";a=a.join(""),b.push({index:f,apply:c.apply})}}),{regex:new RegExp("^"+d.join("")+"$"),map:c(b,"index")}}function e(a,b,c){return 1>c?!1:1===b&&c>28?29===c&&(a%4===0&&a%100!==0||a%400===0):3===b||5===b||8===b||10===b?31>c:!0}var f=/[\\\^\$\*\+\?\|\[\]\(\)\.\{\}]/g;this.parsers={};var g={yyyy:{regex:"\\d{4}",apply:function(a){this.year=+a}},yy:{regex:"\\d{2}",apply:function(a){this.year=+a+2e3}},y:{regex:"\\d{1,4}",apply:function(a){this.year=+a}},MMMM:{regex:b.DATETIME_FORMATS.MONTH.join("|"),apply:function(a){this.month=b.DATETIME_FORMATS.MONTH.indexOf(a)}},MMM:{regex:b.DATETIME_FORMATS.SHORTMONTH.join("|"),apply:function(a){this.month=b.DATETIME_FORMATS.SHORTMONTH.indexOf(a)}},MM:{regex:"0[1-9]|1[0-2]",apply:function(a){this.month=a-1}},M:{regex:"[1-9]|1[0-2]",apply:function(a){this.month=a-1}},dd:{regex:"[0-2][0-9]{1}|3[0-1]{1}",apply:function(a){this.date=+a}},d:{regex:"[1-2]?[0-9]{1}|3[0-1]{1}",apply:function(a){this.date=+a}},EEEE:{regex:b.DATETIME_FORMATS.DAY.join("|")},EEE:{regex:b.DATETIME_FORMATS.SHORTDAY.join("|")},HH:{regex:"(?:0|1)[0-9]|2[0-3]",apply:function(a){this.hours=+a}},H:{regex:"1?[0-9]|2[0-3]",apply:function(a){this.hours=+a}},mm:{regex:"[0-5][0-9]",apply:function(a){this.minutes=+a}},m:{regex:"[0-9]|[1-5][0-9]",apply:function(a){this.minutes=+a}},sss:{regex:"[0-9][0-9][0-9]",apply:function(a){this.milliseconds=+a}},ss:{regex:"[0-5][0-9]",apply:function(a){this.seconds=+a}},s:{regex:"[0-9]|[1-5][0-9]",apply:function(a){this.seconds=+a}}};this.parse=function(c,g,h){if(!angular.isString(c)||!g)return c;g=b.DATETIME_FORMATS[g]||g,g=g.replace(f,"\\$&"),this.parsers[g]||(this.parsers[g]=d(g));var i=this.parsers[g],j=i.regex,k=i.map,l=c.match(j);if(l&&l.length){var m,n;angular.isDate(h)&&!isNaN(h.getTime())?m={year:h.getFullYear(),month:h.getMonth(),date:h.getDate(),hours:h.getHours(),minutes:h.getMinutes(),seconds:h.getSeconds(),milliseconds:h.getMilliseconds()}:(h&&a.warn("dateparser:","baseDate is not a valid date"),m={year:1900,month:0,date:1,hours:0,minutes:0,seconds:0,milliseconds:0});for(var o=1,p=l.length;p>o;o++){var q=k[o-1];q.apply&&q.apply.call(m,l[o])}return e(m.year,m.month,m.date)&&(n=new Date(m.year,m.month,m.date,m.hours,m.minutes,m.seconds,m.milliseconds||0)),n}}}]),angular.module("ui.bootstrap.position",[]).factory("$position",["$document","$window",function(a,b){function c(a,c){return a.currentStyle?a.currentStyle[c]:b.getComputedStyle?b.getComputedStyle(a)[c]:a.style[c]}function d(a){return"static"===(c(a,"position")||"static")}var e=function(b){for(var c=a[0],e=b.offsetParent||c;e&&e!==c&&d(e);)e=e.offsetParent;return e||c};return{position:function(b){var c=this.offset(b),d={top:0,left:0},f=e(b[0]);f!=a[0]&&(d=this.offset(angular.element(f)),d.top+=f.clientTop-f.scrollTop,d.left+=f.clientLeft-f.scrollLeft);var g=b[0].getBoundingClientRect();return{width:g.width||b.prop("offsetWidth"),height:g.height||b.prop("offsetHeight"),top:c.top-d.top,left:c.left-d.left}},offset:function(c){var d=c[0].getBoundingClientRect();return{width:d.width||c.prop("offsetWidth"),height:d.height||c.prop("offsetHeight"),top:d.top+(b.pageYOffset||a[0].documentElement.scrollTop),left:d.left+(b.pageXOffset||a[0].documentElement.scrollLeft)}},positionElements:function(a,b,c,d){var e,f,g,h,i=c.split("-"),j=i[0],k=i[1]||"center";e=d?this.offset(a):this.position(a),f=b.prop("offsetWidth"),g=b.prop("offsetHeight");var l={center:function(){return e.left+e.width/2-f/2},left:function(){return e.left},right:function(){return e.left+e.width}},m={center:function(){return e.top+e.height/2-g/2},top:function(){return e.top},bottom:function(){return e.top+e.height}};switch(j){case"right":h={top:m[k](),left:l[j]()};break;case"left":h={top:m[k](),left:e.left-f};break;case"bottom":h={top:m[j](),left:l[k]()};break;default:h={top:e.top-g,left:l[k]()}}return h}}}]),angular.module("ui.bootstrap.datepicker",["ui.bootstrap.dateparser","ui.bootstrap.position"]).constant("datepickerConfig",{formatDay:"dd",formatMonth:"MMMM",formatYear:"yyyy",formatDayHeader:"EEE",formatDayTitle:"MMMM yyyy",formatMonthTitle:"yyyy",datepickerMode:"day",minMode:"day",maxMode:"year",showWeeks:!0,startingDay:0,yearRange:20,minDate:null,maxDate:null,shortcutPropagation:!1}).controller("DatepickerController",["$scope","$attrs","$parse","$interpolate","$log","dateFilter","datepickerConfig",function(a,b,c,d,e,f,g){var h=this,i={$setViewValue:angular.noop};this.modes=["day","month","year"],angular.forEach(["formatDay","formatMonth","formatYear","formatDayHeader","formatDayTitle","formatMonthTitle","minMode","maxMode","showWeeks","startingDay","yearRange","shortcutPropagation"],function(c,e){h[c]=angular.isDefined(b[c])?8>e?d(b[c])(a.$parent):a.$parent.$eval(b[c]):g[c]}),angular.forEach(["minDate","maxDate"],function(d){b[d]?a.$parent.$watch(c(b[d]),function(a){h[d]=a?new Date(a):null,h.refreshView()}):h[d]=g[d]?new Date(g[d]):null}),a.datepickerMode=a.datepickerMode||g.datepickerMode,a.maxMode=h.maxMode,a.uniqueId="datepicker-"+a.$id+"-"+Math.floor(1e4*Math.random()),angular.isDefined(b.initDate)?(this.activeDate=a.$parent.$eval(b.initDate)||new Date,a.$parent.$watch(b.initDate,function(a){a&&(i.$isEmpty(i.$modelValue)||i.$invalid)&&(h.activeDate=a,h.refreshView())})):this.activeDate=new Date,a.isActive=function(b){return 0===h.compare(b.date,h.activeDate)?(a.activeDateId=b.uid,!0):!1},this.init=function(a){i=a,i.$render=function(){h.render()}},this.render=function(){if(i.$viewValue){var a=new Date(i.$viewValue),b=!isNaN(a);b?this.activeDate=a:e.error('Datepicker directive: "ng-model" value must be a Date object, a number of milliseconds since 01.01.1970 or a string representing an RFC2822 or ISO 8601 date.')}this.refreshView()},this.refreshView=function(){if(this.element){this._refreshView();var a=i.$viewValue?new Date(i.$viewValue):null;i.$setValidity("date-disabled",!a||this.element&&!this.isDisabled(a))}},this.createDateObject=function(a,b){var c=i.$viewValue?new Date(i.$viewValue):null;return{date:a,label:f(a,b),selected:c&&0===this.compare(a,c),disabled:this.isDisabled(a),current:0===this.compare(a,new Date),customClass:this.customClass(a)}},this.isDisabled=function(c){return this.minDate&&this.compare(c,this.minDate)<0||this.maxDate&&this.compare(c,this.maxDate)>0||b.dateDisabled&&a.dateDisabled({date:c,mode:a.datepickerMode})},this.customClass=function(b){return a.customClass({date:b,mode:a.datepickerMode})},this.split=function(a,b){for(var c=[];a.length>0;)c.push(a.splice(0,b));return c},this.fixTimeZone=function(a){var b=a.getHours();a.setHours(23===b?b+2:0)},a.select=function(b){if(a.datepickerMode===h.minMode){var c=i.$viewValue?new Date(i.$viewValue):new Date(0,0,0,0,0,0,0);c.setFullYear(b.getFullYear(),b.getMonth(),b.getDate()),i.$setViewValue(c),i.$render()}else h.activeDate=b,a.datepickerMode=h.modes[h.modes.indexOf(a.datepickerMode)-1]},a.move=function(a){var b=h.activeDate.getFullYear()+a*(h.step.years||0),c=h.activeDate.getMonth()+a*(h.step.months||0);h.activeDate.setFullYear(b,c,1),h.refreshView()},a.toggleMode=function(b){b=b||1,a.datepickerMode===h.maxMode&&1===b||a.datepickerMode===h.minMode&&-1===b||(a.datepickerMode=h.modes[h.modes.indexOf(a.datepickerMode)+b])},a.keys={13:"enter",32:"space",33:"pageup",34:"pagedown",35:"end",36:"home",37:"left",38:"up",39:"right",40:"down"};var j=function(){h.element[0].focus()};a.$on("datepicker.focus",j),a.keydown=function(b){var c=a.keys[b.which];if(c&&!b.shiftKey&&!b.altKey)if(b.preventDefault(),h.shortcutPropagation||b.stopPropagation(),"enter"===c||"space"===c){if(h.isDisabled(h.activeDate))return;a.select(h.activeDate),j()}else!b.ctrlKey||"up"!==c&&"down"!==c?(h.handleKeyDown(c,b),h.refreshView()):(a.toggleMode("up"===c?1:-1),j())}}]).directive("datepicker",function(){return{restrict:"EA",replace:!0,templateUrl:"template/datepicker/datepicker.html",scope:{datepickerMode:"=?",dateDisabled:"&",customClass:"&",shortcutPropagation:"&?"},require:["datepicker","?^ngModel"],controller:"DatepickerController",link:function(a,b,c,d){var e=d[0],f=d[1];f&&e.init(f)}}}).directive("daypicker",["dateFilter",function(a){return{restrict:"EA",replace:!0,templateUrl:"template/datepicker/day.html",require:"^datepicker",link:function(b,c,d,e){function f(a,b){return 1!==b||a%4!==0||a%100===0&&a%400!==0?i[b]:29}function g(a,b){for(var c,d=new Array(b),f=new Date(a),g=0;b>g;)c=new Date(f),e.fixTimeZone(c),d[g++]=c,f.setDate(f.getDate()+1);return d}function h(a){var b=new Date(a);b.setDate(b.getDate()+4-(b.getDay()||7));var c=b.getTime();return b.setMonth(0),b.setDate(1),Math.floor(Math.round((c-b)/864e5)/7)+1}b.showWeeks=e.showWeeks,e.step={months:1},e.element=c;var i=[31,28,31,30,31,30,31,31,30,31,30,31];e._refreshView=function(){var c=e.activeDate.getFullYear(),d=e.activeDate.getMonth(),f=new Date(c,d,1),i=e.startingDay-f.getDay(),j=i>0?7-i:-i,k=new Date(f);j>0&&k.setDate(-j+1);for(var l=g(k,42),m=0;42>m;m++)l[m]=angular.extend(e.createDateObject(l[m],e.formatDay),{secondary:l[m].getMonth()!==d,uid:b.uniqueId+"-"+m});b.labels=new Array(7);for(var n=0;7>n;n++)b.labels[n]={abbr:a(l[n].date,e.formatDayHeader),full:a(l[n].date,"EEEE")};if(b.title=a(e.activeDate,e.formatDayTitle),b.rows=e.split(l,7),b.showWeeks){b.weekNumbers=[];for(var o=(11-e.startingDay)%7,p=b.rows.length,q=0;p>q;q++)b.weekNumbers.push(h(b.rows[q][o].date))}},e.compare=function(a,b){return new Date(a.getFullYear(),a.getMonth(),a.getDate())-new Date(b.getFullYear(),b.getMonth(),b.getDate())},e.handleKeyDown=function(a){var b=e.activeDate.getDate();if("left"===a)b-=1;else if("up"===a)b-=7;else if("right"===a)b+=1;else if("down"===a)b+=7;else if("pageup"===a||"pagedown"===a){var c=e.activeDate.getMonth()+("pageup"===a?-1:1);e.activeDate.setMonth(c,1),b=Math.min(f(e.activeDate.getFullYear(),e.activeDate.getMonth()),b)}else"home"===a?b=1:"end"===a&&(b=f(e.activeDate.getFullYear(),e.activeDate.getMonth()));e.activeDate.setDate(b)},e.refreshView()}}}]).directive("monthpicker",["dateFilter",function(a){return{restrict:"EA",replace:!0,templateUrl:"template/datepicker/month.html",require:"^datepicker",link:function(b,c,d,e){e.step={years:1},e.element=c,e._refreshView=function(){for(var c,d=new Array(12),f=e.activeDate.getFullYear(),g=0;12>g;g++)c=new Date(f,g,1),e.fixTimeZone(c),d[g]=angular.extend(e.createDateObject(c,e.formatMonth),{uid:b.uniqueId+"-"+g});b.title=a(e.activeDate,e.formatMonthTitle),b.rows=e.split(d,3)},e.compare=function(a,b){return new Date(a.getFullYear(),a.getMonth())-new Date(b.getFullYear(),b.getMonth())},e.handleKeyDown=function(a){var b=e.activeDate.getMonth();if("left"===a)b-=1;else if("up"===a)b-=3;else if("right"===a)b+=1;else if("down"===a)b+=3;else if("pageup"===a||"pagedown"===a){var c=e.activeDate.getFullYear()+("pageup"===a?-1:1);e.activeDate.setFullYear(c)}else"home"===a?b=0:"end"===a&&(b=11);e.activeDate.setMonth(b)},e.refreshView()}}}]).directive("yearpicker",["dateFilter",function(){return{restrict:"EA",replace:!0,templateUrl:"template/datepicker/year.html",require:"^datepicker",link:function(a,b,c,d){function e(a){return parseInt((a-1)/f,10)*f+1}var f=d.yearRange;d.step={years:f},d.element=b,d._refreshView=function(){for(var b,c=new Array(f),g=0,h=e(d.activeDate.getFullYear());f>g;g++)b=new Date(h+g,0,1),d.fixTimeZone(b),c[g]=angular.extend(d.createDateObject(b,d.formatYear),{uid:a.uniqueId+"-"+g});a.title=[c[0].label,c[f-1].label].join(" - "),a.rows=d.split(c,5)},d.compare=function(a,b){return a.getFullYear()-b.getFullYear()},d.handleKeyDown=function(a){var b=d.activeDate.getFullYear();"left"===a?b-=1:"up"===a?b-=5:"right"===a?b+=1:"down"===a?b+=5:"pageup"===a||"pagedown"===a?b+=("pageup"===a?-1:1)*d.step.years:"home"===a?b=e(d.activeDate.getFullYear()):"end"===a&&(b=e(d.activeDate.getFullYear())+f-1),d.activeDate.setFullYear(b)},d.refreshView()}}}]).constant("datepickerPopupConfig",{datepickerPopup:"yyyy-MM-dd",html5Types:{date:"yyyy-MM-dd","datetime-local":"yyyy-MM-ddTHH:mm:ss.sss",month:"yyyy-MM"},currentText:"Today",clearText:"Clear",closeText:"Done",closeOnDateSelection:!0,appendToBody:!1,showButtonBar:!0}).directive("datepickerPopup",["$compile","$parse","$document","$position","dateFilter","dateParser","datepickerPopupConfig","$timeout",function(a,b,c,d,e,f,g,h){return{restrict:"EA",require:"ngModel",scope:{isOpen:"=?",currentText:"@",clearText:"@",closeText:"@",dateDisabled:"&",customClass:"&"},link:function(i,j,k,l){function m(a){return a.replace(/([A-Z])/g,function(a){return"-"+a.toLowerCase()})}function n(a){if(angular.isNumber(a)&&(a=new Date(a)),a){if(angular.isDate(a)&&!isNaN(a))return a;if(angular.isString(a)){var b=f.parse(a,p,i.date);return isNaN(b)?void 0:b}return void 0}return null}function o(a,b){var c=a||b;if(!k.ngRequired&&!c)return!0;if(angular.isNumber(c)&&(c=new Date(c)),c){if(angular.isDate(c)&&!isNaN(c))return!0;if(angular.isString(c)){var d=f.parse(c,p);return!isNaN(d)}return!1}return!0}var p,q=angular.isDefined(k.closeOnDateSelection)?i.$parent.$eval(k.closeOnDateSelection):g.closeOnDateSelection,r=angular.isDefined(k.datepickerAppendToBody)?i.$parent.$eval(k.datepickerAppendToBody):g.appendToBody;i.showButtonBar=angular.isDefined(k.showButtonBar)?i.$parent.$eval(k.showButtonBar):g.showButtonBar,i.getText=function(a){return i[a+"Text"]||g[a+"Text"]};var s=!1;if(g.html5Types[k.type]?(p=g.html5Types[k.type],s=!0):(p=k.datepickerPopup||g.datepickerPopup,k.$observe("datepickerPopup",function(a){var b=a||g.datepickerPopup;if(b!==p&&(p=b,l.$modelValue=null,!p))throw new Error("datepickerPopup must have a date format specified.")})),!p)throw new Error("datepickerPopup must have a date format specified.");if(s&&k.datepickerPopup)throw new Error("HTML5 date input types do not support custom formats.");var t=angular.element("<div datepicker-popup-wrap><div datepicker></div></div>");t.attr({"ng-model":"date","ng-change":"dateSelection(date)"});var u=angular.element(t.children()[0]);if(s&&"month"==k.type&&(u.attr("datepicker-mode",'"month"'),u.attr("min-mode","month")),k.datepickerOptions){var v=i.$parent.$eval(k.datepickerOptions);v&&v.initDate&&(i.initDate=v.initDate,u.attr("init-date","initDate"),delete v.initDate),angular.forEach(v,function(a,b){u.attr(m(b),a)})}i.watchData={},angular.forEach(["minDate","maxDate","datepickerMode","initDate","shortcutPropagation"],function(a){if(k[a]){var c=b(k[a]);if(i.$parent.$watch(c,function(b){i.watchData[a]=b}),u.attr(m(a),"watchData."+a),"datepickerMode"===a){var d=c.assign;i.$watch("watchData."+a,function(a,b){angular.isFunction(d)&&a!==b&&d(i.$parent,a)})}}}),k.dateDisabled&&u.attr("date-disabled","dateDisabled({ date: date, mode: mode })"),k.showWeeks&&u.attr("show-weeks",k.showWeeks),k.customClass&&u.attr("custom-class","customClass({ date: date, mode: mode })"),s?l.$formatters.push(function(a){return i.date=a,a}):(l.$$parserName="date",l.$validators.date=o,l.$parsers.unshift(n),l.$formatters.push(function(a){return i.date=a,l.$isEmpty(a)?a:e(a,p)})),i.dateSelection=function(a){angular.isDefined(a)&&(i.date=a);var b=i.date?e(i.date,p):null;j.val(b),l.$setViewValue(b),q&&(i.isOpen=!1,j[0].focus())},l.$viewChangeListeners.push(function(){i.date=f.parse(l.$viewValue,p,i.date)});var w=function(a){i.isOpen&&!j[0].contains(a.target)&&i.$apply(function(){i.isOpen=!1})},x=function(a){27===a.which&&i.isOpen?(a.preventDefault(),a.stopPropagation(),i.$apply(function(){i.isOpen=!1}),j[0].focus()):40!==a.which||i.isOpen||(a.preventDefault(),a.stopPropagation(),i.$apply(function(){i.isOpen=!0}))};j.bind("keydown",x),i.keydown=function(a){27===a.which&&(i.isOpen=!1,j[0].focus())},i.$watch("isOpen",function(a){a?(i.position=r?d.offset(j):d.position(j),i.position.top=i.position.top+j.prop("offsetHeight"),h(function(){i.$broadcast("datepicker.focus"),c.bind("click",w)},0,!1)):c.unbind("click",w)}),i.select=function(a){if("today"===a){var b=new Date;angular.isDate(i.date)?(a=new Date(i.date),a.setFullYear(b.getFullYear(),b.getMonth(),b.getDate())):a=new Date(b.setHours(0,0,0,0))}i.dateSelection(a)},i.close=function(){i.isOpen=!1,j[0].focus()};var y=a(t)(i);t.remove(),r?c.find("body").append(y):j.after(y),i.$on("$destroy",function(){i.isOpen===!0&&i.$apply(function(){i.isOpen=!1}),y.remove(),j.unbind("keydown",x),c.unbind("click",w)})}}}]).directive("datepickerPopupWrap",function(){return{restrict:"EA",replace:!0,transclude:!0,templateUrl:"template/datepicker/popup.html"}}),angular.module("ui.bootstrap.dropdown",["ui.bootstrap.position"]).constant("dropdownConfig",{openClass:"open"}).service("dropdownService",["$document","$rootScope",function(a,b){var c=null;this.open=function(b){c||(a.bind("click",d),a.bind("keydown",e)),c&&c!==b&&(c.isOpen=!1),c=b},this.close=function(b){c===b&&(c=null,a.unbind("click",d),a.unbind("keydown",e))};var d=function(a){if(c&&(!a||"disabled"!==c.getAutoClose())){var d=c.getToggleElement();if(!(a&&d&&d[0].contains(a.target))){var e=c.getDropdownElement();a&&"outsideClick"===c.getAutoClose()&&e&&e[0].contains(a.target)||(c.isOpen=!1,b.$$phase||c.$apply())}}},e=function(a){27===a.which?(c.focusToggleElement(),d()):c.isKeynavEnabled()&&/(38|40)/.test(a.which)&&c.isOpen&&(a.preventDefault(),a.stopPropagation(),c.focusDropdownEntry(a.which))}}]).controller("DropdownController",["$scope","$attrs","$parse","dropdownConfig","dropdownService","$animate","$position","$document","$compile","$templateRequest",function(a,b,c,d,e,f,g,h,i,j){var k,l,m=this,n=a.$new(),o=d.openClass,p=angular.noop,q=b.onToggle?c(b.onToggle):angular.noop,r=!1,s=!1;this.init=function(d){m.$element=d,b.isOpen&&(l=c(b.isOpen),p=l.assign,a.$watch(l,function(a){n.isOpen=!!a})),r=angular.isDefined(b.dropdownAppendToBody),s=angular.isDefined(b.keyboardNav),r&&m.dropdownMenu&&(h.find("body").append(m.dropdownMenu),d.on("$destroy",function(){m.dropdownMenu.remove()}))},this.toggle=function(a){return n.isOpen=arguments.length?!!a:!n.isOpen},this.isOpen=function(){return n.isOpen},n.getToggleElement=function(){return m.toggleElement},n.getAutoClose=function(){return b.autoClose||"always"},n.getElement=function(){return m.$element},n.isKeynavEnabled=function(){return s},n.focusDropdownEntry=function(a){var b=m.dropdownMenu?angular.element(m.dropdownMenu).find("a"):angular.element(m.$element).find("ul").eq(0).find("a");switch(a){case 40:m.selectedOption=angular.isNumber(m.selectedOption)?m.selectedOption===b.length-1?m.selectedOption:m.selectedOption+1:0;break;case 38:if(!angular.isNumber(m.selectedOption))return;m.selectedOption=0===m.selectedOption?0:m.selectedOption-1}b[m.selectedOption].focus()},n.getDropdownElement=function(){return m.dropdownMenu},n.focusToggleElement=function(){m.toggleElement&&m.toggleElement[0].focus()},n.$watch("isOpen",function(b,c){if(r&&m.dropdownMenu){var d=g.positionElements(m.$element,m.dropdownMenu,"bottom-left",!0),h={top:d.top+"px",display:b?"block":"none"},l=m.dropdownMenu.hasClass("dropdown-menu-right");l?(h.left="auto",h.right=window.innerWidth-(d.left+m.$element.prop("offsetWidth"))+"px"):(h.left=d.left+"px",h.right="auto"),m.dropdownMenu.css(h)}if(f[b?"addClass":"removeClass"](m.$element,o).then(function(){angular.isDefined(b)&&b!==c&&q(a,{open:!!b})}),b)m.dropdownMenuTemplateUrl&&j(m.dropdownMenuTemplateUrl).then(function(a){k=n.$new(),i(a.trim())(k,function(a){var b=a;m.dropdownMenu.replaceWith(b),m.dropdownMenu=b})}),n.focusToggleElement(),e.open(n);else{if(m.dropdownMenuTemplateUrl){k&&k.$destroy();var s=angular.element('<ul class="dropdown-menu"></ul>');m.dropdownMenu.replaceWith(s),m.dropdownMenu=s}e.close(n),m.selectedOption=null}angular.isFunction(p)&&p(a,b)}),a.$on("$locationChangeSuccess",function(){"disabled"!==n.getAutoClose()&&(n.isOpen=!1)}),a.$on("$destroy",function(){n.$destroy()})}]).directive("dropdown",function(){return{controller:"DropdownController",link:function(a,b,c,d){d.init(b),b.addClass("dropdown")}}}).directive("dropdownMenu",function(){return{restrict:"AC",require:"?^dropdown",link:function(a,b,c,d){if(d){var e=c.templateUrl;e&&(d.dropdownMenuTemplateUrl=e),d.dropdownMenu||(d.dropdownMenu=b)}}}}).directive("keyboardNav",function(){return{restrict:"A",require:"?^dropdown",link:function(a,b,c,d){b.bind("keydown",function(a){if(-1!==[38,40].indexOf(a.which)){a.preventDefault(),a.stopPropagation();var c=angular.element(b).find("a");switch(a.keyCode){case 40:d.selectedOption=angular.isNumber(d.selectedOption)?d.selectedOption===c.length-1?d.selectedOption:d.selectedOption+1:0;break;case 38:d.selectedOption=0===d.selectedOption?0:d.selectedOption-1}c[d.selectedOption].focus()}})}}}).directive("dropdownToggle",function(){return{require:"?^dropdown",link:function(a,b,c,d){if(d){b.addClass("dropdown-toggle"),d.toggleElement=b;var e=function(e){e.preventDefault(),b.hasClass("disabled")||c.disabled||a.$apply(function(){d.toggle()})};b.bind("click",e),b.attr({"aria-haspopup":!0,"aria-expanded":!1}),a.$watch(d.isOpen,function(a){b.attr("aria-expanded",!!a)}),a.$on("$destroy",function(){b.unbind("click",e)})}}}}),angular.module("ui.bootstrap.modal",[]).factory("$$stackedMap",function(){return{createNew:function(){var a=[];return{add:function(b,c){a.push({key:b,value:c})},get:function(b){for(var c=0;c<a.length;c++)if(b==a[c].key)return a[c]},keys:function(){for(var b=[],c=0;c<a.length;c++)b.push(a[c].key);return b},top:function(){return a[a.length-1]},remove:function(b){for(var c=-1,d=0;d<a.length;d++)if(b==a[d].key){c=d;break}return a.splice(c,1)[0]},removeTop:function(){return a.splice(a.length-1,1)[0]},length:function(){return a.length}}}}}).directive("modalBackdrop",["$animate","$modalStack",function(a,b){function c(c,d,e){e.modalInClass&&(a.addClass(d,e.modalInClass),c.$on(b.NOW_CLOSING_EVENT,function(b,c){var f=c();a.removeClass(d,e.modalInClass).then(f)}))}return{restrict:"EA",replace:!0,templateUrl:"template/modal/backdrop.html",compile:function(a,b){return a.addClass(b.backdropClass),c}}}]).directive("modalWindow",["$modalStack","$q","$animate",function(a,b,c){return{restrict:"EA",scope:{index:"@"},replace:!0,transclude:!0,templateUrl:function(a,b){return b.templateUrl||"template/modal/window.html"},link:function(d,e,f){e.addClass(f.windowClass||""),d.size=f.size,d.close=function(b){var c=a.getTop();c&&c.value.backdrop&&"static"!=c.value.backdrop&&b.target===b.currentTarget&&(b.preventDefault(),b.stopPropagation(),a.dismiss(c.key,"backdrop click"))},d.$isRendered=!0;var g=b.defer();f.$observe("modalRender",function(a){"true"==a&&g.resolve()}),g.promise.then(function(){f.modalInClass&&(c.addClass(e,f.modalInClass),d.$on(a.NOW_CLOSING_EVENT,function(a,b){var d=b();c.removeClass(e,f.modalInClass).then(d)}));var b=e[0].querySelectorAll("[autofocus]");b.length?b[0].focus():e[0].focus();var g=a.getTop();g&&a.modalRendered(g.key)})}}}]).directive("modalAnimationClass",[function(){return{compile:function(a,b){b.modalAnimation&&a.addClass(b.modalAnimationClass)}}}]).directive("modalTransclude",function(){return{link:function(a,b,c,d,e){e(a.$parent,function(a){b.empty(),b.append(a)})}}}).factory("$modalStack",["$animate","$timeout","$document","$compile","$rootScope","$q","$$stackedMap",function(a,b,c,d,e,f,g){function h(){for(var a=-1,b=q.keys(),c=0;c<b.length;c++)q.get(b[c]).value.backdrop&&(a=c);

return a}function i(a,b){var d=c.find("body").eq(0),e=q.get(a).value;q.remove(a),k(e.modalDomEl,e.modalScope,function(){d.toggleClass(p,q.length()>0)}),j(),b&&b.focus?b.focus():d.focus()}function j(){if(m&&-1==h()){var a=n;k(m,n,function(){a=null}),m=void 0,n=void 0}}function k(b,c,d){function e(){e.done||(e.done=!0,a.leave(b),c.$destroy(),d&&d())}var g,h=null,i=function(){return g||(g=f.defer(),h=g.promise),function(){g.resolve()}};return c.$broadcast(r.NOW_CLOSING_EVENT,i),f.when(h).then(e)}function l(a,b,c){return!a.value.modalScope.$broadcast("modal.closing",b,c).defaultPrevented}var m,n,o,p="modal-open",q=g.createNew(),r={NOW_CLOSING_EVENT:"modal.stack.now-closing"},s=0,t="a[href], area[href], input:not([disabled]), button:not([disabled]),select:not([disabled]), textarea:not([disabled]), iframe, object, embed, *[tabindex], *[contenteditable=true]";return e.$watch(h,function(a){n&&(n.index=a)}),c.bind("keydown",function(a){var b=q.top();if(b&&b.value.keyboard)switch(a.which){case 27:a.preventDefault(),e.$apply(function(){r.dismiss(b.key,"escape key press")});break;case 9:r.loadFocusElementList(b);var c=!1;a.shiftKey?r.isFocusInFirstItem(a)&&(c=r.focusLastFocusableElement()):r.isFocusInLastItem(a)&&(c=r.focusFirstFocusableElement()),c&&(a.preventDefault(),a.stopPropagation())}}),r.open=function(a,b){var f=c[0].activeElement;q.add(a,{deferred:b.deferred,renderDeferred:b.renderDeferred,modalScope:b.scope,backdrop:b.backdrop,keyboard:b.keyboard});var g=c.find("body").eq(0),i=h();if(i>=0&&!m){n=e.$new(!0),n.index=i;var j=angular.element('<div modal-backdrop="modal-backdrop"></div>');j.attr("backdrop-class",b.backdropClass),b.animation&&j.attr("modal-animation","true"),m=d(j)(n),g.append(m)}var k=angular.element('<div modal-window="modal-window"></div>');k.attr({"template-url":b.windowTemplateUrl,"window-class":b.windowClass,size:b.size,index:q.length()-1,animate:"animate"}).html(b.content),b.animation&&k.attr("modal-animation","true");var l=d(k)(b.scope);q.top().value.modalDomEl=l,q.top().value.modalOpener=f,g.append(l),g.addClass(p),r.clearFocusListCache()},r.close=function(a,b){var c=q.get(a);return c&&l(c,b,!0)?(c.value.deferred.resolve(b),i(a,c.value.modalOpener),!0):!c},r.dismiss=function(a,b){var c=q.get(a);return c&&l(c,b,!1)?(c.value.deferred.reject(b),i(a,c.value.modalOpener),!0):!c},r.dismissAll=function(a){for(var b=this.getTop();b&&this.dismiss(b.key,a);)b=this.getTop()},r.getTop=function(){return q.top()},r.modalRendered=function(a){var b=q.get(a);b&&b.value.renderDeferred.resolve()},r.focusFirstFocusableElement=function(){return o.length>0?(o[0].focus(),!0):!1},r.focusLastFocusableElement=function(){return o.length>0?(o[o.length-1].focus(),!0):!1},r.isFocusInFirstItem=function(a){return o.length>0?(a.target||a.srcElement)==o[0]:!1},r.isFocusInLastItem=function(a){return o.length>0?(a.target||a.srcElement)==o[o.length-1]:!1},r.clearFocusListCache=function(){o=[],s=0},r.loadFocusElementList=function(a){if((void 0===o||!o.length0)&&a){var b=a.value.modalDomEl;b&&b.length&&(o=b[0].querySelectorAll(t))}},r}]).provider("$modal",function(){var a={options:{animation:!0,backdrop:!0,keyboard:!0},$get:["$injector","$rootScope","$q","$templateRequest","$controller","$modalStack",function(b,c,d,e,f,g){function h(a){return a.template?d.when(a.template):e(angular.isFunction(a.templateUrl)?a.templateUrl():a.templateUrl)}function i(a){var c=[];return angular.forEach(a,function(a){(angular.isFunction(a)||angular.isArray(a))&&c.push(d.when(b.invoke(a)))}),c}var j={};return j.open=function(b){var e=d.defer(),j=d.defer(),k=d.defer(),l={result:e.promise,opened:j.promise,rendered:k.promise,close:function(a){return g.close(l,a)},dismiss:function(a){return g.dismiss(l,a)}};if(b=angular.extend({},a.options,b),b.resolve=b.resolve||{},!b.template&&!b.templateUrl)throw new Error("One of template or templateUrl options is required.");var m=d.all([h(b)].concat(i(b.resolve)));return m.then(function(a){var d=(b.scope||c).$new();d.$close=l.close,d.$dismiss=l.dismiss;var h,i={},j=1;b.controller&&(i.$scope=d,i.$modalInstance=l,angular.forEach(b.resolve,function(b,c){i[c]=a[j++]}),h=f(b.controller,i),b.controllerAs&&(b.bindToController&&angular.extend(h,d),d[b.controllerAs]=h)),g.open(l,{scope:d,deferred:e,renderDeferred:k,content:a[0],animation:b.animation,backdrop:b.backdrop,keyboard:b.keyboard,backdropClass:b.backdropClass,windowClass:b.windowClass,windowTemplateUrl:b.windowTemplateUrl,size:b.size})},function(a){e.reject(a)}),m.then(function(){j.resolve(!0)},function(a){j.reject(a)}),l},j}]};return a}),angular.module("ui.bootstrap.pagination",[]).controller("PaginationController",["$scope","$attrs","$parse",function(a,b,c){var d=this,e={$setViewValue:angular.noop},f=b.numPages?c(b.numPages).assign:angular.noop;this.init=function(g,h){e=g,this.config=h,e.$render=function(){d.render()},b.itemsPerPage?a.$parent.$watch(c(b.itemsPerPage),function(b){d.itemsPerPage=parseInt(b,10),a.totalPages=d.calculateTotalPages()}):this.itemsPerPage=h.itemsPerPage,a.$watch("totalItems",function(){a.totalPages=d.calculateTotalPages()}),a.$watch("totalPages",function(b){f(a.$parent,b),a.page>b?a.selectPage(b):e.$render()})},this.calculateTotalPages=function(){var b=this.itemsPerPage<1?1:Math.ceil(a.totalItems/this.itemsPerPage);return Math.max(b||0,1)},this.render=function(){a.page=parseInt(e.$viewValue,10)||1},a.selectPage=function(b,c){var d=!a.ngDisabled||!c;d&&a.page!==b&&b>0&&b<=a.totalPages&&(c&&c.target&&c.target.blur(),e.$setViewValue(b),e.$render())},a.getText=function(b){return a[b+"Text"]||d.config[b+"Text"]},a.noPrevious=function(){return 1===a.page},a.noNext=function(){return a.page===a.totalPages}}]).constant("paginationConfig",{itemsPerPage:10,boundaryLinks:!1,directionLinks:!0,firstText:"First",previousText:"Previous",nextText:"Next",lastText:"Last",rotate:!0}).directive("pagination",["$parse","paginationConfig",function(a,b){return{restrict:"EA",scope:{totalItems:"=",firstText:"@",previousText:"@",nextText:"@",lastText:"@",ngDisabled:"="},require:["pagination","?ngModel"],controller:"PaginationController",templateUrl:"template/pagination/pagination.html",replace:!0,link:function(c,d,e,f){function g(a,b,c){return{number:a,text:b,active:c}}function h(a,b){var c=[],d=1,e=b,f=angular.isDefined(k)&&b>k;f&&(l?(d=Math.max(a-Math.floor(k/2),1),e=d+k-1,e>b&&(e=b,d=e-k+1)):(d=(Math.ceil(a/k)-1)*k+1,e=Math.min(d+k-1,b)));for(var h=d;e>=h;h++){var i=g(h,h,h===a);c.push(i)}if(f&&!l){if(d>1){var j=g(d-1,"...",!1);c.unshift(j)}if(b>e){var m=g(e+1,"...",!1);c.push(m)}}return c}var i=f[0],j=f[1];if(j){var k=angular.isDefined(e.maxSize)?c.$parent.$eval(e.maxSize):b.maxSize,l=angular.isDefined(e.rotate)?c.$parent.$eval(e.rotate):b.rotate;c.boundaryLinks=angular.isDefined(e.boundaryLinks)?c.$parent.$eval(e.boundaryLinks):b.boundaryLinks,c.directionLinks=angular.isDefined(e.directionLinks)?c.$parent.$eval(e.directionLinks):b.directionLinks,i.init(j,b),e.maxSize&&c.$parent.$watch(a(e.maxSize),function(a){k=parseInt(a,10),i.render()});var m=i.render;i.render=function(){m(),c.page>0&&c.page<=c.totalPages&&(c.pages=h(c.page,c.totalPages))}}}}}]).constant("pagerConfig",{itemsPerPage:10,previousText:"« Previous",nextText:"Next »",align:!0}).directive("pager",["pagerConfig",function(a){return{restrict:"EA",scope:{totalItems:"=",previousText:"@",nextText:"@"},require:["pager","?ngModel"],controller:"PaginationController",templateUrl:"template/pagination/pager.html",replace:!0,link:function(b,c,d,e){var f=e[0],g=e[1];g&&(b.align=angular.isDefined(d.align)?b.$parent.$eval(d.align):a.align,f.init(g,a))}}}]),angular.module("ui.bootstrap.tooltip",["ui.bootstrap.position","ui.bootstrap.bindHtml"]).provider("$tooltip",function(){function a(a){var b=/[A-Z]/g,c="-";return a.replace(b,function(a,b){return(b?c:"")+a.toLowerCase()})}var b={placement:"top",animation:!0,popupDelay:0,useContentExp:!1},c={mouseenter:"mouseleave",click:"click",focus:"blur"},d={};this.options=function(a){angular.extend(d,a)},this.setTriggers=function(a){angular.extend(c,a)},this.$get=["$window","$compile","$timeout","$document","$position","$interpolate",function(e,f,g,h,i,j){return function(e,k,l,m){function n(a){var b=a||m.trigger||l,d=c[b]||b;return{show:b,hide:d}}m=angular.extend({},b,d,m);var o=a(e),p=j.startSymbol(),q=j.endSymbol(),r="<div "+o+'-popup title="'+p+"title"+q+'" '+(m.useContentExp?'content-exp="contentExp()" ':'content="'+p+"content"+q+'" ')+'placement="'+p+"placement"+q+'" popup-class="'+p+"popupClass"+q+'" animation="animation" is-open="isOpen"origin-scope="origScope" ></div>';return{restrict:"EA",compile:function(){var a=f(r);return function(b,c,d){function f(){E.isOpen?l():j()}function j(){(!D||b.$eval(d[k+"Enable"]))&&(s(),E.popupDelay?A||(A=g(o,E.popupDelay,!1),A.then(function(a){a()})):o()())}function l(){b.$apply(function(){p()})}function o(){return A=null,z&&(g.cancel(z),z=null),(m.useContentExp?E.contentExp():E.content)?(q(),x.css({top:0,left:0,display:"block"}),E.$digest(),F(),E.isOpen=!0,E.$apply(),F):angular.noop}function p(){E.isOpen=!1,g.cancel(A),A=null,E.animation?z||(z=g(r,500)):r()}function q(){x&&r(),y=E.$new(),x=a(y,function(a){B?h.find("body").append(a):c.after(a)}),m.useContentExp&&y.$watch("contentExp()",function(a){G(),!a&&E.isOpen&&p()})}function r(){z=null,x&&(x.remove(),x=null),y&&(y.$destroy(),y=null)}function s(){t(),u(),v()}function t(){E.popupClass=d[k+"Class"]}function u(){var a=d[k+"Placement"];E.placement=angular.isDefined(a)?a:m.placement}function v(){var a=d[k+"PopupDelay"],b=parseInt(a,10);E.popupDelay=isNaN(b)?m.popupDelay:b}function w(){var a=d[k+"Trigger"];H(),C=n(a),C.show===C.hide?c.bind(C.show,f):(c.bind(C.show,j),c.bind(C.hide,l))}var x,y,z,A,B=angular.isDefined(m.appendToBody)?m.appendToBody:!1,C=n(void 0),D=angular.isDefined(d[k+"Enable"]),E=b.$new(!0),F=function(){if(x){var a=i.positionElements(c,x,E.placement,B);a.top+="px",a.left+="px",x.css(a)}},G=function(){g(F,0,!1)};E.origScope=b,E.isOpen=!1,E.contentExp=function(){return b.$eval(d[e])},m.useContentExp||d.$observe(e,function(a){E.content=a,G(),!a&&E.isOpen&&p()}),d.$observe("disabled",function(a){a&&E.isOpen&&p()}),d.$observe(k+"Title",function(a){E.title=a,G()}),d.$observe(k+"Placement",function(){E.isOpen&&g(function(){u(),o()()},0,!1)});var H=function(){c.unbind(C.show,j),c.unbind(C.hide,l)};w();var I=b.$eval(d[k+"Animation"]);E.animation=angular.isDefined(I)?!!I:m.animation;var J=b.$eval(d[k+"AppendToBody"]);B=angular.isDefined(J)?J:B,B&&b.$on("$locationChangeSuccess",function(){E.isOpen&&p()}),b.$on("$destroy",function(){g.cancel(z),g.cancel(A),H(),r(),E=null})}}}}}]}).directive("tooltipTemplateTransclude",["$animate","$sce","$compile","$templateRequest",function(a,b,c,d){return{link:function(e,f,g){var h,i,j,k=e.$eval(g.tooltipTemplateTranscludeScope),l=0,m=function(){i&&(i.remove(),i=null),h&&(h.$destroy(),h=null),j&&(a.leave(j).then(function(){i=null}),i=j,j=null)};e.$watch(b.parseAsResourceUrl(g.tooltipTemplateTransclude),function(b){var g=++l;b?(d(b,!0).then(function(d){if(g===l){var e=k.$new(),i=d,n=c(i)(e,function(b){m(),a.enter(b,f)});h=e,j=n,h.$emit("$includeContentLoaded",b)}},function(){g===l&&(m(),e.$emit("$includeContentError",b))}),e.$emit("$includeContentRequested",b)):m()}),e.$on("$destroy",m)}}}]).directive("tooltipClasses",function(){return{restrict:"A",link:function(a,b,c){a.placement&&b.addClass(a.placement),a.popupClass&&b.addClass(a.popupClass),a.animation()&&b.addClass(c.tooltipAnimationClass)}}}).directive("tooltipPopup",function(){return{restrict:"EA",replace:!0,scope:{content:"@",placement:"@",popupClass:"@",animation:"&",isOpen:"&"},templateUrl:"template/tooltip/tooltip-popup.html"}}).directive("tooltip",["$tooltip",function(a){return a("tooltip","tooltip","mouseenter")}]).directive("tooltipTemplatePopup",function(){return{restrict:"EA",replace:!0,scope:{contentExp:"&",placement:"@",popupClass:"@",animation:"&",isOpen:"&",originScope:"&"},templateUrl:"template/tooltip/tooltip-template-popup.html"}}).directive("tooltipTemplate",["$tooltip",function(a){return a("tooltipTemplate","tooltip","mouseenter",{useContentExp:!0})}]).directive("tooltipHtmlPopup",function(){return{restrict:"EA",replace:!0,scope:{contentExp:"&",placement:"@",popupClass:"@",animation:"&",isOpen:"&"},templateUrl:"template/tooltip/tooltip-html-popup.html"}}).directive("tooltipHtml",["$tooltip",function(a){return a("tooltipHtml","tooltip","mouseenter",{useContentExp:!0})}]).directive("tooltipHtmlUnsafePopup",function(){return{restrict:"EA",replace:!0,scope:{content:"@",placement:"@",popupClass:"@",animation:"&",isOpen:"&"},templateUrl:"template/tooltip/tooltip-html-unsafe-popup.html"}}).value("tooltipHtmlUnsafeSuppressDeprecated",!1).directive("tooltipHtmlUnsafe",["$tooltip","tooltipHtmlUnsafeSuppressDeprecated","$log",function(a,b,c){return b||c.warn("tooltip-html-unsafe is now deprecated. Use tooltip-html or tooltip-template instead."),a("tooltipHtmlUnsafe","tooltip","mouseenter")}]),angular.module("ui.bootstrap.popover",["ui.bootstrap.tooltip"]).directive("popoverTemplatePopup",function(){return{restrict:"EA",replace:!0,scope:{title:"@",contentExp:"&",placement:"@",popupClass:"@",animation:"&",isOpen:"&",originScope:"&"},templateUrl:"template/popover/popover-template.html"}}).directive("popoverTemplate",["$tooltip",function(a){return a("popoverTemplate","popover","click",{useContentExp:!0})}]).directive("popoverHtmlPopup",function(){return{restrict:"EA",replace:!0,scope:{contentExp:"&",title:"@",placement:"@",popupClass:"@",animation:"&",isOpen:"&"},templateUrl:"template/popover/popover-html.html"}}).directive("popoverHtml",["$tooltip",function(a){return a("popoverHtml","popover","click",{useContentExp:!0})}]).directive("popoverPopup",function(){return{restrict:"EA",replace:!0,scope:{title:"@",content:"@",placement:"@",popupClass:"@",animation:"&",isOpen:"&"},templateUrl:"template/popover/popover.html"}}).directive("popover",["$tooltip",function(a){return a("popover","popover","click")}]),angular.module("ui.bootstrap.progressbar",[]).constant("progressConfig",{animate:!0,max:100}).controller("ProgressController",["$scope","$attrs","progressConfig",function(a,b,c){var d=this,e=angular.isDefined(b.animate)?a.$parent.$eval(b.animate):c.animate;this.bars=[],a.max=angular.isDefined(a.max)?a.max:c.max,this.addBar=function(b,c){e||c.css({transition:"none"}),this.bars.push(b),b.max=a.max,b.$watch("value",function(){b.recalculatePercentage()}),b.recalculatePercentage=function(){b.percent=+(100*b.value/b.max).toFixed(2);var a=0;d.bars.forEach(function(b){a+=b.percent}),a>100&&(b.percent-=a-100)},b.$on("$destroy",function(){c=null,d.removeBar(b)})},this.removeBar=function(a){this.bars.splice(this.bars.indexOf(a),1)},a.$watch("max",function(){d.bars.forEach(function(b){b.max=a.max,b.recalculatePercentage()})})}]).directive("progress",function(){return{restrict:"EA",replace:!0,transclude:!0,controller:"ProgressController",require:"progress",scope:{max:"=?"},templateUrl:"template/progressbar/progress.html"}}).directive("bar",function(){return{restrict:"EA",replace:!0,transclude:!0,require:"^progress",scope:{value:"=",type:"@"},templateUrl:"template/progressbar/bar.html",link:function(a,b,c,d){d.addBar(a,b)}}}).directive("progressbar",function(){return{restrict:"EA",replace:!0,transclude:!0,controller:"ProgressController",scope:{value:"=",max:"=?",type:"@"},templateUrl:"template/progressbar/progressbar.html",link:function(a,b,c,d){d.addBar(a,angular.element(b.children()[0]))}}}),angular.module("ui.bootstrap.rating",[]).constant("ratingConfig",{max:5,stateOn:null,stateOff:null,titles:["one","two","three","four","five"]}).controller("RatingController",["$scope","$attrs","ratingConfig",function(a,b,c){var d={$setViewValue:angular.noop};this.init=function(e){d=e,d.$render=this.render,d.$formatters.push(function(a){return angular.isNumber(a)&&a<<0!==a&&(a=Math.round(a)),a}),this.stateOn=angular.isDefined(b.stateOn)?a.$parent.$eval(b.stateOn):c.stateOn,this.stateOff=angular.isDefined(b.stateOff)?a.$parent.$eval(b.stateOff):c.stateOff;var f=angular.isDefined(b.titles)?a.$parent.$eval(b.titles):c.titles;this.titles=angular.isArray(f)&&f.length>0?f:c.titles;var g=angular.isDefined(b.ratingStates)?a.$parent.$eval(b.ratingStates):new Array(angular.isDefined(b.max)?a.$parent.$eval(b.max):c.max);a.range=this.buildTemplateObjects(g)},this.buildTemplateObjects=function(a){for(var b=0,c=a.length;c>b;b++)a[b]=angular.extend({index:b},{stateOn:this.stateOn,stateOff:this.stateOff,title:this.getTitle(b)},a[b]);return a},this.getTitle=function(a){return a>=this.titles.length?a+1:this.titles[a]},a.rate=function(b){!a.readonly&&b>=0&&b<=a.range.length&&(d.$setViewValue(d.$viewValue===b?0:b),d.$render())},a.enter=function(b){a.readonly||(a.value=b),a.onHover({value:b})},a.reset=function(){a.value=d.$viewValue,a.onLeave()},a.onKeydown=function(b){/(37|38|39|40)/.test(b.which)&&(b.preventDefault(),b.stopPropagation(),a.rate(a.value+(38===b.which||39===b.which?1:-1)))},this.render=function(){a.value=d.$viewValue}}]).directive("rating",function(){return{restrict:"EA",require:["rating","ngModel"],scope:{readonly:"=?",onHover:"&",onLeave:"&"},controller:"RatingController",templateUrl:"template/rating/rating.html",replace:!0,link:function(a,b,c,d){var e=d[0],f=d[1];e.init(f)}}}),angular.module("ui.bootstrap.tabs",[]).controller("TabsetController",["$scope",function(a){var b=this,c=b.tabs=a.tabs=[];b.select=function(a){angular.forEach(c,function(b){b.active&&b!==a&&(b.active=!1,b.onDeselect())}),a.active=!0,a.onSelect()},b.addTab=function(a){c.push(a),1===c.length&&a.active!==!1?a.active=!0:a.active?b.select(a):a.active=!1},b.removeTab=function(a){var e=c.indexOf(a);if(a.active&&c.length>1&&!d){var f=e==c.length-1?e-1:e+1;b.select(c[f])}c.splice(e,1)};var d;a.$on("$destroy",function(){d=!0})}]).directive("tabset",function(){return{restrict:"EA",transclude:!0,replace:!0,scope:{type:"@"},controller:"TabsetController",templateUrl:"template/tabs/tabset.html",link:function(a,b,c){a.vertical=angular.isDefined(c.vertical)?a.$parent.$eval(c.vertical):!1,a.justified=angular.isDefined(c.justified)?a.$parent.$eval(c.justified):!1}}}).directive("tab",["$parse","$log",function(a,b){return{require:"^tabset",restrict:"EA",replace:!0,templateUrl:"template/tabs/tab.html",transclude:!0,scope:{active:"=?",heading:"@",onSelect:"&select",onDeselect:"&deselect"},controller:function(){},link:function(c,d,e,f,g){c.$watch("active",function(a){a&&f.select(c)}),c.disabled=!1,e.disable&&c.$parent.$watch(a(e.disable),function(a){c.disabled=!!a}),e.disabled&&(b.warn('Use of "disabled" attribute has been deprecated, please use "disable"'),c.$parent.$watch(a(e.disabled),function(a){c.disabled=!!a})),c.select=function(){c.disabled||(c.active=!0)},f.addTab(c),c.$on("$destroy",function(){f.removeTab(c)}),c.$transcludeFn=g}}}]).directive("tabHeadingTransclude",[function(){return{restrict:"A",require:"^tab",link:function(a,b){a.$watch("headingElement",function(a){a&&(b.html(""),b.append(a))})}}}]).directive("tabContentTransclude",function(){function a(a){return a.tagName&&(a.hasAttribute("tab-heading")||a.hasAttribute("data-tab-heading")||"tab-heading"===a.tagName.toLowerCase()||"data-tab-heading"===a.tagName.toLowerCase())}return{restrict:"A",require:"^tabset",link:function(b,c,d){var e=b.$eval(d.tabContentTransclude);e.$transcludeFn(e.$parent,function(b){angular.forEach(b,function(b){a(b)?e.headingElement=b:c.append(b)})})}}}),angular.module("ui.bootstrap.timepicker",[]).constant("timepickerConfig",{hourStep:1,minuteStep:1,showMeridian:!0,meridians:null,readonlyInput:!1,mousewheel:!0,arrowkeys:!0,showSpinners:!0}).controller("TimepickerController",["$scope","$attrs","$parse","$log","$locale","timepickerConfig",function(a,b,c,d,e,f){function g(){var b=parseInt(a.hours,10),c=a.showMeridian?b>0&&13>b:b>=0&&24>b;return c?(a.showMeridian&&(12===b&&(b=0),a.meridian===p[1]&&(b+=12)),b):void 0}function h(){var b=parseInt(a.minutes,10);return b>=0&&60>b?b:void 0}function i(a){return angular.isDefined(a)&&a.toString().length<2?"0"+a:a.toString()}function j(a){k(),o.$setViewValue(new Date(n)),l(a)}function k(){o.$setValidity("time",!0),a.invalidHours=!1,a.invalidMinutes=!1}function l(b){var c=n.getHours(),d=n.getMinutes();a.showMeridian&&(c=0===c||12===c?12:c%12),a.hours="h"===b?c:i(c),"m"!==b&&(a.minutes=i(d)),a.meridian=n.getHours()<12?p[0]:p[1]}function m(a){var b=new Date(n.getTime()+6e4*a);n.setHours(b.getHours(),b.getMinutes()),j()}var n=new Date,o={$setViewValue:angular.noop},p=angular.isDefined(b.meridians)?a.$parent.$eval(b.meridians):f.meridians||e.DATETIME_FORMATS.AMPMS;this.init=function(c,d){o=c,o.$render=this.render,o.$formatters.unshift(function(a){return a?new Date(a):null});var e=d.eq(0),g=d.eq(1),h=angular.isDefined(b.mousewheel)?a.$parent.$eval(b.mousewheel):f.mousewheel;h&&this.setupMousewheelEvents(e,g);var i=angular.isDefined(b.arrowkeys)?a.$parent.$eval(b.arrowkeys):f.arrowkeys;i&&this.setupArrowkeyEvents(e,g),a.readonlyInput=angular.isDefined(b.readonlyInput)?a.$parent.$eval(b.readonlyInput):f.readonlyInput,this.setupInputEvents(e,g)};var q=f.hourStep;b.hourStep&&a.$parent.$watch(c(b.hourStep),function(a){q=parseInt(a,10)});var r=f.minuteStep;b.minuteStep&&a.$parent.$watch(c(b.minuteStep),function(a){r=parseInt(a,10)}),a.showMeridian=f.showMeridian,b.showMeridian&&a.$parent.$watch(c(b.showMeridian),function(b){if(a.showMeridian=!!b,o.$error.time){var c=g(),d=h();angular.isDefined(c)&&angular.isDefined(d)&&(n.setHours(c),j())}else l()}),this.setupMousewheelEvents=function(b,c){var d=function(a){a.originalEvent&&(a=a.originalEvent);var b=a.wheelDelta?a.wheelDelta:-a.deltaY;return a.detail||b>0};b.bind("mousewheel wheel",function(b){a.$apply(d(b)?a.incrementHours():a.decrementHours()),b.preventDefault()}),c.bind("mousewheel wheel",function(b){a.$apply(d(b)?a.incrementMinutes():a.decrementMinutes()),b.preventDefault()})},this.setupArrowkeyEvents=function(b,c){b.bind("keydown",function(b){38===b.which?(b.preventDefault(),a.incrementHours(),a.$apply()):40===b.which&&(b.preventDefault(),a.decrementHours(),a.$apply())}),c.bind("keydown",function(b){38===b.which?(b.preventDefault(),a.incrementMinutes(),a.$apply()):40===b.which&&(b.preventDefault(),a.decrementMinutes(),a.$apply())})},this.setupInputEvents=function(b,c){if(a.readonlyInput)return a.updateHours=angular.noop,void(a.updateMinutes=angular.noop);var d=function(b,c){o.$setViewValue(null),o.$setValidity("time",!1),angular.isDefined(b)&&(a.invalidHours=b),angular.isDefined(c)&&(a.invalidMinutes=c)};a.updateHours=function(){var a=g();angular.isDefined(a)?(n.setHours(a),j("h")):d(!0)},b.bind("blur",function(){!a.invalidHours&&a.hours<10&&a.$apply(function(){a.hours=i(a.hours)})}),a.updateMinutes=function(){var a=h();angular.isDefined(a)?(n.setMinutes(a),j("m")):d(void 0,!0)},c.bind("blur",function(){!a.invalidMinutes&&a.minutes<10&&a.$apply(function(){a.minutes=i(a.minutes)})})},this.render=function(){var a=o.$viewValue;isNaN(a)?(o.$setValidity("time",!1),d.error('Timepicker directive: "ng-model" value must be a Date object, a number of milliseconds since 01.01.1970 or a string representing an RFC2822 or ISO 8601 date.')):(a&&(n=a),k(),l())},a.showSpinners=angular.isDefined(b.showSpinners)?a.$parent.$eval(b.showSpinners):f.showSpinners,a.incrementHours=function(){m(60*q)},a.decrementHours=function(){m(60*-q)},a.incrementMinutes=function(){m(r)},a.decrementMinutes=function(){m(-r)},a.toggleMeridian=function(){m(720*(n.getHours()<12?1:-1))}}]).directive("timepicker",function(){return{restrict:"EA",require:["timepicker","?^ngModel"],controller:"TimepickerController",replace:!0,scope:{},templateUrl:"template/timepicker/timepicker.html",link:function(a,b,c,d){var e=d[0],f=d[1];f&&e.init(f,b.find("input"))}}}),angular.module("ui.bootstrap.transition",[]).value("$transitionSuppressDeprecated",!1).factory("$transition",["$q","$timeout","$rootScope","$log","$transitionSuppressDeprecated",function(a,b,c,d,e){function f(a){for(var b in a)if(void 0!==h.style[b])return a[b]}e||d.warn("$transition is now deprecated. Use $animate from ngAnimate instead.");var g=function(d,e,f){f=f||{};var h=a.defer(),i=g[f.animation?"animationEndEventName":"transitionEndEventName"],j=function(){c.$apply(function(){d.unbind(i,j),h.resolve(d)})};return i&&d.bind(i,j),b(function(){angular.isString(e)?d.addClass(e):angular.isFunction(e)?e(d):angular.isObject(e)&&d.css(e),i||h.resolve(d)}),h.promise.cancel=function(){i&&d.unbind(i,j),h.reject("Transition cancelled")},h.promise},h=document.createElement("trans"),i={WebkitTransition:"webkitTransitionEnd",MozTransition:"transitionend",OTransition:"oTransitionEnd",transition:"transitionend"},j={WebkitTransition:"webkitAnimationEnd",MozTransition:"animationend",OTransition:"oAnimationEnd",transition:"animationend"};return g.transitionEndEventName=f(i),g.animationEndEventName=f(j),g}]),angular.module("ui.bootstrap.typeahead",["ui.bootstrap.position","ui.bootstrap.bindHtml"]).factory("typeaheadParser",["$parse",function(a){var b=/^\s*([\s\S]+?)(?:\s+as\s+([\s\S]+?))?\s+for\s+(?:([\$\w][\$\w\d]*))\s+in\s+([\s\S]+?)$/;return{parse:function(c){var d=c.match(b);if(!d)throw new Error('Expected typeahead specification in form of "_modelValue_ (as _label_)? for _item_ in _collection_" but got "'+c+'".');return{itemName:d[3],source:a(d[4]),viewMapper:a(d[2]||d[1]),modelMapper:a(d[1])}}}}]).directive("typeahead",["$compile","$parse","$q","$timeout","$document","$window","$rootScope","$position","typeaheadParser",function(a,b,c,d,e,f,g,h,i){var j=[9,13,27,38,40],k=200;return{require:"ngModel",link:function(l,m,n,o){function p(){G.moveInProgress||(G.moveInProgress=!0,G.$digest()),N&&d.cancel(N),N=d(function(){G.matches.length&&q(),G.moveInProgress=!1,G.$digest()},k)}function q(){G.position=B?h.offset(m):h.position(m),G.position.top+=m.prop("offsetHeight")}var r=l.$eval(n.typeaheadMinLength);r||0===r||(r=1);var s,t,u=l.$eval(n.typeaheadWaitMs)||0,v=l.$eval(n.typeaheadEditable)!==!1,w=b(n.typeaheadLoading).assign||angular.noop,x=b(n.typeaheadOnSelect),y=angular.isDefined(n.typeaheadSelectOnBlur)?l.$eval(n.typeaheadSelectOnBlur):!1,z=b(n.typeaheadNoResults).assign||angular.noop,A=n.typeaheadInputFormatter?b(n.typeaheadInputFormatter):void 0,B=n.typeaheadAppendToBody?l.$eval(n.typeaheadAppendToBody):!1,C=l.$eval(n.typeaheadFocusFirst)!==!1,D=n.typeaheadSelectOnExact?l.$eval(n.typeaheadSelectOnExact):!1,E=b(n.ngModel).assign,F=i.parse(n.typeahead),G=l.$new();l.$on("$destroy",function(){G.$destroy()});var H="typeahead-"+G.$id+"-"+Math.floor(1e4*Math.random());m.attr({"aria-autocomplete":"list","aria-expanded":!1,"aria-owns":H});var I=angular.element("<div typeahead-popup></div>");I.attr({id:H,matches:"matches",active:"activeIdx",select:"select(activeIdx)","move-in-progress":"moveInProgress",query:"query",position:"position"}),angular.isDefined(n.typeaheadTemplateUrl)&&I.attr("template-url",n.typeaheadTemplateUrl);var J=function(){G.matches=[],G.activeIdx=-1,m.attr("aria-expanded",!1)},K=function(a){return H+"-option-"+a};G.$watch("activeIdx",function(a){0>a?m.removeAttr("aria-activedescendant"):m.attr("aria-activedescendant",K(a))});var L=function(a,b){return G.matches.length>b&&a?a.toUpperCase()===G.matches[b].label.toUpperCase():!1},M=function(a){var b={$viewValue:a};w(l,!0),z(l,!1),c.when(F.source(l,b)).then(function(c){var d=a===o.$viewValue;if(d&&s)if(c&&c.length>0){G.activeIdx=C?0:-1,z(l,!1),G.matches.length=0;for(var e=0;e<c.length;e++)b[F.itemName]=c[e],G.matches.push({id:K(e),label:F.viewMapper(G,b),model:c[e]});G.query=a,q(),m.attr("aria-expanded",!0),D&&1===G.matches.length&&L(a,0)&&G.select(0)}else J(),z(l,!0);d&&w(l,!1)},function(){J(),w(l,!1),z(l,!0)})};B&&(angular.element(f).bind("resize",p),e.find("body").bind("scroll",p));var N;G.moveInProgress=!1,J(),G.query=void 0;var O,P=function(a){O=d(function(){M(a)},u)},Q=function(){O&&d.cancel(O)};o.$parsers.unshift(function(a){return s=!0,0===r||a&&a.length>=r?u>0?(Q(),P(a)):M(a):(w(l,!1),Q(),J()),v?a:a?void o.$setValidity("editable",!1):(o.$setValidity("editable",!0),a)}),o.$formatters.push(function(a){var b,c,d={};return v||o.$setValidity("editable",!0),A?(d.$model=a,A(l,d)):(d[F.itemName]=a,b=F.viewMapper(l,d),d[F.itemName]=void 0,c=F.viewMapper(l,d),b!==c?b:a)}),G.select=function(a){var b,c,e={};t=!0,e[F.itemName]=c=G.matches[a].model,b=F.modelMapper(l,e),E(l,b),o.$setValidity("editable",!0),o.$setValidity("parse",!0),x(l,{$item:c,$model:b,$label:F.viewMapper(l,e)}),J(),d(function(){m[0].focus()},0,!1)},m.bind("keydown",function(a){if(0!==G.matches.length&&-1!==j.indexOf(a.which)){if(-1===G.activeIdx&&(9===a.which||13===a.which))return J(),void G.$digest();a.preventDefault(),40===a.which?(G.activeIdx=(G.activeIdx+1)%G.matches.length,G.$digest()):38===a.which?(G.activeIdx=(G.activeIdx>0?G.activeIdx:G.matches.length)-1,G.$digest()):13===a.which||9===a.which?G.$apply(function(){G.select(G.activeIdx)}):27===a.which&&(a.stopPropagation(),J(),G.$digest())}}),m.bind("blur",function(){y&&G.matches.length&&-1!==G.activeIdx&&!t&&(t=!0,G.$apply(function(){G.select(G.activeIdx)})),s=!1,t=!1});var R=function(a){m[0]!==a.target&&3!==a.which&&0!==G.matches.length&&(J(),g.$$phase||G.$digest())};e.bind("click",R),l.$on("$destroy",function(){e.unbind("click",R),B&&S.remove(),I.remove()});var S=a(I)(G);B?e.find("body").append(S):m.after(S)}}}]).directive("typeaheadPopup",function(){return{restrict:"EA",scope:{matches:"=",query:"=",active:"=",position:"&",moveInProgress:"=",select:"&"},replace:!0,templateUrl:"template/typeahead/typeahead-popup.html",link:function(a,b,c){a.templateUrl=c.templateUrl,a.isOpen=function(){return a.matches.length>0},a.isActive=function(b){return a.active==b},a.selectActive=function(b){a.active=b},a.selectMatch=function(b){a.select({activeIdx:b})}}}}).directive("typeaheadMatch",["$templateRequest","$compile","$parse",function(a,b,c){return{restrict:"EA",scope:{index:"=",match:"=",query:"="},link:function(d,e,f){var g=c(f.templateUrl)(d.$parent)||"template/typeahead/typeahead-match.html";a(g).then(function(a){b(a.trim())(d,function(a){e.replaceWith(a)})})}}}]).filter("typeaheadHighlight",function(){function a(a){return a.replace(/([.?*+^$[\]\\(){}|-])/g,"\\$1")}return function(b,c){return c?(""+b).replace(new RegExp(a(c),"gi"),"<strong>$&</strong>"):b}}),!angular.$$csp()&&angular.element(document).find("head").prepend('<style type="text/css">.ng-animate.item:not(.left):not(.right){-webkit-transition:0s ease-in-out left;transition:0s ease-in-out left}</style>');

