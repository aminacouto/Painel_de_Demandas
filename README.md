### Acesso ao LAD Issues no GitHub Codespaces

---

#### Criar um Token de Acesso no GitHub
1. Acesse GitHub Developer Settings.
2. Clique em "Generate new token" (ou "Generate new token (classic)", dependendo da versão).
3. Dê um nome para o token (por exemplo, LAD-Token).
4. Defina a data de expiração conforme necessário.
5. Em Scopes, selecione pelo menos:
- repo (acesso a repositórios privados, se necessário)
6. Clique em Generate token.
7. Copie o token gerado e guarde-o temporariamente (não será possível vê-lo novamente).

#### Adicionar o Token ao Codespaces
1. Criar um novo codespace.
2. No terminal do Codespace, execute o comando: 
   bash script.sh
3. O script solicitará que você insira o token de segurança gerado anteriormente.
4. Pressione Enter e aguarde o script ser finalizado.
   
**Importante:** O token ficará disponível enquanto o Codespace estiver ativo. Se um novo Codespace for aberto, será necessário adicionar novamente um token válido.
