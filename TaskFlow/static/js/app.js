// Espera o navegador construir toda a página antes de procurar elementos ou
// executar comportamentos da interface.
document.addEventListener('DOMContentLoaded', () => {
    // Confirma, pelo DevTools, que o JavaScript foi carregado.
    console.log('TaskFlow loaded');

    // Alterna o tema e guarda a escolha para ela continuar após recarregar.
    const themeToggle = document.querySelector('#theme-toggle');
    const savedTheme = localStorage.getItem('taskflow-theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
        themeToggle.setAttribute('aria-pressed', 'true');
    }
    themeToggle.addEventListener('click', () => {
        const isLight = document.body.classList.toggle('light-theme');
        themeToggle.setAttribute('aria-pressed', String(isLight));
        localStorage.setItem('taskflow-theme', isLight ? 'light' : 'dark');
    });

    // Em telas menores, abre e fecha a barra lateral pelo botão do cabeçalho.
    const menuButton = document.querySelector('.menu-button');
    const sidebar = document.querySelector('.sidebar');
    menuButton.addEventListener('click', () => sidebar.classList.toggle('menu-open'));

    // Leva o usuário diretamente ao formulário ao clicar em Nova tarefa.
    const newTaskButton = document.querySelector('#new-task-button');
    newTaskButton.addEventListener('click', () => {
        document.querySelector('#new-task').scrollIntoView({ behavior: 'smooth' });
        document.querySelector('#new-task input').focus();
    });
});
