module.exports = {

"[externals]/next/dist/compiled/next-server/app-page-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-page-turbo.runtime.dev.js, cjs)": ((__turbopack_context__) => {

var { m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js", () => require("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js"));

module.exports = mod;
}}),
"[externals]/util [external] (util, cjs)": ((__turbopack_context__) => {

var { m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("util", () => require("util"));

module.exports = mod;
}}),
"[externals]/stream [external] (stream, cjs)": ((__turbopack_context__) => {

var { m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("stream", () => require("stream"));

module.exports = mod;
}}),
"[externals]/path [external] (path, cjs)": ((__turbopack_context__) => {

var { m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("path", () => require("path"));

module.exports = mod;
}}),
"[externals]/http [external] (http, cjs)": ((__turbopack_context__) => {

var { m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("http", () => require("http"));

module.exports = mod;
}}),
"[externals]/https [external] (https, cjs)": ((__turbopack_context__) => {

var { m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("https", () => require("https"));

module.exports = mod;
}}),
"[externals]/url [external] (url, cjs)": ((__turbopack_context__) => {

var { m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("url", () => require("url"));

module.exports = mod;
}}),
"[externals]/fs [external] (fs, cjs)": ((__turbopack_context__) => {

var { m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("fs", () => require("fs"));

module.exports = mod;
}}),
"[externals]/crypto [external] (crypto, cjs)": ((__turbopack_context__) => {

var { m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("crypto", () => require("crypto"));

module.exports = mod;
}}),
"[externals]/assert [external] (assert, cjs)": ((__turbopack_context__) => {

var { m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("assert", () => require("assert"));

module.exports = mod;
}}),
"[externals]/zlib [external] (zlib, cjs)": ((__turbopack_context__) => {

var { m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("zlib", () => require("zlib"));

module.exports = mod;
}}),
"[externals]/events [external] (events, cjs)": ((__turbopack_context__) => {

var { m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("events", () => require("events"));

module.exports = mod;
}}),
"[project]/src/lib/api/axois.ts [app-ssr] (ecmascript)": ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s({
    "default": ()=>__TURBOPACK__default__export__
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$axios$2f$lib$2f$axios$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/axios/lib/axios.js [app-ssr] (ecmascript)");
;
const axoisInstance = __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$axios$2f$lib$2f$axios$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"].create({
    baseURL: ("TURBOPACK compile-time value", "http://127.0.0.1:5001/"),
    headers: {
        "centent-Type": "application/json"
    }
});
axoisInstance.interceptors.request.use((config)=>{
    const tokenDataStr = ("TURBOPACK compile-time falsy", 0) ? "TURBOPACK unreachable" : null;
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    return config;
}, (error)=>Promise.reject(error));
let isRefreshing = false;
let failedQueue = [];
function processQueue(error, token = null) {
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
}),
"[project]/src/lib/api/services/userServices/index.ts [app-ssr] (ecmascript)": ((__turbopack_context__) => {
"use strict";

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
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$axois$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/lib/api/axois.ts [app-ssr] (ecmascript)");
;
const getUser = (id)=>__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$axois$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"].get(`/api/v1/users/${id}`);
const loginUser = (data)=>{
    return __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$axois$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"].post(`/api/v1/users/authenticate`, data);
};
const refreshToken = (data)=>{
    return __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$axois$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"].post("/auth/refresh", data);
};
const forgetPassword = (data)=>{
    return __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$axois$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"].post("/auth/forgot-password", data);
};
const resetPassword = (data)=>{
    return __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$axois$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"].post("/auth/reset-password", data);
};
const signupUser = (data)=>{
    return __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$axois$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"].post("/api/v1/users/", data);
};
const getAllUsers = ()=>__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$axois$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"].get("/api/v1/users/");
const deleteUser = (id)=>__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$axois$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"].delete(`/api/v1/users/${id}`);
}),
"[project]/src/contexts/AuthContext.tsx [app-ssr] (ecmascript)": ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s({
    "AuthProvider": ()=>AuthProvider,
    "useAuth": ()=>useAuth
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$services$2f$userServices$2f$index$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/lib/api/services/userServices/index.ts [app-ssr] (ecmascript)");
'use client';
;
;
;
const AuthContext = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["createContext"])(undefined);
const useAuth = ()=>{
    const context = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useContext"])(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
const AuthProvider = ({ children })=>{
    const [user, setUser] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const [token, setToken] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const [isLoading, setIsLoading] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(true);
    // Token management functions
    const saveToken = (token, expiresAt)=>{
        const tokenData = {
            token,
            expiresAt
        };
        localStorage.setItem('tokenData', JSON.stringify(tokenData));
        setToken(token);
    };
    const getToken = ()=>{
        const tokenDataStr = localStorage.getItem('tokenData');
        if (!tokenDataStr) return null;
        try {
            const tokenData = JSON.parse(tokenDataStr);
            if (Date.now() > tokenData.expiresAt) {
                // Token expired
                localStorage.removeItem('tokenData');
                localStorage.removeItem('user');
                setToken(null);
                setUser(null);
                return null;
            }
            return tokenData.token;
        } catch (error) {
            console.error('Error parsing token data:', error);
            localStorage.removeItem('tokenData');
            return null;
        }
    };
    const clearToken = ()=>{
        localStorage.removeItem('tokenData');
        localStorage.removeItem('user');
        setToken(null);
        setUser(null);
    };
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        // Check if user is logged in on app start
        const currentToken = getToken();
        const userData = localStorage.getItem('user');
        if (currentToken && userData) {
            try {
                setUser(JSON.parse(userData));
                setToken(currentToken);
            } catch (error) {
                console.error('Error parsing user data:', error);
                clearToken();
            }
        }
        setIsLoading(false);
    }, []);
    // Check token expiration every minute
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        const interval = setInterval(()=>{
            const currentToken = getToken();
            if (!currentToken && user) {
                // Token expired, logout user
                clearToken();
            }
        }, 60000); // Check every minute
        return ()=>clearInterval(interval);
    }, [
        user
    ]);
    const login = async (email, password)=>{
        try {
            setIsLoading(true);
            const response = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$services$2f$userServices$2f$index$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["loginUser"])({
                email,
                password
            });
            if (response.data) {
                const { user: userData, token, expires_at } = response.data;
                setUser(userData);
                localStorage.setItem('user', JSON.stringify(userData));
                // Save token with expiration (convert seconds to milliseconds)
                const expiresAtMs = expires_at * 1000;
                saveToken(token, expiresAtMs);
            }
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        } finally{
            setIsLoading(false);
        }
    };
    const signup = async (name, email, password, role = 'user')=>{
        try {
            setIsLoading(true);
            const response = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$lib$2f$api$2f$services$2f$userServices$2f$index$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["signupUser"])({
                name,
                email,
                password,
                is_active: true,
                role
            });
            if (response.data) {
                const userData = response.data;
                setUser(userData);
                localStorage.setItem('user', JSON.stringify(userData));
                // Generate a dummy token for signup (in real app, this would come from the backend)
                const dummyToken = `token_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
                const expiresAt = Date.now() + 5 * 60 * 1000; // 5 minutes from now
                saveToken(dummyToken, expiresAt);
            }
        } catch (error) {
            console.error('Signup error:', error);
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
        isAdmin: ()=>user?.role === 'admin',
        isTenant: ()=>user?.role === 'tenant',
        isUser: ()=>user?.role === 'user',
        hasRole: (role)=>user?.role === role
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(AuthContext.Provider, {
        value: value,
        children: children
    }, void 0, false, {
        fileName: "[project]/src/contexts/AuthContext.tsx",
        lineNumber: 190,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
}),

};

//# sourceMappingURL=%5Broot-of-the-server%5D__9a0f1f52._.js.map