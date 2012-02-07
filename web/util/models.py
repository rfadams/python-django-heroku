class DefaultsMixin(object):

    def get_context_data(self, **kwargs):
        context = super(DefaultsMixin, self).get_context_data(**kwargs)
        
        try:
            context['form_title'] = self.form_title
        except AttributeError:
            pass
        
        try:
            context['form_action_url'] = self.form_action_url
        except AttributeError:
            pass

        try:
            context['form_cancel_url'] = self.form_cancel_url
        except AttributeError:
            pass
        
        try:
            context['table_title'] = self.table_title
        except AttributeError:
            pass
        
        try:
            context['column_title'] = self.column_title
        except AttributeError:
            pass

        try:
            context['object_title'] = self.object_title
        except AttributeError:
            pass

        return context
