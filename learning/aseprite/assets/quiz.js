document.querySelectorAll("[data-quiz]").forEach(function(q){
  var check=q.querySelector("[data-check]"),result=q.querySelector("[data-result]");
  if(!check||!result)return;
  check.addEventListener("click",function(){
    var chosen=q.querySelector("input[type=radio]:checked");
    if(!chosen){result.textContent="Choose one answer first.";result.className="answer bad";return;}
    var correct=chosen.value===q.dataset.correct;
    result.textContent=(correct?"Correct. ":"Not yet. ")+(correct?q.dataset.explain:"Try again: think about which information stays editable.");
    result.className="answer "+(correct?"good":"bad");
  });
});
