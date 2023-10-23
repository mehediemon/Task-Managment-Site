
let assign_user;

function myfunction() {
    let bttn = document.getElementById("btn1");
    alert("HELLO mia vaiasdasdad");
}

function get_username() {
    console.log('gfds')
    return assign_user;
}

$(document).ready(function () {
    $('.edit-task').click(function () {
        var taskId = $(this).data('task-id');
        $.ajax({
            url: '/get_task_details/' + taskId + '/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                $('#taskIds').val(data.id);
                $('#taskName').val(data.name);
                $('#taskDate').val(data.date);
                $('#finishDate').val(data.fdate);
                $('#taskClient').val(data.client)
                $('#taskStatus').val(data.status);
                $('#taskType').val(data.type);
                $('#taskAssignedUser').val(data.assigned_user_id);
                $('#taskTime').val(data.time);
                assign_user = data.assigned_user_id;


            },
            error: function () {
                // Handle error
            }
        });
    });

    $('#saveChanges').click(function () {
        var taskId = $('#taskIds').val();
        console.log(taskId)
        var taskName = $('#taskName').val();
        var taskDate = $('#finishDate').val();
        var taskStatus = $('#taskStatus').val();
        var taskAssignUser = $('#taskAssignedUser').val()
        var taskTime = $('#taskTime').val();
        $.ajax({
            url: '/update_task/' + taskId + '/',
            type: 'POST',
            cache: false,
            data: {
                task_name: taskName,
                date: taskDate,
                status: taskStatus,
                time: taskTime,
                assign_user: taskAssignUser,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (data) {
                $('#exampleModal').modal('hide');
                $('.modal-backdrop').remove();

                location.reload();

                // Update the table or display a success message
            },
            error: function () {
                // Handle error
            }
        });
    });
});
