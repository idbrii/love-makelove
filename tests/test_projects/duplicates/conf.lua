function love.conf(t)
    if true then
        t.identity     = 'normalname'
        t.version      = '11.0'
        t.window.title = 'Title of Window'
    else
        t.identity     = 'debugname'
        t.version      = '11.1'
        t.window.title = 'Debug Window'
    end
end
