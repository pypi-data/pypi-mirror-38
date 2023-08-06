
window.onload = function () {

    $('#sidebarCollapse').on('click', function () {
        $('#wrapper').toggleClass('sidebar-collapsed');
        if($('#wrapper').hasClass('sidebar-collapsed')){
           localStorage.setItem('sidebarCollapse', true);
        }
        else{
           localStorage.setItem('sidebarCollapse', false);
        }
    });
}


const Main = new function(){

    this.Utils = new function(){

        this.getDateTimeFromTimestamp = function(timestamp){
            var sp = timestamp.split('.');
            var dateTimeString = sp[0]+'/'+sp[1]+'/'+sp[2]+' '+sp[3]+':'+sp[4];
            return dateTimeString
        }

        this.toast = function(type, msg, duration){
            toastr.options = {
                "positionClass": "toast-top-center",
                "timeOut": duration.toString(),
                "hideDuration": "100"
            }
            if(type == 'success')
                toastr.success(msg)
            else if(type == 'error')
                toastr.error(msg)
            else if(type == 'info')
                toastr.info(msg)
        }

        this.displayErrorModal = function(errors){
            var ulContent = '';
            for(e in errors){
                ulContent += "<li>"+errors[e]+"</li>";
            }
            $("#errorList").html(ulContent);
            $("#errorModal").modal("show");
            window.setTimeout(function(){
                $("#errorModal .dismiss-modal").focus();
            }, 500);
        }

        // How to use the confirm modal:
        // Call displayConfirmModal(title, message, callback),
        //
        // When the Confirm Modal is confirmed the callback is called.
        // Pass an anonymous function as callback in order to include parameters with it,
        // example:
        // var callback = function(){
        //     myCustomFunction(param1, param2);
        // }
        this.displayConfirmModal = function(title, message, callback){
            $("#confirmModal .modal-title").html(title);
            $("#confirmModal .modal-body").html(message);
            $("#confirmModal button.confirm").click(function(){
                $("#confirmModal .modal-title").html('');
                $("#confirmModal .modal-body").html('');
                $("#confirmModal button.confirm").unbind('click');
                $("#confirmModal").modal("hide");
                callback();
            })
            $("#confirmModal").modal("show");
            $('#confirmModal').on('shown.bs.modal', function () {
                $("#confirmModal button.confirm").focus();
            });
        }

        // How to use the prompt modal:
        // Call displayPromptModal(title, description, inputValue, callback),
        //
        // When the 'Save' button is clicked, the callback function is called.
        // Pass an anonymous function as callback in order to include parameters with it,
        // example:
        // var callback = function(){
        //     myCustomFunction(param1, param2);
        // }
        this.displayPromptModal = function(title, description, inputValue, inputPlaceholder, callback){
            $("#promptModal .modal-title").html(title);
            $("#promptModal .modal-body .description").html(description);
            $("#promptModal .modal-body input").val(inputValue);

            $("#promptModal").modal("show");
            $('#promptModal').on('shown.bs.modal', function () {
                $('#promptModalInput').focus();
            });

            var sendValue = function(){
                var sentValue = $("#promptModalInput").val();
                callback(sentValue);
                $("#promptModal").modal("hide");
                $("#prompSaveButton").unbind('click');
            }

            $("#promptModal button.confirm").click(function(){
                sendValue();
            })
        }

        // How to use the select prompt modal:
        // Call displaySelectPromptModal(title, description, options, buttonLabel, callback),
        //
        // When the user selects an option from the select, the callback function is called.
        // Pass an anonymous function as callback in order to include parameters with it,
        // example:
        // var callback = function(){
        //     myCustomFunction(param1, param2);
        // }
        this.displaySelectPromptModal = function(title, description, options, buttonLabel, callback){
            buttonLabel = buttonLabel || 'Continue';
            $("#selectPromptModal .modal-title").html(title);
            $("#selectPromptModal .modal-body .description").html(description);

            $("#selectPromptContinueButton").html(buttonLabel);

            $("#selectPromptSelect").html('');
            $.each(options, function(i){
                var itemval = "<option value='"+options[i]+"'>"+options[i]+"</option>";
                $("#selectPromptSelect").append(itemval)
            });
            $("#selectPromptModal button.confirm").focus();
            $("#selectPromptModal").modal("show");
            $('#selectPromptModal').on('shown.bs.modal', function () {
                $("#selectPromptModal button.confirm").focus();
            });
            var confirm = function(){
                var selectedVal = $("#selectPromptSelect").val();
                callback(selectedVal);
                $("#selectPromptModal").modal("hide");
                $("#selectPromptSelect").unbind('change');
                $("#selectPromptSelect").unbind('change');
                $("#selectPromptModal button.confirm").unbind('click');
            }
            $("#selectPromptModal button.confirm").click(function(){
                confirm();
            })
        }

        this.guid = function()  {
            function s4() {
                return Math.floor((1 + Math.random()) * 0x10000)
                    .toString(16)
                    .substring(1);
            }
            return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
        }

        this.getResultIcon = function(result){
            let classValue;
            switch(result) {
                case Main.ResultsEnum.success.code:
                    classValue = 'fa fa-check-circle-o';
                    break;
                case Main.ResultsEnum.failure.code:
                    classValue = 'fa fa-times-circle';
                    break;
                case Main.ResultsEnum.error.code:
                    classValue = 'fa fa-exclamation-circle';
                    break;
                case Main.ResultsEnum['code error'].code:
                    classValue = 'fa fa-exclamation-circle';
                    break;
                default:
                    classValue = 'fa fa-question-circle-o'
            }
            let color = Main.ReportUtils.getResultColor(result);
            let html = $(`<span><i class="${classValue}"></i></span>`);
            html.css('color', color);
            return html[0].outerHTML
        }

        this.capitalizeWords = function(str){
            return str.replace(/(^|\s)\S/g, l => l.toUpperCase())
        }
    }


    this.ReportUtils = new function(){

        this.getResultColor = function(result){
            if(result in Main.ResultsEnum){

                return Main.ResultsEnum[result].color
            }
            else{
                return Main.ReportUtils.colorFromString(result)
            }
        }

        this.colorFromString = function(str){
            let hash = 0;
            if (str.length === 0) return hash;
            for (var i = 0; i < str.length; i++) {
                hash = str.charCodeAt(i) + ((hash << 5) - hash);
                hash = hash & hash;
            }
            hash = Math.abs(hash);
            let hue = hash % 360;
            let s = 50 + hash % 30;
            let l = 40 + hash % 30;
            return `hsl(${hue}, ${s}%, ${l}%)`
        }

        this.createProgressBars = function(container, results){
            results.forEach(function(result){
                let color = Main.ReportUtils.getResultColor(result);
                let bar = $(`
                    <div aria-valuenow='10' style='width: 0%;'
                        class='progress-bar' result-code="${result}"
                        data-transitiongoal='10'>
                    </div>
                `);
                bar.css('background-color', color); 
                container.append(bar);
            });           
        }

        this.expandImg = function(e){
            $("#expandedScreenshot").attr('src', e.srcElement.src);
            $("#screenshotModal").modal('show');
        }

        this.animateProgressBar = function(container, result, percentage){
            setTimeout(function(){
                let bar = container.find(`div.progress-bar[result-code='${result}']`);
                bar.css('width', `${percentage}%`);
            }, 100);
        }

        this.hasProgressBarForResult = function(container, result){
            return container.find(`div.progress-bar[result-code='${result}']`).length != 0
        }
    }


    this.ResultsEnum = {
        // taken from https://yeun.github.io/open-color/
        'success': {
            code: 'success',
            //color: '#95BD65'
            color: '#37b24d',
        },
        'failure': {
            code: 'failure',
            //color: '#fd5a3e'
            color: '#f03e3e'
        },
        'error': {
            code: 'error',
            color: '#fd7e14',
        },
        'code error': {
            code: 'code error',
            color: '#fcc419',
        },
        'pending': {
            code: 'pending',
            color: '#74c0fc'
        },
        'skipped': {
            code: 'skipped',
            color: '#ced4da'
        },
        'not run': {
            code: 'skipped',
            color: '#868e96'
        }
    }
}