from widgetastic.utils import ParametrizedLocator
from widgetastic.widget import FileInput, Select, Text, TextInput, View
from widgetastic_patternfly import BreadCrumb, Tab
from widgetastic_patternfly5.ouia import PatternflyTable

from airgun.views.common import BaseLoggedInView, SearchableViewMixinPF4
from airgun.widgets import (
    ConfirmationDialog,
    EditableEntry,
    PF4Search,
    ReadOnlyEntry,
)


class ContentCredentialsTableView(BaseLoggedInView, SearchableViewMixinPF4):
    title = Text("//h1[contains(., 'Content Credentials')]")
    new = Text("//button[contains(@href, '/content_credentials/new')]")
    table = PatternflyTable(
        component_id='content-credentials-table',
        column_widgets={
            'Name': Text('./a'),
            'Organization': Text('.//td[2]'),
            'Type': Text('.//td[3]'),
            'Products': Text('.//td[4]'),
            'Repositories': Text('.//td[5]'),
            'Alternate content sources': Text('.//td[6]'),
        },
    )

    @property
    def is_displayed(self):
        return self.browser.wait_for_element(self.title, exception=False) is not None


class ContentCredentialCreateView(BaseLoggedInView):
    breadcrumb = BreadCrumb()
    name = TextInput(id='name')
    content_type = Select(id='content_type')
    content = TextInput(name='content')
    upload_file = FileInput(name='file_path')
    submit = Text("//button[contains(@ng-click, 'handleSave')]")

    @property
    def is_displayed(self):
        breadcrumb_loaded = self.browser.wait_for_element(self.breadcrumb, exception=False)
        return (
            breadcrumb_loaded
            and self.breadcrumb.locations[0] == 'Content Credential'
            and self.breadcrumb.read() == 'New Content Credential'
        )


class ContentCredentialEditView(BaseLoggedInView):
    breadcrumb = BreadCrumb()
    remove = Text("//button[contains(., 'Remove Content Credential')]")
    dialog = ConfirmationDialog()

    @property
    def is_displayed(self):
        breadcrumb_loaded = self.browser.wait_for_element(self.breadcrumb, exception=False)
        return (
            breadcrumb_loaded
            and self.breadcrumb.locations[0] == 'Content Credentials'
        )

    @View.nested
    class details(Tab):
        TAB_LOCATOR = ParametrizedLocator('//a[contains(@href, "#/details")]')
        name = EditableEntry(name='Name')
        content_type = ReadOnlyEntry(name='Type')
        content = EditableEntry(name='Content')
        products = ReadOnlyEntry(name='Products')
        repos = ReadOnlyEntry(name='Repositories')

    @View.nested
    class products(Tab):
        TAB_LOCATOR = ParametrizedLocator('//a[contains(@href, "#/products")]')
        searchbox = PF4Search()
        table = PatternflyTable(
            component_id='content-credential-products-table',
            column_widgets={
                'Name': Text('./a'),
                'Used as': Text('.//td[2]'),
            },
        )

        def search(self, value):
            self.searchbox.search(value)
            return self.table.read()

    @View.nested
    class repositories(Tab):
        TAB_LOCATOR = ParametrizedLocator('//a[contains(@href, "#/repositories")]')
        searchbox = PF4Search()
        table = PatternflyTable(
            component_id='content-credential-repositories-table',
            column_widgets={
                'Name': Text('./a'),
                'Product': Text('.//td[2]'),
                'Type': Text('.//td[3]'),
                'Used as': Text('.//td[4]'),
            },
        )

        def search(self, value):
            self.searchbox.search(value)
            return self.table.read()

    @View.nested
    class alternate_content_sources(Tab):
        TAB_LOCATOR = ParametrizedLocator(
            '//a[contains(@href, "#/alternate_content_sources")]'
        )
        searchbox = PF4Search()
        table = PatternflyTable(
            component_id='content-credential-acs-table',
            column_widgets={
                'Name': Text('./a'),
                'Used as': Text('.//td[2]'),
            },
        )

        def search(self, value):
            self.searchbox.search(value)
            return self.table.read()
