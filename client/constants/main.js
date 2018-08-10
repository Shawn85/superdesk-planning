export const MAIN = {
    ACTIONS: {
        PREVIEW: 'MAIN_PREVIEW',
        OPEN_EDITOR: 'MAIN_OPEN_EDITOR',
        OPEN_EDITOR_MODAL: 'OPEN_EDITOR_MODAL',
        CLOSE_EDITOR: 'MAIN_CLOSE_EDITOR',
        CLOSE_EDITOR_MODAL: 'CLOSE_EDITOR_MODAL',
        FILTER: 'MAIN_FILTER',
        HISTORY: 'MAIN_HISTORY',
        CLOSE_PREVIEW: 'MAIN_CLOSE_PREVIEW',
        REQUEST: 'MAIN_REQUEST',
        CLEAR_SEARCH: 'MAIN_CLEAR_SEARCH',
        SET_TOTAL: 'MAIN_SET_TOTAL',
        SET_UNSET_LOADING_INDICATOR: 'MAIN_SET_UNSET_LOADING_INDICATOR',

        SET_PREVIEW_ITEM: 'MAIN_SET_PREVIEW_ITEM',
        PREVIEW_LOADING_START: 'MAIN_PREVIEW_LOADING_START',
        PREVIEW_LOADING_COMPLETE: 'MAIN_PREVIEW_LOADING_COMPLETE',

        SET_EDIT_ITEM: 'MAIN_SET_EDIT_ITEM',
        EDIT_LOADING_START: 'MAIN_EDIT_LOADING_START',
        EDIT_LOADING_COMPLETE: 'MAIN_EDIT_LOADING_COMPLETE',
        EDIT_LOADING_START_MODAL: 'MAIN_EDIT_LOADING_START_MODAL',
        EDIT_LOADING_COMPLETE_MODAL: 'MAIN_EDIT_LOADING_COMPLETE_MODAL',

        SET_JUMP_INTERVAL: 'MAIN_SET_JUMP_INTERVAL',
        JUMP_TO: 'MAIN_JUMP_TO',
        RECEIVE_EDITOR_ITEM_HISTORY: 'RECEIVE_EDITOR_ITEM_HISTORY',
        RECEIVE_PREVIEW_ITEM_HISTORY: 'RECEIVE_PREVIEW_ITEM_HISTORY',
        SET_PUBLISH_QUEUE_ITEM: 'SET_PUBLISH_QUEUE_ITEM',
        RECEIVE_EDITOR_MODAL_ITEM_HISTORY: 'RECEIVE_EDITOR_MODAL_ITEM_HISTORY',
    },
    FILTERS: {
        COMBINED: 'COMBINED',
        EVENTS: 'EVENTS',
        PLANNING: 'PLANNING',
    },
    PAGE_SIZE: 100,
    PREVIEW: 'preview',
    EDIT: 'edit',
    JUMP: {
        FORWARD: 'FORWARD',
        BACK: 'BACK',
        TODAY: 'TODAY',
        DAY: 'DAY',
        WEEK: 'WEEK',
        MONTH: 'MONTH',
    },
    DATE_RANGE: {
        TODAY: 'today',
        TOMORROW: 'tomorrow',
        THIS_WEEK: 'this_week',
        NEXT_WEEK: 'next_week',
        LAST_24: 'last24',
        FOR_DATE: 'forDate',
    },
};
