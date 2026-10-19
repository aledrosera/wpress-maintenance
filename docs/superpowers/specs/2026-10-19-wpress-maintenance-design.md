# wpress-maintenance: design

Data: 19/10/2026 · Repository: `github.com/aledrosera/wpress-maintenance` (pubblico) · Licenza: MIT

## 1. Scopo
Un plugin per Claude Code che, partendo da un backup All-in-One WP Migration (`.wpress`) di un sito WordPress qualsiasi, porta il sito in locale e lo rende:
- **bonificato**: compromissioni individuate e rimosse;
- **pulito**: niente componenti, contenuti, dati o media inutilizzati;
- **ottimizzato**: media, cache e caricamento delle risorse;
- **verificato**: nessuna regressione visiva o funzionale non voluta rispetto al sito online.

Alla fine produce un report tecnico e, su conferma, il backup `.wpress` del sito ottimizzato.

Il plugin è un **playbook adattivo**, non un'automazione a script. Insegna a Claude obiettivi, criteri di decisione, metodi di verifica e rischi noti, così che si adatti a qualsiasi combinazione di tema, page builder, plugin, stack server e stato di compromissione.

## 2. Scenario d'uso
- **Chi lo usa:** chi gestisce o manutiene siti WordPress (agenzia, freelance, sistemista).
- **Cosa fornisce:** una cartella di lavoro con il `.wpress` del sito (oppure l'URL da cui scaricarlo) e lo zip di All-in-One WP Migration Unlimited Extension.
- **Come si avvia:** con `/wpress-maintenance:wpress`. Il flusso procede in autonomia fino al risultato, fermandosi solo nei casi previsti al §7.

## 3. Fuori ambito
- Il deploy in produzione: il plugin consegna la copia pulita, il backup e la checklist delle azioni sul server.
- Qualunque scrittura sul sito online, sul server o su servizi esterni.
- Redesign o modifiche di contenuto non necessarie alla bonifica, alla pulizia o all'ottimizzazione.

## 4. Input e preflight
1. **Backup.** Si cerca il `.wpress` nella cartella di lavoro. Se manca, si chiede all'utente un URL raggiungibile e lo si scarica in autonomia nella cartella di lavoro. Il download deve poter riprendere se si interrompe, e alla fine si verifica che il file sia un `.wpress` valido. Se ci sono più `.wpress`, si chiede quale usare.
2. **Unlimited Extension.** Si cerca lo zip dell'add-on nella cartella di lavoro. Se manca, lo si scarica da `https://nextcloud.joinindots.com/index.php/s/PJxrSyW2gSwqDxZ/download/all-in-one-wp-migration-unlimited-extension.zip`. Se il download non riesce, si chiede all'utente di fornire lo zip o di indicare dove si trova.
3. **Lettura dei metadati in streaming.** Da `package.json` dentro l'archivio si ricavano:
   - URL del sito;
   - versioni di WordPress, PHP e database;
   - prefisso delle tabelle;
   - plugin attivi, tema;
   - presenza di cifratura: se l'archivio è cifrato si chiede la password.
4. **Requisiti locali:**
   - Docker disponibile;
   - spazio su disco sufficiente: l'import occupa circa la dimensione dell'archivio, più il database;
   - una porta libera.

   Se manca qualcosa, il flusso si ferma con un'indicazione precisa di cosa manca.

## 5. Principi operativi
1. **Il `.wpress` originale non si modifica né si cancella.** Lo si legge in streaming oppure se ne estraggono solo le parti necessarie. Durante l'import è montato in sola lettura.
2. **Niente copie di backup aggiuntive**, salvo casi gravi e motivati. Il `.wpress` originale è il backup di riferimento.
3. **I file temporanei creati dal flusso si cancellano alla fine.** Questo vale anche per gli strumenti installati temporaneamente nei container. Nella cartella di lavoro restano solo gli artefatti consegnati (§6.10).
4. **Una verifica reale vale più di un'ipotesi**, ma con rapidità e buonsenso. Si verifica alla fine di ogni fase e prima delle azioni distruttive, non a ogni singolo passo.
5. **Il sito online è il riferimento visivo.** Serve a scoprire cambiamenti di aspetto o di funzionamento non richiesti e non necessari. Si consulta solo in lettura, con poche richieste in parallelo, bloccando le risorse di terze parti nel rendering (il sito potrebbe essere compromesso).
6. **Si decide in base alle evidenze raccolte sul sito in esame** (fa eccezione la preferenza del proprietario per The SEO Framework), non in base a preferenze predefinite. Il playbook non contiene raccomandazioni di prodotti né comandi d'esempio da riprodurre. Se l'utente indica una preferenza, quella prevale.
7. **Gli account esistenti non si modificano.** Per lavorare si crea un amministratore locale dedicato, che va rimosso prima dell'export finale.
8. **Il report** è nella lingua dell'utente (in mancanza d'altro, quella della conversazione), tecnico, per punti ed essenziale.

## 6. Fasi
Ogni fase ha un obiettivo e un criterio di uscita. Il *come* lo decide Claude sul sito in esame, seguendo i criteri indicati. Ogni fase si può rilanciare da sola (§9).

### 6.0 Preflight
- **Obiettivo:** input completi e ambiente idoneo (§4).
- **Uscita:** archivio valido e leggibile, add-on disponibile, requisiti soddisfatti.

### 6.1 Ambiente locale
- **Obiettivo:** un WordPress locale in container che riproduca le versioni di produzione. Se una versione esatta non è disponibile, si usa la più vicina compatibile e lo si annota.
- **Configurazione:**
  - limiti PHP adeguati all'import;
  - un servizio wp-cli;
  - il `.wpress` montato in sola lettura.
  - I file di configurazione dell'ambiente stanno nella cartella di lavoro.
- **Uscita:** WordPress raggiungibile in locale.

### 6.2 Import
- **Obiettivo:** il sito importato in locale.
- **Procedura:**
  1. installare il plugin base dalla fonte ufficiale;
  2. installare l'add-on dallo zip e verificarne l'aggiornamento;
  3. importare da riga di comando, leggendo l'archivio montato.
- **Dopo l'import:**
  - creare l'amministratore locale dedicato;
  - verificare che URL e permalink funzionino.
- **Uscita:** il sito risponde e l'amministrazione è accessibile.

### 6.3 Baseline e inventario
- **Obiettivo:** sapere cosa esiste e com'è fatto il sito prima di toccarlo.
- **Inventario degli URL pubblici:** sitemap, scoperta dei link interni e URL raggiungibili ma non linkati (archivi di tassonomie e simili).
- **Stato:** codici di risposta, asset caricati, errori.
- **Stack di produzione:** rilevato in lettura dagli header (server, cache, compressione, protocollo).
- **Uscita:** inventario e baseline registrati, in forma utile ai confronti finali.

### 6.4 Audit (agenti in parallelo)
- **Obiettivo:** individuare compromissioni, rischi e superfluo, con le evidenze.
- **Agenti**, in sola lettura, con un metodo d'indagine e non una checklist chiusa:
  - **file**: integrità rispetto alle fonti ufficiali dove esistono, codice anomalo, file fuori posto, cronologia delle modifiche, versioni nulled;
  - **database**: utenti e capability, credenziali applicative, iniezioni in opzioni e contenuti, cron, regole di redirect, artefatti di exploit;
  - **componenti**: vulnerabilità note alle versioni installate, uso reale di ogni plugin e tema, bloat del db, tabelle e opzioni orfane.
- **Uscita:** elenco dei finding con gravità, evidenze e azione proposta. Se c'è una compromissione, si fa lo stop del §7.

### 6.5 Bonifica
- **Obiettivo:** rimuovere ogni elemento malevolo e chiudere i vettori sfruttati o sfruttabili, in modo adatto allo stack.
- **Uscita:** nessun finding critico o alto ancora aperto in locale; ciò che riguarda solo il server va nella checklist di produzione.

### 6.6 Pulizia
- **Obiettivo:** eliminare plugin, temi, contenuti, dati e file che non servono.
- **Criteri:**
  - si rimuove solo ciò che le evidenze dicono inutilizzato, oppure ciò che va rimosso perché nulled, vulnerabile o malevolo;
  - se un componente da rimuovere è in uso, lo si sostituisce con un equivalente legittimo o lo si ricostruisce, verificando l'aspetto contro il sito online;
  - prima di eliminare contenuti si controllano le dipendenze: gerarchie, riferimenti, menu, URL.
- **Uscita:** db e file senza residui di componenti rimossi; pagine pubbliche invariate.

### 6.7 Media
- **Obiettivo:** tenere solo i media usati, ottimizzati.
- **Uso reale:** si determina visitando con un browser vero tutte le pagine, a più larghezze di schermo e scorrendo fino in fondo. Contano sia i file richiesti sia quelli referenziati nel DOM e nei CSS. Si includono le dipendenze generate dai page builder e si incrocia il risultato col sito online.
- **Pulizia:** si eliminano allegati e file inutilizzati, si riducono i formati generati e mai usati, mantenendo i metadati coerenti.
- **Ottimizzazione:** si ricomprimono immagini e video senza cambiare nomi e percorsi, scegliendo formati e codec in base alla compatibilità e al guadagno misurato.
- **Strumenti:** si installano temporaneamente nei container e si rimuovono alla fine.
- **Uscita:** nessun media mancante nella visita reale; peso ridotto e misurato.

### 6.7b SEO
- **Obiettivo:** The SEO Framework come unico plugin SEO, per preferenza del proprietario.
- **Procedura:** migrazione completa dei dati dei plugin SEO precedenti (titoli, descrizioni, canonical, robots, social, redirect, organizzazione, sitemap), verificata confrontando i tag SEO stampati su ogni URL; poi si crea la SEO mancante, nella lingua del sito e senza toccare i termini del brand.

### 6.7c Accessibilità
- **Obiettivo:** audit automatico più controlli sull'HTML reale.
- **Cosa si sistema:** alt text sensati scritti nella libreria media, nomi accessibili sui link fatti di sole icone, contrasto, titoli, form, "riduci movimento", coerenza della lingua.

### 6.8 Prestazioni
- **Obiettivo:** migliorare tempi di risposta e caricamento.
- **Criteri:**
  - si rileva la cache già presente lato server e lato WordPress, e si sceglie la soluzione coerente con lo stack, senza duplicazioni inutili;
  - si ottimizza il caricamento di CSS e JS preservando gli script che devono eseguire presto o in un ordine preciso;
  - si misura prima e dopo, nelle stesse condizioni.
- **Uscita:** miglioramento misurato, senza errori JS e senza cambiamenti visivi non voluti.

### 6.9 Verifica finale
- **Visita reale completa:** tutte le pagine dell'inventario, con zero errori di pagina, di asset e di JavaScript.
- **Confronto visivo col sito online:** ogni differenza va spiegata come voluta, oppure corretta.
- **Prove funzionali essenziali:** form, pannelli usati dai plugin rimasti.
- **Integrità:**
  - checksum di core e plugin dove disponibili;
  - pattern malevoli nei file;
  - assenza di PHP negli uploads;
  - drop-in, cron, utenti e opzioni.
- **Uscita:** tutti i controlli superati, oppure le eccezioni motivate nel report.

### 6.10 Report e consegna
- **Report Markdown nella cartella di lavoro:** cosa è stato trovato, cosa è stato fatto, numeri prima e dopo, esito della verifica, azioni in produzione e pendenze.
- **Checklist di produzione:** solo ciò che la copia pulita non porta con sé, cioè deploy pulito, server, credenziali e servizi esterni.
- **Backup finale, su conferma dell'utente:**
  1. rimuovere l'amministratore locale;
  2. esportare con All-in-One WP Migration;
  3. **spostare** il file accanto al `.wpress` originale, con un nome che non sovrascriva nulla.
- **Pulizia finale** dei temporanei (§5.3).
- **Deliverable nella cartella di lavoro:** `.wpress` originale (intatto), configurazione dell'ambiente, report, backup ottimizzato.

## 7. Interazioni con l'utente
Il flusso si ferma solo in questi casi:
1. **Input mancanti o ambigui** (§4).
2. **Dopo l'audit, se c'è una compromissione:** si mostra un riepilogo dei punti critici e poi si prosegue in autonomia.
3. **Prima dell'export del backup finale:** serve la conferma.
4. **Azioni che richiedono licenze, acquisti, credenziali o scritture fuori dall'ambiente locale.**

## 8. Rischi noti da verificare
Sono conoscenze generali da usare come **controlli**, non come ricette.
- **Contenuti:**
  - eliminare pagine madri (anche in bozza) cambia gli URL delle figlie;
  - eliminare contenuti può rimuovere voci di menu collegate.
- **Componenti:**
  - rimuovendo un plugin, i widget o gli shortcode che fornisce smettono di funzionare senza dare errori;
  - le versioni "free" e "pro" di un plugin forniscono widget diversi.
- **Media:**
  - i page builder generano file derivati (miniature, CSS) che dipendono dall'allegato originale;
  - un media può essere richiamato da codice custom con URL costruiti dinamicamente.
- **Ottimizzazione:** spostare in `defer` gli script inline può rompere la logica che deve girare durante il parsing della pagina.
- **Cache:**
  - una cache lato server può servire versioni vecchie per tutto il suo tempo di validità;
  - le costanti di cache stanno in `wp-config.php`, che All-in-One WP Migration non migra.
- **Migrazione:** l'import di All-in-One WP Migration sovrascrive db e `wp-content`, ma non cancella i file già presenti sul server.
- **Compromissioni:** firme ricorrenti da cercare sono
  - account amministratore anomali;
  - artefatti di exploit nel db;
  - opzioni con payload;
  - `.htaccess` generati in massa;
  - cartelle di plugin vuote o sconosciute;
  - redirect o pagine spam;
  - versioni nulled che dirottano richieste verso terzi.
- **Sito online:** visitarlo può eseguire codice malevolo, quindi si bloccano le risorse di terze parti.

## 9. Architettura del plugin
Il repository è insieme marketplace e plugin.

```
.claude-plugin/marketplace.json      marketplace (un plugin)
plugins/wpress-maintenance/
  .claude-plugin/plugin.json         manifest
  skills/wpress/
    SKILL.md                         skill invocabile (/wpress-maintenance:wpress [fase|resume]): principi, fasi, stop, ripresa
    references/                      una scheda per fase: obiettivo, criteri, rischi, uscita
  agents/                            audit-files, audit-database, audit-components (§6.4)
  scripts/wpress.py                  lettore del formato .wpress (§10)
README.md  LICENSE  CHANGELOG.md
docs/superpowers/specs/              questo documento
```

- Le istruzioni del plugin sono **in inglese**, per un pubblico internazionale; report e dialogo sono nella lingua dell'utente.
- `SKILL.md` resta breve. Le schede di fase si caricano solo quando servono.
- Gli agenti hanno un metodo d'indagine e un formato di output con evidenze e gravità, ma nessuna checklist rigida.
- Tutto il resto (scansioni, confronti, analisi) Claude lo costruisce sul momento per il sito in esame.

## 10. Lettore `.wpress` (unico script)
- **Funzioni:** elenco delle voci, lettura dei metadati, lettura in streaming di una voce su stdout, estrazione selettiva di percorsi o pattern in una cartella indicata.
- **Robustezza:** gestisce le varianti di header note (con e senza checksum) e rileva gli archivi cifrati o compressi. Davanti a un formato non riconosciuto fallisce con un messaggio chiaro, senza produrre output parziali silenziosi.
- **Vincoli:** sola lettura sull'archivio; solo libreria standard di Python.

## 11. Stato e ripresa
- Lo stato vive nel report in costruzione nella cartella di lavoro: fasi completate, finding e numeri. Non servono altri file di stato.
- `/wpress-maintenance:wpress resume` legge il report e l'ambiente esistente e riparte dalla prima fase incompleta.
- `/wpress-maintenance:wpress <fase>` rilancia una fase singola.

## 12. Sicurezza e privacy
- Nel repository pubblico non entrano dati di clienti: nomi, URL, credenziali, report, archivi.
- Le credenziali locali si mostrano all'utente e non si scrivono nel report.
- Nessuna scrittura verso la produzione; le richieste al sito online sono solo in lettura.

## 13. Validazione del plugin
- **Struttura:** manifest e componenti si caricano senza errori in Claude Code.
- **Lettore `.wpress`:**
  - test su un archivio piccolo generato da un'installazione locale di prova;
  - lettura in streaming di un archivio reale di grandi dimensioni, verificando la sola lettura (dimensione e data invariate).
- **Prova del flusso:** installazione dal marketplace e `/wpress` su una cartella di prova con un `.wpress` piccolo generato apposta, fino al report e al backup finale. Esito atteso: fasi completate, nessun temporaneo residuo, originale intatto.

## 14. Compatibilità e installazione
- Funziona in Claude Code da terminale e in Claude Desktop, modalità "Code", nelle sessioni locali. Le sessioni cloud e WSL non caricano plugin e non hanno il Docker locale.
- Il percorso del lettore si scrive come `${CLAUDE_PLUGIN_ROOT}/scripts/wpress.py`, che viene sostituito nel testo della skill.
- Le domande all'utente partono solo dalla sessione principale.
- Il preflight verifica che Docker sia raggiungibile dalla shell della sessione, perché un sandbox dei comandi può bloccarlo.
- Il README offre l'installazione con un prompt da incollare: Claude esegue i comandi `claude plugin`. Offre anche l'installazione manuale e le note per Claude Desktop.

## 15. Decisioni
- **Playbook adattivo invece di script.** La varietà dei siti WordPress rende fragili gli automatismi; gli script restano solo dove il formato è fisso.
- **Niente comandi d'esempio né prodotti consigliati nel playbook**, per non orientare le scelte.
- **Autonomia completa**, con gli stop del §7.
- **Import automatico tramite l'Unlimited Extension**, con l'archivio montato in sola lettura. Lo zip è fornito nella cartella di lavoro oppure scaricato dall'URL predefinito per uso interno. L'URL predefinito è pubblico finché il repository è pubblico: è una scelta del proprietario, e la sicurezza del link la gestisce lui.
- **Repository pubblico unico**, che fa sia da marketplace sia da plugin; licenza MIT.
