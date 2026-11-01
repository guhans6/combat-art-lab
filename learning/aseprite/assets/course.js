document.querySelectorAll('[data-quiz]').forEach(quiz => {
  const feedback = quiz.querySelector('[role="status"]');
  quiz.querySelectorAll('button[data-answer]').forEach(button => {
    button.addEventListener('click', () => {
      const correct = button.dataset.answer === quiz.dataset.correct;
      feedback.textContent = correct ? quiz.dataset.success : quiz.dataset.retry;
      feedback.className = 'feedback ' + (correct ? 'correct' : 'incorrect');
      quiz.querySelectorAll('button').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    });
  });
});
document.querySelectorAll('input[data-check]').forEach(input => {
  const key = 'aseprite-course:' + location.pathname + ':' + input.dataset.check;
  try { input.checked = localStorage.getItem(key) === 'true'; } catch {}
  input.addEventListener('change', () => {
    try { localStorage.setItem(key, String(input.checked)); } catch {}
  });
});
