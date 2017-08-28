import { AngularSeedPage } from './app.po';

describe('angular-seed App', () => {
  let page: AngularSeedPage;

  beforeEach(() => {
    page = new AngularSeedPage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!');
  });
});
