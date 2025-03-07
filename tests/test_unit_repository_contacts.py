import unittest
from unittest.mock import MagicMock, AsyncMock
from datetime import datetime
import sys
import os

from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact, User
from src.repository.contacts import get_contacts, get_contact, create_contacts, delete_contacts, update_contacts


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class TestAsyncContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.contacts = User(name='John', surname='Watson', created_at=datetime.now, updated_at=None, confirmed=True,email='deduction@gmail.com')
        self.mock_session = AsyncMock(spec=AsyncSession)

    async def test_get_contacts(self):
        limit= 10
        offset = 0
        test_contancts = [
            Contact(id=1, name='John', surname='Watson', email='deduction@gmail.com', birthday='01.12.1990'),
            Contact(id=1, name='Sherlock', surname='Holms', email='detecitive@gmail.com', birthday='09.02.1990')]
        mocked_contacts = MagicMock
        mocked_contacts.scalar.return_value.all = test_contancts
        self.mock_session.execute.return_value = mocked_contacts
        result = await get_contacts(limit, offset, self.mock_session)
        self.assertEqual(result, test_contancts)