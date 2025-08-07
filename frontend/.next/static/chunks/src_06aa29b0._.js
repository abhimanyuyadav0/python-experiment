(globalThis.TURBOPACK = globalThis.TURBOPACK || []).push([typeof document === "object" ? document.currentScript : undefined, {

"[project]/src/lib/api/axois.ts [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "default": ()=>__TURBOPACK__default__export__
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$axios$2f$lib$2f$axios$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/axios/lib/axios.js [app-client] (ecmascript)");
;
const axoisInstance = __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$axios$2f$lib$2f$axios$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].create({
    baseURL: ("TURBOPACK compile-time value", "http://127.0.0.1:5001/"),
    headers: {
        "centent-Type": "application/json"
    }
});
axoisInstance.interceptors.request.use((config)=>{
    const tokenDataStr = ("TURBOPACK compile-time truthy", 1) ? localStorage.getItem("tokenData") : "TURBOPACK unreachable";
    if (tokenDataStr) {
        try {
            const tokenData = JSON.parse(tokenDataStr);
            if (Date.now() <= tokenData.expiresAt) {
                config.headers.Authorization = "Bearer ".concat(tokenData.token);
            }
        } catch (error) {
            console.error('Error parsing token data:', error);
        }
    }
    return config;
}, (error)=>Promise.reject(error));
let isRefreshing = false;
let failedQueue = [];
function processQueue(error) {
    let token = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : null;
    failedQueue.forEach((prom)=>{
        if (error) {
            prom.reject(error);
        } else {
            prom.resolve(token);
        }
    });
    failedQueue = [];
}
axoisInstance.interceptors.response.use((response)=>response, async (error)=>{
    const originalRequest = error.config;
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
        if (isRefreshing) {
            return new Promise(function(resolve, reject) {
                failedQueue.push({
                    resolve,
                    reject
                });
            }).then((token)=>{
                originalRequest.headers["Authorization"] = "Bearer " + token;
                return axoisInstance(originalRequest);
            }).catch((err)=>Promise.reject(err));
        }
        originalRequest._retry = true;
        isRefreshing = true;
        // Token expired, redirect to login
        localStorage.removeItem("tokenData");
        localStorage.removeItem("user");
        window.location.href = "/auth/login";
        return Promise.reject(error);
    }
    return Promise.reject(error);
});
const __TURBOPACK__default__export__ = axoisInstance;
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/lib/api/services/userServices/index.ts [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "deleteUser": ()=>deleteUser,
    "forgetPassword": ()=>forgetPassword,
    "getAllUsers": ()=>getAllUsers,
    "getUser": ()=>getUser,
    "loginUser": ()=>loginUser,
    "refreshToken": ()=>refreshToken,
    "resetPassword": ()=>resetPassword,
    "signupUser": ()=>signupUser
});
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$axois$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/lib/api/axois.ts [app-client] (ecmascript)");
;
const getUser = (id)=>__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$axois$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].get("/api/v1/users/".concat(id));
const loginUser = (data)=>{
    return __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$axois$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].post("/api/v1/users/authenticate", data);
};
const refreshToken = (data)=>{
    return __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$axois$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].post("/auth/refresh", data);
};
const forgetPassword = (data)=>{
    return __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$axois$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].post("/auth/forgot-password", data);
};
const resetPassword = (data)=>{
    return __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$axois$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].post("/auth/reset-password", data);
};
const signupUser = (data)=>{
    return __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$axois$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].post("/api/v1/users/", data);
};
const getAllUsers = ()=>__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$axois$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].get("/api/v1/users/");
const deleteUser = (id)=>__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$axois$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].delete("/api/v1/users/".concat(id));
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/contexts/AuthContext.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "AuthProvider": ()=>AuthProvider,
    "useAuth": ()=>useAuth
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$services$2f$userServices$2f$index$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/lib/api/services/userServices/index.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/navigation.js [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature(), _s1 = __turbopack_context__.k.signature();
"use client";
;
;
;
const AuthContext = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["createContext"])(undefined);
const useAuth = ()=>{
    _s();
    const context = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useContext"])(AuthContext);
    if (context === undefined) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
};
_s(useAuth, "b9L3QQ+jgeyIrH0NfHrJ8nn7VMU=");
const AuthProvider = (param)=>{
    let { children } = param;
    _s1();
    const [user, setUser] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [token, setToken] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [isLoading, setIsLoading] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(true);
    const router = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRouter"])();
    // Token management functions
    const saveToken = (token, expiresAt)=>{
        const tokenData = {
            token,
            expiresAt
        };
        localStorage.setItem("tokenData", JSON.stringify(tokenData));
        setToken(token);
    };
    const getToken = ()=>{
        const tokenDataStr = localStorage.getItem("tokenData");
        if (!tokenDataStr) return null;
        try {
            const tokenData = JSON.parse(tokenDataStr);
            if (Date.now() > tokenData.expiresAt) {
                // Token expired
                localStorage.removeItem("tokenData");
                localStorage.removeItem("user");
                setToken(null);
                setUser(null);
                return null;
            }
            return tokenData.token;
        } catch (error) {
            console.error("Error parsing token data:", error);
            localStorage.removeItem("tokenData");
            return null;
        }
    };
    const clearToken = ()=>{
        localStorage.removeItem("tokenData");
        localStorage.removeItem("user");
        setToken(null);
        setUser(null);
        router.push("/auth/login");
    };
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "AuthProvider.useEffect": ()=>{
            // Check if user is logged in on app start
            const currentToken = getToken();
            const userData = localStorage.getItem("user");
            if (currentToken && userData) {
                try {
                    setUser(JSON.parse(userData));
                    setToken(currentToken);
                } catch (error) {
                    console.error("Error parsing user data:", error);
                    clearToken();
                }
            }
            setIsLoading(false);
        }
    }["AuthProvider.useEffect"], []);
    // Check token expiration every minute
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "AuthProvider.useEffect": ()=>{
            const interval = setInterval({
                "AuthProvider.useEffect.interval": ()=>{
                    const currentToken = getToken();
                    if (!currentToken && user) {
                        clearToken();
                    }
                }
            }["AuthProvider.useEffect.interval"], 60000); // Check every minute
            return ({
                "AuthProvider.useEffect": ()=>clearInterval(interval)
            })["AuthProvider.useEffect"];
        }
    }["AuthProvider.useEffect"], [
        user
    ]);
    const redirectToDashboard = (role)=>{
        if (role === "admin") {
            router.push("/admin/dashboard");
        } else if (role === "tenant") {
            router.push("/tenant");
        } else if (role === "user") {
            router.push("/user");
        }
    };
    const login = async (email, password)=>{
        try {
            setIsLoading(true);
            const response = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$services$2f$userServices$2f$index$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["loginUser"])({
                email,
                password
            });
            if (response.data) {
                const { user: userData, token, expires_at } = response.data;
                setUser(userData);
                localStorage.setItem("user", JSON.stringify(userData));
                // Save token with expiration (convert seconds to milliseconds)
                const expiresAtMs = expires_at * 1000;
                saveToken(token, expiresAtMs);
                redirectToDashboard(userData.role);
            }
        } catch (error) {
            console.error("Login error:", error);
            throw error;
        } finally{
            setIsLoading(false);
        }
    };
    const signup = async function(name, email, password) {
        let role = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : "user";
        try {
            setIsLoading(true);
            const response = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$services$2f$userServices$2f$index$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["signupUser"])({
                name,
                email,
                password,
                is_active: true,
                role
            });
            if (response.data) {
                const userData = response.data;
                setUser(userData);
                localStorage.setItem("user", JSON.stringify(userData));
                const expiresAt = Date.now() + 5 * 60 * 1000; // 5 minutes from now
                const token = "token_".concat(Date.now(), "_").concat(Math.random().toString(36).substr(2, 9));
                saveToken(token, expiresAt);
                redirectToDashboard(userData.role);
            }
        } catch (error) {
            console.error("Signup error:", error);
            throw error;
        } finally{
            setIsLoading(false);
        }
    };
    const logout = ()=>{
        clearToken();
    };
    const value = {
        user,
        isAuthenticated: !!user,
        isLoading,
        token,
        login,
        signup,
        logout,
        isAdmin: ()=>(user === null || user === void 0 ? void 0 : user.role) === "admin",
        isTenant: ()=>(user === null || user === void 0 ? void 0 : user.role) === "tenant",
        isUser: ()=>(user === null || user === void 0 ? void 0 : user.role) === "user",
        hasRole: (role)=>(user === null || user === void 0 ? void 0 : user.role) === role
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(AuthContext.Provider, {
        value: value,
        children: children
    }, void 0, false, {
        fileName: "[project]/src/contexts/AuthContext.tsx",
        lineNumber: 216,
        columnNumber: 10
    }, ("TURBOPACK compile-time value", void 0));
};
_s1(AuthProvider, "VPCfXJZdo36DSLlj/i8TEIK8OVw=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRouter"]
    ];
});
_c = AuthProvider;
var _c;
__turbopack_context__.k.register(_c, "AuthProvider");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
}]);

//# sourceMappingURL=src_06aa29b0._.js.map