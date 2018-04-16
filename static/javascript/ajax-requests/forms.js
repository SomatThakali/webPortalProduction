function getVerboseName(form_name){
  var arr = form_name.split('_');
  for (var i = 0; i < arr.length; i++){
    arr[i] = arr[i][0].toUpperCase() + arr[i].slice(1);
  }
  var verbose_name = arr.join(" ");
  return verbose_name;
}
function changeSubmit(index){
  index = parseInt(index)+1;
  var id = "button_"+index;
  var no_exist = document.getElementById(id)===null;
  if (no_exist){
    $next_button = $('.next-page-button')
    document.getElementsByClassName('next-page-button')[0].innerHTML = "Submit Form";
    $next_button.removeClass('next-page-button');
    $next_button.addClass('submit-form')
  } else {
    $next_button = $('.submit-form');
    if (document.getElementsByClassName('submit-form')[0] != undefined){
      document.getElementsByClassName('submit-form')[0].innerHTML = "Next Page";
    }
    $next_button.removeClass('submit-form');
    $next_button.addClass('next-page-button');
  }
}
function getRequest(id){
  var arr = id.split('_');
  event = arr.shift();
  form = arr.join('_');
  return {event: event, form: form}
}
function getQuestionPanelHeight(isPanel, action){
  if (action == 'create'){
    if (isPanel){
      return '55%'
    }
    return '55%'
  }
  if (isPanel){
    return '75%'
  }
  return '85%'
}
function getQuestionPanelVisible(index){
  if (index == 0){
    return 'visible'
  } return ''
}
function getBottomBorder(index,last_index){
  if (index == last_index){
    return ""
  }
    return'bottom-grey-border'
}
function getChoices(select_choices){
  var options = select_choices.split('|');
  var choices = [];
  for (var i in options){
    var arr = options[i].split(',');
    var choice = {'value': arr[0],'label': arr[1]};
    choices.push(choice);
  }
  return choices;
}
function toggleClasses($circle_current, $panel_current, $circle_change, $panel_change){
  $circle_current.removeClass('active-circle');
  $panel_current.removeClass('visible');
  $circle_change.addClass('active-circle');
  $panel_change.addClass('visible');
}

// want patients to be actually a dictionary such that patient = {'name' = name; 'record_id' = record_id}
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


  var is_odd = (question_group.length % 2 == 1 );
  var last_index = (parseInt(question_group.length/2)+is_odd);
  if (is_header){
    height = 85/last_index;
  }else{
  height = 100/last_index;
  }
  for (var i = 0; i < last_index; i ++){
    var question_1 = question_group[2*i];

    // Need to prevent breaking if only 1 question in the row
    if (i == last_index-1 && is_odd){
      var question_2 = ""
    }else{
      var question_2 = question_group[2*i+1];
    }

    var border = getBottomBorder(i, last_index-1);

    opening_html += "<div style='height: "+ height + "%' class='row question-row "+border+"'>"
    +"<div class='col-sm-6 question-cushion right-grey-border'>"
      + genQuestion(question_1) + "</div>"
      + "<div class='col-sm-6 question-cushion'>"
      + genQuestion(question_2) + "</div></div>"

  }
  var closing_html = "</div>";
  return (opening_html+closing_html);
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

function displayForm(res){
  var question_groups = res.question_groups;
  var form_name = question_groups[0][0].form_name;
  var form_verbose_name = getVerboseName(form_name);

  var leading_html =
  "<div class='pop-up'>"
    + "<form class='redcap-form' id='"+form_name+"'>"
      + "<div class='question-view'>"
  //
  patients = [{'name': 'Testdcap2', 'record_id': 'testdcap2'}, {'name': 'Test Dcap3', 'record_id':'testdcap3'}]
  leading_html += genHeader(form_verbose_name, res.event,patients)
  // TODOonly doing 1 question group to test atfirst.

  for (var i = 0; i < question_groups.length; i++){
    question_group = question_groups[i];
    question_panel = genQuestionPanel(question_group,i,res.event);
    leading_html += question_panel; // The question_panel is closed within the function
  }
  leading_html += genProgressPanel(question_groups.length, form_name);

  var lagging_html ="</div>"
      + "</form>"
    +"</div>"

  $("body").append(leading_html+lagging_html);

}

$(document).ready(function(){
  $('.form-button').click(function(e){
    e.preventDefault();
    var id = $(this).attr('id');
    var action = getRequest(id);
    $.ajax({
      url: '',
      type: 'get',
      dataType: 'json',
      data: action,
      success: function(res){
        displayForm(res);
      },
      error: function(res){
        console.log("oops");
      }
    })
  })
  $('div').click(function(e){
    e.stopPropagation();
    if (($('.pop-up')[0]) && $(this).attr("class") != 'pop-up'){
      $('.pop-up').remove();
    }
  })
})
$(document).on('click','.next-page-button',function(){
  var $circle_current = $('.active-circle');
  var $panel_current = $('.visible');
  var current_id = $circle_current.attr('id');
  var arr = current_id.split('_')
  var index = parseInt(arr[arr.length-1])+1;
  //We want to check if the next id exists if it doesnt we need to switch our button next page to submit
  changeSubmit(index);
  var $circle_change = $("#button_"+index);
  var $panel_change = $("#question_panel_"+index);
  toggleClasses($circle_current, $panel_current, $circle_change, $panel_change)
})

$(document).on('click','.form-circle',function(){
  var $circle_current = $('.active-circle');
  var $panel_current = $('.visible');
  $circle_change = $(this);
  var id = $circle_change.attr('id');
  var index = id.split('_')[1];
  //We want to check if the next id exists if it doesnt we need to switch our button next page to submit
  changeSubmit(index);
  var $panel_change = $('#question_panel_'+index);
  toggleClasses($circle_current, $panel_current, $circle_change, $panel_change)
})

$(document).on('click','.submit-form',function(e){
  e.preventDefault();
  var form_array = $(this).attr('id').split('_');
  form_array = form_array.slice(0,-1);
  var form_name = form_array.join('_');
  var $form = $('#'+form_name);
  var data = $form.serialize();

  var csrf_token=$('meta[name="csrf-token"]').attr('content')
  // FIXME cohort_num must come from somewhereelse
  data += ('&cohort_num=' +'1');
  data += ('&csrfmiddlewaretoken='+csrf_token);
  $.ajax({
    url: '',
    type: 'post',
    dataType: 'json',
    data: data,
    success: function(res){
      $('.pop-up').remove();
      //displayForm(res);
    },
    error: function(res){
      console.log("oops");
    }
  })
    //var data = $('#'+form_name).serialize();
  //console.log(data);
})
