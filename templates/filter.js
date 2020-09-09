(function (DLFrontend) {
  function convertNodeListToArray (nl) {
    return Array.prototype.slice.call(nl)
  }

  // adapted from https://stackoverflow.com/questions/2970525/converting-any-string-into-camel-case
  function camelize (str) {
    return str
      .replace(/-/g, " ")
      .replace(/(?:^\w|[A-Z]|\b\w|\s+)/g, function (match, index) {
        if (+match === 0) return ""; // or if (/\s+/.test(match)) for white spaces
        return index === 0 ? match.toLowerCase() : match.toUpperCase()
      })
  }

  function FacetSearch ($list, $form) {
    this.$list = $list
    this.$form = $form
    this.filterTimeout = null
    this.$noMatches = document.querySelector('.js-no-filter-list-matches')
  }

  FacetSearch.prototype.init = function (params) {
    this.setupOptions(params)
    this.$currentCount = this.$list.querySelector(this.count_selector)
    this.$items = this.allListItems()
    this.filters = this.allFilters()

    console.log('List items: ', this.$items.length)
    console.log('Filters: ', this.filters)

    const boundFilterListHandler = this.filterListHandler.bind(this)
    this.$form.addEventListener('submit', boundFilterListHandler)
    const boundResetHandler = this.resetHandler.bind(this)
    this.$form.addEventListener('reset', boundResetHandler)
  }

  FacetSearch.prototype.allListItems = function () {
    const $list = this.$list
    var $items = $list.querySelectorAll('[data-facet-search="item"]')
    return convertNodeListToArray($items)
  }

  FacetSearch.prototype.allFilters = function () {
    const $form = this.$form
    var filters = []
    var $filters = convertNodeListToArray($form.querySelectorAll('[data-facet-search="filter"]'))
    $filters.forEach(function ($filter) {
      filters.push({
        $element: $filter,
        name: $filter.dataset.facetSearchName,
        type: $filter.dataset.facetSearchType
      })
    })
    return filters
  }

  FacetSearch.prototype.filterListHandler = function (e) {
    e.preventDefault()
    this.filterList()
  }

  FacetSearch.prototype.resetHandler = function (e) {
    console.log('reset the form')
    this.showAll()
  }

  FacetSearch.prototype.showAll = function () {
    const $items = this.$items
    $items.forEach(function ($item) {
      $item.classList.remove('js-hidden')
    })
    this.updateCountDisplay($items.length)
  }

  FacetSearch.prototype.filterList = function () {
    const filters = this.filters
    const $items = this.$items
    const that = this

    // start with a full list of items
    let filteredList = $items
    $items.forEach(function ($item) {
      $item.classList.add('js-hidden')
    })
    // go through a filter at a time
    filters.forEach(function (filter) {
      // only perform filter if there is something to filter
      if (filteredList.length > 0) {
        filteredList = that.performFilter(filteredList, filter)
      }
      // how many left
      console.log("after filter: ", filteredList.length)
    })

    if (filteredList.length > 0) {
      filteredList.forEach(function ($item) {
        $item.classList.remove('js-hidden')
      })
    }

    this.updateCountDisplay(filteredList.length)
  }

  FacetSearch.prototype.performFilter = function (list, filter) {
    const that = this
    // handle text input filters
    if (filter.type === 'text') {
      const $input = filter.$element.querySelector('input')
      const _val = $input.value

      if (_val !== '') {
        return list.filter(function (i) {
          return that.matchTextString(i, filter.name, _val)
        })
      }
      return list
    } else if (filter.type === 'radio') {
      const checkedRadio = filter.$element.querySelector('input[type="radio"]:checked')
      if (checkedRadio) {
        const _val = checkedRadio.value
        return list.filter(function (i) {
          return that.matchTextString(i, filter.name, _val)
        })
      }
    }
    return list
  }

  FacetSearch.prototype.matchTextString = function ($item, propName, _val) {
    if ($item.dataset[camelize(propName)].toString() === _val) {
      return true
    }
    return false
  }

  FacetSearch.prototype.updateCountDisplay = function (count) {
    this.$currentCount.textContent = count
  }

  FacetSearch.prototype.setupOptions = function (params) {
    params = params || {}
    this.total_count_selector = params.total_count_selector || '.facet-search__total-count'
    this.count_selector = params.count_selector || '.facet-search__count'
  }

  DLFrontend.FacetSearch = FacetSearch
})(DLFrontend)
