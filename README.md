<div align="center">
    <img alt="logo" src="https://github.com/imum-ai/promptlab/blob/main/img/logo.png" style="height:300px">
    <h1>PromptLab</h1>
    <p>Ein kostenloses, leichtgewichtiges, quelloffenes Experimentier-Tool für Gen-AI-Anwendungen</p>
    <a href="https://pypi.org/project/promptlab/"><img src="https://img.shields.io/pypi/v/promptlab.svg" alt="PyPI Version"></a>
    <a href="https://github.com/imum-ai/promptlab/blob/main/LICENSE"><img src="https://img.shields.io/github/license/imum-ai/promptlab.svg" alt="Lizenz"></a>
    <a href="https://github.com/imum-ai/promptlab/stargazers"><img src="https://img.shields.io/github/stars/imum-ai/promptlab.svg" alt="GitHub Sterne"></a>
</div>📋 Inhaltsverzeichnis

Überblick

Funktionen

Installation

Schnellstart

Kernkonzepte

Dokumentation

Unterstützte Modelle

Beispiele

Artikel & Tutorials

Beitragen

Lizenz


Überblick 🔍

PromptLab ist ein kostenloses, leichtgewichtiges, quelloffenes Experimentier-Tool für Gen-AI-Anwendungen.
Es vereinfacht das Prompt-Engineering, indem es die Einrichtung von Experimenten, die Auswertung von Prompts und das Tracking in der Produktion erleichtert – ohne Cloud-Dienste oder komplexe Infrastruktur.

Mit PromptLab kannst du:

Prompt-Vorlagen mit Versionsverwaltung erstellen und verwalten

Evaluations-Datensätze aufbauen und pflegen

Experimente mit verschiedenen Modellen und Prompts durchführen

Modell- und Prompt-Leistung anhand integrierter oder benutzerdefinierter Metriken bewerten

Ergebnisse von Experimenten nebeneinander vergleichen

Optimierte Prompts in die Produktion überführen


<div align="center">
    <img alt="PromptLab Studio" src="img/studio-exp.png" style="max-width:800px">
</div>Funktionen ✨

Wirklich leichtgewichtig: Kein Cloud-Abo, keine zusätzlichen Server, kein Docker – einfach nur ein Python-Paket

Einfach zu verwenden: Keine ML- oder Data-Science-Kenntnisse erforderlich

Vollständig eigenständig: Keine zusätzlichen Cloud-Dienste nötig für Tracking oder Zusammenarbeit

Nahtlose Integration: Funktioniert in vorhandenen Web-, Mobile- oder Backend-Projekten

Flexible Bewertung: Nutze eingebaute Metriken oder bringe eigene Evaluatoren mit

Web-Oberfläche: Vergleiche Experimente und verwalte Assets über ein Web-Interface

Unterstützung mehrerer Modelle: Funktioniert mit Azure OpenAI, Ollama, DeepSeek und mehr – oder integriere dein eigenes Modell

Versionskontrolle: Automatische Versionierung aller Assets für Reproduzierbarkeit

Async-Unterstützung: Führe Experimente und Modellaufrufe asynchron aus für bessere Performance


Installation 📦

pip install promptlab

Es wird empfohlen, eine virtuelle Umgebung zu verwenden:

python -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate
pip install promptlab

Schnellstart 🚀

Schau dir das Schnellstart-Beispiel hier an – samples/quickstart

Kernkonzepte 🧩

Tracer

Der Tracer ist für das Speichern und Aktualisieren von Assets und Experimenten in der Speicher-Schicht verantwortlich.
Derzeit wird ausschließlich SQLite unterstützt.

Assets

Unveränderliche Artefakte, die in Experimenten verwendet werden, mit automatischer Versionierung:

Prompt-Vorlagen: Prompts mit optionalen Platzhaltern für dynamische Inhalte

Datensätze: JSONL-Dateien mit Evaluationsdaten


Experimente

Bewerte Prompts gegen Datensätze mit bestimmten Modellen und Metriken.

PromptLab Studio

Eine Web-Oberfläche zur Visualisierung von Experimenten und zum Vergleich von Ergebnissen.

Dokumentation 📖

Für eine umfassende Dokumentation besuche die Dokumentationsseite.

Wichtige Dokumentation:

Kernkonzepte

Evaluatoren – Detaillierte Informationen über eingebaute und benutzerdefinierte Evaluatoren


Unterstützte Modelle 🤖

Azure OpenAI: Verbindung zu Azure-gehosteten OpenAI-Modellen

Ollama: Führe Experimente mit lokal gehosteten Modellen aus

OpenRouter: Zugriff auf eine Vielzahl von KI-Modellen (OpenAI, Anthropic, DeepSeek, Mistral usw.) über die OpenRouter-API

Eigene Modelle: Integriere deine eigenen Modell-Implementierungen


Beispiele 📚

Quickstart: Einstieg in PromptLab

Asset-Versionierung: Versionierung von Prompts und Datensätzen

Eigene Metrik: Erstellen benutzerdefinierter Evaluationsmetriken

Async-Beispiel: Nutzung asynchroner Funktionen mit Ollama und OpenRouter für bessere Performance

Eigenes Modell: Verwende dein eigenes Modell zur Bewertung


Artikel & Tutorials 📝

Bewertung von Prompts lokal mit Ollama und PromptLab

Erstellen benutzerdefinierter Prompt-Bewertungsmetriken mit PromptLab


CI/CD 🔄

PromptLab verwendet GitHub Actions für kontinuierliche Integration und Tests:

Unit-Tests: Führt Komponententests für alle Teile von PromptLab aus

Integrations-Tests: Testen die Zusammenarbeit mehrerer Komponenten

Performance-Tests: Sicherstellen, dass Leistungsanforderungen erfüllt werden


Die Tests sind in folgende Verzeichnisse organisiert:

tests/unit/: Komponententests einzelner Bausteine

tests/integration/: Tests, die mehrere Komponenten zusammen prüfen

tests/performance/: Tests zur Messung der Performance

tests/fixtures/: Gemeinsame Test-Hilfsmittel und Utilities


Weitere Informationen zu den CI/CD-Workflows findest du im Verzeichnis
.github/workflows.

Beitragen 👥

Beiträge sind willkommen! Du kannst gerne einen Pull-Request einreichen.

1. Forke das Repository


2. Erstelle deinen Feature-Branch (git checkout -b feature/amazing-feature)


3. Committe deine Änderungen (git commit -m 'Add some amazing feature')


4. Push deine Änderungen (git push origin feature/amazing-feature)


5. Öffne einen Pull-Request



Lizenz 📄

Dieses Projekt ist unter der MIT-Lizenz lizenziert – siehe die LICENSE-Datei für Details.