function getVerboseName(form_name) {
  var arr = form_name.split('_');
  for (var i = 0; i < arr.length; i++) {
    arr[i] = arr[i][0].toUpperCase() + arr[i].slice(1);
  }
  var verbose_name = arr.join(" ");
  return verbose_name;
}

function changeSubmit(index) {
  index = parseInt(index) + 1;
  var id = "button_" + index;
  var no_exist = document.getElementById(id) === null;
  if (no_exist) {
    $next_button = $('.next-page-button')
    document.getElementsByClassName('next-page-button')[0].innerHTML = "Submit Form";
    $next_button.removeClass('next-page-button');
    $next_button.addClass('submit-form')
  } else {
    $next_button = $('.submit-form');
    if (document.getElementsByClassName('submit-form')[0] != undefined) {
      document.getElementsByClassName('submit-form')[0].innerHTML = "Next Page";
    }
    $next_button.removeClass('submit-form');
    $next_button.addClass('next-page-button');
  }
}

function getRequest(id) {
  var arr = id.split('_');
  event = arr.shift();
  form = arr.join('_');
  return {
    event: event,
    form: form
  }
}

function getQuestionPanelHeight(isPanel, action) {
  if (action == 'create') {
    if (isPanel) {
      return '55%'
    }
    return '55%'
  }
  if (isPanel) {
    return '75%'
  }
  return '85%'
}

function getQuestionPanelVisible(index) {
  if (index == 0) {
    return 'visible'
  }
  return ''
}

function getBottomBorder(index, last_index) {
  if (index == last_index) {
    return ""
  }
  return 'bottom-grey-border'
}

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

function toggleClasses($circle_current, $panel_current, $circle_change, $panel_change) {
  $circle_current.removeClass('active-circle');
  $panel_current.removeClass('visible');
  $circle_change.addClass('active-circle');
  $panel_change.addClass('visible');
}

function displayForm(res) {
  var question_groups = res.question_groups;
  var form_name = question_groups[0][0].form_name;
  var form_verbose_name = getVerboseName(form_name);

  var leading_html =
    "<div class='pop-up'>" +
    "<form class='redcap-form' id='" + form_name + "'>" +
    "<div class='question-view'>"
  //
  patients = [{
    'name': 'Testdcap2',
    'record_id': 'testdcap2'
  }, {
    'name': 'Test Dcap3',
    'record_id': 'testdcap3'
  }]
  leading_html += genHeader(form_verbose_name, res.event, patients)
  // TODOonly doing 1 question group to test atfirst.

  for (var i = 0; i < question_groups.length; i++) {
    question_group = question_groups[i];
    question_panel = genQuestionPanel(question_group, i, res.event);
    leading_html += question_panel; // The question_panel is closed within the function
  }
  leading_html += genProgressPanel(question_groups.length, form_name);

  var lagging_html = "</div>" +
    "</form>" +
    "</div>"

  $("body").append(leading_html + lagging_html);

}

$(document).ready(function() {
  $('.form-button').click(function(e) {
    e.preventDefault();
    var id = $(this).attr('id');
    var action = getRequest(id);
    $.ajax({
      url: '',
      type: 'get',
      dataType: 'json',
      data: action,
      success: function(res) {
        displayForm(res);
      },
      error: function(res) {
        console.log("oops");
      }
    })
  })
  $('div').click(function(e) {
    e.stopPropagation();
    if (($('.pop-up')[0]) && $(this).attr("class") != 'pop-up') {
      $('.pop-up').remove();
    }
  })
})
$(document).on('click', '.next-page-button', function() {
  var $circle_current = $('.active-circle');
  var $panel_current = $('.visible');
  var current_id = $circle_current.attr('id');
  var arr = current_id.split('_')
  var index = parseInt(arr[arr.length - 1]) + 1;
  //We want to check if the next id exists if it doesnt we need to switch our button next page to submit
  changeSubmit(index);
  var $circle_change = $("#button_" + index);
  var $panel_change = $("#question_panel_" + index);
  toggleClasses($circle_current, $panel_current, $circle_change, $panel_change)
})

$(document).on('click', '.form-circle', function() {
  var $circle_current = $('.active-circle');
  var $panel_current = $('.visible');
  $circle_change = $(this);
  var id = $circle_change.attr('id');
  var index = id.split('_')[1];
  //We want to check if the next id exists if it doesnt we need to switch our button next page to submit
  changeSubmit(index);
  var $panel_change = $('#question_panel_' + index);
  toggleClasses($circle_current, $panel_current, $circle_change, $panel_change)
})

$(document).on('click', '.submit-form', function(e) {
  e.preventDefault();
  var form_array = $(this).attr('id').split('_');
  form_array = form_array.slice(0, -1);
  var form_name = form_array.join('_');
  var $form = $('#' + form_name);
  var data = $form.serialize();

  var csrf_token = $('meta[name="csrf-token"]').attr('content')
  // FIXME cohort_num must come from somewhereelse
  data += ('&cohort_num=' + '1');
  data += ('&csrfmiddlewaretoken=' + csrf_token);
  $.ajax({
    url: '',
    type: 'post',
    dataType: 'json',
    data: data,
    success: function(res) {
      $('.pop-up').remove();
      //displayForm(res);
    },
    error: function(res) {
      console.log("oops");
    }
  })
  //var data = $('#'+form_name).serialize();
  //console.log(data);
})