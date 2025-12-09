import unittest
from unittest.mock import patch, MagicMock
from vibe_todo.state import (
    init_session_state,
    get_current_view,
    set_current_view,
    get_selected_list_id,
    toggle_task_expansion,
    is_task_expanded,
    set_task_filter,
    get_task_filter,
    clear_task_filters
)

class MockSessionState(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

class TestState(unittest.TestCase):
    def setUp(self):
        self.mock_st_patcher = patch('vibe_todo.state.st')
        self.mock_st = self.mock_st_patcher.start()
        self.mock_st.session_state = MockSessionState()

    def tearDown(self):
        self.mock_st_patcher.stop()

    def test_init_session_state(self):
        init_session_state()
        self.assertIn("current_view", self.mock_st.session_state)
        self.assertEqual(self.mock_st.session_state.current_view, "My Day")
        self.assertIn("selected_list_id", self.mock_st.session_state)
        self.assertIsNone(self.mock_st.session_state.selected_list_id)
        self.assertIn("task_filters", self.mock_st.session_state)
        self.assertEqual(self.mock_st.session_state.task_filters, {})
        self.assertIn("expanded_tasks", self.mock_st.session_state)
        self.assertEqual(self.mock_st.session_state.expanded_tasks, set())

    def test_view_management(self):
        self.mock_st.session_state.current_view = "Old"
        self.mock_st.session_state.selected_list_id = None
        
        set_current_view("New View", 123)
        self.assertEqual(self.mock_st.session_state.current_view, "New View")
        self.assertEqual(self.mock_st.session_state.selected_list_id, 123)
        
        self.assertEqual(get_current_view(), "New View")
        self.assertEqual(get_selected_list_id(), 123)

    def test_task_expansion(self):
        self.mock_st.session_state.expanded_tasks = set()
        
        toggle_task_expansion(1)
        self.assertTrue(is_task_expanded(1))
        
        toggle_task_expansion(1)
        self.assertFalse(is_task_expanded(1))

    def test_task_filters(self):
        self.mock_st.session_state.task_filters = {}
        
        set_task_filter("priority", "high")
        self.assertEqual(get_task_filter("priority"), "high")
        
        clear_task_filters()
        self.assertEqual(self.mock_st.session_state.task_filters, {})
