$(document).ready(function(){
    
    $(".sticky").sticky();

    $('#add_video_form_tags').dropdown({
        allowAdditions: true,
    });

    $('#activity_type').dropdown({
        apiSettings: {
          url: '/activity_classes/'
        },
        fields: {
          name   : 'label',
          value  : 'uri',
          text : 'label'
        },
        minCharacters : 3 
      })

    $('#scene_concepts').dropdown({
        apiSettings: {
          url: '/activity_search/:Activity/{query}'
        },
        fields: {
          name   : 'label',
          value  : 'activity',
          text : 'label'
        },
        minCharacters : 3 
      })

      $('#scene_places').dropdown({
        apiSettings: {
          url: '/activity_search/:Destination/{query}'
        },
        fields: {
          name   : 'label',
          value  : 'activity',
          text : 'label'
        },
        minCharacters : 3
      })

    $("#add_video_form_tags").parent().find("i").hide()

    var ytURLVideoIdRegex = /(embed\/|watch\?v=)(.*)$/gm; 

    var secondsToHMSISO = function(seconds) {
        var _d =  moment.duration(Number(Math.round(seconds)), 'seconds')
        return `PT${_d.hours()}H${_d.minutes()}M${_d.seconds()}S`
    }

    var getYTVideoInfo = function(url) {
        var id = ytURLVideoIdRegex.exec(url)[2]
        console.log(id)
        $.getJSON(`/yt_video_info/${id}`, function(result) {

            Object.keys(result).map(function(key, index) {
                result[key] = decodeURIComponent(result[key]);
            });

            if (result !== undefined) {
                if ("title" in result) {
                    result.title = result.title.split("+").join(" ")
                }
    
                if ("keywords" in result) {
                    result.keywords = result.keywords.split(",").map(k => k.split("+").join(" "))
                }

                $("#title").val(result.title)
                $("#add_video_form_tags").dropdown("set selected", result.keywords)
            }
        });
        
    }

    window.setAddVideoFormPreview = function(url) {
        
        if (url === undefined || url.length <= 0) {
            return false;
        }

        getYTVideoInfo(url)

        if($("#video_preview .video-js").length == 1) {
            videojs("add_video_form_preview").ready(function() {
                var player = this;
                player.src({ type: 'video/youtube', src: url });
                player.play();
            });
        } else {

            $("#video_preview").find(".placeholder").remove()

            $("#video_preview").append(`<video
                style="width: 100%; height: 100%;"
                id="add_video_form_preview"
                class="video-js vjs-default-skin"
                controls
                data-setup='{ "fluid": false, "techOrder": ["youtube"], "sources":[{ "type": "video/youtube", "src": "${url}" }]}'>
            </video>`)
            videojs("add_video_form_preview").ready(function() { 
                var player = this;
                this.on('timeupdate', function _updateDuration (){ 
                    var d = player.duration();

                    if (d > 0) {
                        $("#duration")
                        .val(secondsToHMSISO(d));
                        this.off('timeupdate', _updateDuration);
                    }
                    console.log("time", d);
                });
                player.play();
            });
        }

        return false;	
    };

    window.currentVideoPosTo = function(to) {
        videojs("add_video_form_preview").ready(function() { 
            var d = this.currentTime();
            var t = moment.duration(d, 'seconds');
            $(`input[name='${to}']`).val(moment.utc(t.asMilliseconds()).format("HH:mm:ss"));
        });
    }

    $("form").on('keyup keypress', function(e) {
        var keyCode = e.keyCode || e.which;
        if (keyCode === 13) { 
            e.preventDefault();
            return false;
        }
    });

    window.currStep = 1;

    window.nextStep = function() {
        var _nextStep = currStep + 1 
        if (_nextStep > 3) return;
        $(`.step-${currStep}`).slideUp();
        $(`.step-${_nextStep}`).slideDown();
        $(`#add_video_form_step_${currStep}`).addClass("completed")
        $(`#add_video_form_step_${_nextStep}`)
            .removeClass("disabled")
            .addClass("active")
        currStep = _nextStep
    };

    window.prevStep = function() {
        var _prevStep = currStep - 1
        if (_prevStep < 1) return;
        $(`.step-${currStep}`).slideUp();
        $(`.step-${_prevStep}`).slideDown()
        $(`#add_video_form_step_${currStep}`)
            .removeClass("completed")
            .addClass("disabled")
        $(`#add_video_form_step_${_prevStep}`)
            .removeClass("completed")
            .addClass("active")
        currStep = _prevStep
    };

    window.addCurrScene = function() {
        var start = $(".step-2").find("form").form("get value", "scene_start")
        var end = $(".step-2").find("form").form("get value", "scene_end")
        var label = $(".step-2").find("form").form("get value", "scene_label")
        
        var newScene = $.parseHTML(`<tr class="scene">
                    <td data-label="Start">${start}</td>
                    <td data-label="End">${end}</td>
                    <td data-label="Label">${label}</td>
                    <td data-label="Concepts"><div class="ui divided list concepts"></div></td>
                    <td style="text-align:center";><button class="ui circular negative basic icon button" onclick="$(this).parents('tr').remove(); return false;">
                        <i class="cancel icon"></i>
                    </button></td></tr>`)

        var newSceneElem = $(newScene);

        $("#scene_places").dropdown("get value").forEach(element => {
            var name = element.split("#")[1]
            newSceneElem.find('.concepts').append(`
                <div class="item">
                <div class="ui green label" data-type="place" data-uri="${element}"><i class="map marker alternate icon"></i>${name}</div>
                </div>`)
        });
        
        $("#scene_concepts").dropdown("get value").forEach(element => {
            var name = element.split("#")[1]
            newSceneElem.find('.concepts').append(`
                <div class="item">
                <div class="ui blue label" data-type="activity" data-uri="${element}"><i class="bolt icon"></i>${name}</div>
                </div>`)
        });

        newSceneElem.appendTo($(".step-2").find("tbody"));
    }


    window.uploadNewVideo = function() {

        var form1 = $("form.step-1")
        var url = form1.form("get value", "url")
        var title = form1.form("get value", "title")
        var description = form1.form("get value", "description")
        var duration = form1.form("get value", "duration")
        var tags = form1.form("get value", "tags").join(" ")
        
        var _scenes = $(".scene")
        var scenes = []
        for(i=0; i < _scenes.length; i++) {
            var s = _scenes.eq(i)
            var _concepts = s.find("td[data-label='Concepts'] .label")
            var concepts = []
            for(j=0; j < _concepts.length; j++) {
                concepts.push(_concepts[j].getAttribute("data-uri"))
            }
            var r = {
                start: s.find("td[data-label='Start']").text(),
                end: s.find("td[data-label='End']").text(), 
                label: s.find("td[data-label='Label']").text(), 
                concepts: concepts
            }
            scenes.push(r)
        }

        var newVideo = {
            url: url,
            title: title,
            duration: duration,
            keywords: tags,
            description: description,
            scenes: scenes
        }

        $.ajax({
            type: 'POST',
            url: '/upload_video',
            data:  JSON.stringify(newVideo),
            success: function(data) { console.log("result", data); },
            contentType: "application/json",
            dataType: 'json'
        });
    }

    window.createNewActivity = function () {
        var form = $("#new_activity_form")
        var a = {
            name: $(form).form("get value", "activity_name"),
            label: $(form).form("get value", "activity_label"),
            type: $("#activity_type").dropdown("get value")
        }

        $.ajax({
            type: 'POST',
            url: '/add_activity',
            data:  JSON.stringify(a),
            success: function(data) { console.log("result", data); },
            contentType: "application/json",
            dataType: 'json'
        });
    }
});