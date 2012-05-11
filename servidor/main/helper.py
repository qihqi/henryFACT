from django.shortcuts import render_to_response

###### Renders a page that only contains a form #########
# meta is a dict that contains
#    form -  the form to render
#    method - get or post
#    action - action
#    st_message - any status message
#    submit_name - to display on the submit button
#    title - title
##########################################################
def render_form(meta, instance):
    if meta['method'] == 'post':
        return render_to_response('form_page.html', meta, context_instance=instance)
    else:
        return render_to_response('form_page.html', meta)


