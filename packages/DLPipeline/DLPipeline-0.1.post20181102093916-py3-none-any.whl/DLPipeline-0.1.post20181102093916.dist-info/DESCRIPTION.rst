
# [Innovativ brug af Big Data: Deep learning-baseretbilledanalyse](https://confluence.alexandra.dk/display/IBBD5/IBBD5+-+Deep+Learning+baseret+billedanalyse)



<p align="center" width="100%">
  <a href="https://alexandra.dk">
    <img alt="AlexandraInstittutet" src=".bitbucket/images/Alexandra_Instituttet_B-logo_BLACK_red-IT_UK.svg" height="40" align="left" />
  </a>
    <a href="http://applicateit.dk/">
    <img alt="applicateit" src=".bitbucket/images/applicateit-favicon.png" height="40" align="left" />
  </a>
    <a href="http://gamescorekeeper.com/">
    <img alt="gamescorekeeper" src=".bitbucket/images/gamescorekeeper-favivon.png" height="40" align="left" />
  </a>
    <a href="https://www.retinalyze.com/">
    <img alt="retinalyze" src=".bitbucket/images/retinalyze-favicon.png" height="40" align="left" />
  </a>
    <a href="http://www.worksystems.dk/">
    <img alt="worksystems" src=".bitbucket/images/worksystems-favicon.png" height="40" align="left" />
  </a>
</p>

<br/>

## DLpipeline

### Projektbeskrivelse
Deep learning har revolutioneret den måde, vi arbejder med billeder og data generelt på. I gamle dage skulle man være computer vision ekspert for at trække meningsfuld information ud af billeder. I  dag - takket være deep learning - findes der mange offentligt tilgængelige værktøjer, som kan løse meget komplekse problemer for én, og som man må bruge kvit og frit på sine egne billeddata. Denne data-drevne måde at arbejde med billeder på har åbnet op for en masse nye muligheder, dels fordi deep learning kan løse computer vision problemer, man ikke kunne løse for bare 5-6 år siden, og dels fordi teknologierne er blevet tilgængelige for alle. Det sidste har især medført, at der begynder at opstå rigtig mange ideer til nye forretninger, produkter, ydelser hos folk, som ikke har baggrund inden for computer vision-området. Det er vigtigt for væksten i Danmark, at virksomheder og vidensinstitutioner står sammen og griber disse ideer, når de opstår. Der har virksomhederne især brug for at kunne trække på den nyeste viden og forskning fra vidensinstitutionerne. Samtidig er det hele så nyt, at vi endnu ikke har lært, hvordan vi bedst understøtter hinanden i forhold til deling af viden, kompetencer og erfaringer. Der skal der øget fokus på samarbejdet mellem virksomheder og videninstitutioner, hvis Danmark skal stå stærkt i den globale konkurrence med store IT-giganter som Google og Amazon. Så dette er den overordnede tanke bag projektet; at skabe et forum, hvor virksomheder og vidensinstitutioner står sammen om at udvikle nye deep  learning-baserede teknologier og (på sigt) produkter relateret til computer vision.

Vi har samlet fire virksomheder, som har det til fælles, at de hver især står med en udfordring inden for billedbehandling, som bedst løses ved hjælp af deep learning, men hvor virksomhederne i varierende grad mangler praktisk erfaring med og viden om teknologien og har brug for hjælp til at komme i gang selv. For at understøtte denne proces vil vi oprette en wiki eller et chat-forum, hvor virksomhederne kan stille spørgsmål til hinanden (og vidensinstitutionerne) og dele deres resultater, viden og erfaringer med hinanden. Vidensinstitutionerne vil skabe det nødvendige fundament af kildekode for, at hvert af de fire delprojekter beskrevet nedenfor kan komme i gang. De konkrete deep learning-algoritmer skal tilpasses hver enkelt virksomheds unikke problem, men den underliggende kildekode vil være næsten identisk. En del af synergien i  projektet består derfor i  at arbejde sammen omkring den fælles kodebase.

<br/>

<table>
  <tr>
    <td>
      <a href='https://www.python.org/'>
        <img src='.bitbucket/images/python.svg' />
      </a>
    </td>
    <td>
      <a href='https://www.tensorflow.org/'>
        <img src='.bitbucket/images/tensorflow.svg' />
      </a>
    </td>
  </tr>
</table>

### Features

-
-
-

### Installation

```bash
  pip3 install dlpipeline -U
```

eller hvis du har hentet repositoriet ned kan du bruge

```bash
  python3 setup.py install
```

#### DLpipeline Udviklings Miljø
Du kan også vælge at lave et udviklings setup hvor du nemt kan ændre koden i dette projekt og lade andre 
drage nytte af dine ændringer, hvis du engang vælger at dele dem. Dette kan du gøre ved at bruge kommandoen:

```bash
  python3 setup.py develop
```

og så senere dele dem med også andre ved f.eks.

```bash
  git add -A
  git commit -m"Jeg har lavet [disse ændringer]"
  git push origin
```

