(function($) {

    var markItUpSettingsBasic = {
        onTab:    		{keepDefault:false, replaceWith:'    '},
        onShiftEnter:       {keepDefault:false, openWith:'\n\n'},
        markupSet:  []
    };

    var markItUpSettingsMarkdown = {
        onTab:    		{keepDefault:false, replaceWith:'    '},
        onShiftEnter:       {keepDefault:false, openWith:'\n\n'},
        markupSet:  [
            {name:'Bold', key:"B", className:'button-b', openWith:'**', closeWith:'**'},
            {name:'Italic', key:"I", className: 'button-i', openWith:'_', closeWith:'_'},
            {separator:'---------------' },
            {name:'Bulleted List', className: 'button-ul', openWith:'- ' },
            {name:'Numeric List', className: 'button-ol', openWith:function(markItUp) {
                return markItUp.line+'. ';
            }},
            {separator:'---------------' },
            {name:'Picture', key:"P", className: 'button-img',
                replaceWith:'![[![Alternative text]!]]([![Url:!:http://]!] "[![Title]!]")'},
            {name:'Link', key:"L", className: 'button-a', openWith:'[',
                closeWith:']([![Url:!:http://]!] "[![Title]!]")',
                placeHolder:'Your text to link here...' },
            {separator:'---------------'},
            {name:'Quotes', className: 'button-q', openWith:'> '},
            {name:'Code Block / Code', className: 'button-code',
                openWith:'(!(\t|!|`)!)', closeWith:'(!(`)!)'},
        ]
    };

    var markItUpSettingsHtml = {
        onShiftEnter:  	{keepDefault:false, replaceWith:'<br />\n'},
        onCtrlEnter:  	{keepDefault:false, openWith:'\n<p>', closeWith:'</p>'},
        onTab:    		{keepDefault:false, replaceWith:'    '},
        markupSet:  [
            {name:'Bold', key:'B', className:'button-b', openWith:'<strong>', closeWith:'</strong>' },
            {name:'Italic', key:'I', className: 'button-i', openWith:'<em>', closeWith:'</em>'  },
            {separator:'---------------' },
            {name:'Bulleted List', className: 'button-ul', openWith:'    <li>', closeWith:'</li>',
                multiline:true, openBlockWith:'<ul>\n', closeBlockWith:'\n</ul>'},
            {name:'Numeric List', className: 'button-ol', openWith:'    <li>', closeWith:'</li>',
                multiline:true, openBlockWith:'<ol>\n', closeBlockWith:'\n</ol>'},
            {separator:'---------------' },
            {name:'Picture', key:'P', className: 'button-img',
                replaceWith:'<img src="[![Source:!:http://]!]" alt="[![Alternative text]!]" />' },
            {name:'Link', key:'L', className: 'button-a',
                openWith:'<a href="[![Link:!:http://]!]"(!( title="[![Title]!]")!)>',
                closeWith:'</a>', placeHolder:'Your text to link...' },
        ]
    };

    var markItUpSettingsHtmlLight = {
        onShiftEnter:  	{keepDefault:false, replaceWith:'<br />\n'},
        onCtrlEnter:  	{keepDefault:false, openWith:'\n<p>', closeWith:'</p>'},
        onTab:    		{keepDefault:false, replaceWith:'    '},
        markupSet:  [
            {name:'Bold', key:'B', className:'button-b', openWith:'<strong>', closeWith:'</strong>' },
            {name:'Italic', key:'I', className: 'button-i', openWith:'<em>', closeWith:'</em>'  },
            {name:'Link', key:'L', className: 'button-a',
                openWith:'<a href="[![Link:!:http://]!]"(!( title="[![Title]!]")!)>',
                closeWith:'</a>', placeHolder:'Your text to link...' },
        ]
    };

    var markItUpSettings = {
        'html-light': markItUpSettingsHtmlLight,
        'html': markItUpSettingsHtml,
        'markdown': markItUpSettingsMarkdown,
        'basic': markItUpSettingsBasic,

//        'email': markItUpSettingsHtml,
//        'email-html': markItUpSettingsHtml,
//        'email-md': markItUpSettingsMarkdown,
//        'postmark-template': markItUpSettingsBasic,
//        'json-webhook': markItUpSettingsBasic,
//        'twilio': markItUpSettingsBasic,
//        'twitter': markItUpSettingsBasic,
//        'slack-webhook': markItUpSettingsBasic,
//        'xmpp': markItUpSettingsBasic,
    };

    function parseVariables(recipient, variables) {
        var result = [];
        if (Object.keys(variables).includes(recipient)) {
            result = result.concat(parseSubVariables([variables[recipient]]));
        }
        result = result.concat(parseSubVariables(variables._static));
        return result;
    }

    function parseSubVariables(variables){
        var result = [];
        for (var i=0; i<variables.length; i++) {
            var variable = variables[i];
            var item = {name: variable.label, replaceWith: '{{ '+variable.value+' }}'};
            if ('attrs' in variable) {
                var attrs_list = [];
                var rel_list = [];
                for (var j=0; j<variable.attrs.length; j++) {
                    var sub = variable.attrs[j];
                    attrs_list.push({name: sub.label, replaceWith: '{{ '+sub.value+' }}'});
                }
                if ('rels' in variable) {
                    var rel_list = parseSubVariables(variable.rels);
                }
                var rel_len = rel_list.length
                if (rel_len < 1 || rel_len + attrs_list.length < 11) {
                    item.dropMenu = attrs_list.concat(rel_list);
                } else {
                    item.dropMenu = [{name: 'Attributes', dropMenu: attrs_list},
                                     {name: 'Relations', dropMenu: rel_list}];
                }
            }
            result.push(item);
        }
        return result;
    }


    function getMarkItUpSettings(backend, editor, recipient, variables) {
        var settings = Object.assign({}, markItUpSettings[editor]);
        settings.previewParserPath = '../preview/' + backend + '/';
        settings.previewParserVar = 'body';
        var variableList = parseVariables(recipient, variables);
        settings.markupSet = [
            {name:'Variables', className:'variable', openWith:'{{ ', closeWith:' }}',
                dropMenu: variableList},
            {separator:'---------------' },
        ].concat(settings.markupSet);
        var lms = settings.markupSet.length;
        if (!('separator' in settings.markupSet[lms-1])) {
            settings.markupSet = settings.markupSet.concat(
                {separator:'---------------' });
        }
        settings.markupSet = settings.markupSet.concat(
            [{name:'Preview', className:'preview',  call:'preview'}]);
        return settings;
    }

    function disableTargetsByPrefix(options, prefix) {
        for (var i=0;i<options.length;i++) {
            if (options[i].value.startsWith(prefix)) {
                options[i].disabled=true;
            }
        }
    }

    function setup(variables) {
        // show subject based on backends
        var recipientSelects = django.jQuery(
            '.field-recipient select, .grp-row.recipient select')
        recipientSelects.on('change', function() {
            selectRecipient(this, variables);});
        var backendSelects = django.jQuery(
            '.field-backend select, .grp-row.backend select');
        backendSelects.each(function() {selectBackend(this, variables);});
        backendSelects.on('change', function() {selectBackend(this, variables);});
    }

    function selectBackend(elem, variables) {
        var opt = elem.options[elem.selectedIndex];
        var backend = elem.value;
        var editor = opt.dataset.editor;
        var useSubject = opt.dataset.subject == 'true';
        var useAttachment = opt.dataset.attachment == 'true';
        var fieldset = $(elem).closest('fieldset')
        // update subject
        var subject_div = django.jQuery(
            '.field-subject, .grp-row.subject');
        subject_div.toggle(useSubject);
        // update attachments
        var attachment_div = django.jQuery(
            '.field-attachments, .grp-row.attachments');
        attachment_div.toggle(useAttachment);
        // update markitup
        var recipient = fieldset.find(
            '.field-recipient select, .grp-row.recipient select').val();
        var textarea = fieldset.find(
            '.field-content textarea, .grp-row.content textarea');
        textarea.markItUpRemove();
        if (editor in markItUpSettings) {
            textarea.markItUp(getMarkItUpSettings(
                backend, editor, recipient, variables));
        }
    }

    function selectRecipient(elem, variables) {
        var fieldset = $(elem).closest('fieldset')
        var backendSelect = fieldset.find(
            '.field-backend select, .grp-row.backend select')[0]
        var opt = backendSelect.selectedOptions[0]
        var backend = opt.value;
        var editor = opt.dataset.editor;
        var textarea = fieldset.find(
            '.field-content textarea, .grp-row.content textarea');
        textarea.markItUpRemove();
        if (editor in markItUpSettings) {
            textarea.markItUp(getMarkItUpSettings(
                backend, editor, elem.value, variables));
        }
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }


    $(document).ready(function() {
        // only on the change page with the template inline
        if (document.getElementById('template_set-group')) {
            // set up CSRF ajax stuff
            var csrftoken = $("[name=csrfmiddlewaretoken]").val();
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });
            django.jQuery.ajax({
                type: 'POST',
                global: false,
                url: '../variables/',
                success: setup,
            });
        }
    });
})(django.jQuery)
