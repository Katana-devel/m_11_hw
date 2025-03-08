import unittest
from datetime import date
from unittest.mock import MagicMock, AsyncMock
from datetime import datetime
import sys
import os

from pydantic.v1 import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact, User
from src.repository.contacts import get_contacts, get_contact, create_contacts, delete_contacts, update_contacts
from src.schemas.contact import ContactSchema, ContactUpdateSchema

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestAsyncContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.contacts = User(name='John', surname='Watson', created_at=datetime.now, updated_at=None, confirmed=True,
                             email='deduction@gmail.com')
        self.mock_session = AsyncMock(spec=AsyncSession)

    async def test_get_contacts(self):
        limit = 10
        offset = 0
        test_contacts = [
            Contact(id=1, name='John', surname='Watson', email='deduction@gmail.com', birthday='1990.12.01'),
            Contact(id=1, name='Sherlock', surname='Holms', email='detecitive@gmail.com', birthday='1990.02.09')]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = test_contacts
        self.mock_session.execute.return_value = mocked_contacts
        result = await get_contacts(limit, offset, self.mock_session)
        self.assertEqual(result, test_contacts)

    async def test_get_contact(self):
        test_contact = Contact(id=1, name='John', surname='Watson', email='deduction@gmail.com', birthday='1990.12.01')
        mocked_contacts = MagicMock()
        mocked_contacts.scalar_one_or_none.return_value = test_contact
        self.mock_session.execute.return_value = mocked_contacts
        result = await get_contact(1, self.mock_session)
        self.assertEqual(result, test_contact)

    async def test_create_contacts(self):
        body = ContactSchema(name='John', surname='Watson', email=EmailStr('deduction@gmail.com'), phone='0891211629',
                             birthday=date(1990, 12, 1), extra_info=None)
        result = await create_contacts(body, self.mock_session)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.name, 'John')
        self.assertEqual(result.surname, 'Watson')
        self.assertEqual(result.email, 'deduction@gmail.com')
        self.assertEqual(result.phone, '0891211629')
        self.assertEqual(result.birthday, date(1990, 12, 1))
        self.assertIsNone(result.extra_info)

    async def test_update_contacts(self):
        contact_id = 1
        body = ContactUpdateSchema(name='John', surname='Watson', email=EmailStr('deduction@gmail.com'),
                                   phone='0891211629', birthday=date(1990, 12, 1), extra_info=None)
        test_contact = Contact(id=1, name='John', surname='Watson', email='deduction@gmail.com', birthday='1990.12.01')
        mocked_contacts = MagicMock()
        mocked_contacts.scalar_one_or_none.return_value = test_contact
        self.mock_session.execute.return_value = mocked_contacts
        result = await update_contacts(contact_id, body, self.mock_session)
        self.assertIsInstance(result, Contact)

    async def test_delete_contacts(self):
        contact_id = 1
        mocked_contacts = MagicMock()
        mocked_contacts.scalar_one_or_none.return_value = Contact(id=contact_id, name='John', surname='Watson', email=EmailStr('deduction@gmail.com'),
                               phone='0891211629', birthday=date(1990, 12, 1), extra_info=None)
        self.mock_session.execute.return_value = mocked_contacts
        result = await delete_contacts(contact_id, self.mock_session)
        self.mock_session.delete.assert_called_once()
        self.assertIsInstance(result, Contact)
