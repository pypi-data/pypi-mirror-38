/*
 * Registers 'profile' url and all profile sublinks' urls.
 */
tabSignal.connect("openapi.completed", function()
{
    let subLinksArr = ['actions', 'links'];

    let pathObj = guiSchema.path['/user/{pk}/'];

    for (let i in subLinksArr)
    {
        let sublink_type = subLinksArr[i];

        for (let j in pathObj[sublink_type])
        {
            let sublink = pathObj[sublink_type][j]

            if(sublink.type == 'action')
            {
                registerProfileSublinkAction(sublink.name, sublink.path, my_user_id);
            }
            else if(sublink.type == 'page')
            {
                registerProfileSublinkPage(sublink.name, sublink.path, my_user_id);
            }
            else if(sublink.type == 'list')
            {
                registerProfileSublinkList(sublink.name, sublink.path, my_user_id);
            }
        }
    }

    spajs.addMenu({
        id:"profile",
        urlregexp:[/^profile$/],
        priority:0,
        onOpen:function(holder, menuInfo, data, onClose_promise)
        {
            let pageItem = new guiObjectFactory('/user/{pk}/', {
                page:'user/'+ my_user_id,
                api_pk:my_user_id
            })

            var def = new $.Deferred();
            $.when(pageItem.load(my_user_id)).done(function()
            {
                def.resolve(pageItem.renderAsPage())
            }).fail(function(err)
            {
                def.resolve(renderErrorAsPage(err));
            })

            $.when(onClose_promise).always(() => {
                pageItem.stopUpdates();
            })

            return def.promise();
        },
    })
})


/*
 * Registers Profile's sublink with Action Type
 * @param {sublink} - string - name of sublink
 * @param {path} - string - api_path
 * @param {api_pk} - integer - object's id
 * @returns {html}
 */
function registerProfileSublinkAction(sublink, path, api_pk)
{
    let reg_url = new RegExp('^profile/' + sublink + '$');
    let url_id = 'profile_' + sublink.replace(/\/+/g,'_');

    spajs.addMenu({
        id:url_id,
        urlregexp:[reg_url],
        priority:0,
        onOpen:function(holder, menuInfo, data, onClose_promise)
        {
            let pageItem = new guiObjectFactory(path, {
                page:'user/'+ api_pk +'/' + sublink,
                api_pk:api_pk,
            })

            var def = new $.Deferred();
            $.when(pageItem).done(function()
            {
                def.resolve(pageItem.renderAsPage())
            }).fail(function(err)
            {
                def.resolve(renderErrorAsPage(err));
            })

            $.when(onClose_promise).always(() => {
                pageItem.stopUpdates();
            })

            return def.promise();
        },
    })
}


/*
 * Registers Profile's sublink with Page Type
 * @param {sublink} - string - name of sublink
 * @param {path} - string - api_path
 * @param {api_pk} - integer - object's id
 * @returns {deferred}
 */
function registerProfileSublinkPage(sublink, path, api_pk)
{
    let reg_url = new RegExp('^profile/' + sublink + '$');
    let url_id = 'profile_' + sublink.replace(/\/+/g,'_');

    spajs.addMenu({
        id:url_id,
        urlregexp:[reg_url],
        priority:0,
        onOpen:function(holder, menuInfo, data, onClose_promise)
        {
            let pageItem = new guiObjectFactory(path, {
                page: 'user/' + api_pk + '/' + sublink,
                api_pk:api_pk,
            })

            var def = new $.Deferred();
            $.when(pageItem.load(api_pk)).done(function()
            {
                def.resolve(pageItem.renderAsPage())
            }).fail(function(err)
            {
                def.resolve(renderErrorAsPage(err));
            })

            $.when(onClose_promise).always(() => {
                pageItem.stopUpdates();
            })

            return def.promise();
        },
    })
}


/*
 * Registers Profile's sublink with List Type
 * @param {sublink} - string - name of sublink
 * @param {path} - string - api_path
 * @param {api_pk} - integer - object's id
 * @returns {deferred}
 */
function registerProfileSublinkList(sublink, path, api_pk)
{
    let reg_url = new RegExp('^profile/' + sublink + '$');
    let url_id = 'profile_' + sublink.replace(/\/+/g,'_');

    spajs.addMenu({
        id:url_id,
        urlregexp:[reg_url],
        priority:0,
        onOpen:function(holder, menuInfo, data, onClose_promise)
        {
            let pageItem = new guiObjectFactory(path, {
                page: 'user/' + api_pk + '/' + sublink,
                api_pk:api_pk,
            })

            var def = new $.Deferred();
            $.when(pageItem.load()).done(function()
            {
                def.resolve(pageItem.renderAsPage())
            }).fail(function(err)
            {
                def.resolve(renderErrorAsPage(err));
            })

            $.when(onClose_promise).always(() => {
                pageItem.stopUpdates();
            })

            return def.promise();
        },
    })
}