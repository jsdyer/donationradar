export default {
  "title": "Donation Radar",
  "intro": "Explore reported federal contributions and compare return versions. Keep source corrections visible without guessing who a contributor is.",
  "eyebrow": "POLITICAL FINANCING / REPORTED CONTRIBUTIONS",
  "accent": "#80503b",
  "tint": "#f6e9e0",
  "method": [
    "The initial complete cohort is registered-party annual returns for the year ending in 2023, across all reported provinces and territories. More recent reviewed cohorts were incomplete at the initial capture. Annual and quarterly totals are not combined.",
    "Submitted and reviewed versions are separate datasets. Compare aggregate return cohorts or exact reported-row multisets; the source supplies no stable contribution identifier that would justify pairing a corrected row to a particular person.",
    "Only reported contributor name, province, entity, period and contribution figures are retained. Street addresses, cities and postal codes are excluded. Identical public rows remain distinct occurrences rather than being silently removed.",
    "Directed contributions to leadership contestants are kept separate from ordinary party contributions. Names can refer to different people, and one person can appear in several forms. Counts describe reported records, never unique donors."
  ],
  "id": "donationradar",
  "explorer-title": "Follow the record.",
  "cadence": "Weekly automated collection. Source dates and capture dates are shown separately.",
  "facets": [
    {
      "key": "entity",
      "label": "Political entity"
    },
    {
      "key": "kind",
      "label": "Contribution type"
    }
  ],
  "columns": [
    {
      "key": "contributor",
      "label": "Reported contributor"
    },
    {
      "key": "entity",
      "label": "Political entity"
    },
    {
      "key": "province",
      "label": "Province"
    },
    {
      "key": "amount",
      "label": "Amount (CAD)",
      "money": true
    },
    {
      "key": "period",
      "label": "Fiscal period"
    },
    {
      "key": "version",
      "label": "Return version"
    },
    {
      "key": "kind",
      "label": "Type"
    }
  ],
  "related": [
    {
      "label": "Lobby Trail",
      "url": "https://coolcode.ca/lobbytrail/"
    },
    {
      "label": "Contract Patterns",
      "url": "https://coolcode.ca/contractpatterns/"
    }
  ],
  "defaults": {
    "kind": "ordinary"
  },
  "controls": [
    {
      "key": "province",
      "label": "Province / territory",
      "options": [
        {
          "value": "AB",
          "label": "AB"
        },
        {
          "value": "BC",
          "label": "BC"
        },
        {
          "value": "MB",
          "label": "MB"
        },
        {
          "value": "NA",
          "label": "NA"
        },
        {
          "value": "NB",
          "label": "NB"
        },
        {
          "value": "NL",
          "label": "NL"
        },
        {
          "value": "NS",
          "label": "NS"
        },
        {
          "value": "NT",
          "label": "NT"
        },
        {
          "value": "NU",
          "label": "NU"
        },
        {
          "value": "ON",
          "label": "ON"
        },
        {
          "value": "PE",
          "label": "PE"
        },
        {
          "value": "QC",
          "label": "QC"
        },
        {
          "value": "SK",
          "label": "SK"
        },
        {
          "value": "UNKNOWN",
          "label": "UNKNOWN"
        },
        {
          "value": "YT",
          "label": "YT"
        }
      ],
      "default": "BC"
    },
    {
      "key": "version",
      "label": "Return version",
      "options": [
        {
          "value": "reviewed",
          "label": "Reviewed returns"
        },
        {
          "value": "submitted",
          "label": "Submitted returns"
        }
      ],
      "default": "reviewed"
    }
  ]
};
