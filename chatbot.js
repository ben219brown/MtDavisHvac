/* Mt Davis HVAC: progressive-enhancement guided intake with an optional AI question. */
(() => {
  'use strict';
  if (document.getElementById('mdh-chat-launcher')) return;
  const AI_URL = 'https://chat.mtdavishvac.com/chat';
  const FORM_URL = 'https://formsubmit.co/ajax/mark@mtdavishvac.com';
  const PHONE = 'tel:+18149266646';
  const steps = [
    {field:'request', question:'What brings you here today?', options:['Repair or service','New installation or replacement','Maintenance','General HVAC question']},
    {field:'property', question:'Is the service for a home or a business?', options:['Home','Business']},
    {field:'service', question:'Which type of heating or cooling equipment?', options:['Furnace / heating','Air conditioning','Heat pump','Mini-split / ductless','Not sure / other']},
    {field:'urgency', question:'How soon is service needed?', options:['Emergency / immediate concern','Within a few days','Flexible / planning ahead']},
    {field:'issue', question:'Please describe what you need or what the system is doing.', type:'textarea', max:900, help:'Please do not include your name, number, address or sensitive information here. Only this description and equipment type may be used to generate an AI follow-up.'},
    {field:'followup', question:'One more equipment detail', type:'ai', max:500, optional:true},
    {field:'town', question:'What town or ZIP code is the service location in?', type:'text', max:110},
    {field:'name', question:'What name should we put on the request?', type:'text', max:100},
    {field:'phone', question:'What phone number can Mt Davis HVAC reach you at?', type:'tel', max:30},
    {field:'email', question:'Would you like to leave an email address too?', type:'email', max:180, optional:true},
    {field:'contact', question:'What is the best way to contact you?', options:['Phone call','Text message','Email','Phone or email']}
  ];
  const labels = {
    request:'Request type', property:'Property', service:'Equipment', urgency:'Urgency',
    issue:'Problem / project description', followup:'Additional equipment detail',
    town:'Service location', name:'Name', phone:'Phone', email:'Email', contact:'Contact preference'
  };
  const values = {};
  const history = [];
  let index = -1;
  let dynamicQuestion = '';
  let active = false;
  let loading = false;

  const el = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  };
  const launcher = el('button','mdh-chat-launcher');
  launcher.id = 'mdh-chat-launcher';
  launcher.type = 'button';
  launcher.setAttribute('aria-controls','mdh-chat-panel');
  launcher.setAttribute('aria-expanded','false');
  launcher.setAttribute('aria-label','Open HVAC service chat');
  launcher.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-.9 3.8A8.5 8.5 0 0 1 12.5 20a8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8A8.5 8.5 0 0 1 12.5 3 8.5 8.5 0 0 1 21 11.5Z"/></svg><span>Ask Mt Davis HVAC</span>';
  const panel = el('section','mdh-chat-panel');
  panel.id = 'mdh-chat-panel';
  panel.setAttribute('aria-label','Mt Davis HVAC website assistant');
  panel.hidden = true;
  const head = el('div','mdh-chat-head');
  const title = el('div');
  title.append(el('strong','', 'Mt Davis HVAC Assistant'),el('small','', 'Guided service requests · AI-assisted follow-up'));
  const close = el('button','', '×');
  close.type = 'button';
  close.setAttribute('aria-label','Close chat');
  head.append(title,close);
  const log = el('div','mdh-chat-log');
  log.setAttribute('role','log');
  log.setAttribute('aria-label','Conversation');
  log.setAttribute('aria-live','polite');
  const controls = el('div','mdh-chat-controls');
  panel.append(head,log,controls);
  document.body.append(launcher,panel);

  function bubble(text, from='bot', transient=false) {
    const item = el('div','mdh-chat-bubble ' + (from==='user'?'user':from==='alert'?'alert':''),text);
    log.append(item);
    log.scrollTop = log.scrollHeight;
    return item;
  }
  function setControls(...items) {
    controls.replaceChildren(...items);
    log.scrollTop = log.scrollHeight;
  }
  function button(text, handler, primary=false) {
    const item = el('button', primary?'primary':'', text);
    item.type = 'button';
    item.addEventListener('click',handler);
    return item;
  }
  function buttons(items) {
    const area = el('div','mdh-chat-actions');
    items.forEach(item=>area.append(item));
    setControls(area);
    return area;
  }
  function begin() {
    Object.keys(values).forEach(key=>delete values[key]);
    history.length=0;
    dynamicQuestion='';
    index=-1;
    log.replaceChildren();
    bubble('Hi! I can collect your service details and send a request to Mt Davis HVAC. I am an automated website assistant, not a live technician.');
    bubble('For urgent service, please call (814) 926-6646. If you suspect a gas leak, fire, or carbon monoxide, leave the area and contact emergency services or your gas utility from a safe location.', 'alert');
    buttons([button('Start a request',next,true),button('Call now',()=>{window.location.href=PHONE;})]);
  }
  function record(question,field,value) {
    values[field]=value;
    history.push({question,answer:value||'(not provided)'});
    if (value) bubble(value,'user');
  }
  function next() {
    index+=1;
    if (index>=steps.length) return review();
    const step = steps[index];
    if (step.type==='ai') return askAI(step);
    bubble(step.question);
    if (step.options) {
      let options = step.options;
      if (step.field==='contact' && !values.email) options=['Phone call','Text message'];
      buttons(options.map(value=>button(value,()=>{
        record(step.question,step.field,value);
        if(step.field==='urgency' && value.startsWith('Emergency')) return emergencyNotice();
        next();
      })));
    } else {
      renderField(step,step.question);
    }
  }
  function emergencyNotice() {
    bubble('Do not wait for this form if you need immediate help. Call Mt Davis HVAC directly. If there is a gas or carbon-monoxide concern, smoke or fire, leave the area and contact emergency services or your utility from a safe location. This chat does not dispatch service.', 'alert');
    const link = el('a','', 'Call (814) 926-6646');
    link.href=PHONE;
    buttons([link,button('Continue submitting details',next)]);
  }
  function renderField(step,question) {
    const form=el('form','mdh-chat-field');
    const label=el('label','',step.field==='issue'?'What should the technician know?':
      step.field==='followup'?'Your answer (optional)':step.field==='town'?'Town or ZIP':
      step.field==='name'?'Your name':step.field==='phone'?'Phone number':'Email address (optional)');
    const field=el(step.type==='textarea'?'textarea':'input');
    field.id='mdh-input';
    label.htmlFor=field.id;
    if (field.tagName==='INPUT') field.type=step.type==='tel'?'tel':step.type==='email'?'email':'text';
    field.name=step.field;
    field.maxLength=step.max||100;
    field.required=!step.optional;
    if (step.field==='name') field.autocomplete='name';
    if (step.field==='phone') field.autocomplete='tel';
    if (step.field==='email') field.autocomplete='email';
    if (step.field==='issue') field.placeholder='Describe the equipment and the issue; no personal details here.';
    form.append(label,field);
    if (step.help) form.append(el('small','',step.help));
    const actions=el('div','mdh-chat-actions');
    const submit=el('button','primary', 'Continue →');
    submit.type='submit';
    actions.append(submit);
    if(step.optional) actions.append(button('Skip',()=>{
      record(question,step.field,'');
      next();
    }));
    form.append(actions);
    form.addEventListener('submit',event=>{
      event.preventDefault();
      const value=field.value.trim();
      if (!step.optional && !value) return field.reportValidity();
      if (step.field==='phone' && value.replace(/\D/g,'').length<10) {
        field.setCustomValidity('Please enter a valid 10-digit phone number.');
        field.reportValidity();return;
      }
      field.setCustomValidity('');
      if(step.field==='issue' && /(?:smell(?:s|ing)?\s+(?:of\s+)?gas|carbon monoxide|co alarm|gas leak|smoke|on fire)/i.test(value)) {
        bubble('If this involves a possible gas leak, carbon monoxide, smoke or fire, leave the area and contact emergency services or your gas utility from a safe location. Do not wait for this chat.','alert');
      }
      record(question,step.field,value);
      next();
    });
    field.addEventListener('input',()=>field.setCustomValidity(''));
    setControls(form);
    field.focus({preventScroll:true});
  }
  async function askAI(step) {
    if (/(?:smell(?:s|ing)?\s+(?:of\s+)?gas|carbon monoxide|co alarm|gas leak|smoke|on fire)/i.test(values.issue)) {
      bubble('A possible safety hazard should be handled by emergency services or the gas utility from a safe location. Do not wait for this chat.', 'alert');
      const call = el('a','','Call Mt Davis HVAC'); call.href=PHONE;
      buttons([call,button('Continue non-emergency request',()=>{record('Additional equipment detail','followup',''); next();})]);
      return;
    }
    const pending=bubble('Checking for a relevant follow-up question…');
    setControls(el('p','mdh-chat-help','Your description is used only for the optional AI follow-up. Contact details are collected separately.'));
    let question='Is there anything else about the equipment or problem that would help the technician prepare?';
    try {
      const controller=new AbortController();
      const timer=setTimeout(()=>controller.abort(),5500);
      let response;
      try {
        // Never include name, phone, email, service location or chat history in an AI request.
        const safeIssue=values.issue.replace(/\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b/g,'[email omitted]')
          .replace(/(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b/g,'[phone omitted]');
        response=await fetch(AI_URL,{
          method:'POST',mode:'cors',signal:controller.signal,
          headers:{'Content-Type':'application/json'},
          body:JSON.stringify({service:values.service,issue:safeIssue})
        });
      } finally {clearTimeout(timer);}
      if (response.ok) {
        const json=await response.json();
        if(typeof json.question==='string' && json.question.length>=10 && json.question.length<=240)
          question=json.question;
      }
    } catch {
      // A deterministic question keeps lead intake usable if the AI service is offline.
    }
    pending.remove();
    dynamicQuestion=question;
    bubble(question);
    renderField(step,question);
  }
  function review() {
    bubble('Thanks! Please review the request and approve sending it to Mt Davis HVAC. Nothing has been sent yet.');
    const wrapper=el('div');
    const dl=el('dl','mdh-chat-review');
    for (const [key,label] of Object.entries(labels)) {
      if (key==='email'&&!values.email) continue;
      const row=el('div');
      row.append(el('dt','',label),el('dd','',values[key]||'Not provided'));
      dl.append(row);
    }
    wrapper.append(dl);
    const consent=el('label','mdh-chat-consent');
    const checkbox=el('input');checkbox.type='checkbox';checkbox.required=true;
    const consentText=el('span');
    consentText.append(document.createTextNode('I agree that Mt Davis HVAC may contact me about this inquiry. This chat sends my details through FormSubmit. My equipment description may have been sent to an AI provider for an optional follow-up. See the '));
    const link=el('a','', 'privacy notice');link.href='/privacy/';link.target='_blank';link.rel='noopener';
    consentText.append(link,document.createTextNode('.'));
    consent.append(checkbox,consentText);
    const row=el('div','mdh-chat-actions');
    const submit=button('Submit request →',submitLead,true);submit.disabled=true;
    checkbox.addEventListener('change',()=>submit.disabled=!checkbox.checked);
    row.append(submit,button('Start over / change answers',begin));
    wrapper.append(consent,row);
    wrapper.append(el('p','mdh-chat-help','For emergencies, call (814) 926-6646. A submission does not reserve an appointment.'));
    setControls(wrapper);
    async function submitLead() {
      if (loading||!checkbox.checked) return;
      loading=true;submit.disabled=true;submit.textContent='Submitting…';
      const conversation=history.map(x=>x.question+'\n'+x.answer).join('\n\n');
      const payload={
        _subject:'Mt Davis HVAC — Website Assistant Request',
        _template:'table',_honey:'',
        source:'Website assistant',
        name:values.name,phone:values.phone,
        ...(values.email?{email:values.email}:{}),
        request_type:values.request,property_type:values.property,
        service:values.service,urgency:values.urgency,
        service_location:values.town,preferred_contact:values.contact,
        message:values.issue,
        additional_details:values.followup||'(none)',
        conversation:conversation,
        consent:'Approved chat submission and contact'
      };
      try {
        const controller=new AbortController();
        const timer=setTimeout(()=>controller.abort(),15000);
        let response;
        try {
          response=await fetch(FORM_URL,{
            method:'POST',mode:'cors',signal:controller.signal,
            headers:{'Content-Type':'application/json','Accept':'application/json'},
            body:JSON.stringify(payload)
          });
        } finally {clearTimeout(timer);}
        const result=await response.json();
        if (!response.ok || (result.success!==true && result.success!=='true')) throw Error('Unconfirmed');
        bubble('Your request has been submitted to our form service. Mt Davis HVAC can contact you using the information you supplied. If the request is urgent, call rather than waiting for a reply.');
        setControls(el('div','mdh-chat-actions'));
        const done=button('Start a new request',begin);
        controls.firstChild.append(done);
        history.length=0;
        Object.keys(values).forEach(key=>delete values[key]);
      } catch {
        bubble('We could not confirm the submission. You can retry, use the regular quote form, or call (814) 926-6646. If you already received a confirmation, avoid submitting a duplicate.','alert');
        submit.disabled=false;
      } finally {
        loading=false;submit.textContent='Submit request →';
      }
    }
  }
  function toggle(open) {
    active=open;
    panel.hidden=!open;
    launcher.setAttribute('aria-expanded',String(open));
    if(open) {
      if(index===-1 && !log.children.length) begin();
      close.focus({preventScroll:true});
    } else launcher.focus({preventScroll:true});
  }
  launcher.addEventListener('click',()=>toggle(!active));
  close.addEventListener('click',()=>toggle(false));
  document.addEventListener('keydown',event=>{
    if(event.key==='Escape' && active) toggle(false);
  });
})();
