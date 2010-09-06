// Copyright 2007-2010 Google, Inc.

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//     http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


package com.metaweb.acre.script;

import org.mozilla.javascript.Callable;
import org.mozilla.javascript.Context;
import org.mozilla.javascript.ContextFactory;
import org.mozilla.javascript.Scriptable;

import com.metaweb.acre.Configuration;
import com.metaweb.acre.util.exceptions.AcreScriptError;
import com.metaweb.util.logging.MetawebLogger;

/**
 * Custom ContextFactory <br>
 * It is setup as the global {@link ContextFactory} by the {@link HostEnv} It is
 * used to setup custom {@link AcreClassShutter}<br>
 * it also monitors the execution time to impose a time limit based on the given time quota
 */
public class AcreContextFactory extends ContextFactory {

    private static MetawebLogger _logger = new MetawebLogger();

    private static boolean GENERATE_JS_DEBUG_INFO = Configuration.Values.GENERATE_JS_DEBUG_INFO.getBoolean();

    // Custom {@link Context} to store execution time.
    @SuppressWarnings("deprecation")
    public static class AcreContext extends Context {
        public long startTime;
        public long deadline;
    }
    
    @Override
    protected Context makeContext() {
        AcreContext cx = new AcreContext();
        
        // this allows for script line numbers in stack traces
        cx.setGeneratingDebug(GENERATE_JS_DEBUG_INFO);

        // Make Rhino runtime to call observeInstructionCount
        // each 10000 bytecode instructions
        cx.setInstructionObserverThreshold(1000);

        // these will be used to lock down the LiveConnect things
        cx.setClassShutter(new AcreClassShutter());

        cx.setGeneratingSource(true);

        // provide JavaScript version 1.7
        cx.setLanguageVersion(Context.VERSION_1_7);

        return cx;
    }

    @Override
    protected void observeInstructionCount(Context cx, int instructionCount) {
        AcreContext mcx = (AcreContext) cx;

        if (System.currentTimeMillis() > mcx.deadline) {
            _logger.error("script.time_limit.exceeded", "script terminated (was taking too long to complete)");
            throw new AcreScriptError("the script was taking too long to complete");
        }
    }

    @Override
    protected Object doTopCall(Callable callable, Context cx, Scriptable scope, Scriptable thisObj, Object[] args) {
        ((AcreContext) cx).startTime = System.currentTimeMillis();
        return super.doTopCall(callable, cx, scope, thisObj, args);
    }

    @Override
    public boolean hasFeature(Context cx, int featureIndex) {
        if (featureIndex == Context.FEATURE_E4X) {
            return false;
        }
        return super.hasFeature(cx, featureIndex);
    }
}