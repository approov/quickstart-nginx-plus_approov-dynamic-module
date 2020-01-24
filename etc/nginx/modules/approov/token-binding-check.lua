local basexx = require "basexx"
local resty_sha256 = require "resty.sha256"

local Approov = {}

function Approov.checkTokenBinding(pay_claim, token_binding)

    if pay_claim == nil then
        ngx.log(ngx.WARN, "Approov Token Binding not present.")
        return
    end

    if token_binding == nil then
        ngx.log(ngx.ERR, "Missing the value for the token binding header.")
        ngx.exit(ngx.HTTP_UNAUTHORIZED)
    end

    local sha256 = resty_sha256:new()
    sha256:update(token_binding)
    local token_binding_hash = basexx.to_base64(sha256:final())

    if token_binding_hash ~= pay_claim then
        ngx.log(ngx.ERR, "The Approov token binding is not matching.")
        ngx.exit(ngx.HTTP_UNAUTHORIZED)
    end

end

return Approov
