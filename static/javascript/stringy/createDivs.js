function getChoices(select_choices) {
  var options = select_choices.split('|');
  var choices = [];
  for (var i in options) {
    var arr = options[i].split(',');
    var choice = {
      'value': arr[0],
      'label': arr[1]
    };
    choices.push(choice);
  }
  return choices;
}
function genQuestionHeader(header){
  var opening_html = "<div class='section-header'>"
  opening_html += "<h5>" + header + "</h5>"
  var closing_html = "</div>"
  return opening_html+closing_html
}
function genQuestion(question){
  if (question == ""){
    return ""
  }
  var question_label = question.field_label;
  var required = question.required_field == 'y'; // 'y' || ''
  var note = question.field_note;         // Might not be included
  var question_data_type = question.field_type; // 'text' || 'radio' || 'calculation'
  var select_choices_or_calc = question.select_choices_or_calculations;
  var question_name = question.field_name;

  var opening_html = "<div class='question'>"
  opening_html += "<label>"+question_label+"</label><br>";
  console.log(question_data_type);
  if (question_data_type == 'radio' || question_data_type == 'dropdown' || question_data_type == 'checkbox'){
    if (question_data_type == "checkbox"){
      var type = 'checkbox'
    } else{
      var type = 'radio'
    }
    var choices = getChoices(select_choices_or_calc);
    for (var i in choices){
      var choice = choices[i];
      var value = choice.value;
      var label = choice.label;
      if (required && i == 0){
        var add_require = "required"
      } else{
        add_require = ""
      }
      //<input type=radio name=question_name value=value>label<br>
      var input = "<input style ='display: inline' type='"+type+"' name='"+question_name+"' value='"+value+"' "+add_require+">"+label
      opening_html += input;
    }
  }
  if (question_data_type == "text"){
    var input = "<input type='text' name='"+question_name+"'>"
    opening_html += input;
  }
  if (question_data_type == "notes"){
    var input = "<textarea style='width: 400px; height: 100px;' name='"+question_name+"'></textarea>"
    opening_html += input;
  }

  var closing_html = "</div>"
  return opening_html+closing_html;
}
function genQuestionPanel(question_group, index, action){
  var is_header = (question_group[0]['section_header'] != '')
  var height = getQuestionPanelHeight(is_header, action);
  var visible = getQuestionPanelVisible(index);

  var opening_html = "<div id='question_panel_"+(index+1)+"' style='height: "+height+"' class='question-panel "+visible+"'>";

  var header = question_group[0]['section_header']
  if (is_header){
    opening_html += genQuestionHeader(header);
  }
}
function genHeader(form_name, action, patients){
  var opening_html = "<div class='question-header "+action+"'>"
     + "<h4> " + form_name + "</h4>";
  if (action == "create"){
     opening_html += "<label>Patient</label>"
     + "<select name='record_id'>"
     + "<option value ='' disabled selected>Patient- Record-ID</option>";
     for (index in patients){
       patient = patients[index];
       opening_html += "<option value = '" + patient.record_id + "' > " + patient.name + " - " + patient.record_id +"</option>";
     }
      opening_html += "</select>"
     + "<select name='event_arm' class='pull-right'>"
     + "<option value='' disabled selected>Arm-Label</option>"
     + "<option value='admin'>Admin</option>"
     + "<option value='dc'>D/C</option> "
     + "</select>"
     + "<label class='pull-right'>Arm</label>";
  }
  var closing_html = "</div>";
  return (opening_html + closing_html);
}
function genProgressPanel(pages,form_name){
  var opening_html = "<div class='progress'><div class='progress-centering'>";
  opening_html += "<div class='next-page-button' id='"+form_name+"_button'>Next Page</div>";
  for (var i = 0; i < pages; i++){
    var active =""
    if (i==0){
      active = "active-circle"
    }
    opening_html += "<div class='form-circle "+active+"' id='button_"+(i+1)+"'></div>";
  }
  var closing_html = "</div></div>";
  return (opening_html + closing_html)
}
