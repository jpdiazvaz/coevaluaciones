
(function(window, undefined) {

    var qtemplate  = $('#template-pregunta').children('div').clone();
    var optemplate = $('#template-opcion').children('li').clone();

    // helper to reset a compound attribute
    // *at* is the attribute to reset
    // *val* is the new number to set in the attribute value
    // *posFromBack* is the position of the new value in the compound
    //   value, for example, "asdf_1_32_17" could be reset to
    //   "asdf_1_0_17" with *posFromBack* = 1 (it's 0-based)
    var resetAttr = function(elem, at, val, posFromBack) {
        var has = $(elem).attr(at);
        var parts = has ? has.split("_") : [];
        if (parts.length > posFromBack) {
            var tail = [];
            for (var i = 0; i <= posFromBack; i++)
                tail.push(parts.pop());
            parts.push(val);
            tail.pop();
            while (tail.length > 0)
                parts.push(tail.pop());
            $(elem).attr(at, parts.join("_"));
        }
    };

    window.resetAttr = resetAttr;

    // helper to update numbered attributes and other fields in a
    // question
    var modifyQuestion = function(q, qnum) {
        // the id
        resetAttr(q, 'id', qnum, 0);
        // the badge dislaying the question number
        var badge = $(q).children().first().children().first();
        badge.text(qnum);
        badge.attr('title', 'Pregunta número ' + qnum);
        // input 'name' and 'id' attributes
        $(q).find('input').each(function(index, e) {
            resetAttr(e, 'name', qnum, 0);
            resetAttr(e, 'id',   qnum, 0);
        });
        // textarea 'name' attribute
        $(q).find('textarea').each(function(index, e) {
            resetAttr(e, 'name', qnum, 0);
        });
        // select 'name' and 'id' attributes
        $(q).find('select').each(function(index, e) {
            resetAttr(e, 'name', qnum, 0);
            resetAttr(e, 'id',   qnum, 0);
        });
        // label 'for' attributes
        $(q).find('label').each(function(index, e) {
            resetAttr(e, 'for', qnum, 0);
        });
        // button or select 'pregunta_id' attributes
        $(q).find('button, select').each(function(index, e) {
            resetAttr($(this), 'pregunta_id', qnum, 0);
        });
        // modify options
        $(q).find('.opcion').each(function(index, e) {
            modifyOption($(this), index + 1, qnum);
        });
    };

    // remove, reorder, add questions
    var removeQuestion = function(event) {
        var qnum = parseInt($(event.currentTarget).attr("pregunta_id"));
        var q = $("#pregunta_" + qnum);
        if (!q || q === undefined) return;
        q.nextAll('.pregunta').each(function(ind, e) {
            var prevnum = e.id.split("_").pop();
            modifyQuestion(e, prevnum - 1);
        });
        q.remove();
        var total = $('#total_preguntas').val();
        $('#total_preguntas').val(parseInt(total) - 1);
    };

    var addQuestion = function(event) {
        var total = $('#total_preguntas').val();
        var newq = qtemplate.clone();
        var newtotal = parseInt(total) + 1;
        modifyQuestion(newq, newtotal);
        setQuestionEvents(newq);
        $(newq).appendTo($('#preguntas'));
        $('#total_preguntas').val(newtotal);
    };

    var moveUpQuestion = function(event) {
        var qnum = parseInt($(event.currentTarget).attr("pregunta_id"));
        var q = $("#pregunta_" + qnum);
        if (qnum <= 1) return;
        var pq = q.prev();
        modifyQuestion(q, qnum - 1);
        modifyQuestion(pq, qnum);
        q.detach();
        q.insertBefore(pq);        
    };

    var moveDownQuestion = function(event) {
        var qnum = parseInt($(event.currentTarget).attr("pregunta_id"));
        var q = $("#pregunta_" + qnum);
        var total = parseInt($('#total_preguntas').val());
        if (qnum >= total) return;
        var nq = q.next();
        modifyQuestion(nq, qnum);
        modifyQuestion(q, qnum + 1);
        q.detach();
        q.insertAfter(nq);
    };

    // change the question type
    var changeType = function(event) {
        var qnum = $(event.currentTarget).attr("pregunta_id");
        var q = $('#pregunta_' + qnum);
        var type = q.find(".cambiar-tipo option:selected").val();
        if (type == "A" || type == "M") {
            q.find(".numerico").css("display", "none");
            q.find(".opciones").css("display", "block");
        } else if (type == "N") {
            q.find(".numerico").css("display", "block");
            q.find(".opciones").css("display", "none");
        } else {
            q.find(".numerico").css("display", "none");
            q.find(".opciones").css("display", "none");
        }
    };

    // helper to update numbered attributes in an option
    var modifyOption = function(op, num, qnum) {
        // id attribute
        resetAttr(op, 'id', num, 1);
        resetAttr(op, 'id', qnum, 0);
        // input 'name' attributes
        $(op).find('input').each(function(i, e) {
            resetAttr($(this), 'name', num, 1);
            resetAttr($(this), 'name', qnum, 0);
        });
        // button 'opcion_id' and 'pregunta_id' attributes
        $(op).find('button').each(function(i, e) {
            resetAttr($(this), "opcion_id", num, 0);
            resetAttr($(this), "pregunta_id", qnum, 0);
        });
    };

    // add, move up, move down options
    var addOption = function(event) {
        var qnum = parseInt($(event.currentTarget).attr("pregunta_id"));
        var q = $('#pregunta_' + qnum);
        var total = $(q).find('.total-opciones').val();
        var newtotal = parseInt(total) + 1;
        var newop = optemplate.clone();
        modifyOption(newop, newtotal, qnum);
        setOptionEvents(newop);
        $(newop).appendTo($(q).find('.lista-opciones'));
        $(q).find('.total-opciones').val(newtotal);
    };

    var moveUpOption = function(event) {
        console.log("moveUpOption");
        var qnum = parseInt($(event.currentTarget).attr("pregunta_id"));
        console.log(qnum);
        var opnum = parseInt($(event.currentTarget).attr("opcion_id"));
        console.log(opnum);
        if (opnum <= 1) return;
        var op = $('#opcion_' + opnum + "_" + qnum);
        var prevOp = op.prev();
        modifyOption(op, opnum - 1, qnum);
        modifyOption(prevOp, opnum, qnum);
        op.detach();
        op.insertBefore(prevOp);
    };

    var moveDownOption = function(event) {
        console.log("moveDownOption");
        var qnum = parseInt($(event.currentTarget).attr("pregunta_id"));
        var opnum = parseInt($(event.currentTarget).attr("opcion_id"));
        var total = parseInt($('#total_opciones_' + qnum).val());
        if (opnum >= total) return;
        var op = $('#opcion_' + opnum + "_" + qnum);
        var nextOp = op.next();
        modifyOption(op, opnum + 1, qnum);
        modifyOption(nextOp, opnum, qnum);
        op.detach();
        op.insertAfter(nextOp);
    };

    var removeOption = function(event) {
        console.log("removeOption");
        var qnum = parseInt($(event.currentTarget).attr("pregunta_id"));
        var opnum = parseInt($(event.currentTarget).attr("opcion_id"));
        var op = $('#opcion_' + opnum + '_' + qnum);
        if (!op || op === undefined) return;
        op.nextAll('.opcion').each(function(ind, e) {
            var parts = e.id.split("_");
            parts.pop();
            var prevnum = parts.pop();
            modifyOption(e, prevnum - 1, qnum);
        });
        op.remove();
        var total = $('#total_opciones_' + qnum).val();
        $('#total_opciones_' + qnum).val(parseInt(total) - 1);
    };

    // sets the main events for a question widget
    var setQuestionEvents = function(selector) {
        selector.find('.borrar-pregunta').click(removeQuestion);
        selector.find('.subir-pregunta').click(moveUpQuestion);
        selector.find('.bajar-pregunta').click(moveDownQuestion);
        selector.find('.cambiar-tipo').change(changeType);
        setOptionEvents(selector);
    };

    var setOptionEvents = function(selector) {
        selector.find('.borrar-opcion').click(removeOption);
        selector.find('.subir-opcion').click(moveUpOption);
        selector.find('.bajar-opcion').click(moveDownOption);
        selector.find('.agregar-opcion').click(addOption);
    };

    window.addQuestion       = addQuestion;
    window.setQuestionEvents = setQuestionEvents;

})(window);
